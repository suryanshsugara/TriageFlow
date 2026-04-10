"""TriageFlow Environment - OpenEnv-compliant support ticket triage benchmark."""

import json
import os
import random
import copy
from pathlib import Path
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from typing import Any


# ──────────────────────────── Pydantic Models ────────────────────────────


class Observation(BaseModel):
    """Observable state presented to the agent at each step."""
    ticket_id: str
    subject: str
    body: str
    sender: str
    timestamp: str
    attachments: list[str]
    history: list[dict[str, Any]]
    queue_depth: int
    current_step: int
    max_steps: int
    task_name: str


class Action(BaseModel):
    """Action taken by the agent on the current ticket."""
    action_type: str
    urgency: str | None = None
    category: str | None = None
    assigned_team: str | None = None
    missing_fields: list[str] | None = None
    resolution_note: str | None = None
    escalation_reason: str | None = None


class Reward(BaseModel):
    """Dense reward signal returned after each step."""
    total: float
    breakdown: dict[str, float]
    step_penalty: float
    correctness: float
    routing_score: float
    completeness: float
    policy_compliance: float


class TicketState(BaseModel):
    """Internal tracking state for a single ticket during an episode."""
    ticket_id: str
    classified: bool = False
    classified_urgency: str | None = None
    classified_category: str | None = None
    routed: bool = False
    routed_team: str | None = None
    info_requested: bool = False
    requested_fields: list[str] = Field(default_factory=list)
    escalated: bool = False
    resolved: bool = False
    skipped: bool = False
    steps_spent: int = 0
    action_history: list[dict[str, Any]] = Field(default_factory=list)


# ──────────────────────────── Constants ────────────────────────────

VALID_ACTION_TYPES = {"classify", "route", "request_info", "escalate", "resolve", "skip"}
VALID_URGENCIES = {"low", "medium", "high", "critical"}
VALID_CATEGORIES = {"billing", "technical", "account", "policy", "other"}
VALID_TEAMS = {"tier1", "tier2", "billing", "security", "management"}

TASK_CONFIG = {
    "ticket_classification": {"queue_size": 5, "max_steps": 10, "difficulty": "easy"},
    "ticket_routing": {"queue_size": 8, "max_steps": 20, "difficulty": "medium"},
    "policy_triage": {"queue_size": 10, "max_steps": 30, "difficulty": "hard"},
}

TERMINAL_ACTIONS = {
    "easy": {"classify", "resolve", "skip", "escalate"},
    "medium": {"route", "resolve", "skip", "escalate"},
    "hard": {"resolve", "skip", "escalate"},
}


# ──────────────────────────── Routing Rules ────────────────────────────


def get_correct_team(category: str, urgency: str) -> str:
    """Determine the correct team assignment based on category and urgency."""
    if category == "billing":
        return "billing"
    elif category == "technical":
        return "tier2" if urgency in ("high", "critical") else "tier1"
    elif category == "account":
        return "tier1"
    elif category == "policy":
        return "management"
    return "tier1"


# ──────────────────────────── Reward Computation ────────────────────────────


def compute_reward(
    action: Action,
    ground_truth: dict[str, Any],
    ticket_state: TicketState,
    step_number: int,
    max_steps: int,
    task_name: str,
) -> Reward:
    """Compute dense reward for a single agent action.

    Returns a Reward with per-component scores and a clamped total in [-1.0, 1.0].
    """
    breakdown: dict[str, float] = {}
    correctness = 0.0
    routing_score = 0.0
    completeness = 0.0
    policy_compliance = 0.0
    step_penalty = -0.01

    if action.action_type == "classify":
        if action.urgency == ground_truth["urgency"]:
            correctness += 0.10
            breakdown["urgency_correct"] = 0.10
        if action.category == ground_truth["category"]:
            correctness += 0.10
            breakdown["category_correct"] = 0.10

    elif action.action_type == "route":
        if ticket_state.classified:
            correct_team = get_correct_team(
                ground_truth["category"], ground_truth["urgency"]
            )
            if action.assigned_team == correct_team:
                if (
                    ticket_state.classified_category == ground_truth["category"]
                    and ticket_state.classified_urgency == ground_truth["urgency"]
                ):
                    routing_score += 0.10
                    breakdown["routing_correct"] = 0.10
                else:
                    breakdown["routing_no_credit_wrong_classify"] = 0.0
            else:
                breakdown["routing_incorrect"] = 0.0
        else:
            breakdown["routing_no_classify_first"] = 0.0

    elif action.action_type == "request_info":
        if action.missing_fields:
            expected = set(ground_truth.get("missing_fields", []))
            requested = set(action.missing_fields)
            if expected and requested & expected:
                completeness += 0.05
                breakdown["missing_fields_correct"] = 0.05
            elif not expected and requested:
                breakdown["unnecessary_info_request"] = 0.0

    elif action.action_type == "escalate":
        needs_escalation = ground_truth.get("sla_critical", False) or ground_truth.get(
            "has_policy_violation", False
        )
        if needs_escalation:
            policy_compliance += 0.10
            breakdown["escalation_correct"] = 0.10
        else:
            policy_compliance -= 0.05
            breakdown["false_escalation"] = -0.05

    elif action.action_type == "resolve":
        note = action.resolution_note or ""
        if len(note) > 20 and note.lower().strip() != "resolved":
            if task_name == "ticket_classification" or ticket_state.routed:
                correctness += 0.10
                breakdown["resolution_quality"] = 0.10
            else:
                breakdown["resolution_no_credit_no_route"] = 0.0
        else:
            breakdown["resolution_low_quality"] = 0.0

    elif action.action_type == "skip":
        if ground_truth.get("is_duplicate", False):
            completeness += 0.05
            breakdown["duplicate_detected"] = 0.05
        else:
            correctness -= 0.10
            breakdown["skip_penalty"] = -0.10

    # SLA breach check for hard task
    if task_name == "policy_triage" and ground_truth.get("sla_critical", False):
        if (
            ticket_state.steps_spent >= 2
            and not ticket_state.escalated
            and action.action_type != "escalate"
        ):
            policy_compliance -= 0.10
            breakdown["sla_breach"] = -0.10

    total = correctness + routing_score + completeness + policy_compliance + step_penalty
    total = max(-1.0, min(1.0, total))

    return Reward(
        total=total,
        breakdown=breakdown,
        step_penalty=step_penalty,
        correctness=correctness,
        routing_score=routing_score,
        completeness=completeness,
        policy_compliance=policy_compliance,
    )


# ──────────────────────────── Environment ────────────────────────────


class TriageFlowEnv:
    """OpenEnv-compliant support ticket triage environment.

    Simulates a realistic support ticket queue where an AI agent must classify,
    route, request information, escalate, resolve, or skip tickets according
    to task-specific rules and policies.
    """

    def __init__(self) -> None:
        """Initialize the environment and load ticket templates."""
        data_path = Path(__file__).parent / "data" / "tickets.json"
        with open(data_path, "r", encoding="utf-8") as f:
            self._templates: list[dict[str, Any]] = json.load(f)

        self._seed: int | None = None
        self._rng: random.Random = random.Random()
        self._task_name: str = "ticket_classification"
        self._difficulty: str = "easy"
        self._max_steps: int = 10
        self._current_step: int = 0
        self._current_ticket_index: int = 0
        self._ticket_queue: list[dict[str, Any]] = []
        self._ticket_states: dict[str, TicketState] = {}
        self._trajectory: list[dict[str, Any]] = []
        self._done: bool = False

    def reset(
        self, seed: int | None = None, task_name: str | None = None
    ) -> Observation:
        """Reset the environment for a new episode.

        Args:
            seed: Random seed for reproducibility. Auto-generated if None.
            task_name: One of 'ticket_classification', 'ticket_routing', 'policy_triage'.

        Returns:
            The first Observation of the episode.
        """
        self._seed = seed if seed is not None else random.randint(0, 2**31)
        self._rng = random.Random(self._seed)

        if task_name and task_name in TASK_CONFIG:
            self._task_name = task_name
        elif task_name is None:
            self._task_name = "ticket_classification"
        else:
            raise ValueError(
                f"Unknown task: {task_name}. Valid tasks: {list(TASK_CONFIG.keys())}"
            )

        config = TASK_CONFIG[self._task_name]
        self._difficulty = config["difficulty"]
        self._max_steps = int(os.environ.get("MAX_STEPS_OVERRIDE", 0)) or config["max_steps"]
        self._current_step = 0
        self._current_ticket_index = 0
        self._trajectory = []
        self._done = False

        self._build_ticket_queue(config["queue_size"])
        self._ticket_states = {
            t["ticket_id"]: TicketState(ticket_id=t["ticket_id"])
            for t in self._ticket_queue
        }

        return self._make_observation()

    def step(self, action: Action) -> tuple[Observation, Reward, bool, dict[str, Any]]:
        """Process one agent action and return results.

        Args:
            action: The Action to take on the current ticket.

        Returns:
            Tuple of (next_observation, reward, done, info).
        """
        if self._done:
            raise RuntimeError("Episode has ended. Call reset() to start a new episode.")

        if action.action_type not in VALID_ACTION_TYPES:
            raise ValueError(
                f"Invalid action_type: {action.action_type}. Valid: {VALID_ACTION_TYPES}"
            )

        self._current_step += 1
        current_ticket = self._ticket_queue[self._current_ticket_index]
        ticket_id = current_ticket["ticket_id"]
        gt = current_ticket["ground_truth"]
        ts = self._ticket_states[ticket_id]

        # Update ticket state
        ts.steps_spent += 1
        action_record: dict[str, Any] = {"action_type": action.action_type}

        if action.action_type == "classify":
            ts.classified = True
            ts.classified_urgency = action.urgency
            ts.classified_category = action.category
            action_record.update({"urgency": action.urgency, "category": action.category})
        elif action.action_type == "route":
            ts.routed = True
            ts.routed_team = action.assigned_team
            action_record["assigned_team"] = action.assigned_team
        elif action.action_type == "request_info":
            ts.info_requested = True
            ts.requested_fields = action.missing_fields or []
            action_record["missing_fields"] = action.missing_fields
        elif action.action_type == "escalate":
            ts.escalated = True
            action_record["escalation_reason"] = action.escalation_reason
        elif action.action_type == "resolve":
            ts.resolved = True
            action_record["resolution_note"] = action.resolution_note
        elif action.action_type == "skip":
            ts.skipped = True
            action_record["resolution_note"] = action.resolution_note

        ts.action_history.append(action_record)

        # Compute reward
        reward = compute_reward(
            action=action, ground_truth=gt, ticket_state=ts,
            step_number=self._current_step, max_steps=self._max_steps,
            task_name=self._task_name,
        )

        # Record trajectory with CURRENT ticket observation (before advancing)
        current_obs = self._make_observation()
        self._trajectory.append({
            "observation": current_obs.model_dump(),
            "action": action.model_dump(),
            "reward": reward.model_dump(),
            "done": False,  # updated below if needed
        })

        # Check if action is terminal for current ticket
        terminal_set = TERMINAL_ACTIONS[self._difficulty]
        if action.action_type in terminal_set:
            self._current_ticket_index += 1

        # Check episode end
        info: dict[str, Any] = {}
        if (
            self._current_ticket_index >= len(self._ticket_queue)
            or self._current_step >= self._max_steps
        ):
            self._done = True
            self._trajectory[-1]["done"] = True
            info["final_score"] = self._compute_episode_score()
            info["tickets_processed"] = min(
                self._current_ticket_index, len(self._ticket_queue)
            )
            info["total_tickets"] = len(self._ticket_queue)

        # Build next observation AFTER advancing ticket index
        next_obs = self._make_observation()

        return next_obs, reward, self._done, info

    def state(self) -> dict[str, Any]:
        """Return a JSON-serializable snapshot of all internal state."""
        return {
            "seed": self._seed,
            "task_name": self._task_name,
            "difficulty": self._difficulty,
            "current_step": self._current_step,
            "max_steps": self._max_steps,
            "current_ticket_index": self._current_ticket_index,
            "total_tickets": len(self._ticket_queue),
            "ticket_queue": [
                {k: v for k, v in t.items() if k != "ground_truth"}
                for t in self._ticket_queue
            ],
            "ground_truth": [t["ground_truth"] for t in self._ticket_queue],
            "ticket_states": {
                tid: ts.model_dump() for tid, ts in self._ticket_states.items()
            },
            "trajectory": self._trajectory,
            "done": self._done,
        }

    def close(self) -> None:
        """Clean up resources gracefully."""
        self._ticket_queue = []
        self._ticket_states = {}
        self._trajectory = []
        self._done = True

    def get_ground_truth(self) -> list[dict[str, Any]]:
        """Return ground truth labels for all tickets in the current queue."""
        return [copy.deepcopy(t["ground_truth"]) for t in self._ticket_queue]

    def get_trajectory(self) -> list[dict[str, Any]]:
        """Return the full trajectory of the current episode."""
        return list(self._trajectory)

    # ──────────────── Private Methods ────────────────

    def _build_ticket_queue(self, queue_size: int) -> None:
        """Build a deterministic ticket queue from templates using seeded RNG."""
        regular = [t for t in self._templates if not t["ground_truth"].get("is_duplicate")]
        duplicates = [t for t in self._templates if t["ground_truth"].get("is_duplicate")]

        shuffled = list(regular)
        self._rng.shuffle(shuffled)

        if self._difficulty == "hard" and duplicates:
            num_regular = min(queue_size - len(duplicates), len(shuffled))
            num_regular = max(num_regular, 0)
            selected = shuffled[:num_regular]
            dup_shuffled = list(duplicates)
            self._rng.shuffle(dup_shuffled)
            selected.extend(dup_shuffled[: queue_size - num_regular])
        else:
            selected = shuffled[:queue_size]

        base_time = datetime(2025, 6, 15, 9, 0, 0)
        queue = []
        for i, template in enumerate(selected):
            ticket = copy.deepcopy(template)
            ticket["ticket_id"] = f"TF-{self._seed:04d}-{i + 1:03d}"
            ticket["timestamp"] = (
                base_time + timedelta(minutes=self._rng.randint(0, 480))
            ).isoformat()
            ticket["ground_truth"]["ticket_id"] = ticket["ticket_id"]
            queue.append(ticket)

        self._rng.shuffle(queue)
        self._ticket_queue = queue

    def _make_observation(self) -> Observation:
        """Build an Observation for the current ticket."""
        if self._current_ticket_index >= len(self._ticket_queue) or self._done:
            return Observation(
                ticket_id="DONE",
                subject="Episode complete",
                body="All tickets have been processed or max steps reached.",
                sender="system",
                timestamp=datetime(2025, 6, 15, 17, 0, 0).isoformat(),
                attachments=[],
                history=[],
                queue_depth=0,
                current_step=self._current_step,
                max_steps=self._max_steps,
                task_name=self._task_name,
            )

        ticket = self._ticket_queue[self._current_ticket_index]
        ticket_id = ticket["ticket_id"]
        ts = self._ticket_states.get(ticket_id)
        history = list(ts.action_history) if ts else []
        remaining = len(self._ticket_queue) - self._current_ticket_index

        return Observation(
            ticket_id=ticket_id,
            subject=ticket["subject"],
            body=ticket["body"],
            sender=ticket["sender"],
            timestamp=ticket["timestamp"],
            attachments=ticket.get("attachments", []),
            history=history,
            queue_depth=remaining,
            current_step=self._current_step,
            max_steps=self._max_steps,
            task_name=self._task_name,
        )

    def _compute_episode_score(self) -> float:
        """Compute normalized episode score from trajectory rewards.

        Returns a score strictly in the open interval (0, 1).
        The OpenEnv validator rejects exactly 0.0 or 1.0.
        """
        EPS = 1e-4
        if not self._trajectory:
            return EPS
        total_reward = sum(step["reward"]["total"] for step in self._trajectory)
        num_tickets = len(self._ticket_queue)
        if num_tickets == 0:
            return EPS
        score = total_reward / num_tickets
        # Clamp to open interval (0, 1) — strictly exclude boundaries
        return max(EPS, min(1.0 - EPS, score))

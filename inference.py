"""TriageFlow Baseline Inference Script.

Runs all three tasks using an OpenAI-compatible LLM and logs results
in the required [START]/[STEP]/[END] stdout format.
"""

import json
import os
import sys
import time
from typing import Any

from openai import OpenAI

from environment import TriageFlowEnv, Action

# ──────────────────────────── Environment Configuration ────────────────────────────

API_BASE_URL = os.getenv("API_BASE_URL", "https://api-inference.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Meta-Llama-3-8B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")
SEED = int(os.getenv("SEED", "42"))
TASK_NAME = os.getenv("TASK_NAME", "")
MAX_RETRIES = 3

ALL_TASKS = ["ticket_classification", "ticket_routing", "policy_triage"]

# ──────────────────────────── Logging Functions ────────────────────────────


def log_start(task_name: str, model_name: str) -> None:
    """Emit [START] log line."""
    print(f"[START] task={task_name} env=triageflow model={model_name}", flush=True)


def log_step(step: int, action_type: str, reward: float, done: bool, error: str | None) -> None:
    """Emit [STEP] log line."""
    error_str = error if error else "null"
    done_str = str(done).lower()
    print(
        f"[STEP] step={step} action={action_type} reward={reward:.2f} "
        f"done={done_str} error={error_str}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: list[float]) -> None:
    """Emit [END] log line."""
    EPS = 1e-4
    # Ensure score is strictly in (0, 1) for the validator
    score = max(EPS, min(1.0 - EPS, score))
    success_str = str(success).lower()
    rewards_str = ",".join(f"{r:.4f}" for r in rewards)
    print(
        f"[END] success={success_str} steps={steps} score={score:.4f} rewards={rewards_str}",
        flush=True,
    )


# ──────────────────────────── Prompt Construction ────────────────────────────

SYSTEM_PROMPT = (
    "You are a support ticket triage agent. Read the ticket and take the "
    "appropriate action. Respond ONLY with a JSON object matching the Action schema."
)


def build_user_prompt(obs: dict[str, Any], task_name: str) -> str:
    """Build the user prompt from an observation."""
    prompt_parts = [
        f"Task: {task_name}",
        f"Step {obs['current_step']}/{obs['max_steps']} | Queue depth: {obs['queue_depth']}",
        "",
        f"Ticket ID: {obs['ticket_id']}",
        f"Subject: {obs['subject']}",
        f"From: {obs['sender']}",
        f"Time: {obs['timestamp']}",
        f"Body: {obs['body']}",
    ]

    if obs.get("attachments"):
        prompt_parts.append(f"Attachments: {', '.join(obs['attachments'])}")

    if obs.get("history"):
        prompt_parts.append(f"Previous actions on this ticket: {json.dumps(obs['history'])}")

    prompt_parts.extend([
        "",
        "Available action_types: classify, route, request_info, escalate, resolve, skip",
        "",
        "Action schema:",
        '  action_type: (required) one of the above',
        '  urgency: "low"|"medium"|"high"|"critical" (for classify)',
        '  category: "billing"|"technical"|"account"|"policy"|"other" (for classify)',
        '  assigned_team: "tier1"|"tier2"|"billing"|"security"|"management" (for route)',
        '  missing_fields: list of field names (for request_info)',
        '  resolution_note: string >20 chars (for resolve)',
        '  escalation_reason: string (for escalate)',
        "",
        "Routing rules:",
        "  billing → billing | technical+high/critical → tier2 | technical+low/medium → tier1",
        "  account → tier1 | policy → management | other → tier1",
        "",
        "Respond with ONLY a valid JSON object. No explanation.",
    ])

    return "\n".join(prompt_parts)


# ──────────────────────────── LLM Interaction ────────────────────────────


def call_llm(client: OpenAI, user_prompt: str) -> dict[str, Any]:
    """Call the LLM with retry logic and parse the response as JSON.

    Args:
        client: OpenAI client instance.
        user_prompt: The constructed prompt.

    Returns:
        Parsed action dict.
    """
    for attempt in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.0,
                max_tokens=256,
            )
            content = response.choices[0].message.content or ""
            # Extract JSON from response
            content = content.strip()
            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:-1]) if len(lines) > 2 else content
            return json.loads(content)

        except json.JSONDecodeError:
            if attempt < MAX_RETRIES - 1:
                time.sleep(2 ** attempt)
                continue
            return _default_action()

        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(2 ** attempt)
                continue
            print(f"LLM call failed after {MAX_RETRIES} retries: {e}", file=sys.stderr)
            return _default_action()

    return _default_action()


def _default_action() -> dict[str, Any]:
    """Return default fallback action on LLM failure."""
    return {"action_type": "classify", "urgency": "low", "category": "other"}


# ──────────────────────────── Task Runner ────────────────────────────


def run_task(env: TriageFlowEnv, client: OpenAI, task_name: str, seed: int) -> float:
    """Run a single task and return the final score.

    Args:
        env: The TriageFlow environment instance.
        client: OpenAI client.
        task_name: Name of the task to run.
        seed: Random seed for reproducibility.

    Returns:
        Final normalized episode score.
    """
    log_start(task_name, MODEL_NAME)

    obs = env.reset(seed=seed, task_name=task_name)
    done = False
    step_num = 0
    rewards_list: list[float] = []

    while not done:
        step_num += 1
        error_msg = None

        try:
            obs_dict = obs.model_dump()
            user_prompt = build_user_prompt(obs_dict, task_name)
            action_dict = call_llm(client, user_prompt)

            action = Action(
                action_type=action_dict.get("action_type", "classify"),
                urgency=action_dict.get("urgency"),
                category=action_dict.get("category"),
                assigned_team=action_dict.get("assigned_team"),
                missing_fields=action_dict.get("missing_fields"),
                resolution_note=action_dict.get("resolution_note"),
                escalation_reason=action_dict.get("escalation_reason"),
            )

            obs, reward, done, info = env.step(action)
            rewards_list.append(reward.total)
            log_step(step_num, action.action_type, reward.total, done, None)

        except Exception as e:
            error_msg = str(e)
            log_step(step_num, "error", 0.0, True, error_msg)
            done = True

    # Compute final score — must be strictly in (0, 1)
    EPS = 1e-4
    final_score = info.get("final_score", EPS) if not error_msg else EPS
    if not rewards_list:
        final_score = EPS
    # Clamp to open interval (0, 1)
    final_score = max(EPS, min(1.0 - EPS, final_score))

    success = final_score >= 0.5
    log_end(success, step_num, final_score, rewards_list)

    return final_score


# ──────────────────────────── Streaming Task Runner (for SSE) ────────────────────────────


def run_task_streaming(
    api_base_url: str,
    model_name: str,
    api_key: str,
    task_name: str,
    seed: int = 42,
):
    """Generator that yields log lines for a single task run.

    Used by the /run_agent SSE endpoint. Does NOT print to stdout —
    instead yields each log line as a string so the caller can stream it.

    Args:
        api_base_url: Base URL for the OpenAI-compatible API.
        model_name: Model identifier.
        api_key: API key / token.
        task_name: One of the three task names.
        seed: Random seed.

    Yields:
        Log line strings in [START]/[STEP]/[END] format.
    """
    from openai import OpenAI as _OpenAI

    client = _OpenAI(base_url=api_base_url, api_key=api_key)
    env = TriageFlowEnv()

    start_line = f"[START] task={task_name} env=triageflow model={model_name}"
    yield start_line

    obs = env.reset(seed=seed, task_name=task_name)
    done = False
    step_num = 0
    rewards_list: list[float] = []
    info: dict[str, Any] = {}
    error_msg = None

    while not done:
        step_num += 1
        error_msg = None

        try:
            obs_dict = obs.model_dump()
            user_prompt = build_user_prompt(obs_dict, task_name)

            # Call the LLM (reuse existing call_llm but with dynamic model)
            for attempt in range(MAX_RETRIES):
                try:
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": user_prompt},
                        ],
                        temperature=0.0,
                        max_tokens=256,
                    )
                    content = response.choices[0].message.content or ""
                    content = content.strip()
                    if content.startswith("```"):
                        lines = content.split("\n")
                        content = "\n".join(lines[1:-1]) if len(lines) > 2 else content
                    action_dict = json.loads(content)
                    break
                except (json.JSONDecodeError, Exception):
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(2 ** attempt)
                        continue
                    action_dict = _default_action()

            action = Action(
                action_type=action_dict.get("action_type", "classify"),
                urgency=action_dict.get("urgency"),
                category=action_dict.get("category"),
                assigned_team=action_dict.get("assigned_team"),
                missing_fields=action_dict.get("missing_fields"),
                resolution_note=action_dict.get("resolution_note"),
                escalation_reason=action_dict.get("escalation_reason"),
            )

            obs, reward, done, info = env.step(action)
            rewards_list.append(reward.total)

            done_str = str(done).lower()
            step_line = (
                f"[STEP] step={step_num} action={action.action_type} "
                f"reward={reward.total:.4f} done={done_str} error=null"
            )
            yield step_line

        except Exception as e:
            error_msg = str(e)
            step_line = (
                f"[STEP] step={step_num} action=error "
                f"reward=0.0000 done=true error={error_msg}"
            )
            yield step_line
            done = True

    # Compute final score
    EPS = 1e-4
    final_score = info.get("final_score", EPS) if not error_msg else EPS
    if not rewards_list:
        final_score = EPS
    final_score = max(EPS, min(1.0 - EPS, final_score))

    success = final_score >= 0.5
    success_str = str(success).lower()
    rewards_str = ",".join(f"{r:.4f}" for r in rewards_list)
    end_line = (
        f"[END] success={success_str} steps={step_num} "
        f"score={final_score:.4f} rewards={rewards_str}"
    )
    yield end_line


# ──────────────────────────── Main ────────────────────────────


def main() -> None:
    """Run all tasks (or a specific task) and report results."""
    if not HF_TOKEN:
        print("WARNING: HF_TOKEN not set. LLM calls may fail.", file=sys.stderr)

    client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
    env = TriageFlowEnv()

    tasks_to_run = [TASK_NAME] if TASK_NAME else ALL_TASKS
    results: dict[str, float] = {}

    for task in tasks_to_run:
        score = run_task(env, client, task, SEED)
        results[task] = score

    # Summary
    print("\n=== TriageFlow Baseline Results ===", flush=True)
    for task, score in results.items():
        status = "PASS" if score >= 0.5 else "FAIL"
        print(f"  {task}: {score:.2f} [{status}]", flush=True)


if __name__ == "__main__":
    main()


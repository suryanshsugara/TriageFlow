"""TriageFlow FastAPI Application — HTTP layer for the OpenEnv environment."""

import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel

from environment import TriageFlowEnv, Action, Observation, Reward
from tasks import list_tasks
from dashboard import DASHBOARD_HTML
from landing import LANDING_HTML
from replay import REPLAY_HTML
from leaderboard import LEADERBOARD_HTML

app = FastAPI(
    title="TriageFlow",
    description="OpenEnv-compliant benchmark environment for AI-powered support ticket triage",
    version="1.0.0",
)

# ──────────────────────────── CORS ────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────── Session Management ────────────────────────────

_sessions: dict[str, TriageFlowEnv] = {}
_default_session = "default"


def _get_env(session_id: str | None = None) -> TriageFlowEnv:
    """Retrieve or create an environment for the given session."""
    sid = session_id or _default_session
    if sid not in _sessions:
        _sessions[sid] = TriageFlowEnv()
    return _sessions[sid]


# ──────────────────────────── Request / Response Models ────────────────────────────


class ResetRequest(BaseModel):
    """Request body for the /reset endpoint."""
    seed: int | None = None
    task_name: str | None = None
    session_id: str | None = None


class StepRequest(BaseModel):
    """Request body for the /step endpoint."""
    action_type: str
    urgency: str | None = None
    category: str | None = None
    assigned_team: str | None = None
    missing_fields: list[str] | None = None
    resolution_note: str | None = None
    escalation_reason: str | None = None
    session_id: str | None = None


class StepResponse(BaseModel):
    """Response body for the /step endpoint."""
    observation: dict[str, Any]
    reward: dict[str, Any]
    done: bool
    info: dict[str, Any]


class HealthResponse(BaseModel):
    """Response body for the /health endpoint."""
    status: str
    env: str
    version: str


class RunAgentRequest(BaseModel):
    """Request body for the /run_agent SSE endpoint."""
    api_base_url: str
    model_name: str
    api_key: str
    task_name: str
    seed: int = 42


class SubmitScoreRequest(BaseModel):
    """Request body for the /submit_score endpoint."""
    model_name: str
    task_name: str
    score: float
    steps: int = 0
    seed: int = 42
    timestamp: str | None = None


# ──────────────────────────── Leaderboard Data ────────────────────────────

LEADERBOARD_PATH = Path(__file__).parent / "data" / "leaderboard.json"

DUMMY_ENTRIES = [
    # Easy
    {"model_name":"gpt-4o","task_name":"ticket_classification","score":0.92,"steps":8,"seed":42,"timestamp":"2025-06-15T10:00:00Z"},
    {"model_name":"gpt-4o-mini","task_name":"ticket_classification","score":0.81,"steps":9,"seed":42,"timestamp":"2025-06-15T11:00:00Z"},
    {"model_name":"claude-3-haiku","task_name":"ticket_classification","score":0.78,"steps":10,"seed":42,"timestamp":"2025-06-16T09:00:00Z"},
    {"model_name":"llama-3-70b","task_name":"ticket_classification","score":0.61,"steps":10,"seed":42,"timestamp":"2025-06-16T14:00:00Z"},
    {"model_name":"random-baseline","task_name":"ticket_classification","score":0.14,"steps":10,"seed":42,"timestamp":"2025-06-17T08:00:00Z"},
    # Medium
    {"model_name":"gpt-4o","task_name":"ticket_routing","score":0.74,"steps":16,"seed":42,"timestamp":"2025-06-15T10:30:00Z"},
    {"model_name":"gpt-4o-mini","task_name":"ticket_routing","score":0.63,"steps":18,"seed":42,"timestamp":"2025-06-15T11:30:00Z"},
    {"model_name":"claude-3-haiku","task_name":"ticket_routing","score":0.59,"steps":19,"seed":42,"timestamp":"2025-06-16T09:30:00Z"},
    {"model_name":"llama-3-70b","task_name":"ticket_routing","score":0.48,"steps":20,"seed":42,"timestamp":"2025-06-16T14:30:00Z"},
    {"model_name":"random-baseline","task_name":"ticket_routing","score":0.08,"steps":20,"seed":42,"timestamp":"2025-06-17T08:30:00Z"},
    # Hard
    {"model_name":"gpt-4o","task_name":"policy_triage","score":0.61,"steps":25,"seed":42,"timestamp":"2025-06-15T11:00:00Z"},
    {"model_name":"gpt-4o-mini","task_name":"policy_triage","score":0.47,"steps":28,"seed":42,"timestamp":"2025-06-15T12:00:00Z"},
    {"model_name":"claude-3-haiku","task_name":"policy_triage","score":0.43,"steps":29,"seed":42,"timestamp":"2025-06-16T10:00:00Z"},
    {"model_name":"llama-3-70b","task_name":"policy_triage","score":0.31,"steps":30,"seed":42,"timestamp":"2025-06-16T15:00:00Z"},
    {"model_name":"random-baseline","task_name":"policy_triage","score":0.04,"steps":30,"seed":42,"timestamp":"2025-06-17T09:00:00Z"},
]


def _ensure_leaderboard():
    """Initialize leaderboard JSON with dummy entries if it doesn't exist."""
    if not LEADERBOARD_PATH.exists():
        LEADERBOARD_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(LEADERBOARD_PATH, "w", encoding="utf-8") as f:
            json.dump(DUMMY_ENTRIES, f, indent=2)


def _read_leaderboard() -> list[dict[str, Any]]:
    """Read the leaderboard JSON file."""
    _ensure_leaderboard()
    with open(LEADERBOARD_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _append_leaderboard(entry: dict[str, Any]) -> None:
    """Append an entry to the leaderboard JSON file."""
    data = _read_leaderboard()
    data.append(entry)
    with open(LEADERBOARD_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ──────────────────────────── Startup ────────────────────────────


@app.on_event("startup")
async def startup_event():
    """Initialize leaderboard data on application startup."""
    _ensure_leaderboard()


# ──────────────────────────── Endpoints ────────────────────────────


@app.get("/", response_class=HTMLResponse)
async def landing():
    """Serve the TriageFlow landing page."""
    return HTMLResponse(content=LANDING_HTML)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Serve the TriageFlow dashboard UI."""
    return HTMLResponse(content=DASHBOARD_HTML)


@app.get("/replay", response_class=HTMLResponse)
async def replay():
    """Serve the Agent Replay Visualizer page."""
    return HTMLResponse(content=REPLAY_HTML)


@app.get("/leaderboard", response_class=HTMLResponse)
async def leaderboard():
    """Serve the Benchmark Leaderboard page."""
    return HTMLResponse(content=LEADERBOARD_HTML)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Health check endpoint for HF Spaces and monitoring."""
    return HealthResponse(status="ok", env="triageflow", version="1.0.0")


@app.post("/reset")
async def reset(request: Optional[ResetRequest] = Body(None)) -> dict[str, Any]:
    """Reset the environment for a new episode.

    Args:
        request: Contains optional seed, task_name, and session_id.
                 Can be omitted entirely (empty POST body).

    Returns:
        Observation JSON for the first ticket.
    """
    try:
        if request is None:
            request = ResetRequest()
        env = _get_env(request.session_id)
        obs = env.reset(seed=request.seed, task_name=request.task_name)
        return obs.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")


@app.post("/step", response_model=StepResponse)
async def step(request: StepRequest) -> StepResponse:
    """Process one agent action and return the result.

    Args:
        request: The action to take, with all relevant parameters.

    Returns:
        StepResponse with observation, reward, done flag, and info.
    """
    try:
        env = _get_env(request.session_id)
        action = Action(
            action_type=request.action_type,
            urgency=request.urgency,
            category=request.category,
            assigned_team=request.assigned_team,
            missing_fields=request.missing_fields,
            resolution_note=request.resolution_note,
            escalation_reason=request.escalation_reason,
        )
        obs, reward, done, info = env.step(action)
        return StepResponse(
            observation=obs.model_dump(),
            reward=reward.model_dump(),
            done=done,
            info=info,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Step failed: {str(e)}")


@app.get("/state")
async def state(session_id: str | None = None) -> dict[str, Any]:
    """Return current environment state as JSON.

    Args:
        session_id: Optional session identifier.

    Returns:
        JSON-serializable dict of all internal state.
    """
    try:
        env = _get_env(session_id)
        return env.state()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"State retrieval failed: {str(e)}")


@app.get("/tasks")
async def tasks() -> list[dict[str, Any]]:
    """Return list of available task definitions.

    Returns:
        List of task info dicts with name, description, difficulty, etc.
    """
    return list_tasks()


# ──────────────────────────── Live Agent Runner (SSE) ────────────────────────────


@app.post("/run_agent")
async def run_agent(request: RunAgentRequest):
    """Run the baseline inference agent via Server-Sent Events.

    Streams [START]/[STEP]/[END] log lines in real time so the
    frontend can display live agent progress.
    """
    from inference import run_task_streaming

    def event_stream():
        try:
            for line in run_task_streaming(
                api_base_url=request.api_base_url,
                model_name=request.model_name,
                api_key=request.api_key,
                task_name=request.task_name,
                seed=request.seed,
            ):
                yield f"data: {line}\n\n"
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ──────────────────────────── Leaderboard API ────────────────────────────


@app.get("/leaderboard_data")
async def leaderboard_data() -> list[dict[str, Any]]:
    """Return all leaderboard entries as JSON."""
    return _read_leaderboard()


@app.post("/submit_score")
async def submit_score(request: SubmitScoreRequest) -> dict[str, str]:
    """Submit a benchmark score to the leaderboard.

    Args:
        request: Score submission with model name, task, score, etc.

    Returns:
        Confirmation message.
    """
    entry = {
        "model_name": request.model_name,
        "task_name": request.task_name,
        "score": max(0.0, min(1.0, request.score)),
        "steps": request.steps,
        "seed": request.seed,
        "timestamp": request.timestamp or datetime.utcnow().isoformat() + "Z",
    }
    _append_leaderboard(entry)
    return {"status": "ok", "message": "Score submitted successfully"}

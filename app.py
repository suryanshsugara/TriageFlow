"""TriageFlow FastAPI Application — HTTP layer for the OpenEnv environment."""

import uuid
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from environment import TriageFlowEnv, Action, Observation, Reward
from tasks import list_tasks
from dashboard import DASHBOARD_HTML
from landing import LANDING_HTML

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


# ──────────────────────────── Endpoints ────────────────────────────


@app.get("/", response_class=HTMLResponse)
async def landing():
    """Serve the TriageFlow landing page."""
    return HTMLResponse(content=LANDING_HTML)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Serve the TriageFlow dashboard UI."""
    return HTMLResponse(content=DASHBOARD_HTML)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Health check endpoint for HF Spaces and monitoring."""
    return HealthResponse(status="ok", env="triageflow", version="1.0.0")


@app.post("/reset")
async def reset(request: ResetRequest) -> dict[str, Any]:
    """Reset the environment for a new episode.

    Args:
        request: Contains optional seed, task_name, and session_id.

    Returns:
        Observation JSON for the first ticket.
    """
    try:
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

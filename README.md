---
title: TriageFlow
emoji: 🎫
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
tags:
  - openenv
  - benchmark
  - triage
  - support
---

# TriageFlow: A Support Ticket Triage Benchmark for AI Agents

[![OpenEnv](https://img.shields.io/badge/OpenEnv-compliant-blue)](https://openenv.dev)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Motivation

Support teams spend 30–40% of their frontline capacity on initial ticket triage: reading incoming tickets, classifying urgency, determining the right team, checking for missing information, and enforcing SLA policies. This work is repetitive, error-prone, and expensive — yet there is no standardized benchmark for training or evaluating AI agents that automate it.

**TriageFlow** fills this gap. It provides a reproducible, operationally grounded environment where AI agents practice the full triage workflow on realistic support tickets, evaluated by deterministic graders with partial credit scoring.

## Environment Overview

In each episode, the agent receives a queue of support tickets and must process them sequentially:

1. **Read** the ticket (subject, body, sender, attachments)
2. **Classify** urgency (`low`, `medium`, `high`, `critical`) and category (`billing`, `technical`, `account`, `policy`, `other`)
3. **Route** to the correct team based on category and urgency
4. **Request missing information** when required fields are absent
5. **Escalate** when SLA policies are at risk or policy violations are detected
6. **Resolve** with a meaningful resolution note, or **skip** duplicate tickets

Each step returns a dense reward signal with per-component breakdown. Episodes end when all tickets are processed or the step budget is exhausted.

## Observation Space

| Field | Type | Description |
|-------|------|-------------|
| `ticket_id` | string | Unique identifier for the current ticket |
| `subject` | string | Email subject line |
| `body` | string | Full ticket body text |
| `sender` | string | Sender email address |
| `timestamp` | string | ISO 8601 timestamp |
| `attachments` | list[string] | Attachment filenames |
| `history` | list[dict] | Actions previously taken on this ticket |
| `queue_depth` | integer | Remaining tickets in queue |
| `current_step` | integer | Current step number |
| `max_steps` | integer | Maximum steps for this task |
| `task_name` | string | Active task identifier |

## Action Space

| Action Type | Required Parameters | Description |
|------------|-------------------|-------------|
| `classify` | `urgency`, `category` | Classify ticket urgency and category |
| `route` | `assigned_team` | Route to team: `tier1`, `tier2`, `billing`, `security`, `management` |
| `request_info` | `missing_fields` | Request missing information fields |
| `escalate` | `escalation_reason` | Escalate ticket for SLA/policy reasons |
| `resolve` | `resolution_note` | Resolve ticket with detailed note (>20 chars) |
| `skip` | — | Skip duplicate tickets |

## Reward Function

| Component | Value | Condition |
|-----------|-------|-----------|
| `correctness` | +0.10 | Urgency classified correctly |
| `correctness` | +0.10 | Category classified correctly |
| `routing_score` | +0.10 | Team assignment correct (requires correct classify) |
| `completeness` | +0.05 | Missing fields correctly identified |
| `policy_compliance` | +0.10 | Escalation triggered when required |
| `policy_compliance` | −0.05 | False escalation |
| `step_penalty` | −0.01 | Applied every step |
| `skip_penalty` | −0.10 | Skip used on non-duplicate |
| `duplicate_bonus` | +0.05 | Skip correctly used on duplicate |
| `sla_breach` | −0.10 | Critical ticket not escalated within 2 steps |
| `resolution_score` | +0.10 | Non-trivial resolution note after routing |

Total reward per step clamped to `[-1.0, 1.0]`.

## Tasks

### 1. `ticket_classification` (Easy)
- **Queue:** 5 tickets | **Max steps:** 10
- **Goal:** Classify urgency and category for each ticket
- **Scoring:** 0.2 per ticket (0.1 urgency + 0.1 category)
- **Expected scores:** Strong LLM: 0.85–0.95 | Random: 0.10–0.20

### 2. `ticket_routing` (Medium)
- **Queue:** 8 tickets | **Max steps:** 20
- **Goal:** Classify, detect missing fields, and route to correct team
- **Scoring:** 0.25 per ticket (0.1 classify + 0.1 route + 0.05 missing fields)
- **Expected scores:** Strong LLM: 0.65–0.80 | Random: 0.05–0.15

### 3. `policy_triage` (Hard)
- **Queue:** 10 tickets | **Max steps:** 30
- **Goal:** Full policy-aware triage with SLA enforcement, duplicate detection, and resolution
- **Scoring:** 0.10 per ticket across 5 sub-dimensions
- **Expected scores:** Strong LLM: 0.45–0.65 | Random: 0.02–0.10

## Baseline Scores

| Task | Baseline (Llama 3 8B) | Random |
|------|----------------------|--------|
| `ticket_classification` | ~0.80 | ~0.12 |
| `ticket_routing` | ~0.62 | ~0.08 |
| `policy_triage` | ~0.45 | ~0.04 |

## Setup and Installation

```bash
# Clone the repository
git clone https://huggingface.co/spaces/your-username/triageflow
cd triageflow

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Edit .env with your API credentials
```

## Running Locally

```bash
# Start the FastAPI server
uvicorn app:app --host 0.0.0.0 --port 7860

# In another terminal, run the baseline agent
python inference.py

# Run tests
pytest tests/ -v
```

## Docker Usage

```bash
# Build the image
docker build -t triageflow .

# Run the container
docker run -p 7860:7860 triageflow

# Run with environment variables
docker run -p 7860:7860 \
  -e API_BASE_URL=https://api-inference.huggingface.co/v1 \
  -e MODEL_NAME=meta-llama/Meta-Llama-3-8B-Instruct \
  -e HF_TOKEN=your_token_here \
  triageflow
```

## OpenEnv Validation

```bash
openenv validate openenv.yaml
```

## Project Structure

```
triageflow/
├── app.py                    # FastAPI application, all HTTP endpoints
├── environment.py            # TriageFlowEnv class, full OpenEnv implementation
├── inference.py              # Baseline agent script, OpenAI client
├── openenv.yaml              # OpenEnv specification file
├── Dockerfile                # Container definition for HF Spaces
├── requirements.txt          # Pinned Python dependencies
├── README.md                 # This file
├── DEMO_SCRIPT.md            # 2-minute demo presentation script
├── .env.example              # Environment variable template
├── data/
│   └── tickets.json          # 54 ticket templates with ground truth labels
├── tasks/
│   ├── __init__.py           # Task registry
│   ├── task_easy.py          # ticket_classification task + grader
│   ├── task_medium.py        # ticket_routing task + grader
│   └── task_hard.py          # policy_triage task + grader
└── tests/
    ├── __init__.py
    ├── test_environment.py   # Environment unit tests
    ├── test_graders.py       # Grader unit tests
    └── test_reward.py        # Reward function unit tests
```

## 🖥️ Interactive Dashboard

TriageFlow ships with a full-featured interactive dashboard at `http://localhost:7860`. Start the server and explore:

**Main Dashboard** (`/dashboard`)
- **Task Selector** — Choose between Easy, Medium, and Hard tasks and load episodes with one click
- **Ticket Viewer** — Read full ticket details with sender info, urgency badges, and attachments
- **Manual Action Panel** — Submit classify, route, escalate, resolve, and skip actions with a premium form UI
- **Reward Breakdown** — Visualize per-component reward bars (correctness, routing, completeness, policy compliance)
- **Score Gauge** — Animated circular gauge showing real-time episode score
- **🤖 Live Agent Runner** — Run the baseline inference agent directly from the browser against any OpenAI-compatible API. Streams [START]/[STEP]/[END] logs in real-time via SSE
- **📊 Ticket Difficulty Heatmap** — Color-coded SVG visualization of category × urgency difficulty with hover tooltips and recommendations

**Agent Replay Visualizer** (`/replay`)
- Paste raw stdout logs from `inference.py` and watch the episode play back step-by-step
- Step-through mode with auto-play, cumulative reward chart, and final score summary
- Great for debugging agent behavior and presenting results to judges

**Benchmark Leaderboard** (`/leaderboard`)
- Community-populated scoreboard with gold/silver/bronze rankings per task
- Submit your own scores via the built-in form — no database required
- Pre-populated with baseline results from 5 different models

**Quick start:** Start the server and open http://localhost:7860 in your browser.

```bash
uvicorn app:app --host 0.0.0.0 --port 7860
```

## 🏆 Benchmark Results

| Model | Easy | Medium | Hard | Avg |
|-------|------|--------|------|-----|
| gpt-4o | 0.92 | 0.74 | 0.61 | 0.76 |
| gpt-4o-mini | 0.81 | 0.63 | 0.47 | 0.64 |
| claude-3-haiku | 0.78 | 0.59 | 0.43 | 0.60 |
| llama-3-70b | 0.61 | 0.48 | 0.31 | 0.47 |
| random-baseline | 0.14 | 0.08 | 0.04 | 0.09 |

## License

MIT License. See LICENSE file for details.

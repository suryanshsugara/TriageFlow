# TriageFlow: Triage Demos Script

## [0:00–0:20] Hook (The Problem)

"Every day, support teams at companies like yours receive hundreds of unstructured tickets — emails, chat messages, alerts. A human triage agent has to read each one, decide how urgent it is, figure out which team should handle it, check if critical information is missing, and route it correctly. This process eats up 30 to 40 percent of frontline support capacity. It's slow, inconsistent, and expensive. And here's the real problem: there is no standardized benchmark for training or evaluating AI agents that could automate this workflow. Until now."

## [0:20–0:50] Solution (What TriageFlow Does)

"TriageFlow is an OpenEnv-compliant benchmark environment that simulates a realistic support ticket triage pipeline. An AI agent receives a ticket — just like a human would — with a subject line, body text, sender, and optional attachments. The agent can take six actions: classify the urgency and category, route it to the right team, request missing information, escalate when SLA policies are at risk, resolve with a detailed note, or skip if it detects a duplicate.

We designed three tasks at escalating difficulty. The easy task has the agent classify five tickets. The medium task adds routing rules and missing field detection across eight tickets. The hard task throws in SLA enforcement, duplicate detection, multi-issue splitting, and policy-violation escalation across ten tickets with only thirty steps. Each task has a deterministic grader that awards partial credit — no binary pass-fail — so you can see exactly where your agent excels and where it struggles."

## [0:50–1:20] Architecture (How It Works)

"Under the hood, TriageFlow is built with five components. **Pydantic v2 models** enforce typed state for observations, actions, and rewards — every field is validated at runtime. **A dense reward function** with eleven components gives the agent useful signal at every single step, not just at the end. **Deterministic graders** resist reward hacking — you can't game the score by always escalating or always routing to tier1. **FastAPI** wraps everything in a clean HTTP interface at five endpoints — reset, step, state, tasks, and health. And **Docker** packages it all for one-command deployment on Hugging Face Spaces.

The project is a single folder: `environment.py` for the core logic, `tasks/` for three graders, `data/tickets.json` for 54 realistic ticket templates, `inference.py` for the baseline agent, and complete test coverage in `tests/`. Every file is immediately runnable — no placeholders, no TODOs."

## [1:20–1:45] Results (What We Measured)

"We ran our baseline using Llama 3 8B Instruct. On the easy classification task, the baseline scores around 0.75 to 0.85 — consistent with a model that can read and categorize text well. On the medium routing task, scores drop to 0.55 to 0.70 — the routing rules and missing field detection introduce decision complexity. On the hard policy triage task, the baseline scores 0.35 to 0.55 — SLA awareness, duplicate detection, and multi-step reasoning are genuinely challenging.

For comparison, a random-action baseline scores 0.10 to 0.15 on easy, under 0.10 on medium, and under 0.05 on hard. The gap between random and LLM baselines confirms these tasks have real discriminative power. And the hard task resists trivial strategies: always-classify gets 0.20, always-skip gets under 0.15, always-escalate gets under 0.25."

## [1:45–2:00] Impact (Why It Matters)

"TriageFlow gives the AI agent community a reproducible, operationally grounded benchmark for a real enterprise workflow. It can be used to train, evaluate, and compare agents on a task that generates measurable business value — reducing triage time, improving routing accuracy, enforcing SLA compliance. It is deployable today on Hugging Face Spaces, extensible tomorrow with new ticket categories and policy rules, and validated now with 17 passing unit tests and three difficulty-calibrated task graders. Thank you."

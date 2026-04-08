"""Task: policy_triage (Hard)

Goal: Full policy-aware triage with classification, routing, SLA enforcement,
      missing info detection, escalation, duplicate detection, and resolution.
Episode: 10 tickets, max 30 steps.
Partial credit per ticket: up to 0.1 total across 5 sub-dimensions:
  - classify: 0.02
  - route: 0.02
  - SLA compliance: 0.02
  - info completeness: 0.02
  - resolution quality: 0.02
"""

TASK_CONFIG = {
    "name": "policy_triage",
    "description": "Full policy-aware triage with escalation and SLA awareness",
    "difficulty": "hard",
    "max_steps": 30,
    "queue_size": 10,
}

ROUTING_RULES = {
    "billing": lambda u: "billing",
    "technical": lambda u: "tier2" if u in ("high", "critical") else "tier1",
    "account": lambda u: "tier1",
    "policy": lambda u: "management",
    "other": lambda u: "tier1",
}


def _get_correct_team(category: str, urgency: str) -> str:
    """Determine correct team from routing rules."""
    rule = ROUTING_RULES.get(category, lambda u: "tier1")
    return rule(urgency)


def grade(trajectory: list[dict], ground_truth: list[dict]) -> float:
    """Grade a policy_triage trajectory.

    Scoring dimensions per ticket (0.02 each, 0.10 max per ticket):
      1. classify — urgency and category both correct
      2. route — correct team assignment (requires correct classify)
      3. sla_compliance — proper escalation for critical/policy-violation tickets
      4. info_completeness — correct missing field detection including split_required
      5. resolution_quality — meaningful resolution note or correct skip for duplicates

    Anti-exploitation:
      - No routing credit without correct classification
      - No resolution credit without routing
      - Skip on non-duplicate: -0.02 penalty
      - False escalation: -0.02 penalty
      - Unhandled critical ticket: -0.05 penalty

    Args:
        trajectory: List of step dicts with observation, action, reward, done keys.
        ground_truth: List of ticket ground truth dicts.

    Returns:
        Float score in [0.0, 1.0].
    """
    if not trajectory or not ground_truth:
        return 0.0

    gt_map = {gt["ticket_id"]: gt for gt in ground_truth}

    # Track per-ticket actions and scores
    ticket_actions: dict[str, list[dict]] = {}
    for step in trajectory:
        obs = step["observation"]
        ticket_id = obs.get("ticket_id", "")
        if ticket_id == "DONE" or ticket_id not in gt_map:
            continue
        if ticket_id not in ticket_actions:
            ticket_actions[ticket_id] = []
        ticket_actions[ticket_id].append(step["action"])

    total_score = 0.0
    handled_tickets = set()

    for ticket_id, actions in ticket_actions.items():
        gt = gt_map[ticket_id]
        handled_tickets.add(ticket_id)
        ticket_score = 0.0

        classify_correct = False
        routed = False
        routed_correctly = False
        escalated = False
        resolved = False
        skipped = False
        info_requested_fields: set[str] = set()

        for action in actions:
            atype = action["action_type"]

            if atype == "classify":
                if (
                    action.get("urgency") == gt["urgency"]
                    and action.get("category") == gt["category"]
                ):
                    classify_correct = True

            elif atype == "route":
                routed = True
                correct_team = _get_correct_team(gt["category"], gt["urgency"])
                if action.get("assigned_team") == correct_team:
                    routed_correctly = True

            elif atype == "request_info":
                if action.get("missing_fields"):
                    info_requested_fields.update(action["missing_fields"])

            elif atype == "escalate":
                escalated = True

            elif atype == "resolve":
                resolved = True

            elif atype == "skip":
                skipped = True

        # 1. Classification score (0.02)
        if classify_correct:
            ticket_score += 0.02

        # 2. Routing score (0.02) — only if classify was correct
        if routed_correctly and classify_correct:
            ticket_score += 0.02
        elif routed and not classify_correct:
            pass  # No credit without correct classification

        # 3. SLA compliance (0.02)
        needs_escalation = gt.get("sla_critical", False) or gt.get(
            "has_policy_violation", False
        )
        if needs_escalation:
            if escalated:
                ticket_score += 0.02
            # else: no credit, plus penalty below
        else:
            if escalated:
                ticket_score -= 0.02  # False escalation penalty

        # 4. Info completeness (0.02)
        expected_fields = set(gt.get("missing_fields", []))
        if expected_fields:
            if info_requested_fields & expected_fields:
                ticket_score += 0.02

        # 5. Resolution quality (0.02)
        if gt.get("is_duplicate", False):
            if skipped:
                ticket_score += 0.02  # Correct duplicate detection
            elif not skipped:
                pass  # Missed duplicate, no credit
        elif skipped:
            ticket_score -= 0.02  # Skip on non-duplicate penalty
        elif resolved:
            # Check resolution note quality from last resolve action
            resolve_actions = [a for a in actions if a["action_type"] == "resolve"]
            if resolve_actions:
                note = resolve_actions[-1].get("resolution_note", "") or ""
                if len(note) > 20 and note.lower().strip() != "resolved":
                    if routed:  # Must have been routed first
                        ticket_score += 0.02

        total_score += ticket_score

    # Penalty for unhandled critical tickets
    for gt in ground_truth:
        if gt["ticket_id"] not in handled_tickets and gt.get("sla_critical", False):
            total_score -= 0.05

    # Normalize: max possible = num_tickets * 0.10
    num_tickets = len(ground_truth)
    max_possible = num_tickets * 0.10

    if max_possible <= 0:
        return 0.0

    normalized = total_score / max_possible
    return max(0.0, min(1.0, normalized))

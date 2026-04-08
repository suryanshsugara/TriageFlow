"""Task: ticket_routing (Medium)

Goal: Classify, route to correct team, and request missing info when needed.
Episode: 8 tickets, max 20 steps.
Partial credit per ticket: 0.1 classify + 0.1 route + 0.05 missing fields.
Routing rules:
  - billing → billing team
  - technical + high/critical → tier2
  - technical + low/medium → tier1
  - account → tier1
  - policy → management
  - other → tier1
Missing field rules:
  - billing requires account_number in body
  - technical requires error_code or product_name in body
"""

TASK_CONFIG = {
    "name": "ticket_routing",
    "description": "Classify, route, and request missing info",
    "difficulty": "medium",
    "max_steps": 20,
    "queue_size": 8,
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
    """Grade a ticket_routing trajectory.

    Args:
        trajectory: List of step dicts with observation, action, reward, done keys.
        ground_truth: List of ticket ground truth dicts.

    Returns:
        Float score in [0.0, 1.0].
    """
    if not trajectory or not ground_truth:
        return 0.0

    gt_map = {gt["ticket_id"]: gt for gt in ground_truth}
    ticket_scores: dict[str, dict[str, float]] = {}

    for step in trajectory:
        action = step["action"]
        obs = step["observation"]
        ticket_id = obs.get("ticket_id", "")

        if ticket_id == "DONE" or ticket_id not in gt_map:
            continue

        if ticket_id not in ticket_scores:
            ticket_scores[ticket_id] = {
                "classify": 0.0,
                "route": 0.0,
                "info": 0.0,
                "classify_correct": False,
            }

        gt = gt_map[ticket_id]
        scores = ticket_scores[ticket_id]

        if action["action_type"] == "classify":
            urgency_ok = action.get("urgency") == gt["urgency"]
            category_ok = action.get("category") == gt["category"]
            classify_score = 0.0
            if urgency_ok:
                classify_score += 0.05
            if category_ok:
                classify_score += 0.05
            scores["classify"] = max(scores["classify"], classify_score)
            scores["classify_correct"] = urgency_ok and category_ok

        elif action["action_type"] == "route":
            correct_team = _get_correct_team(gt["category"], gt["urgency"])
            if action.get("assigned_team") == correct_team:
                # Only award routing if classification was correct
                if scores["classify_correct"]:
                    scores["route"] = 0.1
                # No credit if classify was wrong (anti-exploitation)

        elif action["action_type"] == "request_info":
            expected = set(gt.get("missing_fields", []))
            # Exclude split_required for medium task
            expected = expected - {"split_required"}
            if expected and action.get("missing_fields"):
                requested = set(action["missing_fields"])
                if requested & expected:
                    scores["info"] = 0.05

    # Calculate total
    num_tickets = len(ground_truth)
    max_per_ticket = 0.25  # 0.1 classify + 0.1 route + 0.05 info
    max_possible = num_tickets * max_per_ticket

    if max_possible <= 0:
        return 0.0

    total = sum(
        s["classify"] + s["route"] + s["info"] for s in ticket_scores.values()
    )
    normalized = total / max_possible
    return max(0.0, min(1.0, normalized))

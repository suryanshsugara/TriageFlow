"""Task: ticket_classification (Easy)

Goal: Classify each ticket's urgency and category.
Episode: 5 tickets, max 10 steps.
Partial credit: 0.2 per ticket (0.1 urgency + 0.1 category).
"""

TASK_CONFIG = {
    "name": "ticket_classification",
    "description": "Classify ticket urgency and category",
    "difficulty": "easy",
    "max_steps": 10,
    "queue_size": 5,
}


def grade(trajectory: list[dict], ground_truth: list[dict]) -> float:
    """Grade a ticket_classification trajectory.

    Args:
        trajectory: List of step dicts with observation, action, reward, done keys.
        ground_truth: List of ticket ground truth dicts with urgency, category, etc.

    Returns:
        Float score in [0.0, 1.0].
    """
    if not trajectory or not ground_truth:
        return 0.0

    gt_map = {gt["ticket_id"]: gt for gt in ground_truth}
    total_score = 0.0
    tickets_scored = set()

    for step in trajectory:
        action = step["action"]
        obs = step["observation"]
        ticket_id = obs.get("ticket_id", "")

        if ticket_id == "DONE" or ticket_id in tickets_scored:
            continue

        if action["action_type"] != "classify":
            continue

        if ticket_id not in gt_map:
            continue

        gt = gt_map[ticket_id]
        ticket_score = 0.0

        # Urgency accuracy: 0.1
        if action.get("urgency") == gt["urgency"]:
            ticket_score += 0.1

        # Category accuracy: 0.1
        if action.get("category") == gt["category"]:
            ticket_score += 0.1

        total_score += ticket_score
        tickets_scored.add(ticket_id)

    # Penalize unprocessed tickets
    num_tickets = len(ground_truth)
    max_possible = num_tickets * 0.2

    if max_possible <= 0:
        return 0.0

    normalized = total_score / max_possible
    return max(0.0, min(1.0, normalized))

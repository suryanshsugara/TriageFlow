"""Task registry for TriageFlow benchmark tasks."""

from tasks.task_easy import TASK_CONFIG as EASY_CONFIG, grade as grade_easy
from tasks.task_medium import TASK_CONFIG as MEDIUM_CONFIG, grade as grade_medium
from tasks.task_hard import TASK_CONFIG as HARD_CONFIG, grade as grade_hard

TASK_REGISTRY = {
    "ticket_classification": {
        "config": EASY_CONFIG,
        "grader": grade_easy,
    },
    "ticket_routing": {
        "config": MEDIUM_CONFIG,
        "grader": grade_medium,
    },
    "policy_triage": {
        "config": HARD_CONFIG,
        "grader": grade_hard,
    },
}


def get_task_names() -> list[str]:
    """Return list of all registered task names."""
    return list(TASK_REGISTRY.keys())


def get_task_config(task_name: str) -> dict:
    """Return configuration for a specific task."""
    if task_name not in TASK_REGISTRY:
        raise ValueError(f"Unknown task: {task_name}. Available: {get_task_names()}")
    return TASK_REGISTRY[task_name]["config"]


def get_grader(task_name: str):
    """Return the grader function for a specific task."""
    if task_name not in TASK_REGISTRY:
        raise ValueError(f"Unknown task: {task_name}. Available: {get_task_names()}")
    return TASK_REGISTRY[task_name]["grader"]


def list_tasks() -> list[dict]:
    """Return detailed info about all tasks for the /tasks endpoint."""
    return [
        {
            "name": name,
            "description": entry["config"]["description"],
            "difficulty": entry["config"]["difficulty"],
            "max_steps": entry["config"]["max_steps"],
            "queue_size": entry["config"]["queue_size"],
        }
        for name, entry in TASK_REGISTRY.items()
    ]

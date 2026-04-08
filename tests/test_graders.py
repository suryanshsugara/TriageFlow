"""Unit tests for task graders."""

import pytest
from environment import TriageFlowEnv, Action


def _run_perfect_easy_episode(env: TriageFlowEnv, seed: int = 42) -> tuple[list[dict], list[dict]]:
    """Run a perfect easy episode and return trajectory + ground truth."""
    obs = env.reset(seed=seed, task_name="ticket_classification")
    gt_list = env.get_ground_truth()
    gt_map = {g["ticket_id"]: g for g in gt_list}

    done = False
    while not done:
        gt = gt_map.get(obs.ticket_id, {})
        action = Action(
            action_type="classify",
            urgency=gt.get("urgency", "low"),
            category=gt.get("category", "other"),
        )
        obs, _, done, _ = env.step(action)

    return env.get_trajectory(), gt_list


def _run_wrong_easy_episode(env: TriageFlowEnv, seed: int = 42) -> tuple[list[dict], list[dict]]:
    """Run a completely wrong easy episode."""
    obs = env.reset(seed=seed, task_name="ticket_classification")
    gt_list = env.get_ground_truth()

    done = False
    while not done:
        action = Action(
            action_type="classify",
            urgency="critical",  # always wrong (mostly)
            category="policy",  # always wrong (mostly)
        )
        obs, _, done, _ = env.step(action)

    return env.get_trajectory(), gt_list


@pytest.fixture
def env():
    """Create a fresh environment."""
    return TriageFlowEnv()


class TestEasyGrader:
    """Tests for ticket_classification grader."""

    def test_easy_grader_perfect_score(self, env):
        """Perfect trajectory returns 1.0."""
        from tasks.task_easy import grade
        trajectory, gt = _run_perfect_easy_episode(env)
        score = grade(trajectory, gt)
        assert score == pytest.approx(1.0, abs=0.01)

    def test_easy_grader_zero_score(self, env):
        """All-wrong trajectory returns a low score."""
        from tasks.task_easy import grade
        trajectory, gt = _run_wrong_easy_episode(env)
        score = grade(trajectory, gt)
        assert score < 0.5  # Should be very low but might not be exactly 0

    def test_easy_grader_empty_trajectory(self):
        """Empty trajectory returns 0.0."""
        from tasks.task_easy import grade
        assert grade([], []) == 0.0


class TestMediumGrader:
    """Tests for ticket_routing grader."""

    def test_medium_grader_partial_credit(self, env):
        """Partial trajectory returns value between 0 and 1."""
        from tasks.task_medium import grade

        obs = env.reset(seed=42, task_name="ticket_routing")
        gt_list = env.get_ground_truth()
        gt_map = {g["ticket_id"]: g for g in gt_list}

        # Do some correct classifies but wrong routes
        done = False
        while not done:
            gt = gt_map.get(obs.ticket_id, {})
            # Correct classify
            action = Action(
                action_type="classify",
                urgency=gt.get("urgency", "low"),
                category=gt.get("category", "other"),
            )
            obs, _, done, _ = env.step(action)
            if done:
                break
            # Wrong route
            action = Action(action_type="route", assigned_team="tier1")
            obs, _, done, _ = env.step(action)

        trajectory = env.get_trajectory()
        score = grade(trajectory, gt_list)
        assert 0.0 <= score <= 1.0
        assert score > 0.0  # Should get some classify credit

    def test_medium_grader_empty(self):
        """Empty inputs return 0.0."""
        from tasks.task_medium import grade
        assert grade([], []) == 0.0


class TestHardGrader:
    """Tests for policy_triage grader."""

    def test_hard_grader_range(self, env):
        """Hard grader always returns value in [0.0, 1.0]."""
        from tasks.task_hard import grade

        obs = env.reset(seed=42, task_name="policy_triage")
        gt_list = env.get_ground_truth()

        done = False
        while not done:
            action = Action(action_type="skip", resolution_note="skipping all")
            obs, _, done, _ = env.step(action)

        trajectory = env.get_trajectory()
        score = grade(trajectory, gt_list)
        assert 0.0 <= score <= 1.0

    def test_grader_is_deterministic(self, env):
        """Same input always returns same score."""
        from tasks.task_easy import grade

        traj1, gt1 = _run_perfect_easy_episode(env, seed=42)
        score1 = grade(traj1, gt1)

        traj2, gt2 = _run_perfect_easy_episode(env, seed=42)
        score2 = grade(traj2, gt2)

        assert score1 == score2

    def test_hard_grader_resists_always_skip(self, env):
        """Always-skip strategy scores below 0.3 on hard task."""
        from tasks.task_hard import grade

        obs = env.reset(seed=42, task_name="policy_triage")
        gt_list = env.get_ground_truth()

        done = False
        while not done:
            action = Action(action_type="skip", resolution_note="duplicate")
            obs, _, done, _ = env.step(action)

        score = grade(env.get_trajectory(), gt_list)
        assert score < 0.3

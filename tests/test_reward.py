"""Unit tests for the reward computation function."""

import pytest
from environment import (
    Action, Reward, TicketState, compute_reward,
)


def _make_gt(**overrides) -> dict:
    """Create a ground truth dict with sensible defaults."""
    gt = {
        "ticket_id": "TEST-001",
        "urgency": "medium",
        "category": "technical",
        "required_team": "tier1",
        "missing_fields": [],
        "is_duplicate": False,
        "has_policy_violation": False,
        "sla_critical": False,
    }
    gt.update(overrides)
    return gt


def _make_ts(**overrides) -> TicketState:
    """Create a TicketState with sensible defaults."""
    return TicketState(ticket_id="TEST-001", **overrides)


class TestClassificationReward:
    """Tests for classify action rewards."""

    def test_correct_classification_reward(self):
        """Correct classify gives positive reward."""
        action = Action(action_type="classify", urgency="medium", category="technical")
        gt = _make_gt(urgency="medium", category="technical")
        ts = _make_ts()
        reward = compute_reward(action, gt, ts, 1, 10, "ticket_classification")

        assert isinstance(reward, Reward)
        assert reward.correctness == pytest.approx(0.20)
        assert reward.total > 0
        assert "urgency_correct" in reward.breakdown
        assert "category_correct" in reward.breakdown

    def test_wrong_classification_penalty(self):
        """Wrong classify gives lower reward than correct."""
        correct_action = Action(action_type="classify", urgency="medium", category="technical")
        wrong_action = Action(action_type="classify", urgency="low", category="billing")
        gt = _make_gt(urgency="medium", category="technical")
        ts = _make_ts()

        correct_reward = compute_reward(correct_action, gt, ts, 1, 10, "ticket_classification")
        wrong_reward = compute_reward(wrong_action, gt, ts, 1, 10, "ticket_classification")

        assert correct_reward.total > wrong_reward.total

    def test_partial_classification(self):
        """Correct urgency but wrong category gives partial credit."""
        action = Action(action_type="classify", urgency="medium", category="billing")
        gt = _make_gt(urgency="medium", category="technical")
        ts = _make_ts()
        reward = compute_reward(action, gt, ts, 1, 10, "ticket_classification")

        assert reward.correctness == pytest.approx(0.10)
        assert "urgency_correct" in reward.breakdown
        assert "category_correct" not in reward.breakdown


class TestStepPenalty:
    """Tests for step penalty."""

    def test_step_penalty_applied(self):
        """Every step has step_penalty < 0."""
        action = Action(action_type="classify", urgency="low", category="other")
        gt = _make_gt()
        ts = _make_ts()
        reward = compute_reward(action, gt, ts, 1, 10, "ticket_classification")

        assert reward.step_penalty < 0
        assert reward.step_penalty == pytest.approx(-0.01)


class TestRoutingReward:
    """Tests for route action rewards."""

    def test_correct_routing_after_classify(self):
        """Routing gives credit only after correct classification."""
        action = Action(action_type="route", assigned_team="tier1")
        gt = _make_gt(urgency="medium", category="technical", required_team="tier1")
        ts = _make_ts(
            classified=True,
            classified_urgency="medium",
            classified_category="technical",
        )
        reward = compute_reward(action, gt, ts, 2, 20, "ticket_routing")
        assert reward.routing_score == pytest.approx(0.10)

    def test_routing_no_credit_wrong_classify(self):
        """Routing gives no credit if classification was wrong."""
        action = Action(action_type="route", assigned_team="tier1")
        gt = _make_gt(urgency="medium", category="technical", required_team="tier1")
        ts = _make_ts(
            classified=True,
            classified_urgency="low",  # wrong
            classified_category="billing",  # wrong
        )
        reward = compute_reward(action, gt, ts, 2, 20, "ticket_routing")
        assert reward.routing_score == pytest.approx(0.0)


class TestEscalationReward:
    """Tests for escalation rewards."""

    def test_correct_escalation(self):
        """Escalation gives credit when needed."""
        action = Action(action_type="escalate", escalation_reason="SLA breach")
        gt = _make_gt(sla_critical=True)
        ts = _make_ts()
        reward = compute_reward(action, gt, ts, 1, 30, "policy_triage")
        assert reward.policy_compliance == pytest.approx(0.10)

    def test_false_escalation_penalty(self):
        """False escalation gives negative policy_compliance."""
        action = Action(action_type="escalate", escalation_reason="just in case")
        gt = _make_gt(sla_critical=False, has_policy_violation=False)
        ts = _make_ts()
        reward = compute_reward(action, gt, ts, 1, 30, "policy_triage")
        assert reward.policy_compliance < 0


class TestSLABreach:
    """Tests for SLA breach penalty."""

    def test_sla_breach_penalty(self):
        """Unhandled critical ticket after 2 steps gets penalty."""
        action = Action(action_type="classify", urgency="critical", category="technical")
        gt = _make_gt(sla_critical=True, urgency="critical", category="technical")
        ts = _make_ts(steps_spent=2, escalated=False)
        reward = compute_reward(action, gt, ts, 3, 30, "policy_triage")

        assert reward.policy_compliance < 0
        assert "sla_breach" in reward.breakdown


class TestSkipReward:
    """Tests for skip action rewards."""

    def test_skip_duplicate_bonus(self):
        """Skipping a duplicate gives bonus."""
        action = Action(action_type="skip")
        gt = _make_gt(is_duplicate=True)
        ts = _make_ts()
        reward = compute_reward(action, gt, ts, 1, 30, "policy_triage")
        assert reward.completeness > 0

    def test_skip_non_duplicate_penalty(self):
        """Skipping a non-duplicate gives penalty."""
        action = Action(action_type="skip")
        gt = _make_gt(is_duplicate=False)
        ts = _make_ts()
        reward = compute_reward(action, gt, ts, 1, 30, "policy_triage")
        assert reward.correctness < 0


class TestRewardBounds:
    """Tests for reward value bounds."""

    def test_reward_within_bounds(self):
        """All rewards clamped to [-1.0, 1.0]."""
        actions_and_gts = [
            (Action(action_type="classify", urgency="medium", category="technical"),
             _make_gt()),
            (Action(action_type="skip"), _make_gt(is_duplicate=False)),
            (Action(action_type="escalate", escalation_reason="test"),
             _make_gt(sla_critical=True)),
            (Action(action_type="resolve", resolution_note="x" * 30),
             _make_gt()),
        ]
        for action, gt in actions_and_gts:
            ts = _make_ts(classified=True, routed=True,
                          classified_urgency="medium", classified_category="technical")
            reward = compute_reward(action, gt, ts, 1, 10, "ticket_classification")
            assert -1.0 <= reward.total <= 1.0

"""Tests for cost tracking."""

import pytest
from src.utils.cost_tracker import CostTracker


def test_initial_state():
    """Test cost tracker initial state."""
    tracker = CostTracker()

    assert tracker.total_input_tokens == 0
    assert tracker.total_output_tokens == 0
    assert tracker.message_count == 0
    assert tracker.get_total_cost() == 0.0


def test_add_usage():
    """Test adding token usage."""
    tracker = CostTracker()

    tracker.add_usage(input_tokens=100, output_tokens=50)

    assert tracker.total_input_tokens == 100
    assert tracker.total_output_tokens == 50
    assert tracker.message_count == 1


def test_add_multiple_usage():
    """Test adding usage from multiple messages."""
    tracker = CostTracker()

    tracker.add_usage(input_tokens=100, output_tokens=50)
    tracker.add_usage(input_tokens=200, output_tokens=150)

    assert tracker.total_input_tokens == 300
    assert tracker.total_output_tokens == 200
    assert tracker.message_count == 2


def test_get_total_tokens():
    """Test getting total token count."""
    tracker = CostTracker()

    tracker.add_usage(input_tokens=100, output_tokens=50)

    assert tracker.get_total_tokens() == 150


def test_calculate_costs():
    """Test cost calculation."""
    tracker = CostTracker()

    # Claude Sonnet 4.5 pricing:
    # Input: $3 per million = $0.000003 per token
    # Output: $15 per million = $0.000015 per token

    tracker.add_usage(input_tokens=1000, output_tokens=500)

    input_cost = tracker.get_input_cost()
    output_cost = tracker.get_output_cost()
    total_cost = tracker.get_total_cost()

    # 1000 * 0.000003 = 0.003
    assert abs(input_cost - 0.003) < 0.0001

    # 500 * 0.000015 = 0.0075
    assert abs(output_cost - 0.0075) < 0.0001

    # Total = 0.003 + 0.0075 = 0.0105
    assert abs(total_cost - 0.0105) < 0.0001


def test_get_stats():
    """Test getting complete statistics."""
    tracker = CostTracker()

    tracker.add_usage(input_tokens=100, output_tokens=50)
    tracker.add_usage(input_tokens=200, output_tokens=100)

    stats = tracker.get_stats()

    assert stats["messages"] == 2
    assert stats["input_tokens"] == 300
    assert stats["output_tokens"] == 150
    assert stats["total_tokens"] == 450
    assert "input_cost" in stats
    assert "output_cost" in stats
    assert "total_cost" in stats


def test_reset():
    """Test resetting tracker."""
    tracker = CostTracker()

    tracker.add_usage(input_tokens=100, output_tokens=50)
    assert tracker.message_count == 1

    tracker.reset()

    assert tracker.total_input_tokens == 0
    assert tracker.total_output_tokens == 0
    assert tracker.message_count == 0
    assert tracker.get_total_cost() == 0.0


def test_realistic_conversation_cost():
    """Test cost calculation for a realistic conversation."""
    tracker = CostTracker()

    # Simulate a 5-message conversation
    tracker.add_usage(input_tokens=50, output_tokens=100)
    tracker.add_usage(input_tokens=150, output_tokens=200)
    tracker.add_usage(input_tokens=300, output_tokens=400)
    tracker.add_usage(input_tokens=500, output_tokens=600)
    tracker.add_usage(input_tokens=800, output_tokens=1000)

    stats = tracker.get_stats()

    assert stats["messages"] == 5
    assert stats["input_tokens"] == 1800
    assert stats["output_tokens"] == 2300
    assert stats["total_tokens"] == 4100

    # Verify cost is reasonable (should be a few cents)
    assert 0.03 < stats["total_cost"] < 0.05

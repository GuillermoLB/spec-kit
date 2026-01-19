"""Cost tracking for API token usage.

This module tracks token usage and calculates estimated costs
based on the model's pricing.
"""

from typing import Dict
from src.config import get_config


class CostTracker:
    """Tracks token usage and estimated costs.

    Maintains running totals for a conversation session.
    """

    def __init__(self):
        """Initialize cost tracker."""
        config = get_config()
        self.input_token_cost = config.input_token_cost
        self.output_token_cost = config.output_token_cost

        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.message_count = 0

    def add_usage(self, input_tokens: int, output_tokens: int) -> None:
        """Add token usage from a message.

        Args:
            input_tokens: Number of input tokens used
            output_tokens: Number of output tokens generated
        """
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.message_count += 1

    def get_total_tokens(self) -> int:
        """Get total tokens used (input + output).

        Returns:
            Total token count
        """
        return self.total_input_tokens + self.total_output_tokens

    def get_input_cost(self) -> float:
        """Calculate cost for input tokens.

        Returns:
            Cost in dollars
        """
        return self.total_input_tokens * self.input_token_cost

    def get_output_cost(self) -> float:
        """Calculate cost for output tokens.

        Returns:
            Cost in dollars
        """
        return self.total_output_tokens * self.output_token_cost

    def get_total_cost(self) -> float:
        """Calculate total estimated cost.

        Returns:
            Total cost in dollars
        """
        return self.get_input_cost() + self.get_output_cost()

    def get_stats(self) -> Dict[str, any]:
        """Get complete usage statistics.

        Returns:
            Dict with usage and cost information
        """
        return {
            "messages": self.message_count,
            "input_tokens": self.total_input_tokens,
            "output_tokens": self.total_output_tokens,
            "total_tokens": self.get_total_tokens(),
            "input_cost": self.get_input_cost(),
            "output_cost": self.get_output_cost(),
            "total_cost": self.get_total_cost(),
        }

    def reset(self) -> None:
        """Reset all counters to zero."""
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.message_count = 0

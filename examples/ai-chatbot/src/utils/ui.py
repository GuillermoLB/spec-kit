"""CLI UI formatting and display.

This module provides formatting and display functions for the
command-line interface.
"""

from typing import Dict
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint


class UI:
    """CLI user interface manager.

    Handles formatted output, colors, and display elements.
    """

    def __init__(self):
        """Initialize UI manager."""
        self.console = Console()

    def show_welcome(self, model_name: str) -> None:
        """Display welcome message.

        Args:
            model_name: Name of the AI model being used
        """
        welcome_text = Text()
        welcome_text.append("AI Chatbot\n", style="bold cyan")
        welcome_text.append(f"Model: {model_name}\n", style="dim")
        welcome_text.append("\nCommands:\n", style="bold")
        welcome_text.append("  • Type your message and press Enter\n")
        welcome_text.append("  • 'quit' or 'exit' - Exit the chatbot\n")
        welcome_text.append("  • 'clear' - Reset conversation\n")
        welcome_text.append("  • 'stats' - Show usage statistics\n")

        panel = Panel(welcome_text, border_style="cyan")
        self.console.print(panel)
        self.console.print()

    def show_user_prompt(self) -> str:
        """Display user input prompt.

        Returns:
            User input string
        """
        return self.console.input("[bold green]You:[/bold green] ")

    def show_assistant_prefix(self) -> None:
        """Display assistant response prefix."""
        self.console.print("[bold blue]Assistant:[/bold blue] ", end="")

    def show_streaming_text(self, text: str) -> None:
        """Display streaming text chunk.

        Args:
            text: Text chunk to display
        """
        self.console.print(text, end="")

    def show_newline(self) -> None:
        """Display a newline."""
        self.console.print()

    def show_error(self, message: str) -> None:
        """Display an error message.

        Args:
            message: Error message to display
        """
        self.console.print(f"[bold red]Error:[/bold red] {message}")

    def show_info(self, message: str) -> None:
        """Display an info message.

        Args:
            message: Info message to display
        """
        self.console.print(f"[cyan]ℹ[/cyan] {message}")

    def show_warning(self, message: str) -> None:
        """Display a warning message.

        Args:
            message: Warning message to display
        """
        self.console.print(f"[yellow]⚠[/yellow]  {message}")

    def show_stats(self, stats: Dict[str, any]) -> None:
        """Display usage statistics.

        Args:
            stats: Statistics dictionary from CostTracker
        """
        stats_text = Text()
        stats_text.append("Session Statistics\n", style="bold cyan")
        stats_text.append(f"Messages: {stats['messages']}\n")
        stats_text.append(f"Input tokens: {stats['input_tokens']:,}\n")
        stats_text.append(f"Output tokens: {stats['output_tokens']:,}\n")
        stats_text.append(f"Total tokens: {stats['total_tokens']:,}\n")
        stats_text.append(f"\nEstimated cost: ${stats['total_cost']:.4f}\n", style="bold")

        panel = Panel(stats_text, border_style="cyan")
        self.console.print(panel)

    def show_thinking(self) -> None:
        """Display thinking indicator."""
        self.console.print("[dim]...[/dim]", end="")

    def clear_line(self) -> None:
        """Clear the current line."""
        self.console.print("\r\033[K", end="")

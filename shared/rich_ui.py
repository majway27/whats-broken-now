from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
from rich.control import Control
from rich.columns import Columns

# Create a global console instance
console = Console()

def print_game_header(active_tickets: int, inbox_messages: int, player_level: int) -> None:
    """Print the common game header with status boxes."""
    # Create status boxes
    tickets_box = Panel(
        f"🎫 Active Tickets\n[bold cyan]{active_tickets}[/]",
        style="bold red",
        box=box.ROUNDED,
        expand=False
    )
    
    inbox_box = Panel(
        f"📬 Inbox Messages\n[bold cyan]{inbox_messages}[/]",
        style="bold yellow",
        box=box.ROUNDED,
        expand=False
    )
    
    level_box = Panel(
        f"⭐ Employee Rating\n[bold cyan]Level {player_level}[/]",
        style="bold purple",
        box=box.ROUNDED,
        expand=False
    )
    
    # Create a table to hold the boxes with right alignment for level box
    table = Table(show_header=False, box=None, expand=True)
    table.add_column(justify="left")
    table.add_column(justify="center")
    table.add_column(justify="right")
    
    table.add_row(tickets_box, inbox_box, level_box)
    
    # Print the table
    console.print(table)
    console.print()  # Add a blank line after the header

def print_header(title: str) -> None:
    """Print a styled header."""
    console.print(Panel(
        title,
        style="bold blue",
        box=box.ROUNDED,
        expand=False
    ))

def print_menu(title: str, options: list[str]) -> None:
    """Print a styled menu with options."""
    # Calculate the width needed for the menu
    max_option_length = max(len(option) for option in options)
    menu_width = max_option_length + 4  # Add padding
    
    # Create a table with centered content
    table = Table(show_header=False, box=box.ROUNDED, expand=False)
    table.add_column(style="bold cyan", justify="center", width=menu_width)
    
    for option in options:
        table.add_row(option)
    
    # Create a panel with centered title and position
    panel = Panel(
        table,
        title=title,
        style="bold blue",
        box=box.ROUNDED,
        expand=False
    )
    
    # Center the panel in the terminal
    console.print(panel, justify="center")

def print_info(title: str, content: str) -> None:
    """Print information in a styled panel."""
    console.print(Panel(
        content,
        title=title,
        style="bold green",
        box=box.ROUNDED,
        expand=False
    ))

def print_error(message: str) -> None:
    """Print an error message in a styled panel."""
    console.print(Panel(
        message,
        title="Error",
        style="bold red",
        box=box.ROUNDED,
        expand=False
    ))

def print_table(title: str, headers: list[str], rows: list[list[str]]) -> None:
    """Print a styled table."""
    table = Table(title=title, box=box.ROUNDED, expand=False)
    
    for header in headers:
        table.add_column(header, style="bold cyan")
    
    for row in rows:
        table.add_row(*row)
    
    console.print(table)

def print_status(title: str, status: str) -> None:
    """Print a status message in a styled panel."""
    console.print(Panel(
        status,
        title=title,
        style="bold yellow",
        box=box.ROUNDED,
        expand=False
    ))

def clear_screen() -> None:
    """Clear the screen."""
    console.control(Control.clear(), Control.home()) 
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
from rich.control import Control
from rich.columns import Columns


# Create a global console instance
console = Console()

def print_game_header(active_tickets: int, mailbox_messages: int, game_day: int, player_level: int, meetings_count: int) -> None:
    """Print the common game header with status boxes."""
    # Create status boxes
    game_day_box = Panel(
        f"🌇 [dark_goldenrod]Day (Game)[/]  [bold sea_green2]{game_day}[/]",
        style="yellow4",
        box=box.ROUNDED,
        expand=False
    )

    meetings_box = Panel(
        f"🥱 [dark_goldenrod]Meetings (Today)[/]  [bold sea_green2]{meetings_count}[/]",
        style="yellow4",
        box=box.ROUNDED,
        expand=False
    )

    # Create a parent box for game day and meetings
    calendar_table = Table(show_header=False, box=None, expand=True)
    calendar_table.add_column(justify="left")
    calendar_table.add_column(justify="left")
    calendar_table.add_row(game_day_box, meetings_box)
    
    calendar_box = Panel(
        calendar_table,
        title="📅 Calendar",
        style="dark_sea_green",  # light_slate_grey
        box=box.ROUNDED,
        expand=False
    )

    tickets_box = Panel(
        f"🎫 [dark_goldenrod]Active Tickets[/]  [bold sea_green2]{active_tickets}[/]",
        style="yellow4",
        box=box.ROUNDED,
        expand=False
    )
    
    mailbox_box = Panel(
        f"📬 [dark_goldenrod]Mailbox Messages[/]  [bold sea_green2]{mailbox_messages}[/]",
        style="yellow4",
        box=box.ROUNDED,
        expand=False
    )

    # Create a parent box for tickets and mailbox
    todo_table = Table(show_header=False, box=None, expand=True)
    todo_table.add_column(justify="right")
    todo_table.add_column(justify="right")
    todo_table.add_row(tickets_box, mailbox_box)
    
    todo_box = Panel(
        todo_table,
        title="📋 TODO",
        style="dark_sea_green",
        box=box.ROUNDED,
        expand=False
    )
    
    level_box = Panel(
        f"⭐ [dark_goldenrod]Employee Rating[/]  [bold sea_green2]Level {player_level}[/]",
        style="yellow4",
        box=box.ROUNDED,
        expand=False
    )

    # Create a parent box for career growth
    career_box = Panel(
        level_box,
        title="🚀 Career",
        style="dark_sea_green",
        box=box.ROUNDED,
        expand=False
    )
    
    # Create a table to hold the boxes with right alignment for level box
    table = Table(show_header=False, box=None, expand=True)
    table.add_column(justify="left")
    table.add_column(justify="center")
    table.add_column(justify="right")
    
    table.add_row(calendar_box, career_box, todo_box)
    
    # Print the table
    console.print(table)
    console.print()  # Add a blank line after the header

def print_header(title: str) -> None:
    """Print a styled header."""
    console.print(Panel(
        title,
        style="dark_sea_green",
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
    table.add_column(style="sea_green2", justify="center", width=menu_width)
    
    for option in options:
        table.add_row(option)
    
    # Create a panel with centered title and position
    panel = Panel(
        table,
        title=title,
        style="yellow4",
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
        style="sea_green2",
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
        table.add_column(header, style="sea_green2")
    
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
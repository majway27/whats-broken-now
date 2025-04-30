from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
from rich.control import Control

# Create a global console instance
console = Console()

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
    table = Table(show_header=False, box=box.ROUNDED, expand=False)
    table.add_column(style="bold cyan")
    
    for option in options:
        table.add_row(option)
    
    console.print(Panel(
        table,
        title=title,
        style="bold blue",
        box=box.ROUNDED,
        expand=False
    ))

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
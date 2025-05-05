from . import models
from shared import views as shared_views
from shared.views import print_menu, clear_screen
from shared.common_ui import print_common_header
from shared.rich_ui import print_status, print_info, print_error, print_table
from human_resources.repository import EmployeeRepository
from human_resources.utils import get_current_employee
from player.models import Player
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.table import Table
console = Console()

def clear_screen():
    """Clear the terminal screen."""
    shared_views.clear_screen()

def tickets_management_menu():
    """Central menu for managing all ticket-related operations."""
    while True:
        clear_screen()
        
        # Display common header
        print_common_header()
                       
        # Create menu options panel
        menu_text = "[bold sea_green2]1.[/] Choose a ticket to work on\n"
        menu_text += "[bold sea_green2]2.[/] View my assigned tickets\n"
        menu_text += "[bold sea_green2]3.[/] View tickets by status\n"
        menu_text += "[bold sea_green2]4.[/] View all tickets\n"
        menu_text += "[bold sea_green2]Q.[/] Return to main menu"
        
        menu_panel = Panel(
            menu_text,
            title="🎯 Actions",
            style="dark_sea_green",
            box=box.ROUNDED,
            expand=True
        )
        
        # Create a table to hold the panels
        table = Table.grid(expand=True)
        table.add_column(ratio=100)  # Welcome panel
        table.add_row(menu_panel)
        table.add_row(print_status_pane())
        console.print(table)
        #console.print()  # Add spacing
                
        choice = input("\nEnter your choice (1-4, Q to return to main menu): ")
        
        if choice == '1':
            work_new_ticket()
        elif choice == '2':
            current_employee = get_current_employee()
            if current_employee:
                view_assigned_tickets(current_employee.id)
            else:
                print_error("Error", "No active employee found.")
                input("Press Enter to continue...")
        elif choice == '3':
            view_tickets_by_status()
        elif choice == '4':
            view_all_tickets()
        elif choice.upper() == 'Q':
            clear_screen()
            return
        else:
            print_error("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def print_status_pane():
    """Print the status pane showing unassigned tickets with status information."""
    tickets = models.get_unassigned_tickets()
    if not tickets:
        print_status("Unassigned Tickets", "No unassigned tickets")
    else:
        headers = ["Ticket ID", "Title", "Status"]
        rows = []
        for ticket in tickets:
            rows.append([
                str(ticket['id']),
                ticket['title'],
                ticket['status']
            ])
        print_table("Unassigned Tickets", headers, rows)

def show_ticket_interaction(ticket):
    """Show the ticket interaction screen for the selected ticket."""
    while True:
        clear_screen()
        
        # Display common header
        print_common_header()

        # Create panels for the ticket title and hardware details
        from rich.panel import Panel
        from rich.text import Text
        from rich import box
        from rich.table import Table
        
        # Create hardware panel
        hardware_info = f"🔧 [bold dark_goldenrod]Name:[/] [sea_green2]{ticket['hardware']['name']}[/]\n"
        hardware_info += f"📐 [bold dark_goldenrod]Model:[/] [sea_green2]{ticket['hardware']['model']}[/]\n"
        hardware_info += f"🏭 [bold dark_goldenrod]Manufacturer:[/] [sea_green2]{ticket['hardware']['manufacturer']}[/]"
        
        hardware_panel = Panel(
            hardware_info,
            title="💻 Product",
            style="dark_sea_green",
            box=box.ROUNDED,
            expand=True
        )

        # Create title panel
        title_panel = Panel(
            Text(ticket['title'], style="sea_green2"),
            title="🎫 Summary",
            style="dark_sea_green",
            box=box.ROUNDED,
            expand=True
        )

        # Get current assignee
        assignee = models.get_ticket_assignee(ticket['id'])
        current_employee = get_current_employee()

        # Create status panel
        status_info = f"📊 [bold dark_goldenrod]Status:[/] [sea_green2]{ticket['status']}[/]\n"
        if assignee:
            status_info += f"👤 [bold dark_goldenrod]Assigned to:[/] [sea_green2]{assignee['first_name']} {assignee['last_name']} ({assignee['email']})[/]\n"
        else:
            status_info += "👤 [bold dark_goldenrod]Assigned to:[/] [sea_green2]Unassigned[/]\n"
        
        status_panel = Panel(
            status_info,
            title="📋 State",
            style="dark_sea_green",
            box=box.ROUNDED,
            expand=True
        )

        # Create a table to hold the panels
        table = Table.grid(expand=True)
        table.add_column(ratio=33)  # Hardware panel
        table.add_column(ratio=33)  # Title panel
        table.add_column(ratio=33)  # Status panel
        table.add_row(hardware_panel, title_panel, status_panel)
        console.print(table)
        console.print()  # Add spacing

        # Create a panel for the reporter comment
        comment_panel = Panel(
            Text(ticket['description'], style="sea_green2"),
            title="💬 Reporter Description",
            style="dark_sea_green",
            box=box.ROUNDED,
            expand=True
        )
        console.print(comment_panel)
        console.print()  # Add spacing
        
        # Display recent history with enhanced styling
        history = models.get_ticket_history(ticket['id'])
        if not history:
            history_panel = Panel(
                Text("No history found for this ticket.", style="sea_green2"),
                title="📜 Recent History",
                style="dark_sea_green",
                box=box.ROUNDED,
                expand=True
            )
            console.print(history_panel)
        else:
            from rich.table import Table
            history_table = Table(
                title="📜 Recent Activity (Last Two Entries)",
                box=box.ROUNDED,
                expand=True,
                style="dark_sea_green"
            )
            history_table.add_column("Time", style="bold dark_goldenrod")
            history_table.add_column("Status", style="bold dark_goldenrod")
            history_table.add_column("Assignee", style="bold dark_goldenrod")
            history_table.add_column("Comment", style="bold dark_goldenrod")
            
            for entry in history[:2]:
                comment = entry['comment'] if entry['comment'] else "Status changed"
                assignee_name = entry.get('assignee_name', 'Unassigned')
                history_table.add_row(
                    f"[bold sea_green2]{entry['changed_at']}[/]",
                    f"[bold sea_green2]{entry['status']}[/]",
                    f"[bold sea_green2]{assignee_name}[/]",
                    f"[bold sea_green2]{comment}[/]"
                )
            console.print(history_table)
        
        console.print()  # Add spacing
        
        # Initialize options list
        options = []
        
        # Add assignment options based on current state
        if assignee and assignee['id'] == current_employee.id:
            options.append("1. Unassign ticket from myself")
        elif not assignee:
            options.append("1. Assign ticket to myself")

        # Add remaining options
        options.extend([
            "2. Update ticket status",
            "3. Add comment",
            "4. View full ticket history",
            "Q. Return to ticket selection"
        ])
        
        print_menu("Options", options)

        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            if assignee and assignee['id'] == current_employee.id:
                models.unassign_ticket(ticket['id'])
                print_info("Success", "Ticket unassigned successfully.")
            elif not assignee:
                models.assign_ticket(ticket['id'], current_employee.id)
                print_info("Success", "Ticket assigned to you successfully.")
            input("Press Enter to continue...")
        elif choice == '2':
            update_ticket_status(ticket)
        elif choice == '3':
            add_ticket_comment(ticket)
        elif choice == '4':
            view_ticket_history(ticket)
        elif choice.upper() == 'Q':
            clear_screen()
            return
        else:
            print_error("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def work_new_ticket():
    """Allow user to select and work on a ticket."""
    clear_screen()
    tickets = models.get_active_tickets()
    if not tickets:
        print_info("No Tickets", "No active tickets available to work on.")
        input("Press Enter to continue...")
        return

    # Display common header
    print_common_header()

    # Display tickets with numbers
    headers = ["#", "Ticket ID", "Title", "Status"]
    rows = []
    for i, ticket in enumerate(tickets, 1):
        rows.append([
            str(i),
            str(ticket['id']),
            ticket['title'],
            ticket['status']
        ])
    print_table("Select a Ticket to Work On", headers, rows)
    print_info("Options", "Q. Return to main menu")

    while True:
        try:
            choice = input("\nEnter ticket number (or 0 to return): ")
            if choice.upper() == 'Q':
                clear_screen()
                return
            
            ticket_index = int(choice) - 1
            if 0 <= ticket_index < len(tickets):
                selected_ticket = tickets[ticket_index]
                show_ticket_interaction(selected_ticket)
                return
            else:
                print_error("Invalid ticket number. Please try again.")
        except ValueError:
            print_error("Please enter a valid number.")

def view_all_tickets():
    """View all tickets in the system."""
    clear_screen()
    
    tickets = models.get_all_tickets()
    if not tickets:
        print_info("All Tickets", "No tickets found in the system.")
    else:
        headers = ["ID", "Title", "Status", "Hardware", "Created", "Description"]
        rows = []
        for ticket in tickets:
            rows.append([
                str(ticket['id']),
                ticket['title'],
                ticket['status'],
                f"{ticket['hardware']['name']} ({ticket['hardware']['model']}) by {ticket['hardware']['manufacturer']}",
                ticket['created_at'],
                ticket['description']
            ])
        print_table("All Tickets", headers, rows)
    
    input("\nPress Enter to continue...")

def check_new_tickets():
    """Check for new tickets and display the result."""
    clear_screen()
    
    new_ticket = models.check_new_tickets()
    
    if new_ticket:
        print_info("New Ticket Found", f"New ticket found: {new_ticket['id']}")
    else:
        print_info("No New Tickets", "No new tickets found.")
    
    input("Press Enter to continue...")
    clear_screen()

def view_ticket_history(ticket):
    """Display the history of a ticket including status changes and comments."""
    clear_screen()
    history = models.get_ticket_history(ticket['id'])
    
    if not history:
        print_info("Ticket History", "No history found for this ticket.")
    else:
        headers = ["Time", "Status", "Assignee", "Comment"]
        rows = []
        for entry in history:
            comment = entry['comment'] if entry['comment'] else "Status changed"
            assignee_name = entry.get('assignee_name', 'Unassigned')
            rows.append([
                entry['changed_at'],
                entry['status'],
                assignee_name,
                comment
            ])
        print_table(f"History for Ticket: {ticket['id']}", headers, rows)
    
    input("\nPress Enter to continue...")

def add_ticket_comment(ticket):
    """Add a comment to a ticket."""
    clear_screen()
    print_info(f"Add Comment to Ticket #{ticket['id']}", f"Title: {ticket['title']}")
    
    comment = input("\nEnter your comment: ")
    if comment.strip():
        models.add_ticket_comment(ticket, comment)
        print_info("Success", "Comment added successfully.")
    else:
        print_error("Comment cannot be empty.")
    
    input("Press Enter to continue...")

def update_ticket_status(ticket):
    """Update the status of a ticket."""
    status_options = [
        "1. New",
        "2. In Progress",
        "3. On Hold",
        "4. Resolved",
        "5. Cancel"
    ]
    print_menu("Update Ticket Status", status_options)

    status_map = {
        '1': 'New',
        '2': 'In Progress',
        '3': 'On Hold',
        '4': 'Resolved'
    }

    while True:
        choice = input("\nEnter status number (1-5): ")
        if choice == '5':
            clear_screen()
            return
        elif choice in status_map:
            new_status = status_map[choice]
            models.update_ticket_status(ticket['id'], new_status)
            ticket['status'] = new_status
            print_info("Status Updated", f"Ticket status updated to: {new_status}")
            input("Press Enter to continue...")
            return
        else:
            print_error("Invalid choice. Please try again.")

def view_assigned_tickets(employee_id):
    """View tickets assigned to the current employee."""
    clear_screen()
    
    tickets = models.get_assigned_tickets(employee_id)
    if not tickets:
        print_info("Assigned Tickets", "No tickets assigned to you.")
    else:
        headers = ["ID", "Title", "Status", "Hardware", "Created"]
        rows = []
        for ticket in tickets:
            rows.append([
                str(ticket['id']),
                ticket['title'],
                ticket['status'],
                f"{ticket['hardware']['name']} ({ticket['hardware']['model']})",
                ticket['created_at']
            ])
        print_table("Your Assigned Tickets", headers, rows)
    
    input("\nPress Enter to continue...")

def view_tickets_by_status():
    """View tickets grouped by their status."""
    clear_screen()
    
    status_counts = models.get_tickets_by_status()
    if not status_counts:
        print_info("Ticket Status", "No tickets found in the system.")
    else:
        headers = ["Status", "Count"]
        rows = [[status, str(count)] for status, count in status_counts.items()]
        print_table("Tickets by Status", headers, rows)
    
    input("\nPress Enter to continue...")

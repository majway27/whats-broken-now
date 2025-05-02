from . import models
from shared import views as shared_views
from shared.rich_ui import print_menu, print_status, print_info, print_error, print_table, clear_screen, print_game_header
from rich.console import Console

def clear_screen():
    """Clear the terminal screen."""
    shared_views.clear_screen()

def tickets_management_menu():
    """Central menu for managing all ticket-related operations."""
    while True:
        clear_screen()
        
        # Display common header
        shared_views.print_common_header()
        
        # Display active tickets at the top
        print_status_pane()
        
        menu_options = [
            #"1. Check for new tickets",
            "1. Work on active ticket",
            "2. View all tickets",
            "Q. Return to main menu"
        ]
        print_menu("Tickets Management", menu_options)
        
        choice = input("\nEnter your choice (1-3, Q to return to main menu): ")
        
        #if choice == '1':
        #    check_new_tickets()
        #elif choice == '2':
        if choice == '1':
            work_new_ticket()
        #elif choice == '3':
        elif choice == '2':
            view_all_tickets()
        elif choice.upper() == 'Q':
            clear_screen()
            return
        else:
            print_error("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def print_status_pane():
    """Print the status pane showing active tickets."""
    tickets = models.get_active_tickets()
    if not tickets:
        print_status("Active Tickets", "No active tickets")
    else:
        rows = []
        for ticket in tickets:
            rows.append([f"{ticket['id']}: {ticket['title']} ({ticket['status']})"])
        print_table("Active Tickets", ["Ticket Details"], rows)

def show_ticket_interaction(ticket):
    """Show the ticket interaction screen for the selected ticket."""
    while True:
        clear_screen()
        
        # Display common header
        shared_views.print_common_header()

        # Display ticket information
        ticket_info = f"Title: {ticket['title']}\n"
        ticket_info += f"Status: {ticket['status']}\n\n"
        ticket_info += f"Hardware Details:\n"
        ticket_info += f"  Name: {ticket['hardware']['name']}\n"
        ticket_info += f"  Model: {ticket['hardware']['model']}\n"
        ticket_info += f"  Manufacturer: {ticket['hardware']['manufacturer']}\n\n"
        ticket_info += f"Reporter Comment:\n{ticket['description']}"
        
        print_info(f"Working on Ticket: {ticket['id']}", ticket_info)
        
        # Display recent history
        history = models.get_ticket_history(ticket['id'])
        if not history:
            print_info("Recent History", "No history found for this ticket.")
        else:
            headers = ["Time", "Status", "Comment"]
            rows = []
            for entry in history[:2]:  # Get only the two most recent entries
                comment = entry['comment'] if entry['comment'] else "Status changed"
                rows.append([
                    entry['changed_at'],
                    entry['status'],
                    comment
                ])
            print_table("Recent Activity (Last Two Entries)", headers, rows)
        
        # Display options
        options = [
            "1. Update ticket status",
            "2. Add comment",
            "3. View full ticket history",
            "Q. Return to ticket selection"
        ]
        print_menu("Options", options)

        choice = input("\nEnter your choice (1-3, Q to return to ticket selection): ")
        
        if choice == '1':
            update_ticket_status(ticket)
        elif choice == '2':
            add_ticket_comment(ticket)
        elif choice == '3':
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
    shared_views.print_common_header()

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
                str(ticket[0]),
                ticket[1],
                ticket[2],
                f"{ticket[4]} ({ticket[5]}) by {ticket[6]}",
                ticket[7],
                ticket[3]
            ])
        print_table("All Tickets", headers, rows)
    
    input("\nPress Enter to continue...")

def check_new_tickets():
    """Check for new tickets and display the result."""
    clear_screen()
    console = Console()
    
    with console.status("[bold yellow]Checking for new tickets...", spinner="dots") as status:
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
        headers = ["Time", "Status", "Comment"]
        rows = []
        for entry in history:
            comment = entry['comment'] if entry['comment'] else "Status changed"
            rows.append([
                entry['changed_at'],
                entry['status'],
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
        if models.add_ticket_comment(ticket, comment):
            print_info("Success", "Comment added successfully.")
        else:
            print_error("Error", "Failed to add comment.")
    else:
        print_error("Error", "Comment cannot be empty.")
    
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

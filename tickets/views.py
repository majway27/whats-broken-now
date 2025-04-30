import os
from . import models
from shared import views as shared_views

def clear_screen():
    """Clear the terminal screen."""
    shared_views.clear_screen()

def print_status_pane():
    """Print the status pane showing active tickets."""
    print("\n=== Active Tickets ===")
    tickets = models.get_active_tickets()
    if not tickets:
        print("No active tickets")
    else:
        for ticket in tickets:
            print(f"\n{ticket['id']}: {ticket['title']} ({ticket['status']})")
    print("\n=====================")

def show_ticket_interaction(ticket):
    """Show the ticket interaction screen for the selected ticket."""
    while True:
        clear_screen()
        print(f"\n=== Working on Ticket: {ticket['id']} ===")
        print(f"Title: {ticket['title']}")
        print(f"Status: {ticket['status']}")
        print(f"\nHardware Details:")
        print(f"  Name: {ticket['hardware']['name']}")
        print(f"  Model: {ticket['hardware']['model']}")
        print(f"  Manufacturer: {ticket['hardware']['manufacturer']}")
        print(f"\nReporter Comment:")
        print(f"{ticket['description']}")
        print("\nOptions:")
        print("1. Update ticket status")
        print("2. Add comment")
        print("3. Return to ticket selection")
        print("===============================")

        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            update_ticket_status(ticket)
        elif choice == '2':
            add_ticket_comment(ticket)
        elif choice == '3':
            return
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def update_ticket_status(ticket):
    """Update the status of a ticket."""
    print("\n=== Update Ticket Status ===")
    print("1. New")
    print("2. In Progress")
    print("3. On Hold")
    print("4. Resolved")
    print("5. Cancel")
    print("=========================")

    status_map = {
        '1': 'New',
        '2': 'In Progress',
        '3': 'On Hold',
        '4': 'Resolved'
    }

    while True:
        choice = input("\nEnter status number (1-5): ")
        if choice == '5':
            return
        elif choice in status_map:
            new_status = status_map[choice]
            models.update_ticket_status(ticket['id'], new_status)
            ticket['status'] = new_status
            print(f"\nTicket status updated to: {new_status}")
            input("Press Enter to continue...")
            return
        else:
            print("Invalid choice. Please try again.")

def add_ticket_comment(ticket):
    """Add a comment to a ticket."""
    print("\n=== Add Comment to Ticket ===")
    comment = input("Enter your comment: ")
    if comment.strip():
        # In a real implementation, you would store the comment in a database
        print("\nComment added successfully!")
    else:
        print("\nComment cannot be empty.")
    input("Press Enter to continue...")

def view_all_tickets():
    """View all tickets in the system."""
    clear_screen()
    print("\n=== All Tickets ===")
    
    tickets = models.get_all_tickets()
    if not tickets:
        print("\nNo tickets found in the system.")
    else:
        for ticket in tickets:
            print(f"\nTicket ID: {ticket[0]}")
            print(f"Title: {ticket[1]}")
            print(f"Status: {ticket[2]}")
            print(f"Hardware: {ticket[4]} ({ticket[5]}) by {ticket[6]}")
            print(f"Created: {ticket[7]}")
            print(f"Description: {ticket[3]}")
            print("-" * 50)
    
    input("\nPress Enter to continue...")

def check_new_tickets():
    """Check for new tickets and display the result."""
    print("\nChecking for new tickets...")
    
    new_ticket = models.check_new_tickets()
    if new_ticket:
        print(f"New ticket found: {new_ticket['id']}")
    else:
        print("No new tickets found.")
    
    input("Press Enter to continue...")

def work_new_ticket():
    """Allow user to select and work on a ticket."""
    tickets = models.get_active_tickets()
    if not tickets:
        print("\nNo active tickets available to work on.")
        input("Press Enter to continue...")
        return

    # Display tickets with numbers
    print("\n=== Select a Ticket to Work On ===")
    for i, ticket in enumerate(tickets, 1):
        print(f"{i}. {ticket['id']}: {ticket['title']} ({ticket['status']})")
    print("0. Return to main menu")
    print("===============================")

    while True:
        try:
            choice = input("\nEnter ticket number (or 0 to return): ")
            if choice == '0':
                return
            
            ticket_index = int(choice) - 1
            if 0 <= ticket_index < len(tickets):
                selected_ticket = tickets[ticket_index]
                show_ticket_interaction(selected_ticket)
                return
            else:
                print("Invalid ticket number. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

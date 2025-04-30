from tickets import models as ticket_models, utils as ticket_utils, views as ticket_views
from hardware import models as hardware_models, utils as hardware_utils, views as hardware_views
from shared import views as shared_views


def print_menu():
    """Print the main menu options."""
    print("\n=== Main Menu ===")
    print("1. Check for new tickets")
    print("2. Work new ticket")
    print("3. Administrator")
    print("4. Logout for the day and go home")
    print("===============")
    ticket_views.print_status_pane()

def check_new_tickets():
    print("\nChecking for new tickets...")
    
    new_ticket = ticket_models.check_new_tickets()
    if new_ticket:
        print(f"New ticket found: {new_ticket['id']}")
    else:
        print("No new tickets found.")
    
    input("Press Enter to continue...")

def work_new_ticket():
    """Allow user to select and work on a ticket."""
    tickets = ticket_models.get_active_tickets()
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
                ticket_views.show_ticket_interaction(selected_ticket)
                return
            else:
                print("Invalid ticket number. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def show_ticket_interaction(ticket):
    """Show the ticket interaction screen for the selected ticket."""
    while True:
        shared_views.clear_screen()
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
            ticket_views.update_ticket_status(ticket)
        elif choice == '2':
            ticket_models.add_ticket_comment(ticket)
        elif choice == '3':
            return
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

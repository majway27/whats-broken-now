from tickets import views as ticket_views
from hardware import views as hardware_views
from shared import views as shared_views


def administrator_options():
    """Administrator menu for system management."""
    while True:
        shared_views.clear_screen()
        print("\n=== Administrator Menu ===")
        print("1. View System Statistics")
        print("2. Manage Hardware Catalog")
        print("3. View All Tickets")
        print("4. Return to Main Menu")
        print("========================")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            shared_views.view_system_statistics()
        elif choice == '2':
            hardware_views.manage_hardware_catalog()
        elif choice == '3':
            ticket_views.view_all_tickets()
        elif choice == '4':
            return
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")
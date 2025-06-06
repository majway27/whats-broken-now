from shared.rich_ui import print_menu, print_error, clear_screen


def administrator_options():
    """Administrator menu for system management."""
    while True:
        clear_screen()
        
        menu_options = [
            "1. View System Statistics",
            "2. Manage Hardware Catalog",
            "3. View All Tickets",
            "4. Return to Main Menu"
        ]
        print_menu("Administrator Menu", menu_options)
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            from shared import views as shared_views
            shared_views.view_system_statistics()
        elif choice == '2':
            from hardware import views as hardware_views
            hardware_views.manage_hardware_catalog()
        elif choice == '3':
            from tickets import views as ticket_views
            ticket_views.view_all_tickets()
        elif choice == '4':
            clear_screen()
            return
        else:
            print_error("Invalid choice. Please try again.")
            input("Press Enter to continue...")
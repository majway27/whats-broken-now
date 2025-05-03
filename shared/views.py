from .rich_ui import print_menu, print_status, print_info, print_error, clear_screen


def show_main_menu():
    """Print the main menu options and handle user choice."""
    # Print the common header
    from .common_ui import print_common_header
    clear_screen()
    print_common_header()
    
    menu_options = [
        "1. Tickets",
        "2. Mailbox",
        "3. Schedule",
        "4. Human Resources",
        "Z. SysAdmin",
        "Q. Logout (for the day and go home)"
    ]
    print_menu("Main Menu", menu_options)
    
    choice = input("\nEnter your choice (1-4, Z, Q): ")
    
    if choice == '1':
        from tickets import views as ticket_views
        ticket_views.tickets_management_menu()
    elif choice == '2':
        from mailbox import views as mailbox_views
        mailbox_views.show_mailbox_menu()
    elif choice == '3':
        from game_calendar import views as calendar_views
        calendar_views.show_calendar_menu()
    elif choice == '4':
        from human_resources import views as hr_views
        hr_views.show_hr_menu()
    elif choice.upper() == 'Z':
        from admin import views as admin_views
        admin_views.administrator_options()
    elif choice.upper() == 'Q':
        from .utils import generate_snarky_goodbye
        from game_calendar import models as calendar_models
        
        # Show snarky goodbye message
        print_status("Coworker's Farewell", generate_snarky_goodbye())
        
        # Advance the day
        current_day = calendar_models.get_current_game_day()
        new_day = calendar_models.advance_game_day()
        print_info("System", f"Advanced Day (Game): [bold dark_goldenrod]{current_day}[/] -> [bold sea_green2]{new_day}[/]")
        return True
    else:
        print("\nInvalid choice. Please try again.")
        input("Press Enter to continue...")
        clear_screen()
    
    return False

def view_system_statistics():
    """Display system statistics."""
    from tickets import models as ticket_models
    from hardware import models as hardware_models
    clear_screen()
    
    # Get ticket statistics using model functions
    total_tickets = ticket_models.get_ticket_count()
    status_counts = ticket_models.get_tickets_by_status()
    
    # Get hardware catalog statistics
    hardware_stats = hardware_models.get_hardware_statistics()
    
    # Format ticket statistics
    ticket_info = f"Total Tickets: {total_tickets}\n"
    for status, count in status_counts.items():
        ticket_info += f"{status}: {count}\n"
    
    # Format hardware statistics
    hardware_info = f"Total Hardware Items: {hardware_stats['total_hardware']}\n"
    hardware_info += f"Total Categories: {hardware_stats['total_categories']}"
    
    # Print statistics in panels
    print_info("Tickets", ticket_info)
    print_info("Hardware Catalog", hardware_info)
    
    input("\nPress Enter to continue...")

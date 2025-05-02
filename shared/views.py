from .rich_ui import print_menu, print_status, print_info, print_error, clear_screen, print_game_header
from tickets import models as ticket_models, views as ticket_views
from hardware import models as hardware_models
from mailbox import models as mailbox_models

def print_common_header():
    """Print the common game header with current status."""
    # Get active ticket count
    active_tickets = len(ticket_models.get_active_tickets())
    
    # Get mailbox message count
    mailbox_messages = mailbox_models.get_unread_count("player")
    
    # TODO: Get player level from player module
    player_level = 1  # Placeholder until player module is implemented
    
    # Print the game header
    print_game_header(active_tickets, mailbox_messages, player_level)

def show_main_menu():
    """Print the main menu options and handle user choice."""
    # Print the common header
    print_common_header()
    
    menu_options = [
        "1. Tickets Management",
        "2. Mailbox",
        "3. Human Resources",
        "Z. SysAdmin",
        "Q. Logout (for the day and go home)"
    ]
    print_menu("Main Menu", menu_options)
    
    choice = input("\nEnter your choice (1-3, Z, Q): ")
    
    if choice == '1':
        from tickets import views as ticket_views
        ticket_views.tickets_management_menu()
    elif choice == '2':
        from mailbox import views as mailbox_views
        mailbox_views.show_mailbox_menu()
    elif choice == '3':
        from human_resources import views as hr_views
        hr_views.show_hr_menu()
    elif choice.upper() == 'Z':
        from admin import views as admin_views
        admin_views.administrator_options()
    elif choice.upper() == 'Q':
        print("\nLogging out... Goodbye!")
        return True
    else:
        print("\nInvalid choice. Please try again.")
        input("Press Enter to continue...")
        clear_screen()
    
    return False

def view_system_statistics():
    """Display system statistics."""
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

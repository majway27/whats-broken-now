from .rich_ui import print_menu, print_status, print_info, print_error, clear_screen
from tickets import models as ticket_models, views as ticket_views
from hardware import models as hardware_models

def show_main_menu():
    """Print the main menu options."""
    menu_options = [
        "1. Check for new tickets",
        "2. Work new ticket",
        "3. Administrator",
        "4. Logout for the day and go home"
    ]
    print_menu("Main Menu", menu_options)
    ticket_views.print_status_pane()

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

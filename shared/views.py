import os
from tickets import models as ticket_models, views as ticket_views
from hardware import models as hardware_models

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    """Print the main menu options."""
    print("\n=== Main Menu ===")
    print("1. Check for new tickets")
    print("2. Work new ticket")
    print("3. Administrator")
    print("4. Logout for the day and go home")
    print("===============")
    ticket_views.print_status_pane()

def view_system_statistics():
    """Display system statistics."""
    clear_screen()
    print("\n=== System Statistics ===")
    
    # Get ticket statistics using model functions
    total_tickets = ticket_models.get_ticket_count()
    status_counts = ticket_models.get_tickets_by_status()
    
    # Get hardware catalog statistics
    hardware_stats = hardware_models.get_hardware_statistics()
    
    print(f"\nTickets:")
    print(f"  Total Tickets: {total_tickets}")
    for status, count in status_counts.items():
        print(f"  {status}: {count}")
    
    print(f"\nHardware Catalog:")
    print(f"  Total Hardware Items: {hardware_stats['total_hardware']}")
    print(f"  Total Categories: {hardware_stats['total_categories']}")
    
    input("\nPress Enter to continue...")

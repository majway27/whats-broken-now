import random
import sqlite3
import os
from datetime import datetime
import llm
from tickets import models, views, utils

# Initialize LLM client
client = llm.get_model("mistral-7b-instruct-v0")

# Get the directory where this module is located
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
TICKETS_DB_PATH = os.path.join(MODULE_DIR, 'tickets', 'tickets.db')


def get_hardware_db():
    """Get a connection to the hardware catalog database."""
    return sqlite3.connect('hardware/hardware_catalog.db')

def print_menu():
    """Print the main menu options."""
    print("\n=== Main Menu ===")
    print("1. Check for new tickets")
    print("2. Work new ticket")
    print("3. Administrator")
    print("4. Logout for the day and go home")
    print("===============")
    views.print_status_pane()

def check_new_tickets():
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
                views.show_ticket_interaction(selected_ticket)
                return
            else:
                print("Invalid ticket number. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def show_ticket_interaction(ticket):
    """Show the ticket interaction screen for the selected ticket."""
    while True:
        views.clear_screen()
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
            models.add_ticket_comment(ticket)
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


def administrator_options():
    """Administrator menu for system management."""
    while True:
        views.clear_screen()
        print("\n=== Administrator Menu ===")
        print("1. View System Statistics")
        print("2. Manage Hardware Catalog")
        print("3. View All Tickets")
        print("4. Return to Main Menu")
        print("========================")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            view_system_statistics()
        elif choice == '2':
            manage_hardware_catalog()
        elif choice == '3':
            views.view_all_tickets()
        elif choice == '4':
            return
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def view_system_statistics():
    """Display system statistics."""
    views.clear_screen()
    print("\n=== System Statistics ===")
    
    # Get ticket statistics using model functions
    total_tickets = models.get_ticket_count()
    status_counts = models.get_tickets_by_status()
    
    # Get hardware catalog statistics
    hw_conn = get_hardware_db()
    hw_c = hw_conn.cursor()
    
    # Count hardware items
    hw_c.execute("SELECT COUNT(*) FROM hardware_items")
    total_hardware = hw_c.fetchone()[0]
    
    # Count hardware categories
    hw_c.execute("SELECT COUNT(*) FROM hardware_categories")
    total_categories = hw_c.fetchone()[0]
    
    print(f"\nTickets:")
    print(f"  Total Tickets: {total_tickets}")
    for status, count in status_counts.items():
        print(f"  {status}: {count}")
    
    print(f"\nHardware Catalog:")
    print(f"  Total Hardware Items: {total_hardware}")
    print(f"  Total Categories: {total_categories}")
    
    hw_conn.close()
    
    input("\nPress Enter to continue...")

def manage_hardware_catalog():
    """Manage the hardware catalog."""
    while True:
        views.clear_screen()
        print("\n=== Hardware Catalog Management ===")
        print("1. View All Hardware Items")
        print("2. Add New Hardware Item")
        print("3. Update Hardware Item")
        print("4. Return to Administrator Menu")
        print("================================")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            view_all_hardware()
        elif choice == '2':
            add_hardware_item()
        elif choice == '3':
            update_hardware_item()
        elif choice == '4':
            return
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def view_all_hardware():
    """Display all hardware items in the catalog."""
    views.clear_screen()
    print("\n=== All Hardware Items ===")
    
    conn = get_hardware_db()
    c = conn.cursor()
    
    c.execute("""
        SELECT hi.id, hi.name, hi.manufacturer, hi.model, hc.name as category
        FROM hardware_items hi
        JOIN hardware_categories hc ON hi.category_id = hc.id
        ORDER BY hi.name
    """)
    
    items = c.fetchall()
    if not items:
        print("\nNo hardware items found in the catalog.")
    else:
        for item in items:
            print(f"\nID: {item[0]}")
            print(f"Name: {item[1]}")
            print(f"Manufacturer: {item[2]}")
            print(f"Model: {item[3]}")
            print(f"Category: {item[4]}")
            print("-" * 30)
    
    conn.close()
    input("\nPress Enter to continue...")

def add_hardware_item():
    """Add a new hardware item to the catalog."""
    views.clear_screen()
    print("\n=== Add New Hardware Item ===")
    
    # Get hardware categories
    conn = get_hardware_db()
    c = conn.cursor()
    c.execute("SELECT id, name FROM hardware_categories")
    categories = c.fetchall()
    
    if not categories:
        print("No categories found. Please create categories first.")
        conn.close()
        input("Press Enter to continue...")
        return
    
    print("\nAvailable Categories:")
    for cat_id, cat_name in categories:
        print(f"{cat_id}. {cat_name}")
    
    try:
        category_id = int(input("\nSelect category ID: "))
        name = input("Enter hardware name: ")
        manufacturer = input("Enter manufacturer: ")
        model = input("Enter model: ")
        
        c.execute("""
            INSERT INTO hardware_items (category_id, name, manufacturer, model)
            VALUES (?, ?, ?, ?)
        """, (category_id, name, manufacturer, model))
        
        conn.commit()
        print("\nHardware item added successfully!")
    except ValueError:
        print("Invalid category ID. Please enter a number.")
    except sqlite3.Error as e:
        print(f"Error adding hardware item: {str(e)}")
    finally:
        conn.close()
        input("Press Enter to continue...")

def update_hardware_item():
    """Update an existing hardware item."""
    views.clear_screen()
    print("\n=== Update Hardware Item ===")
    
    conn = get_hardware_db()
    c = conn.cursor()
    
    # Get all hardware items
    c.execute("""
        SELECT id, name, manufacturer, model
        FROM hardware_items
        ORDER BY name
    """)
    items = c.fetchall()
    
    if not items:
        print("No hardware items found in the catalog.")
        conn.close()
        input("Press Enter to continue...")
        return
    
    print("\nAvailable Hardware Items:")
    for item in items:
        print(f"{item[0]}. {item[1]} ({item[2]} {item[3]})")
    
    try:
        item_id = int(input("\nSelect item ID to update: "))
        
        # Verify item exists
        c.execute("SELECT id FROM hardware_items WHERE id = ?", (item_id,))
        if not c.fetchone():
            print("Invalid item ID.")
            conn.close()
            input("Press Enter to continue...")
            return
        
        # Get new values
        name = input("Enter new name (press Enter to keep current): ")
        manufacturer = input("Enter new manufacturer (press Enter to keep current): ")
        model = input("Enter new model (press Enter to keep current): ")
        
        # Build update query
        updates = []
        params = []
        if name:
            updates.append("name = ?")
            params.append(name)
        if manufacturer:
            updates.append("manufacturer = ?")
            params.append(manufacturer)
        if model:
            updates.append("model = ?")
            params.append(model)
        
        if updates:
            params.append(item_id)
            query = f"UPDATE hardware_items SET {', '.join(updates)} WHERE id = ?"
            c.execute(query, params)
            conn.commit()
            print("\nHardware item updated successfully!")
        else:
            print("\nNo changes made.")
    except ValueError:
        print("Invalid item ID. Please enter a number.")
    except sqlite3.Error as e:
        print(f"Error updating hardware item: {str(e)}")
    finally:
        conn.close()
        input("Press Enter to continue...")

def view_all_tickets():
    """View all tickets in the system."""
    views.clear_screen()
    print("\n=== All Tickets ===")
    
    conn = sqlite3.connect(TICKETS_DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        SELECT id, title, status, description, hardware_name, hardware_model, hardware_manufacturer, created_at
        FROM tickets
        ORDER BY created_at DESC
    """)
    
    tickets = c.fetchall()
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
    
    conn.close()
    input("\nPress Enter to continue...")

def generate_snarky_goodbye():
    """Generate a snarky goodbye message from a coworker."""
    messages = [
        "Finally! I was starting to think you'd never leave.",
        "Don't let the door hit you on the way out! Just kidding... or am I?",
        "Leaving already? But who will I blame for all the bugs now?",
        "See you tomorrow! Unless you're working from home... again.",
        "Another day, another dollar... that you're taking home while I'm still here.",
        "Don't forget to take your coffee mug! (The one you never wash)",
        "Bye! Try not to break anything on your way out.",
        "Leaving at a reasonable hour? That's not like you.",
        "Don't worry about the tickets, I'll just... handle them all myself.",
        "See you tomorrow! Unless you're 'working from home' again.",
        "Another day, another ticket you didn't close.",
        "Don't let the bed bugs bite! (They're probably in your desk chair anyway)",
        "Bye! Try not to think about work... too much.",
        "Leaving already? But who will I steal snacks from now?",
        "Don't forget to set your out of office message... again."
    ]
    return random.choice(messages) 
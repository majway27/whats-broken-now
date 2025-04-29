import random
import sqlite3
from datetime import datetime
import os

# Database setup
def init_db():
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tickets
                 (id TEXT PRIMARY KEY,
                  title TEXT,
                  status TEXT,
                  created_at TIMESTAMP)''')
    conn.commit()
    conn.close()

def get_active_tickets():
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute("SELECT id, title, status FROM tickets")
    tickets = [{"id": row[0], "title": row[1], "status": row[2]} for row in c.fetchall()]
    conn.close()
    return tickets

def add_ticket(ticket):
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute("INSERT INTO tickets (id, title, status, created_at) VALUES (?, ?, ?, ?)",
              (ticket['id'], ticket['title'], ticket['status'], datetime.now()))
    conn.commit()
    conn.close()

def print_status_pane():
    """Print the status pane showing active tickets."""
    print("\n=== Active Tickets ===")
    tickets = get_active_tickets()
    if not tickets:
        print("No active tickets")
    else:
        for ticket in tickets:
            print(f"{ticket['id']}: {ticket['title']} ({ticket['status']})")
    print("=====================")

def print_menu():
    """Print the main menu options."""
    print("\n=== Main Menu ===")
    print("1. Check for new tickets")
    print("2. Work new ticket")
    print("3. Option Three")
    print("4. Logout for the day and go home")
    print("===============")
    print_status_pane()

def check_new_tickets():
    print("\nChecking for new tickets...")
    
    # 50% chance to generate a new ticket
    if random.random() < 0.5:
        new_ticket = {
            "id": f"TICKET-{random.randint(1000, 9999)}",
            "title": "New system issue",
            "status": "New"
        }
        add_ticket(new_ticket)
        print(f"New ticket found: {new_ticket['id']}")
    else:
        print("No new tickets found.")
    
    input("Press Enter to continue...")

def work_new_ticket():
    """Allow user to select and work on a ticket."""
    tickets = get_active_tickets()
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

def show_ticket_interaction(ticket):
    """Show the ticket interaction screen for the selected ticket."""
    while True:
        clear_screen()
        print(f"\n=== Working on Ticket: {ticket['id']} ===")
        print(f"Title: {ticket['title']}")
        print(f"Status: {ticket['status']}")
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
            conn = sqlite3.connect('tickets.db')
            c = conn.cursor()
            c.execute("UPDATE tickets SET status = ? WHERE id = ?", 
                     (new_status, ticket['id']))
            conn.commit()
            conn.close()
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

def option_three():
    print("\nYou selected Option Three!")
    input("Press Enter to continue...")

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

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

def main():
    init_db()  # Initialize database on startup
    while True:
        clear_screen()  # Clear screen before showing menu
        print_menu()
        try:
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == '1':
                check_new_tickets()
            elif choice == '2':
                work_new_ticket()
            elif choice == '3':
                option_three()
            elif choice == '4':
                print("\n" + generate_snarky_goodbye())
                break
            else:
                print("\nInvalid choice. Please try again.")
                input("Press Enter to continue...")
        except KeyboardInterrupt:
            print("\n\nExiting program...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main() 
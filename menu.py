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
    print("\nWorking on a new ticket...")
    # Add your ticket working logic here
    print("Ticket work completed.")
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
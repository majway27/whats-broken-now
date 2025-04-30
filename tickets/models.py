import sqlite3
from datetime import datetime
import os
import random
from . import utils

# Get the directory where this module is located
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(MODULE_DIR, 'tickets.db')

def init_db():
    """Initialize the tickets database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create tickets table
    c.execute('''CREATE TABLE IF NOT EXISTS tickets
                 (id TEXT PRIMARY KEY,
                  title TEXT,
                  status TEXT,
                  description TEXT,
                  hardware_name TEXT,
                  hardware_model TEXT,
                  hardware_manufacturer TEXT,
                  created_at TIMESTAMP)''')
    
    conn.commit()
    conn.close()

def get_active_tickets():
    """Get all active tickets from the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, status, description, hardware_name, hardware_model, hardware_manufacturer FROM tickets")
    tickets = [{
        "id": row[0],
        "title": row[1],
        "status": row[2],
        "description": row[3],
        "hardware": {
            "name": row[4],
            "model": row[5],
            "manufacturer": row[6]
        }
    } for row in c.fetchall()]
    conn.close()
    return tickets

def add_ticket(ticket):
    """Add a new ticket to the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO tickets (id, title, status, description, hardware_name, hardware_model, hardware_manufacturer, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (ticket['id'],
               ticket['title'],
               ticket['status'],
               ticket['description'],
               ticket['hardware']['name'],
               ticket['hardware']['model'],
               ticket['hardware']['manufacturer'],
               datetime.now()))
    conn.commit()
    conn.close()

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

def update_ticket_status(ticket_id, new_status):
    """Update the status of a ticket."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE tickets SET status = ? WHERE id = ?", 
             (new_status, ticket_id))
    conn.commit()
    conn.close()

def get_all_tickets():
    """Get all tickets from the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT id, title, status, description, hardware_name, hardware_model, hardware_manufacturer, created_at
        FROM tickets
        ORDER BY created_at DESC
    """)
    tickets = c.fetchall()
    conn.close()
    return tickets

def get_ticket_count():
    """Get the total number of tickets in the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM tickets")
    count = c.fetchone()[0]
    conn.close()
    return count

def get_tickets_by_status():
    """Get a dictionary of ticket counts by status."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT status, COUNT(*) FROM tickets GROUP BY status")
    status_counts = dict(c.fetchall())
    conn.close()
    return status_counts

def check_new_tickets():
    """Check for and potentially create a new ticket."""
    
    # 50% chance to generate a new ticket
    if random.random() < 0.5:
        # Get a random hardware item from the database
        conn = sqlite3.connect(os.path.join(MODULE_DIR, '..', 'hardware', 'hardware_catalog.db'))
        c = conn.cursor()
        
        # Get total count of hardware items
        c.execute("SELECT COUNT(*) FROM hardware_items")
        total_items = c.fetchone()[0]
        
        if total_items > 0:
            # Select a random hardware item
            random_offset = random.randint(0, total_items - 1)
            c.execute("""
                SELECT hi.id, hi.name, hi.manufacturer, hi.model, hc.name as category
                FROM hardware_items hi
                JOIN hardware_categories hc ON hi.category_id = hc.id
                LIMIT 1 OFFSET ?
            """, (random_offset,))
            hardware_item = c.fetchone()
            
            if hardware_item:
                # Get a random failure for this hardware item
                c.execute("""
                    SELECT failure_description
                    FROM hardware_failures
                    WHERE hardware_id = ?
                """, (hardware_item[0],))
                failures = c.fetchall()
                
                if failures:
                    failure = random.choice(failures)[0]
                    
                    # Generate a reporter comment
                    comment = utils.generate_reporter_comment({
                        'name': hardware_item[1],
                        'manufacturer': hardware_item[2],
                        'model': hardware_item[3]
                    })
                    
                    new_ticket = {
                        "id": f"TICKET-{random.randint(1000, 9999)}",
                        "title": f"{hardware_item[1]} ({hardware_item[3]}) - {failure}",
                        "status": "New",
                        "description": comment,
                        "hardware": {
                            "name": hardware_item[1],
                            "model": hardware_item[3],
                            "manufacturer": hardware_item[2]
                        }
                    }
                    add_ticket(new_ticket)
                    conn.close()
                    return new_ticket
        conn.close()
    return None 
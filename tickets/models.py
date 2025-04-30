import sqlite3
from datetime import datetime
import os

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
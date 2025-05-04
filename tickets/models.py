import sqlite3
from datetime import datetime
import os
import random
from . import utils

# Get the directory where this module is located
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(MODULE_DIR, 'tickets.db')
HR_DB_PATH = os.path.join(MODULE_DIR, '..', 'hr', 'hr.db')

def init_db():
    """Initialize the tickets database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create tickets table with assignee field
    c.execute('''CREATE TABLE IF NOT EXISTS tickets
                 (id TEXT PRIMARY KEY,
                  title TEXT,
                  status TEXT,
                  description TEXT,
                  hardware_name TEXT,
                  hardware_model TEXT,
                  hardware_manufacturer TEXT,
                  created_at TIMESTAMP,
                  assignee_id INTEGER)''')
    
    # Create ticket history table with assignee tracking
    c.execute('''CREATE TABLE IF NOT EXISTS ticket_history
                 (audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  ticket_id TEXT,
                  title TEXT,
                  status TEXT,
                  description TEXT,
                  hardware_name TEXT,
                  hardware_model TEXT,
                  hardware_manufacturer TEXT,
                  comment TEXT,
                  changed_at TIMESTAMP,
                  assignee_id INTEGER,
                  FOREIGN KEY (ticket_id) REFERENCES tickets(id))''')
    
    conn.commit()
    conn.close()

def get_active_tickets():
    """Get all active tickets from the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, status, description, hardware_name, hardware_model, hardware_manufacturer FROM tickets WHERE status != 'Resolved'")
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

def get_ticket_history(ticket_id):
    """Get the complete history of a ticket including status changes and comments."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        SELECT audit_id, title, status, description, hardware_name, hardware_model, 
               hardware_manufacturer, comment, changed_at
        FROM ticket_history
        WHERE ticket_id = ?
        ORDER BY changed_at DESC
    """, (ticket_id,))
    
    history = []
    for row in c.fetchall():
        history.append({
            "audit_id": row[0],
            "title": row[1],
            "status": row[2],
            "description": row[3],
            "hardware": {
                "name": row[4],
                "model": row[5],
                "manufacturer": row[6]
            },
            "comment": row[7],
            "changed_at": row[8]
        })
    
    conn.close()
    return history 

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

def add_ticket_comment(ticket, comment):
    """Add a comment to a ticket."""
    if comment.strip():
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Get current ticket state
        c.execute("""
            SELECT title, status, description, hardware_name, hardware_model, hardware_manufacturer
            FROM tickets
            WHERE id = ?
        """, (ticket['id'],))
        
        ticket_data = c.fetchone()
        if ticket_data:
            # Insert into history table with comment
            c.execute("""
                INSERT INTO ticket_history 
                (ticket_id, title, status, description, hardware_name, hardware_model, hardware_manufacturer, comment, changed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (ticket['id'], *ticket_data, comment, datetime.now()))
            
        conn.commit()
        conn.close()
        return True
    return False

def record_ticket_history(ticket_id):
    """Record the current state of a ticket in the history table."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get current ticket state
    c.execute("""
        SELECT title, status, description, hardware_name, hardware_model, hardware_manufacturer
        FROM tickets
        WHERE id = ?
    """, (ticket_id,))
    
    ticket_data = c.fetchone()
    if ticket_data:
        # Insert into history table
        c.execute("""
            INSERT INTO ticket_history 
            (ticket_id, title, status, description, hardware_name, hardware_model, hardware_manufacturer, changed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (ticket_id, *ticket_data, datetime.now()))
        
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
    
    # Record the change in history
    record_ticket_history(ticket_id)

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

def assign_ticket(ticket_id, employee_id):
    """Assign a ticket to an IT specialist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Update ticket assignee
    c.execute("UPDATE tickets SET assignee_id = ? WHERE id = ?", 
             (employee_id, ticket_id))
    
    # Record the change in history
    c.execute("""
        SELECT title, status, description, hardware_name, hardware_model, hardware_manufacturer
        FROM tickets
        WHERE id = ?
    """, (ticket_id,))
    
    ticket_data = c.fetchone()
    if ticket_data:
        c.execute("""
            INSERT INTO ticket_history 
            (ticket_id, title, status, description, hardware_name, hardware_model, 
             hardware_manufacturer, comment, changed_at, assignee_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (ticket_id, *ticket_data, f"Ticket assigned to employee {employee_id}", 
              datetime.now(), employee_id))
    
    conn.commit()
    conn.close()

def unassign_ticket(ticket_id):
    """Remove assignment from a ticket."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get current assignee before unassigning
    c.execute("SELECT assignee_id FROM tickets WHERE id = ?", (ticket_id,))
    current_assignee = c.fetchone()[0]
    
    # Update ticket assignee to NULL
    c.execute("UPDATE tickets SET assignee_id = NULL WHERE id = ?", (ticket_id,))
    
    # Record the change in history
    c.execute("""
        SELECT title, status, description, hardware_name, hardware_model, hardware_manufacturer
        FROM tickets
        WHERE id = ?
    """, (ticket_id,))
    
    ticket_data = c.fetchone()
    if ticket_data:
        c.execute("""
            INSERT INTO ticket_history 
            (ticket_id, title, status, description, hardware_name, hardware_model, 
             hardware_manufacturer, comment, changed_at, assignee_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (ticket_id, *ticket_data, f"Ticket unassigned from employee {current_assignee}", 
              datetime.now(), None))
    
    conn.commit()
    conn.close()

def get_ticket_assignee(ticket_id):
    """Get the current assignee of a ticket."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # First get the assignee_id from tickets table
    c.execute("SELECT assignee_id FROM tickets WHERE id = ?", (ticket_id,))
    assignee_id = c.fetchone()
    
    if not assignee_id or not assignee_id[0]:
        conn.close()
        return None
        
    # Then get employee details from HR database
    hr_conn = sqlite3.connect(HR_DB_PATH)
    hr_cursor = hr_conn.cursor()
    
    hr_cursor.execute("""
        SELECT id, name, email
        FROM employees
        WHERE id = ?
    """, (assignee_id[0],))
    
    assignee = hr_cursor.fetchone()
    hr_conn.close()
    conn.close()
    
    if assignee:
        return {
            "id": assignee[0],
            "name": assignee[1],
            "email": assignee[2]
        }
    return None

def get_assigned_tickets(employee_id):
    """Get all tickets assigned to a specific employee."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        SELECT id, title, status, description, hardware_name, hardware_model, 
               hardware_manufacturer, created_at
        FROM tickets
        WHERE assignee_id = ?
        ORDER BY created_at DESC
    """, (employee_id,))
    
    tickets = [{
        "id": row[0],
        "title": row[1],
        "status": row[2],
        "description": row[3],
        "hardware": {
            "name": row[4],
            "model": row[5],
            "manufacturer": row[6]
        },
        "created_at": row[7]
    } for row in c.fetchall()]
    
    conn.close()
    return tickets 

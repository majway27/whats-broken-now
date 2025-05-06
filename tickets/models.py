from datetime import datetime
import os
from shared.database import DatabaseConnection

# Get the directory where this module is located
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(MODULE_DIR, 'tickets.db')
HR_DB_PATH = os.path.join(MODULE_DIR, '..', 'human_resources', 'hr.db')

# Schema for tickets database
TICKETS_SCHEMA = '''
CREATE TABLE IF NOT EXISTS products
(id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT NOT NULL,
 model TEXT NOT NULL,
 manufacturer TEXT NOT NULL,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS tickets
(id TEXT PRIMARY KEY,
 title TEXT,
 status TEXT,
 product_id INTEGER,
 created_at TIMESTAMP,
 assignee_id INTEGER,
 FOREIGN KEY (product_id) REFERENCES products(id));

CREATE TABLE IF NOT EXISTS ticket_description
(id INTEGER PRIMARY KEY AUTOINCREMENT,
 ticket_id TEXT NOT NULL,
 description TEXT NOT NULL,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (ticket_id) REFERENCES tickets(id));

CREATE TABLE IF NOT EXISTS ticket_history
(audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
 ticket_id TEXT,
 title TEXT,
 status TEXT,
 product_id INTEGER,
 comment TEXT,
 changed_at TIMESTAMP,
 assignee_id INTEGER,
 FOREIGN KEY (ticket_id) REFERENCES tickets(id),
 FOREIGN KEY (product_id) REFERENCES products(id));
'''

def init_db():
    """Initialize the tickets database."""
    DatabaseConnection.init_db('tickets', TICKETS_SCHEMA)

def reset_db():
    """Reset the database by dropping all tables and recreating them."""
    DatabaseConnection.reset_db('tickets', TICKETS_SCHEMA)

def get_active_tickets():
    """Get all active tickets from the database."""
    with DatabaseConnection.get_cursor('tickets') as c:
        c.execute("""
            SELECT 
                t.id as ticket_id,
                t.title as ticket_title,
                t.status as ticket_status,
                td.description as ticket_description,
                p.name as product_name,
                p.model as product_model,
                p.manufacturer as product_manufacturer
            FROM tickets t
            LEFT JOIN products p ON t.product_id = p.id
            LEFT JOIN ticket_description td ON t.id = td.ticket_id
            WHERE t.status != 'Resolved'
        """)
        tickets = [{
            "id": row['ticket_id'],
            "title": row['ticket_title'],
            "status": row['ticket_status'],
            "description": row['ticket_description'],
            "hardware": {
                "name": row['product_name'],
                "model": row['product_model'],
                "manufacturer": row['product_manufacturer']
            }
        } for row in c.fetchall()]
        return tickets

def get_unassigned_tickets():
    """Get all active tickets that are not assigned to anyone."""
    with DatabaseConnection.get_cursor('tickets') as c:
        c.execute("""
            SELECT 
                t.id as ticket_id,
                t.title as ticket_title,
                t.status as ticket_status,
                td.description as ticket_description,
                p.name as product_name,
                p.model as product_model,
                p.manufacturer as product_manufacturer
            FROM tickets t
            LEFT JOIN products p ON t.product_id = p.id
            LEFT JOIN ticket_description td ON t.id = td.ticket_id
            WHERE t.status != 'Resolved' AND t.assignee_id IS NULL
        """)
        tickets = [{
            "id": row['ticket_id'],
            "title": row['ticket_title'],
            "status": row['ticket_status'],
            "description": row['ticket_description'],
            "hardware": {
                "name": row['product_name'],
                "model": row['product_model'],
                "manufacturer": row['product_manufacturer']
            }
        } for row in c.fetchall()]
        return tickets

def get_all_tickets():
    """Get all tickets from the database."""
    with DatabaseConnection.get_cursor('tickets') as c:
        c.execute("""
            SELECT 
                t.id as ticket_id,
                t.title as ticket_title,
                t.status as ticket_status,
                td.description as ticket_description,
                p.name as product_name,
                p.model as product_model,
                p.manufacturer as product_manufacturer,
                t.created_at as ticket_created_at
            FROM tickets t
            LEFT JOIN products p ON t.product_id = p.id
            LEFT JOIN ticket_description td ON t.id = td.ticket_id
            ORDER BY t.created_at DESC
        """)
        tickets = [{
            "id": row['ticket_id'],
            "title": row['ticket_title'],
            "status": row['ticket_status'],
            "description": row['ticket_description'],
            "hardware": {
                "name": row['product_name'],
                "model": row['product_model'],
                "manufacturer": row['product_manufacturer']
            },
            "created_at": row['ticket_created_at']
        } for row in c.fetchall()]
        return tickets

def get_ticket_count():
    """Get the total number of tickets in the database."""
    with DatabaseConnection.get_cursor('tickets') as c:
        c.execute("SELECT COUNT(*) FROM tickets")
        return c.fetchone()[0]

def get_tickets_by_status():
    """Get a dictionary of ticket counts by status."""
    with DatabaseConnection.get_cursor('tickets') as c:
        c.execute("SELECT status, COUNT(*) FROM tickets GROUP BY status")
        return dict(c.fetchall())

def get_ticket_history(ticket_id):
    """Get the complete history of a ticket including status changes and comments."""
    with DatabaseConnection.get_cursor('tickets') as c:
        c.execute("""
            SELECT 
                th.audit_id as history_id,
                th.title as history_title,
                th.status as history_status,
                p.name as product_name,
                p.model as product_model,
                p.manufacturer as product_manufacturer,
                th.comment as history_comment,
                th.changed_at as history_changed_at,
                th.assignee_id as history_assignee_id
            FROM ticket_history th
            LEFT JOIN products p ON th.product_id = p.id
            WHERE th.ticket_id = ?
            ORDER BY th.changed_at DESC
        """, (ticket_id,))
        
        history = []
        for row in c.fetchall():
            history.append({
                "audit_id": row['history_id'],
                "title": row['history_title'],
                "status": row['history_status'],
                "hardware": {
                    "name": row['product_name'],
                    "model": row['product_model'],
                    "manufacturer": row['product_manufacturer']
                },
                "comment": row['history_comment'],
                "changed_at": row['history_changed_at'],
                "assignee_id": row['history_assignee_id']
            })
        return history

def ensure_default_product(cursor):
    """Ensure there is at least one product in the database."""
    # Check if we have any products
    cursor.execute("SELECT id FROM products LIMIT 1")
    result = cursor.fetchone()
    if result:
        return result['id']
        
    # Add a default product
    cursor.execute("""
        INSERT INTO products (name, model, manufacturer)
        VALUES (?, ?, ?)
    """, ("Unknown Product", "Unknown Model", "Unknown Manufacturer"))
    return cursor.lastrowid

def insert_ticket_history(cursor, ticket_id, title, status, description, product_id, comment=None, assignee_id=None):
    """Insert a record into the ticket history table."""
    try:
        cursor.execute("""
            INSERT INTO ticket_history 
            (ticket_id, title, status, product_id, comment, changed_at, assignee_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (ticket_id, title, status, product_id, comment, datetime.now(), assignee_id))
    except Exception as e:
        print(f"Error inserting history: {str(e)}")
        raise

def add_ticket(ticket):
    """Add a new ticket to the database."""
    with DatabaseConnection.get_cursor('tickets') as c:
        # First, ensure the product exists
        c.execute("""
            INSERT OR IGNORE INTO products (name, model, manufacturer)
            VALUES (?, ?, ?)
        """, (ticket['hardware']['name'], 
              ticket['hardware']['model'], 
              ticket['hardware']['manufacturer']))
        
        # Get the product ID
        c.execute("""
            SELECT id FROM products 
            WHERE name = ? AND model = ? AND manufacturer = ?
        """, (ticket['hardware']['name'], 
              ticket['hardware']['model'], 
              ticket['hardware']['manufacturer']))
        product_id = c.fetchone()[0]
        
        # Insert the ticket
        c.execute("""
            INSERT INTO tickets (id, title, status, product_id, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (ticket['id'],
              ticket['title'],
              ticket['status'],
              product_id,
              datetime.now()))
        
        # Insert the description
        c.execute("""
            INSERT INTO ticket_description (ticket_id, description)
            VALUES (?, ?)
        """, (ticket['id'], ticket['description']))

def list_products():
    """List all products in the database."""
    with DatabaseConnection.get_cursor('tickets') as c:
        c.execute("SELECT id, name, model, manufacturer FROM products")
        return c.fetchall()

def append_ticket_comment(ticket, comment):
    """Add a comment to a ticket."""
    if not comment.strip():
        return
        
    try:
        with DatabaseConnection.get_cursor('tickets') as c:
            # First verify the ticket exists
            c.execute("SELECT id FROM tickets WHERE id = ?", (ticket['id'],))
            if not c.fetchone():
                print(f"Error: Ticket {ticket['id']} does not exist")
                return

            # Get current ticket state
            c.execute("""
                SELECT 
                    t.title as ticket_title,
                    t.status as ticket_status,
                    td.description as ticket_description,
                    t.product_id as ticket_product_id
                FROM tickets t
                INNER JOIN ticket_description td ON t.id = td.ticket_id
                WHERE t.id = ?
            """, (ticket['id'],))
            row = c.fetchone()
            
            if not row:
                print(f"Error: No description found for ticket {ticket['id']}")
                return
                
            if row['ticket_product_id'] is None:
                print(f"Error: No product ID found for ticket {ticket['id']}")
                return
                
            # Verify the product exists
            c.execute("SELECT id FROM products WHERE id = ?", (row['ticket_product_id'],))
            if not c.fetchone():
                print(f"Error: Product ID {row['ticket_product_id']} does not exist")
                print("\nFixing missing product...")
                
                # Ensure we have a default product
                default_product_id = ensure_default_product(c)
                if not default_product_id:
                    print("Error: Failed to create default product")
                    return
                
                # Update the ticket to use the default product
                c.execute("""
                    UPDATE tickets 
                    SET product_id = ? 
                    WHERE id = ?
                """, (default_product_id, ticket['id']))
                
                print(f"Updated ticket to use default product (ID: {default_product_id})")
                
                # Get the updated ticket state
                c.execute("""
                    SELECT 
                        t.title as ticket_title,
                        t.status as ticket_status,
                        td.description as ticket_description,
                        t.product_id as ticket_product_id
                    FROM tickets t
                    INNER JOIN ticket_description td ON t.id = td.ticket_id
                    WHERE t.id = ?
                """, (ticket['id'],))
                row = c.fetchone()
                
            print(f"Debug: Adding comment to ticket {ticket['id']}")
            print(f"Debug: Product ID: {row['ticket_product_id']}")
            
            # Insert the history record
            insert_ticket_history(
                c,
                ticket['id'],
                row['ticket_title'],
                row['ticket_status'],
                row['ticket_description'],
                row['ticket_product_id'],
                comment,
                ticket.get('assignee_id')
            )
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

def record_ticket_history(ticket_id):
    """Record the current state of a ticket in the history table."""
    with DatabaseConnection.get_cursor('tickets') as c:
        # Get current ticket state
        c.execute("""
            SELECT t.title, t.status, td.description, t.product_id, t.assignee_id
            FROM tickets t
            LEFT JOIN ticket_description td ON t.id = td.ticket_id
            WHERE t.id = ?
        """, (ticket_id,))
        
        row = c.fetchone()
        if row:
            title, status, description, product_id, assignee_id = row
            insert_ticket_history(
                c,
                ticket_id, title, status, description,
                product_id, None, assignee_id
            )

def mutate_ticket_status(ticket_id, new_status):
    """Update the status of a ticket."""
    with DatabaseConnection.get_cursor('tickets') as c:
        # Get current ticket state before update
        c.execute("""
            SELECT t.title, t.status, td.description, t.product_id, t.assignee_id
            FROM tickets t
            LEFT JOIN ticket_description td ON t.id = td.ticket_id
            WHERE t.id = ?
        """, (ticket_id,))
        
        row = c.fetchone()
        if row:
            # Update the ticket status
            c.execute("""
                UPDATE tickets 
                SET status = ? 
                WHERE id = ?
            """, (new_status, ticket_id))
            
            # Record the history in the same transaction
            c.execute("""
                INSERT INTO ticket_history 
                (ticket_id, title, status, product_id, comment, changed_at, assignee_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                ticket_id,
                row['title'],
                new_status,
                row['product_id'],
                f"Status changed from {row['status']} to {new_status}",
                datetime.now(),
                row['assignee_id']
            ))

def check_new_tickets():
    """Check for new tickets and return them."""
    with DatabaseConnection.get_cursor('tickets') as c:
        c.execute("""
            SELECT 
                t.id as ticket_id,
                t.title as ticket_title,
                t.status as ticket_status,
                td.description as ticket_description,
                p.name as product_name,
                p.model as product_model,
                p.manufacturer as product_manufacturer,
                t.created_at as ticket_created_at
            FROM tickets t
            LEFT JOIN products p ON t.product_id = p.id
            LEFT JOIN ticket_description td ON t.id = td.ticket_id
            WHERE t.status = 'New'
            ORDER BY t.created_at DESC
        """)
        tickets = [{
            "id": row['ticket_id'],
            "title": row['ticket_title'],
            "status": row['ticket_status'],
            "description": row['ticket_description'],
            "hardware": {
                "name": row['product_name'],
                "model": row['product_model'],
                "manufacturer": row['product_manufacturer']
            },
            "created_at": row['ticket_created_at']
        } for row in c.fetchall()]
        return tickets

def assign_ticket(ticket_id, employee_id):
    """Assign a ticket to an employee."""
    with DatabaseConnection.get_cursor('tickets') as c:
        # Get current ticket state before update
        c.execute("""
            SELECT 
                t.title as ticket_title,
                t.status as ticket_status,
                td.description as ticket_description,
                t.product_id as ticket_product_id,
                t.assignee_id as current_assignee_id
            FROM tickets t
            LEFT JOIN ticket_description td ON t.id = td.ticket_id
            WHERE t.id = ?
        """, (ticket_id,))
        row = c.fetchone()
        
        if row:
            # Update the ticket
            c.execute("""
                UPDATE tickets 
                SET assignee_id = ? 
                WHERE id = ?
            """, (employee_id, ticket_id))
            
            # Record the history in the same transaction
            c.execute("""
                INSERT INTO ticket_history 
                (ticket_id, title, status, product_id, comment, changed_at, assignee_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                ticket_id,
                row['ticket_title'],
                row['ticket_status'],
                row['ticket_product_id'],
                f"Ticket reassigned from {row['current_assignee_id']} to {employee_id}",
                datetime.now(),
                employee_id
            ))

def unassign_ticket(ticket_id):
    """Remove the assignment from a ticket."""
    with DatabaseConnection.get_cursor('tickets') as c:
        c.execute("""
            UPDATE tickets 
            SET assignee_id = NULL 
            WHERE id = ?
        """, (ticket_id,))
        record_ticket_history(ticket_id)

def get_ticket_assignee(ticket_id):
    """Get the employee information assigned to a ticket."""
    with DatabaseConnection.get_cursor('tickets') as c:
        # First get the assignee_id from the tickets database
        c.execute("""
            SELECT assignee_id
            FROM tickets 
            WHERE id = ?
        """, (ticket_id,))
        result = c.fetchone()
        if not result or not result['assignee_id']:
            return None
            
        # Then get the employee details from the HR database
        with DatabaseConnection.get_cursor('hr') as hr_cursor:
            hr_cursor.execute("""
                SELECT id, first_name, last_name, email
                FROM employees
                WHERE id = ?
            """, (result['assignee_id'],))
            employee = hr_cursor.fetchone()
            if employee:
                return {
                    'id': employee['id'],
                    'first_name': employee['first_name'],
                    'last_name': employee['last_name'],
                    'email': employee['email']
                }
            return None

def get_assigned_tickets(employee_id):
    """Get all tickets assigned to an employee."""
    with DatabaseConnection.get_cursor('tickets') as c:
        c.execute("""
            SELECT 
                t.id as ticket_id,
                t.title as ticket_title,
                t.status as ticket_status,
                td.description as ticket_description,
                p.name as product_name,
                p.model as product_model,
                p.manufacturer as product_manufacturer,
                t.created_at as ticket_created_at
            FROM tickets t
            LEFT JOIN products p ON t.product_id = p.id
            LEFT JOIN ticket_description td ON t.id = td.ticket_id
            WHERE t.assignee_id = ?
            ORDER BY t.created_at DESC
        """, (employee_id,))
        tickets = [{
            "id": row['ticket_id'],
            "title": row['ticket_title'],
            "status": row['ticket_status'],
            "description": row['ticket_description'],
            "hardware": {
                "name": row['product_name'],
                "model": row['product_model'],
                "manufacturer": row['product_manufacturer']
            },
            "created_at": row['ticket_created_at']
        } for row in c.fetchall()]
        return tickets 

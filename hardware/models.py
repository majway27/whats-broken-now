import sqlite3
import os

# Get the directory where this module is located
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(MODULE_DIR, 'hardware_catalog.db')


def get_hardware_db():
    """Get a connection to the hardware catalog database."""
    return sqlite3.connect(DB_PATH) 

def init_db():
    """Initialize the hardware catalog database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create hardware catalog tables
    c.execute('''CREATE TABLE IF NOT EXISTS hardware_categories
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT UNIQUE NOT NULL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS hardware_items
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  category_id INTEGER NOT NULL,
                  name TEXT NOT NULL,
                  manufacturer TEXT NOT NULL,
                  model TEXT NOT NULL,
                  release_date TEXT,
                  repair_difficulty INTEGER,
                  operating_system TEXT,
                  FOREIGN KEY (category_id) REFERENCES hardware_categories(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS hardware_specs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  hardware_id INTEGER NOT NULL,
                  spec_name TEXT NOT NULL,
                  spec_value TEXT NOT NULL,
                  FOREIGN KEY (hardware_id) REFERENCES hardware_items(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS hardware_failures
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  hardware_id INTEGER NOT NULL,
                  failure_description TEXT NOT NULL,
                  FOREIGN KEY (hardware_id) REFERENCES hardware_items(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS troubleshooting_procedures
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  hardware_id INTEGER NOT NULL,
                  name TEXT NOT NULL,
                  FOREIGN KEY (hardware_id) REFERENCES hardware_items(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS troubleshooting_steps
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  procedure_id INTEGER NOT NULL,
                  step_number INTEGER NOT NULL,
                  description TEXT NOT NULL,
                  FOREIGN KEY (procedure_id) REFERENCES troubleshooting_procedures(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS special_tools
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  hardware_id INTEGER NOT NULL,
                  tool_name TEXT NOT NULL,
                  FOREIGN KEY (hardware_id) REFERENCES hardware_items(id))''')
    
    conn.commit()
    conn.close()

def get_hardware_categories():
    """Get all hardware categories from the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, name FROM hardware_categories")
    categories = [{"id": row[0], "name": row[1]} for row in c.fetchall()]
    conn.close()
    return categories

def get_hardware_items(category_id=None):
    """Get hardware items, optionally filtered by category."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if category_id:
        c.execute("""
            SELECT id, name, manufacturer, model, release_date, repair_difficulty, operating_system
            FROM hardware_items
            WHERE category_id = ?
        """, (category_id,))
    else:
        c.execute("""
            SELECT id, name, manufacturer, model, release_date, repair_difficulty, operating_system
            FROM hardware_items
        """)
    
    items = [{
        "id": row[0],
        "name": row[1],
        "manufacturer": row[2],
        "model": row[3],
        "release_date": row[4],
        "repair_difficulty": row[5],
        "operating_system": row[6]
    } for row in c.fetchall()]
    
    conn.close()
    return items

def get_hardware_specs(hardware_id):
    """Get specifications for a hardware item."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT spec_name, spec_value
        FROM hardware_specs
        WHERE hardware_id = ?
    """, (hardware_id,))
    specs = dict(c.fetchall())
    conn.close()
    return specs

def get_hardware_failures(hardware_id):
    """Get common failures for a hardware item."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT failure_description
        FROM hardware_failures
        WHERE hardware_id = ?
    """, (hardware_id,))
    failures = [row[0] for row in c.fetchall()]
    conn.close()
    return failures

def get_troubleshooting_procedures(hardware_id):
    """Get troubleshooting procedures for a hardware item."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT id, name
        FROM troubleshooting_procedures
        WHERE hardware_id = ?
    """, (hardware_id,))
    procedures = []
    for row in c.fetchall():
        procedure_id = row[0]
        c.execute("""
            SELECT step_number, description
            FROM troubleshooting_steps
            WHERE procedure_id = ?
            ORDER BY step_number
        """, (procedure_id,))
        steps = [{"number": row[0], "description": row[1]} for row in c.fetchall()]
        procedures.append({
            "id": procedure_id,
            "name": row[1],
            "steps": steps
        })
    conn.close()
    return procedures

def get_special_tools(hardware_id):
    """Get special tools required for a hardware item."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT tool_name
        FROM special_tools
        WHERE hardware_id = ?
    """, (hardware_id,))
    tools = [row[0] for row in c.fetchall()]
    conn.close()
    return tools

def get_hardware_statistics():
    """Get statistics about the hardware catalog."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Count hardware items
    c.execute("SELECT COUNT(*) FROM hardware_items")
    total_hardware = c.fetchone()[0]
    
    # Count hardware categories
    c.execute("SELECT COUNT(*) FROM hardware_categories")
    total_categories = c.fetchone()[0]
    
    conn.close()
    return {
        "total_hardware": total_hardware,
        "total_categories": total_categories
    }

def add_hardware_item(category_id, name, manufacturer, model):
    """Add a new hardware item to the catalog.
    
    Args:
        category_id (int): The ID of the category for the hardware item
        name (str): The name of the hardware item
        manufacturer (str): The manufacturer of the hardware item
        model (str): The model of the hardware item
        
    Returns:
        bool: True if successful, False otherwise
        str: Error message if unsuccessful, None if successful
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        c.execute("""
            INSERT INTO hardware_items (category_id, name, manufacturer, model)
            VALUES (?, ?, ?, ?)
        """, (category_id, name, manufacturer, model))
        
        conn.commit()
        return True, None
    except sqlite3.Error as e:
        return False, str(e)
    finally:
        conn.close()

def update_hardware_item(item_id, name=None, manufacturer=None, model=None):
    """Update an existing hardware item in the catalog.
    
    Args:
        item_id (int): The ID of the hardware item to update
        name (str, optional): New name for the hardware item
        manufacturer (str, optional): New manufacturer for the hardware item
        model (str, optional): New model for the hardware item
        
    Returns:
        tuple: (success (bool), error_message (str or None))
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        # Verify item exists
        c.execute("SELECT id FROM hardware_items WHERE id = ?", (item_id,))
        if not c.fetchone():
            return False, "Invalid item ID"
        
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
            return True, None
        else:
            return True, "No changes made"
    except sqlite3.Error as e:
        return False, str(e)
    finally:
        conn.close()

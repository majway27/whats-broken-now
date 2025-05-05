from shared.database import DatabaseConnection

# Schema for hardware catalog database
HARDWARE_SCHEMA = '''
CREATE TABLE IF NOT EXISTS hardware_categories
(id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT UNIQUE NOT NULL);

CREATE TABLE IF NOT EXISTS hardware_items
(id INTEGER PRIMARY KEY AUTOINCREMENT,
 category_id INTEGER NOT NULL,
 name TEXT NOT NULL,
 manufacturer TEXT NOT NULL,
 model TEXT NOT NULL,
 release_date TEXT,
 repair_difficulty INTEGER,
 operating_system TEXT,
 FOREIGN KEY (category_id) REFERENCES hardware_categories(id));

CREATE TABLE IF NOT EXISTS hardware_specs
(id INTEGER PRIMARY KEY AUTOINCREMENT,
 hardware_id INTEGER NOT NULL,
 spec_name TEXT NOT NULL,
 spec_value TEXT NOT NULL,
 FOREIGN KEY (hardware_id) REFERENCES hardware_items(id));

CREATE TABLE IF NOT EXISTS hardware_failures
(id INTEGER PRIMARY KEY AUTOINCREMENT,
 hardware_id INTEGER NOT NULL,
 failure_description TEXT NOT NULL,
 FOREIGN KEY (hardware_id) REFERENCES hardware_items(id));

CREATE TABLE IF NOT EXISTS troubleshooting_procedures
(id INTEGER PRIMARY KEY AUTOINCREMENT,
 hardware_id INTEGER NOT NULL,
 name TEXT NOT NULL,
 FOREIGN KEY (hardware_id) REFERENCES hardware_items(id));

CREATE TABLE IF NOT EXISTS troubleshooting_steps
(id INTEGER PRIMARY KEY AUTOINCREMENT,
 procedure_id INTEGER NOT NULL,
 step_number INTEGER NOT NULL,
 description TEXT NOT NULL,
 FOREIGN KEY (procedure_id) REFERENCES troubleshooting_procedures(id));

CREATE TABLE IF NOT EXISTS special_tools
(id INTEGER PRIMARY KEY AUTOINCREMENT,
 hardware_id INTEGER NOT NULL,
 tool_name TEXT NOT NULL,
 FOREIGN KEY (hardware_id) REFERENCES hardware_items(id));
'''

def init_db():
    """Initialize the hardware catalog database."""
    DatabaseConnection.init_db('hardware', HARDWARE_SCHEMA)

def get_hardware_categories():
    """Get all hardware categories from the database."""
    with DatabaseConnection.get_cursor('hardware') as cursor:
        cursor.execute("SELECT id, name FROM hardware_categories")
        return [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]

def get_hardware_items(category_id=None):
    """Get hardware items, optionally filtered by category."""
    with DatabaseConnection.get_cursor('hardware') as cursor:
        if category_id:
            cursor.execute("""
                SELECT id, name, manufacturer, model, release_date, repair_difficulty, operating_system
                FROM hardware_items
                WHERE category_id = ?
            """, (category_id,))
        else:
            cursor.execute("""
                SELECT id, name, manufacturer, model, release_date, repair_difficulty, operating_system
                FROM hardware_items
            """)
        
        return [{
            "id": row[0],
            "name": row[1],
            "manufacturer": row[2],
            "model": row[3],
            "release_date": row[4],
            "repair_difficulty": row[5],
            "operating_system": row[6]
        } for row in cursor.fetchall()]

def get_hardware_specs(hardware_id):
    """Get specifications for a hardware item."""
    with DatabaseConnection.get_cursor('hardware') as cursor:
        cursor.execute("""
            SELECT spec_name, spec_value
            FROM hardware_specs
            WHERE hardware_id = ?
        """, (hardware_id,))
        return dict(cursor.fetchall())

def get_hardware_failures(hardware_id):
    """Get common failures for a hardware item."""
    with DatabaseConnection.get_cursor('hardware') as cursor:
        cursor.execute("""
            SELECT failure_description
            FROM hardware_failures
            WHERE hardware_id = ?
        """, (hardware_id,))
        return [row[0] for row in cursor.fetchall()]

def get_troubleshooting_procedures(hardware_id):
    """Get troubleshooting procedures for a hardware item."""
    with DatabaseConnection.get_cursor('hardware') as cursor:
        cursor.execute("""
            SELECT id, name
            FROM troubleshooting_procedures
            WHERE hardware_id = ?
        """, (hardware_id,))
        procedures = []
        for row in cursor.fetchall():
            procedure_id = row[0]
            cursor.execute("""
                SELECT step_number, description
                FROM troubleshooting_steps
                WHERE procedure_id = ?
                ORDER BY step_number
            """, (procedure_id,))
            steps = [{"number": row[0], "description": row[1]} for row in cursor.fetchall()]
            procedures.append({
                "id": procedure_id,
                "name": row[1],
                "steps": steps
            })
        return procedures

def get_special_tools(hardware_id):
    """Get special tools required for a hardware item."""
    with DatabaseConnection.get_cursor('hardware') as cursor:
        cursor.execute("""
            SELECT tool_name
            FROM special_tools
            WHERE hardware_id = ?
        """, (hardware_id,))
        return [row[0] for row in cursor.fetchall()]

def get_hardware_statistics():
    """Get statistics about the hardware catalog."""
    with DatabaseConnection.get_cursor('hardware') as cursor:
        # Count hardware items
        cursor.execute("SELECT COUNT(*) FROM hardware_items")
        total_hardware = cursor.fetchone()[0]
        
        # Count hardware categories
        cursor.execute("SELECT COUNT(*) FROM hardware_categories")
        total_categories = cursor.fetchone()[0]
        
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
    try:
        with DatabaseConnection.get_cursor('hardware') as cursor:
            cursor.execute("""
                INSERT INTO hardware_items (category_id, name, manufacturer, model)
                VALUES (?, ?, ?, ?)
            """, (category_id, name, manufacturer, model))
            return True, None
    except Exception as e:
        return False, str(e)

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
    try:
        with DatabaseConnection.get_cursor('hardware') as cursor:
            # Verify item exists
            cursor.execute("SELECT id FROM hardware_items WHERE id = ?", (item_id,))
            if not cursor.fetchone():
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
            
            if not updates:
                return False, "No updates provided"
            
            # Add item_id to params
            params.append(item_id)
            
            # Execute update
            query = f"""
                UPDATE hardware_items 
                SET {', '.join(updates)}
                WHERE id = ?
            """
            cursor.execute(query, params)
            return True, None
    except Exception as e:
        return False, str(e)

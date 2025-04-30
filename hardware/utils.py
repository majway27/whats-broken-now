import sqlite3
import os
import random
from . import data

# Get the directory where this module is located
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(MODULE_DIR, 'hardware_catalog.db')

def migrate_hardware_catalog():
    """Migrate the hardware catalog data into the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Clear existing data
    c.execute("DELETE FROM troubleshooting_steps")
    c.execute("DELETE FROM troubleshooting_procedures")
    c.execute("DELETE FROM special_tools")
    c.execute("DELETE FROM hardware_failures")
    c.execute("DELETE FROM hardware_specs")
    c.execute("DELETE FROM hardware_items")
    c.execute("DELETE FROM hardware_categories")
    
    # Insert categories and hardware items
    for category_name, items in data.HARDWARE_CATALOG.items():
        # Insert category
        c.execute("INSERT INTO hardware_categories (name) VALUES (?)", (category_name,))
        category_id = c.lastrowid
        
        # Insert each hardware item
        for item in items:
            c.execute("""
                INSERT INTO hardware_items 
                (category_id, name, manufacturer, model, release_date, repair_difficulty, operating_system)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                category_id,
                item['name'],
                item['manufacturer'],
                item['model'],
                item.get('release_date'),
                item.get('repair_difficulty'),
                item.get('operating_system')
            ))
            hardware_id = c.lastrowid
            
            # Insert specs
            for spec_name, spec_value in item['specs'].items():
                c.execute("""
                    INSERT INTO hardware_specs (hardware_id, spec_name, spec_value)
                    VALUES (?, ?, ?)
                """, (hardware_id, spec_name, spec_value))
            
            # Insert failures
            for failure in item['common_failures']:
                c.execute("""
                    INSERT INTO hardware_failures (hardware_id, failure_description)
                    VALUES (?, ?)
                """, (hardware_id, failure))
            
            # Insert troubleshooting procedures
            for procedure in item.get('troubleshooting_procedures', []):
                c.execute("""
                    INSERT INTO troubleshooting_procedures (hardware_id, name)
                    VALUES (?, ?)
                """, (hardware_id, procedure['name']))
                procedure_id = c.lastrowid
                
                # Insert procedure steps
                for step_num, step in enumerate(procedure['steps'], 1):
                    c.execute("""
                        INSERT INTO troubleshooting_steps (procedure_id, step_number, description)
                        VALUES (?, ?, ?)
                    """, (procedure_id, step_num, step))
            
            # Insert special tools
            for tool in item.get('special_tools', []):
                c.execute("""
                    INSERT INTO special_tools (hardware_id, tool_name)
                    VALUES (?, ?)
                """, (hardware_id, tool))
    
    conn.commit()
    conn.close()

def get_random_hardware_item():
    """Get a random hardware item from the database."""
    conn = sqlite3.connect(DB_PATH)
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
                conn.close()
                return {
                    "id": hardware_item[0],
                    "name": hardware_item[1],
                    "manufacturer": hardware_item[2],
                    "model": hardware_item[3],
                    "category": hardware_item[4],
                    "failure": failure
                }
    
    conn.close()
    return None 
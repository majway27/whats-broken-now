from . import data
from .database import get_db_connection

def migrate_employee_directory():
    """Migrate the employee directory data into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM performance_ratings")
    cursor.execute("DELETE FROM employees")
    cursor.execute("DELETE FROM roles")
    
    # Insert roles
    role_map = {}  # To store role titles to IDs mapping
    for role in data.ROLES:
        cursor.execute("""
            INSERT INTO roles (title, description)
            VALUES (?, ?)
        """, (role['title'], role['description']))
        role_map[role['title']] = cursor.lastrowid
    
    # Insert employees
    for employee in data.EMPLOYEES:
        cursor.execute("""
            INSERT INTO employees 
            (first_name, last_name, email, role_id, hire_date)
            VALUES (?, ?, ?, ?, ?)
        """, (
            employee['first_name'],
            employee['last_name'],
            employee['email'],
            role_map[employee['role_title']],
            employee['hire_date'].isoformat()
        ))
    
    conn.commit()
    conn.close() 
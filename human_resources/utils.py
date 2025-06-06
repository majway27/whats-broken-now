from . import data
from shared.database import DatabaseConnection
from player.repository import PlayerRepository
from .repository import EmployeeRepository

def migrate_employee_directory():
    """Migrate the employee directory data into the database."""
    with DatabaseConnection.get_cursor('hr') as cursor:
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

def get_current_employee():
    """
    Get the current employee record associated with the current player.
    Returns None if there is no current player or if the player has no associated employee.
    """
    current_player = PlayerRepository.get_most_recent()
    if not current_player or not current_player.employee_id:
        return None
    return EmployeeRepository.get_by_id(current_player.employee_id) 
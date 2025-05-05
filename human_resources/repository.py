from datetime import date
from typing import List, Optional
from shared.database import DatabaseConnection
from .models import Role, Employee, PerformanceRating

class RoleRepository:
    @staticmethod
    def create(title: str, description: Optional[str] = None) -> Role:
        with DatabaseConnection.get_cursor('hr') as cursor:
            cursor.execute(
                'INSERT INTO roles (title, description) VALUES (?, ?)',
                (title, description)
            )
            role_id = cursor.lastrowid
            return Role(id=role_id, title=title, description=description, created_at=None)

    @staticmethod
    def get_by_title(title: str) -> Optional[Role]:
        with DatabaseConnection.get_cursor('hr') as cursor:
            cursor.execute('SELECT * FROM roles WHERE title = ?', (title,))
            row = cursor.fetchone()
            return Role.from_db_row(row) if row else None

    @staticmethod
    def get_by_id(role_id: int) -> Optional[Role]:
        with DatabaseConnection.get_cursor('hr') as cursor:
            cursor.execute('SELECT * FROM roles WHERE id = ?', (role_id,))
            row = cursor.fetchone()
            return Role.from_db_row(row) if row else None

    @staticmethod
    def get_all() -> List[Role]:
        with DatabaseConnection.get_cursor('hr') as cursor:
            cursor.execute('SELECT * FROM roles')
            return [Role.from_db_row(row) for row in cursor.fetchall()]

class EmployeeRepository:
    @staticmethod
    def create(first_name: str, last_name: str, email: str, hire_date: date, role_id: Optional[int] = None, employment_status: str = 'active') -> Employee:
        with DatabaseConnection.get_cursor('hr') as cursor:
            cursor.execute(
                'INSERT INTO employees (first_name, last_name, email, role_id, hire_date, employment_status) VALUES (?, ?, ?, ?, ?, ?)',
                (first_name, last_name, email, role_id, hire_date.isoformat(), employment_status)
            )
            employee_id = cursor.lastrowid
            return Employee(
                id=employee_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                role_id=role_id,
                hire_date=hire_date,
                employment_status=employment_status,
                created_at=None
            )

    @staticmethod
    def get_current_player() -> Optional[Employee]:
        """Get the current player's employee record."""
        with DatabaseConnection.get_cursor('hr') as cursor:
            cursor.execute('''
                SELECT * FROM employees 
                WHERE employment_status = 'active'
                ORDER BY created_at DESC 
                LIMIT 1
            ''')
            row = cursor.fetchone()
            return Employee.from_db_row(row) if row else None

    @staticmethod
    def get_by_id(employee_id: int) -> Optional[Employee]:
        with DatabaseConnection.get_cursor('hr') as cursor:
            cursor.execute('SELECT * FROM employees WHERE id = ?', (employee_id,))
            row = cursor.fetchone()
            return Employee.from_db_row(row) if row else None

    @staticmethod
    def get_by_email(email: str) -> Optional[Employee]:
        """Get an employee by their email address."""
        with DatabaseConnection.get_cursor('hr') as cursor:
            cursor.execute('SELECT * FROM employees WHERE email = ?', (email,))
            row = cursor.fetchone()
            return Employee.from_db_row(row) if row else None

    @staticmethod
    def get_all() -> List[Employee]:
        with DatabaseConnection.get_cursor('hr') as cursor:
            cursor.execute('SELECT * FROM employees')
            return [Employee.from_db_row(row) for row in cursor.fetchall()]

    @staticmethod
    def update_role(employee_id: int, role_id: Optional[int]) -> bool:
        with DatabaseConnection.get_cursor('hr') as cursor:
            cursor.execute(
                'UPDATE employees SET role_id = ? WHERE id = ?',
                (role_id, employee_id)
            )
            return cursor.rowcount > 0

    @staticmethod
    def update_employment_status(employee_id: int, employment_status: str) -> bool:
        with DatabaseConnection.get_cursor('hr') as cursor:
            cursor.execute(
                'UPDATE employees SET employment_status = ? WHERE id = ?',
                (employment_status, employee_id)
            )
            return cursor.rowcount > 0

    @staticmethod
    def deactivate_all_employees() -> bool:
        """Deactivate all employees in the system."""
        with DatabaseConnection.get_cursor('hr') as cursor:
            cursor.execute('UPDATE employees SET employment_status = "inactive"')
            return cursor.rowcount > 0

class PerformanceRatingRepository:
    @staticmethod
    def create(employee_id: int, rating: int, review_date: date, comments: Optional[str] = None) -> PerformanceRating:
        with DatabaseConnection.get_cursor('hr') as cursor:
            cursor.execute(
                'INSERT INTO performance_ratings (employee_id, rating, review_date, comments) VALUES (?, ?, ?, ?)',
                (employee_id, rating, review_date.isoformat(), comments)
            )
            rating_id = cursor.lastrowid
            return PerformanceRating(
                id=rating_id,
                employee_id=employee_id,
                rating=rating,
                review_date=review_date,
                comments=comments,
                created_at=None
            )

    @staticmethod
    def get_by_employee_id(employee_id: int) -> List[PerformanceRating]:
        with DatabaseConnection.get_cursor('hr') as cursor:
            cursor.execute('SELECT * FROM performance_ratings WHERE employee_id = ? ORDER BY review_date DESC', (employee_id,))
            return [PerformanceRating.from_db_row(row) for row in cursor.fetchall()]

    @staticmethod
    def get_latest_by_employee_id(employee_id: int) -> Optional[PerformanceRating]:
        with DatabaseConnection.get_cursor('hr') as cursor:
            cursor.execute(
                'SELECT * FROM performance_ratings WHERE employee_id = ? ORDER BY review_date DESC LIMIT 1',
                (employee_id,)
            )
            row = cursor.fetchone()
            return PerformanceRating.from_db_row(row) if row else None 
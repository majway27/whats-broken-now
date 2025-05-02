from datetime import date
from typing import List, Optional
from .database import get_db_connection
from .models import Role, Employee, PerformanceRating

class RoleRepository:
    @staticmethod
    def create(title: str, description: Optional[str] = None) -> Role:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO roles (title, description) VALUES (?, ?)',
            (title, description)
        )
        role_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return Role(id=role_id, title=title, description=description, created_at=None)

    @staticmethod
    def get_by_title(title: str) -> Optional[Role]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM roles WHERE title = ?', (title,))
        row = cursor.fetchone()
        conn.close()
        return Role.from_db_row(row) if row else None

    @staticmethod
    def get_by_id(role_id: int) -> Optional[Role]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM roles WHERE id = ?', (role_id,))
        row = cursor.fetchone()
        conn.close()
        return Role.from_db_row(row) if row else None

    @staticmethod
    def get_all() -> List[Role]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM roles')
        roles = [Role.from_db_row(row) for row in cursor.fetchall()]
        conn.close()
        return roles

class EmployeeRepository:
    @staticmethod
    def create(first_name: str, last_name: str, email: str, hire_date: date, role_id: Optional[int] = None, employment_status: str = 'active') -> Employee:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO employees (first_name, last_name, email, role_id, hire_date, employment_status) VALUES (?, ?, ?, ?, ?, ?)',
            (first_name, last_name, email, role_id, hire_date.isoformat(), employment_status)
        )
        employee_id = cursor.lastrowid
        conn.commit()
        conn.close()
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
    def get_by_id(employee_id: int) -> Optional[Employee]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees WHERE id = ?', (employee_id,))
        row = cursor.fetchone()
        conn.close()
        return Employee.from_db_row(row) if row else None

    @staticmethod
    def get_all() -> List[Employee]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees')
        employees = [Employee.from_db_row(row) for row in cursor.fetchall()]
        conn.close()
        return employees

    @staticmethod
    def update_role(employee_id: int, role_id: Optional[int]) -> bool:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE employees SET role_id = ? WHERE id = ?',
            (role_id, employee_id)
        )
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    @staticmethod
    def update_employment_status(employee_id: int, employment_status: str) -> bool:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE employees SET employment_status = ? WHERE id = ?',
            (employment_status, employee_id)
        )
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

class PerformanceRatingRepository:
    @staticmethod
    def create(employee_id: int, rating: int, review_date: date, comments: Optional[str] = None) -> PerformanceRating:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO performance_ratings (employee_id, rating, review_date, comments) VALUES (?, ?, ?, ?)',
            (employee_id, rating, review_date.isoformat(), comments)
        )
        rating_id = cursor.lastrowid
        conn.commit()
        conn.close()
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
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM performance_ratings WHERE employee_id = ? ORDER BY review_date DESC', (employee_id,))
        ratings = [PerformanceRating.from_db_row(row) for row in cursor.fetchall()]
        conn.close()
        return ratings

    @staticmethod
    def get_latest_by_employee_id(employee_id: int) -> Optional[PerformanceRating]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM performance_ratings WHERE employee_id = ? ORDER BY review_date DESC LIMIT 1',
            (employee_id,)
        )
        row = cursor.fetchone()
        conn.close()
        return PerformanceRating.from_db_row(row) if row else None 
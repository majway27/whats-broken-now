from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Player:
    id: Optional[int]
    first_name: str
    last_name: str
    email: str
    employee_id: Optional[int]  # Reference to HR employee record
    created_at: Optional[datetime]

    @classmethod
    def from_db_row(cls, row):
        return cls(
            id=row['id'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            email=row['email'],
            employee_id=row['employee_id'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
        )
        
    @classmethod
    def get_most_recent(cls):
        """Returns the most recent player from the repository."""
        from .repository import PlayerRepository
        players = PlayerRepository.get_all()
        return players[0] if players else None

    def get_employee_name(self) -> str:
        """Returns the full name of the employee associated with this player."""
        if not self.employee_id:
            return ""
        from human_resources.repository import EmployeeRepository
        employee = EmployeeRepository.get_by_id(self.employee_id)
        return f"{employee.first_name} {employee.last_name}" if employee else "" 
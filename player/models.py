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
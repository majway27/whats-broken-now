from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

@dataclass
class Role:
    id: Optional[int]
    title: str
    description: Optional[str]
    created_at: Optional[datetime]

    @classmethod
    def from_db_row(cls, row):
        return cls(
            id=row['id'],
            title=row['title'],
            description=row['description'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
        )

@dataclass
class Employee:
    id: Optional[int]
    first_name: str
    last_name: str
    email: str
    role_id: Optional[int]
    hire_date: date
    created_at: Optional[datetime]

    @classmethod
    def from_db_row(cls, row):
        return cls(
            id=row['id'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            email=row['email'],
            role_id=row['role_id'],
            hire_date=date.fromisoformat(row['hire_date']),
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
        )

@dataclass
class PerformanceRating:
    id: Optional[int]
    employee_id: int
    rating: int
    review_date: date
    comments: Optional[str]
    created_at: Optional[datetime]

    @classmethod
    def from_db_row(cls, row):
        return cls(
            id=row['id'],
            employee_id=row['employee_id'],
            rating=row['rating'],
            review_date=date.fromisoformat(row['review_date']),
            comments=row['comments'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
        ) 
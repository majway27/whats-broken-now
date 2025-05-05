from typing import Optional, List
from .models import Player
from shared.database import DatabaseConnection
from human_resources.repository import EmployeeRepository

# Schema for player database
PLAYER_SCHEMA = '''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        employee_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        days_survived INTEGER DEFAULT 0,
        FOREIGN KEY (employee_id) REFERENCES employees (id)
    )
'''

def init_db():
    """Initialize the player database."""
    DatabaseConnection.init_db('player', PLAYER_SCHEMA)

class PlayerRepository:
    @staticmethod
    def create(first_name: str, last_name: str, email: str, employee_id: Optional[int] = None) -> Player:
        """Create a new player record."""
        with DatabaseConnection.get_cursor('player') as cursor:
            cursor.execute(
                'INSERT INTO players (first_name, last_name, email, employee_id) VALUES (?, ?, ?, ?)',
                (first_name, last_name, email, employee_id)
            )
            player_id = cursor.lastrowid
            return Player(
                id=player_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                employee_id=employee_id,
                created_at=None
            )

    @staticmethod
    def get_by_id(player_id: int) -> Optional[Player]:
        """Get a player by their ID."""
        with DatabaseConnection.get_cursor('player') as cursor:
            cursor.execute('SELECT * FROM players WHERE id = ?', (player_id,))
            row = cursor.fetchone()
            return Player.from_db_row(row) if row else None

    @staticmethod
    def get_by_email(email: str) -> Optional[Player]:
        """Get a player by their email."""
        with DatabaseConnection.get_cursor('player') as cursor:
            cursor.execute('SELECT * FROM players WHERE email = ?', (email,))
            row = cursor.fetchone()
            return Player.from_db_row(row) if row else None

    @staticmethod
    def get_all() -> List[Player]:
        """Get all player records."""
        with DatabaseConnection.get_cursor('player') as cursor:
            cursor.execute('SELECT * FROM players ORDER BY created_at DESC')
            return [Player.from_db_row(row) for row in cursor.fetchall()]

    @staticmethod
    def exists() -> bool:
        """Check if any player records exist."""
        with DatabaseConnection.get_cursor('player') as cursor:
            cursor.execute('SELECT COUNT(*) FROM players')
            return cursor.fetchone()[0] > 0

    @staticmethod
    def update_employee_id(player_id: int, employee_id: int) -> bool:
        """Update a player's employee ID reference."""
        with DatabaseConnection.get_cursor('player') as cursor:
            cursor.execute(
                'UPDATE players SET employee_id = ? WHERE id = ?',
                (employee_id, player_id)
            )
            return cursor.rowcount > 0

    @staticmethod
    def update_days_survived(player_id: int, days: int) -> bool:
        """Update a player's days survived count."""
        with DatabaseConnection.get_cursor('player') as cursor:
            cursor.execute(
                'UPDATE players SET days_survived = ? WHERE id = ?',
                (days, player_id)
            )
            return cursor.rowcount > 0

    @staticmethod
    def get_employee_name(player_id: int) -> str:
        """Returns the full name of the employee associated with this player."""
        player = PlayerRepository.get_by_id(player_id)
        if not player or not player.employee_id:
            return ""
        employee = EmployeeRepository.get_by_id(player.employee_id)
        return f"{employee.first_name} {employee.last_name}" if employee else ""

    @staticmethod
    def get_most_recent() -> Optional[Player]:
        """Returns the most recent player from the repository."""
        players = PlayerRepository.get_all()
        return players[0] if players else None 
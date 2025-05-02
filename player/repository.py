import sqlite3
import os
from datetime import datetime
from typing import Optional, List
from .models import Player

DB_PATH = os.path.join(os.path.dirname(__file__), 'player.db')

def get_db_connection():
    """Create a database connection and return it."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the player database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create players table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            employee_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employee_id) REFERENCES employees (id)
        )
    ''')
    
    conn.commit()
    conn.close()

class PlayerRepository:
    @staticmethod
    def create(first_name: str, last_name: str, email: str, employee_id: Optional[int] = None) -> Player:
        """Create a new player record."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO players (first_name, last_name, email, employee_id) VALUES (?, ?, ?, ?)',
            (first_name, last_name, email, employee_id)
        )
        player_id = cursor.lastrowid
        conn.commit()
        conn.close()
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
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM players WHERE id = ?', (player_id,))
        row = cursor.fetchone()
        conn.close()
        return Player.from_db_row(row) if row else None

    @staticmethod
    def get_by_email(email: str) -> Optional[Player]:
        """Get a player by their email."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM players WHERE email = ?', (email,))
        row = cursor.fetchone()
        conn.close()
        return Player.from_db_row(row) if row else None

    @staticmethod
    def get_all() -> List[Player]:
        """Get all player records."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM players ORDER BY created_at DESC')
        players = [Player.from_db_row(row) for row in cursor.fetchall()]
        conn.close()
        return players

    @staticmethod
    def exists() -> bool:
        """Check if any player records exist."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM players')
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    @staticmethod
    def update_employee_id(player_id: int, employee_id: int) -> bool:
        """Update a player's employee ID reference."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE players SET employee_id = ? WHERE id = ?',
            (employee_id, player_id)
        )
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success 
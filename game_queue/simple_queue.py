import json
import time
import threading
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from shared.database import DatabaseConnection

logger = logging.getLogger(__name__)

class GameEventQueue:
    def __init__(self):
        """Initialize the game event queue with SQLite backend."""
        self._init_db()
        self._lock = threading.Lock()
        
    def _init_db(self):
        """Initialize the SQLite database with required tables."""
        schema_sql = """
            CREATE TABLE IF NOT EXISTS game_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                priority INTEGER DEFAULT 0,
                data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_at TIMESTAMP,
                status TEXT DEFAULT 'pending'
            )
        """
        DatabaseConnection.init_db('game_state', schema_sql)

    def add_event(self, event_type: str, data: Dict[str, Any], priority: int = 0) -> int:
        """Add a new game event to the queue."""
        with self._lock:
            with DatabaseConnection.get_cursor('game_state') as cursor:
                cursor.execute(
                    "INSERT INTO game_events (event_type, priority, data) VALUES (?, ?, ?)",
                    (event_type, priority, json.dumps(data))
                )
                return cursor.lastrowid

    def get_next_event(self) -> Optional[Dict[str, Any]]:
        """Get the next event to process, prioritizing by priority and creation time."""
        with self._lock:
            with DatabaseConnection.get_cursor('game_state') as cursor:
                cursor.execute("""
                    SELECT id, event_type, data, created_at 
                    FROM game_events 
                    WHERE status = 'pending'
                    ORDER BY priority DESC, created_at ASC
                    LIMIT 1
                """)
                row = cursor.fetchone()
                if row:
                    event_id, event_type, data, created_at = row
                    return {
                        'id': event_id,
                        'type': event_type,
                        'data': json.loads(data),
                        'created_at': created_at
                    }
                return None

    def mark_event_processed(self, event_id: int, success: bool = True):
        """Mark an event as processed."""
        with self._lock:
            with DatabaseConnection.get_cursor('game_state') as cursor:
                status = 'completed' if success else 'failed'
                cursor.execute(
                    "UPDATE game_events SET status = ?, processed_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (status, event_id)
                )

    def get_pending_events(self) -> List[Dict[str, Any]]:
        """Get all pending events."""
        with DatabaseConnection.get_cursor('game_state') as cursor:
            cursor.execute("""
                SELECT id, event_type, priority, data, created_at 
                FROM game_events 
                WHERE status = 'pending'
                ORDER BY priority DESC, created_at ASC
            """)
            return [{
                'id': row[0],
                'type': row[1],
                'priority': row[2],
                'data': json.loads(row[3]),
                'created_at': row[4]
            } for row in cursor.fetchall()]

    def cleanup_old_events(self, days: int = 30):
        """Clean up events older than specified days."""
        with DatabaseConnection.get_cursor('game_state') as cursor:
            cursor.execute(
                "DELETE FROM game_events WHERE created_at < datetime('now', ?)",
                (f'-{days} days',)
            ) 
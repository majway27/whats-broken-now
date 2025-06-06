import sqlite3
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, Union, Dict

# Base directory for all databases
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'databases')

# Ensure database directory exists
os.makedirs(DB_DIR, exist_ok=True)

# Database paths
DB_PATHS = {
    'tickets': os.path.join(DB_DIR, 'tickets.db'),
    'hardware': os.path.join(DB_DIR, 'hardware_catalog.db'),
    'hr': os.path.join(DB_DIR, 'hr.db'),
    'mailbox': os.path.join(DB_DIR, 'mailbox.db'),
    'calendar': os.path.join(DB_DIR, 'calendar.db'),
    'player': os.path.join(DB_DIR, 'player.db'),
    'game_state': os.path.join(DB_DIR, 'game_state.db')
}

# System tables that should not be dropped
SYSTEM_TABLES = {'sqlite_sequence', 'sqlite_master'}

class DatabaseConnection:
    """Manages database connections with proper timeout and transaction handling."""
    
    _test_db_paths: Dict[str, str] = {}
    
    @classmethod
    def set_test_db_paths(cls, paths: Dict[str, str]):
        """Set test database paths for testing.
        
        Args:
            paths: Dictionary mapping database names to their test file paths
        """
        cls._test_db_paths = paths
    
    @classmethod
    def clear_test_db_paths(cls):
        """Clear test database paths."""
        cls._test_db_paths = {}
    
    @classmethod
    def get_db_path(cls, db_name: str) -> str:
        """Get the path to a database file.
        
        Args:
            db_name: Name of the database
            
        Returns:
            Path to the database file
        """
        if db_name not in DB_PATHS:
            raise ValueError(f"Unknown database: {db_name}. Must be one of {list(DB_PATHS.keys())}")
        return cls._test_db_paths.get(db_name, DB_PATHS[db_name])
    
    @staticmethod
    @contextmanager
    def get_connection(db_name: str, timeout: float = 30.0):
        """Get a database connection with proper timeout settings.
        
        Args:
            db_name: Name of the database (must be a key in DB_PATHS)
            timeout: Connection timeout in seconds
        """
        if db_name not in DB_PATHS:
            raise ValueError(f"Unknown database: {db_name}. Must be one of {list(DB_PATHS.keys())}")
            
        conn = sqlite3.connect(DatabaseConnection.get_db_path(db_name), timeout=timeout)
        # Set row factory to return rows as dictionaries
        conn.row_factory = sqlite3.Row
        try:
            # Enable foreign keys
            conn.execute("PRAGMA foreign_keys = ON")
            # Set busy timeout
            conn.execute(f"PRAGMA busy_timeout = {int(timeout * 1000)}")
            yield conn
        finally:
            conn.close()

    @staticmethod
    @contextmanager
    def get_cursor(db_name: str, timeout: float = 30.0):
        """Get a database cursor with proper timeout settings.
        
        Args:
            db_name: Name of the database (must be a key in DB_PATHS)
            timeout: Connection timeout in seconds
        """
        with DatabaseConnection.get_connection(db_name, timeout) as conn:
            cursor = conn.cursor()
            try:
                yield cursor
                conn.commit()
            except Exception:
                conn.rollback()
                raise

    @staticmethod
    def init_db(db_name: str, schema_sql: str):
        """Initialize a database with the given schema.
        
        Args:
            db_name: Name of the database to initialize
            schema_sql: SQL schema to execute
        """
        with DatabaseConnection.get_cursor(db_name) as cursor:
            cursor.executescript(schema_sql)

    @staticmethod
    def reset_db(db_name: str, schema_sql: str):
        """Reset a database by dropping all tables and reinitializing.
        
        Args:
            db_name: Name of the database to reset
            schema_sql: SQL schema to execute after reset
        """
        with DatabaseConnection.get_cursor(db_name) as cursor:
            # Temporarily disable foreign key constraints
            cursor.execute("PRAGMA foreign_keys = OFF")
            
            # Get list of tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall() if row[0] not in SYSTEM_TABLES]
            
            # Drop all tables
            for table in tables:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
            
            # Re-enable foreign key constraints
            cursor.execute("PRAGMA foreign_keys = ON")
            
            # Reinitialize with schema
            cursor.executescript(schema_sql) 
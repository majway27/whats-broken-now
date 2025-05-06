import os
import tempfile
import pytest
from shared.database import DatabaseConnection, DB_PATHS

# Test schema for creating test tables
TEST_SCHEMA = """
CREATE TABLE test_table (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE related_table (
    id INTEGER PRIMARY KEY,
    test_id INTEGER,
    FOREIGN KEY (test_id) REFERENCES test_table(id)
);
"""

@pytest.fixture
def temp_db_dir():
    """Create a temporary directory for test databases."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test database paths
        test_db_paths = {
            'tickets': os.path.join(temp_dir, 'tickets.db'),
            'hardware': os.path.join(temp_dir, 'hardware_catalog.db'),
            'hr': os.path.join(temp_dir, 'hr.db'),
            'mailbox': os.path.join(temp_dir, 'mailbox.db'),
            'calendar': os.path.join(temp_dir, 'calendar.db'),
            'player': os.path.join(temp_dir, 'player.db'),
            'game_state': os.path.join(temp_dir, 'game_state.db')
        }
        DatabaseConnection.set_test_db_paths(test_db_paths)
        yield temp_dir
        DatabaseConnection.clear_test_db_paths()

def test_get_db_path(temp_db_dir):
    """Test getting database paths."""
    # Test valid database name
    assert DatabaseConnection.get_db_path('tickets') == os.path.join(temp_db_dir, 'tickets.db')
    
    # Test invalid database name
    with pytest.raises(ValueError):
        DatabaseConnection.get_db_path('invalid_db')

def test_database_connection(temp_db_dir):
    """Test basic database connection functionality."""
    db_name = 'tickets'
    
    # Test connection creation and basic operations
    with DatabaseConnection.get_connection(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY)")
        cursor.execute("INSERT INTO test VALUES (1)")
        conn.commit()
        
        cursor.execute("SELECT * FROM test")
        result = cursor.fetchone()
        assert result[0] == 1

def test_database_cursor(temp_db_dir):
    """Test cursor functionality with automatic commit/rollback."""
    db_name = 'tickets'
    
    # Test successful transaction
    with DatabaseConnection.get_cursor(db_name) as cursor:
        cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY)")
        cursor.execute("INSERT INTO test VALUES (1)")
    
    # Verify the transaction was committed
    with DatabaseConnection.get_connection(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test")
        result = cursor.fetchone()
        assert result[0] == 1
    
    # Test failed transaction (should rollback)
    with pytest.raises(Exception):
        with DatabaseConnection.get_cursor(db_name) as cursor:
            cursor.execute("INSERT INTO test VALUES (2)")
            cursor.execute("INSERT INTO nonexistent_table VALUES (3)")  # This will fail
    
    # Verify the failed transaction was rolled back
    with DatabaseConnection.get_connection(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM test")
        count = cursor.fetchone()[0]
        assert count == 1  # Only the first insert should be present

def test_init_db(temp_db_dir):
    """Test database initialization."""
    db_name = 'tickets'
    
    # Initialize database with schema
    DatabaseConnection.init_db(db_name, TEST_SCHEMA)
    
    # Verify tables were created
    with DatabaseConnection.get_connection(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        assert 'test_table' in tables
        assert 'related_table' in tables

def test_reset_db(temp_db_dir):
    """Test database reset functionality."""
    db_name = 'tickets'
    
    # Initialize database first
    DatabaseConnection.init_db(db_name, TEST_SCHEMA)
    
    # Add some data
    with DatabaseConnection.get_cursor(db_name) as cursor:
        cursor.execute("INSERT INTO test_table (name) VALUES ('test1')")
        cursor.execute("INSERT INTO test_table (name) VALUES ('test2')")
    
    # Reset database
    DatabaseConnection.reset_db(db_name, TEST_SCHEMA)
    
    # Verify tables were recreated and data was cleared
    with DatabaseConnection.get_connection(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM test_table")
        count = cursor.fetchone()[0]
        assert count == 0  # Data should be cleared
        
        # Verify tables still exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        assert 'test_table' in tables
        assert 'related_table' in tables

def test_foreign_key_constraints(temp_db_dir):
    """Test foreign key constraint enforcement."""
    db_name = 'tickets'
    
    # Initialize database with schema that includes foreign key
    DatabaseConnection.init_db(db_name, TEST_SCHEMA)
    
    # Test foreign key constraint
    with DatabaseConnection.get_cursor(db_name) as cursor:
        # This should fail because test_id 1 doesn't exist in test_table
        with pytest.raises(Exception):
            cursor.execute("INSERT INTO related_table (test_id) VALUES (1)")
        
        # This should succeed
        cursor.execute("INSERT INTO test_table (name) VALUES ('test1')")
        cursor.execute("INSERT INTO related_table (test_id) VALUES (1)") 
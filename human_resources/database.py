from shared.database import DatabaseConnection

# Schema for HR database
HR_SCHEMA = '''
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role_id INTEGER,
    hire_date DATE NOT NULL,
    employment_status TEXT NOT NULL DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles (id)
);

CREATE TABLE IF NOT EXISTS performance_ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_date DATE NOT NULL,
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees (id)
);
'''

def init_db():
    """Initialize the HR database with required tables."""
    DatabaseConnection.init_db('hr', HR_SCHEMA)

def reset_db():
    """Reset the HR database by dropping all tables and reinitializing."""
    DatabaseConnection.reset_db('hr', HR_SCHEMA)

def get_db_connection():
    """Get a database connection with proper settings."""
    return DatabaseConnection.get_connection('hr') 
import sqlite3
import os
from datetime import datetime
from human_resources.database import get_db_connection as get_hr_db_connection

DB_PATH = os.path.join(os.path.dirname(__file__), 'mailbox.db')
HR_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'human_resources', 'hr.db')

def init_db():
    """Initialize the mailbox database."""
    # First ensure HR database exists and has data
    hr_conn = get_hr_db_connection()
    hr_cursor = hr_conn.cursor()
    
    # Check if employees table exists and has data
    hr_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employees'")
    if not hr_cursor.fetchone():
        hr_conn.close()
        raise Exception("HR database not initialized. Please run the game setup first.")
    
    hr_cursor.execute("SELECT COUNT(*) FROM employees")
    if hr_cursor.fetchone()[0] == 0:
        hr_conn.close()
        raise Exception("No employees found in HR database. Please run the game setup first.")
    
    hr_conn.close()
    
    # Now initialize mailbox database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create messages table with foreign key to employees
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            recipient_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            is_read BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY (sender_id) REFERENCES employees(id),
            FOREIGN KEY (recipient_id) REFERENCES employees(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_message(sender_id, recipient_id, subject, content):
    """Add a new message to the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO messages (sender_id, recipient_id, subject, content, timestamp, is_read)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (sender_id, recipient_id, subject, content, datetime.now(), False))
        conn.commit()

def get_messages(recipient_id):
    """Get all messages for a recipient."""    
    # Get messages from mailbox database
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, sender_id, subject, content, timestamp, is_read
            FROM messages
            WHERE recipient_id = ?
            ORDER BY timestamp DESC
        ''', (recipient_id,))
        messages = cursor.fetchall()
    
    # Get employee names from HR database
    with sqlite3.connect(HR_DB_PATH) as hr_conn:
        hr_cursor = hr_conn.cursor()
        # Create a mapping of employee IDs to their full names
        employee_names = {}
        for msg in messages:
            sender_id = msg[1]  # sender_id is the second column
            if sender_id not in employee_names:
                hr_cursor.execute('''
                    SELECT first_name || ' ' || last_name
                    FROM employees
                    WHERE id = ?
                ''', (sender_id,))
                result = hr_cursor.fetchone()
                employee_names[sender_id] = result[0] if result else "Unknown Sender"
    
    # Combine the data
    formatted_messages = []
    for msg in messages:
        msg_id, sender_id, subject, content, timestamp, is_read = msg
        sender_name = employee_names.get(sender_id, "Unknown Sender")
        formatted_messages.append((msg_id, sender_name, subject, content, timestamp, is_read))
    
    return formatted_messages

def mark_as_read(message_id):
    """Mark a message as read."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE messages
            SET is_read = 1
            WHERE id = ?
        ''', (message_id,))
        conn.commit()

def get_unread_count(recipient_id):
    """Get the count of unread messages for a recipient."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*)
            FROM messages
            WHERE recipient_id = ? AND is_read = 0
        ''', (recipient_id,))
        return cursor.fetchone()[0]

def delete_message(message_id):
    """Delete a message from the database.
    Returns True if message was deleted, False if message didn't exist."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            # First check if message exists
            cursor.execute('SELECT id FROM messages WHERE id = ?', (message_id,))
            if not cursor.fetchone():
                return False
            
            # Delete the message
            cursor.execute('DELETE FROM messages WHERE id = ?', (message_id,))
            
            # Verify the deletion
            cursor.execute('SELECT id FROM messages WHERE id = ?', (message_id,))
            if cursor.fetchone():
                # If we can still find the message, something went wrong
                conn.rollback()
                return False
                
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False 
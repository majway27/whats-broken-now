import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'mailbox.db')
HR_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'human_resources', 'hr.db')

def init_db():
    """Initialize the mailbox database."""
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
            FOREIGN KEY (sender_id) REFERENCES employee(id),
            FOREIGN KEY (recipient_id) REFERENCES employee(id)
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
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT m.id, e.first_name || ' ' || e.last_name as sender_name, 
                   m.subject, m.content, m.timestamp, m.is_read
            FROM messages m
            JOIN employee e ON m.sender_id = e.id
            WHERE m.recipient_id = ?
            ORDER BY m.timestamp DESC
        ''', (recipient_id,))
        return cursor.fetchall()

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
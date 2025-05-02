import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'mailbox.db')

def init_db():
    """Initialize the mailbox database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            recipient TEXT NOT NULL,
            subject TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            is_read BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()

def add_message(sender, recipient, subject, content):
    """Add a new message to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO messages (sender, recipient, subject, content, timestamp, is_read)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (sender, recipient, subject, content, datetime.now(), False))
    
    conn.commit()
    conn.close()

def get_messages(recipient):
    """Get all messages for a recipient."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, sender, subject, content, timestamp, is_read
        FROM messages
        WHERE recipient = ?
        ORDER BY timestamp DESC
    ''', (recipient,))
    
    messages = cursor.fetchall()
    conn.close()
    return messages

def mark_as_read(message_id):
    """Mark a message as read."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE messages
        SET is_read = 1
        WHERE id = ?
    ''', (message_id,))
    
    conn.commit()
    conn.close()

def get_unread_count(recipient):
    """Get the count of unread messages for a recipient."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT COUNT(*)
        FROM messages
        WHERE recipient = ? AND is_read = 0
    ''', (recipient,))
    
    count = cursor.fetchone()[0]
    conn.close()
    return count

def delete_message(message_id):
    """Delete a message from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM messages WHERE id = ?', (message_id,))
    
    conn.commit()
    conn.close() 
from datetime import datetime
from shared.database import DatabaseConnection

# Schema for mailbox database
MAILBOX_SCHEMA = '''
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
'''

def init_db():
    """Initialize the mailbox database."""
    # Initialize mailbox database with schema
    DatabaseConnection.init_db('mailbox', MAILBOX_SCHEMA)

def add_message(sender_id, recipient_id, subject, content):
    """Add a new message to the database."""
    with DatabaseConnection.get_cursor('mailbox') as cursor:
        cursor.execute('''
            INSERT INTO messages (sender_id, recipient_id, subject, content, timestamp, is_read)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (sender_id, recipient_id, subject, content, datetime.now(), False))

def get_messages(recipient_id):
    """Get all messages for a recipient."""    
    # Get messages from mailbox database
    with DatabaseConnection.get_cursor('mailbox') as cursor:
        cursor.execute('''
            SELECT id, sender_id, subject, content, timestamp, is_read
            FROM messages
            WHERE recipient_id = ?
            ORDER BY timestamp DESC
        ''', (recipient_id,))
        messages = cursor.fetchall()
    
    # Get employee names from HR database
    with DatabaseConnection.get_cursor('hr') as hr_cursor:
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
    with DatabaseConnection.get_cursor('mailbox') as cursor:
        cursor.execute('''
            UPDATE messages
            SET is_read = 1
            WHERE id = ?
        ''', (message_id,))

def get_unread_count(recipient_id):
    """Get the count of unread messages for a recipient."""
    with DatabaseConnection.get_cursor('mailbox') as cursor:
        cursor.execute('''
            SELECT COUNT(*)
            FROM messages
            WHERE recipient_id = ? AND is_read = 0
        ''', (recipient_id,))
        return cursor.fetchone()[0]

def delete_message(message_id):
    """Delete a message from the database.
    Returns True if message was deleted, False if message didn't exist."""
    with DatabaseConnection.get_cursor('mailbox') as cursor:
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
            return False
            
        return True 
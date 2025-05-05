import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional
from human_resources.database import get_db_connection as get_hr_db_connection
from human_resources.utils import get_current_employee
from shared.database import DatabaseConnection

# Schema for calendar database
CALENDAR_SCHEMA = '''
    CREATE TABLE IF NOT EXISTS game_days (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day_number INTEGER UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS current_game_day (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        game_day_id INTEGER NOT NULL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (game_day_id) REFERENCES game_days (id)
    );

    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_day_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (game_day_id) REFERENCES game_days (id)
    );

    CREATE TABLE IF NOT EXISTS meeting_attendees (
        meeting_id INTEGER NOT NULL,
        employee_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (meeting_id, employee_id),
        FOREIGN KEY (meeting_id) REFERENCES schedule (id) ON DELETE CASCADE
    );
'''

def init_db():
    """Initialize the calendar database."""
    DatabaseConnection.init_db('calendar', CALENDAR_SCHEMA)
    
    # Initialize current_game_day if empty
    with DatabaseConnection.get_cursor('calendar') as cursor:
        cursor.execute('SELECT COUNT(*) FROM current_game_day')
        if cursor.fetchone()[0] == 0:
            # Insert day 1 into game_days if it doesn't exist
            cursor.execute('INSERT OR IGNORE INTO game_days (day_number) VALUES (1)')
            # Get the id of day 1
            cursor.execute('SELECT id FROM game_days WHERE day_number = 1')
            day1_id = cursor.fetchone()[0]
            # Set it as current day
            cursor.execute('INSERT INTO current_game_day (id, game_day_id) VALUES (1, ?)', (day1_id,))

def reset_game_days():
    """Reset the game days to day 1."""
    with DatabaseConnection.get_cursor('calendar') as cursor:
        # Clear existing game days and related data
        cursor.execute('DELETE FROM meeting_attendees')
        cursor.execute('DELETE FROM schedule')
        cursor.execute('DELETE FROM game_days')
        
        # Insert day 1
        cursor.execute('INSERT INTO game_days (day_number) VALUES (1)')
        day1_id = cursor.lastrowid
        
        # Reset current game day to day 1
        cursor.execute('DELETE FROM current_game_day')
        cursor.execute('INSERT INTO current_game_day (id, game_day_id) VALUES (1, ?)', (day1_id,))

def get_current_game_day() -> int:
    """Get the current game day number."""
    with DatabaseConnection.get_cursor('calendar') as cursor:
        cursor.execute('''
            SELECT g.day_number 
            FROM current_game_day c
            JOIN game_days g ON c.game_day_id = g.id
        ''')
        return cursor.fetchone()[0]

def advance_game_day() -> int:
    """Advance the game day by one and return the new day number."""
    with DatabaseConnection.get_cursor('calendar') as cursor:
        current_day = get_current_game_day()
        new_day = current_day + 1
        
        try:
            # Try to insert the new day
            cursor.execute('INSERT INTO game_days (day_number) VALUES (?)', (new_day,))
            new_day_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # If the day already exists, get its id
            cursor.execute('SELECT id FROM game_days WHERE day_number = ?', (new_day,))
            new_day_id = cursor.fetchone()[0]
        
        # Update current_game_day to point to the new day
        cursor.execute('UPDATE current_game_day SET game_day_id = ?, updated_at = CURRENT_TIMESTAMP', (new_day_id,))
        
        return new_day

def is_valid_scheduling_day(game_day: int) -> bool:
    """Check if the given game day is valid for scheduling meetings."""
    current_day = get_current_game_day()
    return game_day > current_day

def add_meeting(title: str, description: str, start_time: str, end_time: str, employee_ids: List[int], game_day: Optional[int] = None) -> bool:
    """Add a new meeting to the schedule with attendees."""
    if game_day is None:
        game_day = get_current_game_day() + 1
        
    if not is_valid_scheduling_day(game_day):
        return False
    
    # Validate that all employees are active and not the current player
    current_employee = get_current_employee()
    current_employee_id = current_employee.id if current_employee else None
    
    if current_employee_id and current_employee_id in employee_ids:
        return False
    
    # Check if all employees are active
    with DatabaseConnection.get_cursor('hr') as cursor:
        placeholders = ','.join('?' * len(employee_ids))
        cursor.execute(f'''
            SELECT id 
            FROM employees 
            WHERE id IN ({placeholders}) AND employment_status = 'active'
        ''', employee_ids)
        
        active_employee_ids = [row['id'] for row in cursor.fetchall()]
    
    if len(active_employee_ids) != len(employee_ids):
        return False
        
    with DatabaseConnection.get_cursor('calendar') as cursor:
        try:
            # Get current max day
            cursor.execute('SELECT MAX(day_number) FROM game_days')
            current_max_day = cursor.fetchone()[0] or 0
            
            # If target day is beyond current max, add all missing days
            if game_day > current_max_day:
                for day in range(current_max_day + 1, game_day + 1):
                    cursor.execute('INSERT INTO game_days (day_number) VALUES (?)', (day,))
            
            # Get the game day ID for the target day
            cursor.execute('SELECT id FROM game_days WHERE day_number = ?', (game_day,))
            game_day_id = cursor.fetchone()[0]
            
            # Add meeting
            cursor.execute('''
                INSERT INTO schedule (game_day_id, title, description, start_time, end_time)
                VALUES (?, ?, ?, ?, ?)
            ''', (game_day_id, title, description, start_time, end_time))
            
            meeting_id = cursor.lastrowid
            
            # Add attendees
            for employee_id in employee_ids:
                cursor.execute('''
                    INSERT INTO meeting_attendees (meeting_id, employee_id)
                    VALUES (?, ?)
                ''', (meeting_id, employee_id))
            
            return True
        except sqlite3.Error:
            return False

def get_meetings(game_day: int) -> List[Tuple]:
    """Get all meetings for a specific game day with their attendees."""
    with DatabaseConnection.get_cursor('calendar') as cursor:
        # First get all meetings
        cursor.execute('''
            SELECT s.id, s.title, s.description, s.start_time, s.end_time
            FROM schedule s
            JOIN game_days g ON s.game_day_id = g.id
            WHERE g.day_number = ?
            ORDER BY s.start_time
        ''', (game_day,))
        
        meetings = cursor.fetchall()
        
        result = []
        for meeting in meetings:
            meeting_id = meeting[0]
            # Get attendees for this meeting
            cursor.execute('SELECT employee_id FROM meeting_attendees WHERE meeting_id = ?', (meeting_id,))
            attendee_ids = [row[0] for row in cursor.fetchall()]
            
            # Get employee names from HR database
            with DatabaseConnection.get_cursor('hr') as hr_cursor:
                placeholders = ','.join('?' * len(attendee_ids))
                hr_cursor.execute(f'''
                    SELECT id, first_name, last_name 
                    FROM employees 
                    WHERE id IN ({placeholders})
                ''', attendee_ids)
                
                attendees = [(row['id'], f"{row['first_name']} {row['last_name']}") for row in hr_cursor.fetchall()]
            
            result.append((*meeting, attendees))
        
        return result

def update_meeting(meeting_id: int, title: str, description: str, start_time: str, end_time: str, employee_ids: List[int]) -> bool:
    """Update an existing meeting."""
    with DatabaseConnection.get_cursor('calendar') as cursor:
        try:
            # Update meeting details
            cursor.execute('''
                UPDATE schedule 
                SET title = ?, description = ?, start_time = ?, end_time = ?
                WHERE id = ?
            ''', (title, description, start_time, end_time, meeting_id))
            
            # Update attendees
            cursor.execute('DELETE FROM meeting_attendees WHERE meeting_id = ?', (meeting_id,))
            for employee_id in employee_ids:
                cursor.execute('''
                    INSERT INTO meeting_attendees (meeting_id, employee_id)
                    VALUES (?, ?)
                ''', (meeting_id, employee_id))
            
            return True
        except sqlite3.Error:
            return False

def delete_meeting(meeting_id: int) -> bool:
    """Delete a meeting."""
    with DatabaseConnection.get_cursor('calendar') as cursor:
        try:
            cursor.execute('DELETE FROM schedule WHERE id = ?', (meeting_id,))
            return True
        except sqlite3.Error:
            return False

def get_meeting(meeting_id: int) -> Optional[Tuple]:
    """Get details of a specific meeting."""
    with DatabaseConnection.get_cursor('calendar') as cursor:
        # Get meeting details
        cursor.execute('''
            SELECT s.id, s.title, s.description, s.start_time, s.end_time, g.day_number
            FROM schedule s
            JOIN game_days g ON s.game_day_id = g.id
            WHERE s.id = ?
        ''', (meeting_id,))
        
        meeting = cursor.fetchone()
        if not meeting:
            return None
        
        # Get attendees
        cursor.execute('SELECT employee_id FROM meeting_attendees WHERE meeting_id = ?', (meeting_id,))
        attendee_ids = [row[0] for row in cursor.fetchall()]
        
        # Get employee names from HR database
        hr_conn = get_hr_db_connection()
        hr_cursor = hr_conn.cursor()
        
        if attendee_ids:
            placeholders = ','.join('?' * len(attendee_ids))
            hr_cursor.execute(f'''
                SELECT first_name, last_name 
                FROM employees 
                WHERE id IN ({placeholders})
                ORDER BY first_name, last_name
            ''', attendee_ids)
            attendees = [f"{row['first_name']} {row['last_name']}" for row in hr_cursor.fetchall()]
            attendee_str = ', '.join(attendees)
        else:
            attendee_str = "None"
        
        hr_conn.close()
        return meeting + (attendee_str,)

def get_available_employees() -> List[Tuple]:
    """Get list of available employees for meetings."""
    hr_conn = get_hr_db_connection()
    hr_cursor = hr_conn.cursor()
    
    hr_cursor.execute('''
        SELECT id, first_name, last_name 
        FROM employees 
        WHERE employment_status = 'active'
        ORDER BY first_name, last_name
    ''')
    
    employees = [(row['id'], f"{row['first_name']} {row['last_name']}") for row in hr_cursor.fetchall()]
    hr_conn.close()
    
    return employees 
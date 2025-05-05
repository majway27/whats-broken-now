import sqlite3
import os
from datetime import datetime
from typing import List, Tuple, Optional
from human_resources.database import get_db_connection as get_hr_db_connection
from human_resources.utils import get_current_employee

DB_PATH = os.path.join(os.path.dirname(__file__), 'calendar.db')

def init_db():
    """Initialize the calendar database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create game_days table
    c.execute('''
        CREATE TABLE IF NOT EXISTS game_days (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day_number INTEGER UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create current_game_day table
    c.execute('''
        CREATE TABLE IF NOT EXISTS current_game_day (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            game_day_id INTEGER NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (game_day_id) REFERENCES game_days (id)
        )
    ''')
    
    # Create schedule table
    c.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_day_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (game_day_id) REFERENCES game_days (id)
        )
    ''')
    
    # Create meeting_attendees junction table
    c.execute('''
        CREATE TABLE IF NOT EXISTS meeting_attendees (
            meeting_id INTEGER NOT NULL,
            employee_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (meeting_id, employee_id),
            FOREIGN KEY (meeting_id) REFERENCES schedule (id) ON DELETE CASCADE
        )
    ''')
    
    # Initialize current_game_day if empty
    c.execute('SELECT COUNT(*) FROM current_game_day')
    if c.fetchone()[0] == 0:
        # Insert day 1 into game_days if it doesn't exist
        c.execute('INSERT OR IGNORE INTO game_days (day_number) VALUES (1)')
        # Get the id of day 1
        c.execute('SELECT id FROM game_days WHERE day_number = 1')
        day1_id = c.fetchone()[0]
        # Set it as current day
        c.execute('INSERT INTO current_game_day (id, game_day_id) VALUES (1, ?)', (day1_id,))
    
    conn.commit()
    conn.close()

def reset_game_days():
    """Reset the game days to day 1."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Clear existing game days and related data
    c.execute('DELETE FROM meeting_attendees')
    c.execute('DELETE FROM schedule')
    c.execute('DELETE FROM game_days')
    
    # Insert day 1
    c.execute('INSERT INTO game_days (day_number) VALUES (1)')
    day1_id = c.lastrowid
    
    # Reset current game day to day 1
    c.execute('DELETE FROM current_game_day')
    c.execute('INSERT INTO current_game_day (id, game_day_id) VALUES (1, ?)', (day1_id,))
    
    conn.commit()
    conn.close()

def get_current_game_day() -> int:
    """Get the current game day number."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        SELECT g.day_number 
        FROM current_game_day c
        JOIN game_days g ON c.game_day_id = g.id
    ''')
    result = c.fetchone()[0]
    
    conn.close()
    return result

def advance_game_day() -> int:
    """Advance the game day by one and return the new day number."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    current_day = get_current_game_day()
    new_day = current_day + 1
    
    try:
        # Try to insert the new day
        c.execute('INSERT INTO game_days (day_number) VALUES (?)', (new_day,))
        new_day_id = c.lastrowid
    except sqlite3.IntegrityError:
        # If the day already exists, get its id
        conn.rollback()
        c.execute('SELECT id FROM game_days WHERE day_number = ?', (new_day,))
        new_day_id = c.fetchone()[0]
    
    # Update current_game_day to point to the new day
    c.execute('UPDATE current_game_day SET game_day_id = ?, updated_at = CURRENT_TIMESTAMP', (new_day_id,))
    conn.commit()
    conn.close()
    
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
    
    hr_conn = get_hr_db_connection()
    hr_cursor = hr_conn.cursor()
    
    placeholders = ','.join('?' * len(employee_ids))
    hr_cursor.execute(f'''
        SELECT id 
        FROM employees 
        WHERE id IN ({placeholders}) AND employment_status = 'active'
    ''', employee_ids)
    
    active_employee_ids = [row['id'] for row in hr_cursor.fetchall()]
    hr_conn.close()
    
    if len(active_employee_ids) != len(employee_ids):
        return False
        
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        # Get current max day
        c.execute('SELECT MAX(day_number) FROM game_days')
        current_max_day = c.fetchone()[0] or 0
        
        # If target day is beyond current max, add all missing days
        if game_day > current_max_day:
            for day in range(current_max_day + 1, game_day + 1):
                c.execute('INSERT INTO game_days (day_number) VALUES (?)', (day,))
        
        # Get the game day ID for the target day
        c.execute('SELECT id FROM game_days WHERE day_number = ?', (game_day,))
        game_day_id = c.fetchone()[0]
        
        # Add meeting
        c.execute('''
            INSERT INTO schedule (game_day_id, title, description, start_time, end_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (game_day_id, title, description, start_time, end_time))
        
        meeting_id = c.lastrowid
        
        # Add attendees
        for employee_id in employee_ids:
            c.execute('''
                INSERT INTO meeting_attendees (meeting_id, employee_id)
                VALUES (?, ?)
            ''', (meeting_id, employee_id))
        
        conn.commit()
        success = True
    except sqlite3.Error:
        success = False
    finally:
        conn.close()
    
    return success

def get_meetings(game_day: int) -> List[Tuple]:
    """Get all meetings for a specific game day with their attendees."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # First get all meetings
    c.execute('''
        SELECT s.id, s.title, s.description, s.start_time, s.end_time
        FROM schedule s
        JOIN game_days g ON s.game_day_id = g.id
        WHERE g.day_number = ?
        ORDER BY s.start_time
    ''', (game_day,))
    
    meetings = c.fetchall()
    
    # Then get attendees for each meeting
    hr_conn = get_hr_db_connection()
    hr_cursor = hr_conn.cursor()
    
    result = []
    for meeting in meetings:
        meeting_id = meeting[0]
        # Get attendees for this meeting
        c.execute('SELECT employee_id FROM meeting_attendees WHERE meeting_id = ?', (meeting_id,))
        attendee_ids = [row[0] for row in c.fetchall()]
        
        # Get employee names from HR database
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
        
        result.append(meeting + (attendee_str,))
    
    hr_conn.close()
    conn.close()
    
    return result

def update_meeting(meeting_id: int, title: str, description: str, start_time: str, end_time: str, employee_ids: List[int]) -> bool:
    """Update an existing meeting and its attendees."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        # Update meeting details
        c.execute('''
            UPDATE schedule
            SET title = ?, description = ?, start_time = ?, end_time = ?
            WHERE id = ?
        ''', (title, description, start_time, end_time, meeting_id))
        
        # Update attendees
        c.execute('DELETE FROM meeting_attendees WHERE meeting_id = ?', (meeting_id,))
        for employee_id in employee_ids:
            c.execute('''
                INSERT INTO meeting_attendees (meeting_id, employee_id)
                VALUES (?, ?)
            ''', (meeting_id, employee_id))
        
        conn.commit()
        success = True
    except sqlite3.Error:
        success = False
    finally:
        conn.close()
    
    return success

def delete_meeting(meeting_id: int) -> bool:
    """Delete a meeting and its attendees."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        # The ON DELETE CASCADE in meeting_attendees will handle removing attendees
        c.execute('DELETE FROM schedule WHERE id = ?', (meeting_id,))
        conn.commit()
        success = True
    except sqlite3.Error:
        success = False
    finally:
        conn.close()
    
    return success

def get_meeting(meeting_id: int) -> Optional[Tuple]:
    """Get a specific meeting by ID with its attendees."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get meeting details
    c.execute('''
        SELECT s.id, s.title, s.description, s.start_time, s.end_time, g.day_number
        FROM schedule s
        JOIN game_days g ON s.game_day_id = g.id
        WHERE s.id = ?
    ''', (meeting_id,))
    
    meeting = c.fetchone()
    if not meeting:
        conn.close()
        return None
    
    # Get attendees
    c.execute('SELECT employee_id FROM meeting_attendees WHERE meeting_id = ?', (meeting_id,))
    attendee_ids = [row[0] for row in c.fetchall()]
    
    # Get employee details from HR database
    hr_conn = get_hr_db_connection()
    hr_cursor = hr_conn.cursor()
    
    if attendee_ids:
        placeholders = ','.join('?' * len(attendee_ids))
        hr_cursor.execute(f'''
            SELECT id, first_name, last_name 
            FROM employees 
            WHERE id IN ({placeholders})
            ORDER BY first_name, last_name
        ''', attendee_ids)
        attendees = hr_cursor.fetchall()
        attendee_ids_str = ','.join(str(row['id']) for row in attendees)
        attendee_names_str = ','.join(f"{row['first_name']} {row['last_name']}" for row in attendees)
    else:
        attendee_ids_str = None
        attendee_names_str = None
    
    hr_conn.close()
    conn.close()
    
    return meeting + (attendee_ids_str, attendee_names_str)

def get_available_employees() -> List[Tuple]:
    """Get list of all available active employees from HR database, excluding the current player."""
    # Get current employee
    current_employee = get_current_employee()
    current_employee_id = current_employee.id if current_employee else None
    
    conn = get_hr_db_connection()
    c = conn.cursor()
    
    if current_employee_id:
        c.execute('''
            SELECT id, first_name, last_name 
            FROM employees 
            WHERE employment_status = 'active'
            AND id != ?
            ORDER BY first_name, last_name
        ''', (current_employee_id,))
    else:
        c.execute('''
            SELECT id, first_name, last_name 
            FROM employees 
            WHERE employment_status = 'active'
            ORDER BY first_name, last_name
        ''')
    
    employees = [(row['id'], f"{row['first_name']} {row['last_name']}") for row in c.fetchall()]
    conn.close()
    
    return employees 
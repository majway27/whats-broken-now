from . import models
from shared.common_ui import print_common_header
from shared.rich_ui import print_menu, print_status, print_info, print_error, clear_screen
from rich.table import Table
from rich.console import Console
from typing import List

console = Console()

def show_calendar_menu():
    """Display the calendar menu."""
    while True:
        clear_screen()
        print_common_header()
        
        current_day = models.get_current_game_day()
        
        menu_options = [
            "1. View Today's Schedule",
            "2. Add Meeting",
            "3. Edit Meeting",
            "4. Delete Meeting",
            "Q. Return to Main Menu"
        ]
        
        print_menu("Calendar", menu_options)
        choice = input("\nEnter your choice: ").upper()
        
        if choice == '1':
            view_schedule(current_day)
        elif choice == '2':
            add_meeting(current_day)
        elif choice == '3':
            edit_meeting(current_day)
        elif choice == '4':
            delete_meeting(current_day)
        elif choice == 'Q':
            clear_screen()
            break
        else:
            print_error("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def select_employees() -> List[int]:
    """Select employees for a meeting."""
    employees = models.get_available_employees()
    if not employees:
        print_error("No employees available.")
        return []
    
    table = Table(title="Select Employees")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="yellow")
    
    for emp_id, name in employees:
        table.add_row(str(emp_id), name)
    
    console.print(table)
    print("\nEnter employee IDs separated by commas (e.g., 1,2,3)")
    print("Press Enter when done, or 'c' to cancel")
    
    while True:
        choice = input("Employee IDs: ").strip()
        if choice.lower() == 'c':
            return []
        
        try:
            selected_ids = [int(id.strip()) for id in choice.split(',') if id.strip()]
            # Validate that all selected IDs exist
            valid_ids = [emp_id for emp_id, _ in employees]
            if all(id in valid_ids for id in selected_ids):
                return selected_ids
            else:
                print_error("One or more invalid employee IDs. Please try again.")
        except ValueError:
            print_error("Invalid input. Please enter numbers separated by commas.")

def view_schedule(game_day: int):
    """View the schedule for a specific game day."""
    clear_screen()
    print_common_header()
    
    meetings = models.get_meetings(game_day)
    
    if not meetings:
        print_info("Schedule", f"No meetings scheduled for Day {game_day}")
        input("\nPress Enter to continue...")
        return
    
    table = Table(title=f"Schedule for Day {game_day}")
    table.add_column("ID", style="cyan")
    table.add_column("Time", style="green")
    table.add_column("Title", style="yellow")
    table.add_column("Description", style="white")
    table.add_column("Attendees", style="magenta")
    
    for meeting in meetings:
        meeting_id, title, description, start_time, end_time, attendees = meeting
        time_slot = f"{start_time} - {end_time}"
        table.add_row(str(meeting_id), time_slot, title, description or "", attendees or "None")
    
    console.print(table)
    input("\nPress Enter to continue...")

def add_meeting(game_day: int):
    """Add a new meeting to the schedule."""
    clear_screen()
    print_common_header()
    
    if not models.is_valid_scheduling_day(game_day):
        print_error(f"Cannot schedule meetings for Day {game_day}. Meetings can only be scheduled for Day {models.get_current_game_day() + 1}.")
        input("\nPress Enter to continue...")
        return
    
    print_info("Add Meeting", f"Adding meeting for Day {game_day}")
    
    title = input("Meeting Title: ")
    description = input("Description (optional): ")
    
    while True:
        start_time = input("Start Time (HH:MM): ")
        if len(start_time) == 5 and start_time[2] == ':' and start_time[:2].isdigit() and start_time[3:].isdigit():
            break
        print_error("Invalid time format. Please use HH:MM format.")
    
    while True:
        end_time = input("End Time (HH:MM): ")
        if len(end_time) == 5 and end_time[2] == ':' and end_time[:2].isdigit() and end_time[3:].isdigit():
            break
        print_error("Invalid time format. Please use HH:MM format.")
    
    print("\nSelect meeting attendees:")
    employee_ids = select_employees()
    if not employee_ids:
        print_error("No employees selected. Meeting not created.")
        input("\nPress Enter to continue...")
        return
    
    if models.add_meeting(title, description, start_time, end_time, game_day, employee_ids):
        print_status("Success", "Meeting added successfully!")
    else:
        print_error("Failed to add meeting.")
    
    input("\nPress Enter to continue...")

def edit_meeting(game_day: int):
    """Edit an existing meeting."""
    clear_screen()
    print_common_header()
    
    meetings = models.get_meetings(game_day)
    if not meetings:
        print_info("Schedule", f"No meetings scheduled for Day {game_day}")
        input("\nPress Enter to continue...")
        return
    
    table = Table(title=f"Select Meeting to Edit (Day {game_day})")
    table.add_column("ID", style="cyan")
    table.add_column("Time", style="green")
    table.add_column("Title", style="yellow")
    table.add_column("Attendees", style="magenta")
    
    for meeting in meetings:
        meeting_id, title, _, start_time, end_time, attendees = meeting
        time_slot = f"{start_time} - {end_time}"
        table.add_row(str(meeting_id), time_slot, title, attendees or "None")
    
    console.print(table)
    
    try:
        meeting_id = int(input("\nEnter meeting ID to edit (or 0 to cancel): "))
        if meeting_id == 0:
            return
        
        meeting = models.get_meeting(meeting_id)
        if not meeting:
            print_error("Meeting not found.")
            input("\nPress Enter to continue...")
            return
        
        _, title, description, start_time, end_time, _, current_attendees = meeting
        
        print("\nEnter new values (press Enter to keep current value):")
        new_title = input(f"Title [{title}]: ") or title
        new_description = input(f"Description [{description}]: ") or description
        
        while True:
            new_start = input(f"Start Time [{start_time}]: ") or start_time
            if len(new_start) == 5 and new_start[2] == ':' and new_start[:2].isdigit() and new_start[3:].isdigit():
                break
            print_error("Invalid time format. Please use HH:MM format.")
        
        while True:
            new_end = input(f"End Time [{end_time}]: ") or end_time
            if len(new_end) == 5 and new_end[2] == ':' and new_end[:2].isdigit() and new_end[3:].isdigit():
                break
            print_error("Invalid time format. Please use HH:MM format.")
        
        print("\nCurrent attendees:", current_attendees or "None")
        print("Select new attendees:")
        new_employee_ids = select_employees()
        if not new_employee_ids:
            print_error("No employees selected. Meeting not updated.")
            input("\nPress Enter to continue...")
            return
        
        if models.update_meeting(meeting_id, new_title, new_description, new_start, new_end, new_employee_ids):
            print_status("Success", "Meeting updated successfully!")
        else:
            print_error("Failed to update meeting.")
    
    except ValueError:
        print_error("Invalid meeting ID.")
    
    input("\nPress Enter to continue...")

def delete_meeting(game_day: int):
    """Delete a meeting."""
    clear_screen()
    print_common_header()
    
    meetings = models.get_meetings(game_day)
    if not meetings:
        print_info("Schedule", f"No meetings scheduled for Day {game_day}")
        input("\nPress Enter to continue...")
        return
    
    table = Table(title=f"Select Meeting to Delete (Day {game_day})")
    table.add_column("ID", style="cyan")
    table.add_column("Time", style="green")
    table.add_column("Title", style="yellow")
    table.add_column("Attendees", style="magenta")
    
    for meeting in meetings:
        meeting_id, title, _, start_time, end_time, attendees = meeting
        time_slot = f"{start_time} - {end_time}"
        table.add_row(str(meeting_id), time_slot, title, attendees or "None")
    
    console.print(table)
    
    try:
        meeting_id = int(input("\nEnter meeting ID to delete (or 0 to cancel): "))
        if meeting_id == 0:
            return
        
        if models.delete_meeting(meeting_id):
            print_status("Success", "Meeting deleted successfully!")
        else:
            print_error("Failed to delete meeting.")
    
    except ValueError:
        print_error("Invalid meeting ID.")
    
    input("\nPress Enter to continue...") 
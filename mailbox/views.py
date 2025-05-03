from . import models
from shared.views import print_menu, clear_screen
from shared.common_ui import print_common_header
from shared.rich_ui import print_status, print_info, print_error
from datetime import datetime
from human_resources.repository import EmployeeRepository

def format_message_list(messages):
    """Format a list of messages for display."""
    formatted_messages = []
    for msg in messages:
        msg_id, sender_name, subject, _, timestamp, is_read = msg
        status = "📬" if not is_read else "📭"
        formatted_messages.append(f"{status} {msg_id}. From: {sender_name} - {subject} ({timestamp})")
    return formatted_messages

def show_mailbox_menu():
    """Display the mailbox menu."""
    while True:
        clear_screen()
        print_common_header()
        
        # Get current player's employee ID
        current_player = EmployeeRepository.get_current_player()
        if not current_player:
            print_error("No active player found.")
            input("Press Enter to continue...")
            return
        
        # Get messages for the current player
        messages = models.get_messages(current_player.id)
        
        menu_options = [
            "1. View Messages",
            "2. Send Message",
            "3. Delete Message",
            "Q. Return to Main Menu"
        ]
        
        print_menu("Mailbox", menu_options)
        choice = input("\nEnter your choice: ").upper()
        
        if choice == '1':
            view_messages(current_player.id)
        elif choice == '2':
            send_message(current_player.id)
        elif choice == '3':
            delete_message()
        elif choice.upper() == 'Q':
            clear_screen()
            break
        else:
            print_error("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def view_messages(player_id):
    """View all messages."""
    clear_screen()
    print_common_header()
    
    messages = models.get_messages(player_id)
    if not messages:
        print_info("No Messages", "Your mailbox is empty.")
        input("\nPress Enter to continue...")
        return
    
    formatted_messages = format_message_list(messages)
    print_menu("Your Messages", formatted_messages)
    
    choice = input("\nEnter message number to read (or Q to return): ")
    if choice.upper() == 'Q':
        return
    
    try:
        msg_id = int(choice)
        view_message(msg_id)
    except ValueError:
        print_error("Invalid message number.")
        input("Press Enter to continue...")

def view_message(msg_id):
    """View a specific message."""
    clear_screen()
    print_common_header()
    
    current_player = EmployeeRepository.get_current_player()
    if not current_player:
        print_error("No active player found.")
        input("Press Enter to continue...")
        return
    
    messages = models.get_messages(current_player.id)
    message = next((msg for msg in messages if msg[0] == msg_id), None)
    
    if not message:
        print_error("Message not found.")
        input("Press Enter to continue...")
        return
    
    _, sender_name, subject, content, timestamp, _ = message
    models.mark_as_read(msg_id)
    
    print_info("Message Details", f"""
        From: {sender_name}
        Subject: {subject}
        Date: {timestamp}

        {content}
    """)
    
    input("\nPress Enter to continue...")

def select_recipient():
    """Display a list of employees and allow selection of a recipient."""
    employees = EmployeeRepository.get_all()
    if not employees:
        print_error("No employees found in the system.")
        return None
    
    print("\nSelect a recipient:")
    for i, emp in enumerate(employees, 1):
        print(f"{i}. {emp.first_name} {emp.last_name}")
    
    while True:
        try:
            choice = input("\nEnter recipient number (or Q to return): ")
            if choice.upper() == 'Q':
                return None
            
            index = int(choice) - 1
            if 0 <= index < len(employees):
                return employees[index].id
            else:
                print_error("Invalid selection. Please try again.")
        except ValueError:
            print_error("Please enter a valid number.")

def send_message(sender_id):
    """Send a new message."""
    clear_screen()
    print_common_header()
    
    print_info("Send Message", "Enter message details:")
    recipient_id = select_recipient()
    if not recipient_id:
        return
    
    subject = input("Subject: ")
    
    print("\nEnter your message (press Enter twice to finish):")
    content_lines = []
    while True:
        line = input()
        if not line and content_lines and not content_lines[-1]:
            break
        content_lines.append(line)
    
    content = "\n".join(content_lines[:-1])  # Remove the last empty line
    
    if recipient_id and subject and content:
        models.add_message(sender_id, recipient_id, subject, content)
        print_status("Message Status", "Message sent successfully!")
    else:
        print_error("Message not sent. All fields are required.")
    
    input("\nPress Enter to continue...")

def delete_message():
    """Delete a message."""
    clear_screen()
    print_common_header()
    
    current_player = EmployeeRepository.get_current_player()
    if not current_player:
        print_error("No active player found.")
        input("Press Enter to continue...")
        return
    
    messages = models.get_messages(current_player.id)
    if not messages:
        print_info("No Messages", "Your mailbox is empty.")
        input("\nPress Enter to continue...")
        return
    
    formatted_messages = format_message_list(messages)
    print_menu("Delete Message", formatted_messages)
    
    choice = input("\nEnter message number to delete (or Q to return): ")
    if choice.upper() == 'Q':
        return
    
    try:
        msg_id = int(choice)
        result = models.delete_message(msg_id)
        if result is True:
            print_status("Message Status", "Message deleted successfully!")
        elif result is False:
            print_error("Failed to delete message. It may not exist or there was a database error.")
        else:
            print_error("An unexpected error occurred while deleting the message.")
    except ValueError:
        print_error("Invalid message number.")
    
    input("Press Enter to continue...") 
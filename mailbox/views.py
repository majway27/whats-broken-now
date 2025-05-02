from . import models
from shared import views as shared_views
from shared.rich_ui import print_menu, print_status, print_info, print_error, clear_screen
from datetime import datetime

def format_message_list(messages):
    """Format a list of messages for display."""
    formatted_messages = []
    for msg in messages:
        msg_id, sender, subject, _, timestamp, is_read = msg
        status = "📬" if not is_read else "📭"
        formatted_messages.append(f"{status} {msg_id}. From: {sender} - {subject} ({timestamp})")
    return formatted_messages

def show_mailbox_menu():
    """Display the mailbox menu."""
    while True:
        clear_screen()
        shared_views.print_common_header()
        
        # Get messages for the current user (using a default user for now)
        messages = models.get_messages("player")
        
        menu_options = [
            "1. View Messages",
            "2. Send Message",
            "3. Delete Message",
            "Q. Return to Main Menu"
        ]
        
        print_menu("Mailbox", menu_options)
        choice = input("\nEnter your choice: ").upper()
        
        if choice == '1':
            view_messages()
        elif choice == '2':
            send_message()
        elif choice == '3':
            delete_message()
        elif choice.upper() == 'Q':
            break
        else:
            print_error("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def view_messages():
    """View all messages."""
    clear_screen()
    shared_views.print_common_header()
    
    messages = models.get_messages("player")
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
    shared_views.print_common_header()
    
    messages = models.get_messages("player")
    message = next((msg for msg in messages if msg[0] == msg_id), None)
    
    if not message:
        print_error("Message not found.")
        input("Press Enter to continue...")
        return
    
    _, sender, subject, content, timestamp, _ = message
    models.mark_as_read(msg_id)
    
    print_info("Message Details", f"""
From: {sender}
Subject: {subject}
Date: {timestamp}

{content}
    """)
    
    input("\nPress Enter to continue...")

def send_message():
    """Send a new message."""
    clear_screen()
    shared_views.print_common_header()
    
    print_info("Send Message", "Enter message details:")
    recipient = input("To: ")
    subject = input("Subject: ")
    
    print("\nEnter your message (press Enter twice to finish):")
    content_lines = []
    while True:
        line = input()
        if not line and content_lines and not content_lines[-1]:
            break
        content_lines.append(line)
    
    content = "\n".join(content_lines[:-1])  # Remove the last empty line
    
    if recipient and subject and content:
        models.add_message("player", recipient, subject, content)
        print_status("Message sent successfully!")
    else:
        print_error("Message not sent. All fields are required.")
    
    input("\nPress Enter to continue...")

def delete_message():
    """Delete a message."""
    clear_screen()
    shared_views.print_common_header()
    
    messages = models.get_messages("player")
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
        models.delete_message(msg_id)
        print_status("Message deleted successfully!")
    except ValueError:
        print_error("Invalid message number.")
    
    input("Press Enter to continue...") 
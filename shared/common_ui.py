from .rich_ui import print_game_header
from player.repository import PlayerRepository
from human_resources.repository import EmployeeRepository
from player.models import Player

def print_common_header():
    """Print the common game header with current status."""
    from tickets import models as ticket_models
    from mailbox import models as mailbox_models
    from game_calendar import models as calendar_models
    
    # Get current player info
    current_player = Player.get_most_recent()
    employee_name = current_player.get_employee_name() if current_player else ""
    
    # Get active ticket count
    active_tickets = len(ticket_models.get_active_tickets())
    
    # Get mailbox message count
    mailbox_messages = mailbox_models.get_unread_count(current_player.employee_id) if current_player and current_player.employee_id else 0
    
    # TODO: Get player level from player module
    player_level = 1  # Placeholder until player module is implemented
    
    # Get game day from calendar module
    game_day = calendar_models.get_current_game_day()
    
    # Get meetings count for today
    meetings = calendar_models.get_meetings(game_day)
    meetings_count = len(meetings)
        
    # Print the game header
    print_game_header(active_tickets, mailbox_messages, game_day, player_level, meetings_count, employee_name) 
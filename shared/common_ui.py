from .rich_ui import print_game_header
from player.repository import PlayerRepository
from human_resources.repository import EmployeeRepository

def print_common_header():
    """Print the common game header with current status."""
    from tickets import models as ticket_models
    from mailbox import models as mailbox_models
    from game_calendar import models as calendar_models
    # Get active ticket count
    active_tickets = len(ticket_models.get_active_tickets())
    
    # Get mailbox message count
    mailbox_messages = mailbox_models.get_unread_count("player")
    
    # TODO: Get player level from player module
    player_level = 1  # Placeholder until player module is implemented
    
    # Get game day from calendar module
    game_day = calendar_models.get_current_game_day()
    
    # Get meetings count for today
    meetings = calendar_models.get_meetings(game_day)
    meetings_count = len(meetings)
    
    # Get current player's name
    players = PlayerRepository.get_all()
    employee_name = ""
    if players:
        current_player = players[0]  # Get the most recent player
        if current_player.employee_id:
            employee = EmployeeRepository.get_by_id(current_player.employee_id)
            if employee:
                employee_name = f"{employee.first_name} {employee.last_name}"
    
    # Print the game header
    print_game_header(active_tickets, mailbox_messages, game_day, player_level, meetings_count, employee_name) 
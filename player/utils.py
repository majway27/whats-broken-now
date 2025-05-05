from .models import Player
from .views import handle_first_time_setup
from human_resources.repository import EmployeeRepository
from game_calendar.models import get_current_game_day
from .repository import PlayerRepository

def validate_player_setup() -> bool:
    """
    Validates the current player setup and handles first-time setup if needed.
    Returns True if setup is valid or first-time setup was successful, False otherwise.
    """
    players = PlayerRepository.get_all()
    if not players:
        return handle_first_time_setup()
        
    # Get current player info
    current_player = PlayerRepository.get_most_recent()
    if current_player and current_player.employee_id:
        employee = EmployeeRepository.get_by_id(current_player.employee_id)
        if not employee or employee.employment_status != 'active':
            return handle_first_time_setup()
        
        # Update days survived based on current game day
        current_day = get_current_game_day()
        if current_day > current_player.days_survived:
            PlayerRepository.update_days_survived(current_player.id, current_day)
            
    return True

def validate_current_player() -> tuple[bool, Player | None]:
    """
    Validates that there is a current player with an associated employee record.
    Returns a tuple of (is_valid, current_player).
    """
    current_player = PlayerRepository.get_most_recent()
    if not current_player:
        return False, None
    if not current_player.employee_id:
        return False, current_player
    return True, current_player 
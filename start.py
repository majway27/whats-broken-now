from admin import views as admin_views
from hardware import models as hardware_models, utils as hardware_utils
from shared import views as shared_views, utils as shared_utils
from tickets import models as ticket_models, views as ticket_views
from game_queue.start import init_queue, cleanup_queue
from agent.role_agents import init_role_agents, cleanup_role_agents
from agent.hr_agent import init_hr_agent, cleanup_hr_agent
from mailbox import models as mailbox_models, views as mailbox_views
from human_resources import database as hr_database, utils as hr_utils
from game_calendar import models as calendar_models
from player.repository import init_db as init_player_db
from player.views import handle_first_time_setup
from human_resources.repository import EmployeeRepository


def main():
    first_time_setup = False
    
    # Initialize databases
    hardware_models.init_db()  # Initialize hardware catalog database  
    if first_time_setup:
        hardware_utils.migrate_hardware_catalog()  # Populate hardware catalog database
    
    ticket_models.init_db()  # Initialize tickets database
    mailbox_models.init_db()  # Initialize mailbox database
    
    hr_database.init_db()  # Initialize human resources database
    if first_time_setup:
        hr_utils.migrate_employee_directory()  # Populate human resources database
    
    calendar_models.init_db()  # Initialize calendar database
    init_player_db()  # Initialize player database
    
    # Check if this is the first time running the game or if player is inactive
    from player.repository import PlayerRepository
    
    players = PlayerRepository.get_all()
    if not players:
        if not handle_first_time_setup():
            print("\nSetup failed. Please try again.")
            return
    else:
        # Check if the player's employee record is active
        current_player = players[0]  # Get the most recent player
        if current_player.employee_id:
            employee = EmployeeRepository.get_by_id(current_player.employee_id)
            if not employee or employee.employment_status != 'active':
                if not handle_first_time_setup():
                    print("\nSetup failed. Please try again.")
                    return
    
    # Initialize queue system
    queue_manager = init_queue()
    
    # Initialize role agents
    #role_agent_manager = init_role_agents()
    
    # Initialize HR agent
    hr_agent = init_hr_agent()
    
    try:
        while True:
            if shared_views.show_main_menu():
                break
    except KeyboardInterrupt:
        print("\n\nExiting program...")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        input("Press Enter to continue...")
    finally:
        # Clean up queue system
        cleanup_queue()
        # Clean up role agents
        #cleanup_role_agents()
        # Clean up HR agent
        cleanup_hr_agent(hr_agent)

if __name__ == "__main__":
    main() 
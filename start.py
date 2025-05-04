import os

from hardware import models as hardware_models, utils as hardware_utils
from shared import views as shared_views
from tickets import models as ticket_models
from mailbox import models as mailbox_models
from human_resources import database as hr_database, utils as hr_utils
from game_calendar import models as calendar_models

from player.repository import init_db as init_player_db
from player.utils import validate_player_setup

from game_queue.start import init_queue, cleanup_queue
from agent.hr.hr_agent import HRAgent
from agent.customer import CustomerAgent

from rich.console import Console


def init_hr_agent():
    """Initialize and start the HR agent."""
    try:
        # Ensure the config directory exists
        config_dir = os.path.join('agent', 'hr', 'config')
        os.makedirs(config_dir, exist_ok=True)
        
        # Initialize the HR agent with the new architecture
        agent = HRAgent()
        agent.initialize()
        agent.start()
        return agent
    except Exception as e:
        print(f"Error initializing HR agent: {e}")
        return None

def init_customer_agent():
    """Initialize and start the customer agent."""
    try:
        agent = CustomerAgent()
        agent.start()
        return agent
    except Exception as e:
        print(f"Error initializing customer agent: {e}")
        return None

def cleanup_hr_agent(agent):
    """Clean up the HR agent."""
    if agent:
        try:
            agent.stop()
        except Exception as e:
            print(f"Error cleaning up HR agent: {e}")

def cleanup_customer_agent(agent):
    """Clean up the customer agent."""
    if agent:
        try:
            agent.stop()
        except Exception as e:
            print(f"Error cleaning up customer agent: {e}")

def main():
    first_time_setup = False
    
    # Initialize databases
    hardware_models.init_db()  # Initialize hardware catalog database  
    if first_time_setup:
        hardware_utils.migrate_hardware_catalog()  # Populate hardware catalog database
    
    ticket_models.init_db()  # Initialize tickets database
    
    # Initialize HR database first
    hr_database.init_db()  # Initialize human resources database
    if first_time_setup:
        hr_utils.migrate_employee_directory()  # Populate human resources database
    
    # Initialize mailbox database after HR database
    mailbox_models.init_db()  # Initialize mailbox database
    
    calendar_models.init_db()  # Initialize calendar database
    init_player_db()  # Initialize player database
    
    # Validate player setup
    if not validate_player_setup():
        print("\nSetup failed. Please try again.")
        return
    
    # Initialize queue system
    queue_manager = init_queue()
    
    # Initialize agents
    hr_agent = init_hr_agent()
    if not hr_agent:
        print("\nFailed to initialize HR agent. Continuing without HR functionality.")
    
    customer_agent = init_customer_agent()
    if not customer_agent:
        print("\nFailed to initialize customer agent. Continuing without customer functionality.")
    
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
        console = Console()
        with console.status("[bold dark_sea_green]Saving game, don't turn off your computer..", spinner="dots") as status:
            # Clean up queue system
            cleanup_queue()
            # Clean up agents
            cleanup_hr_agent(hr_agent)
            cleanup_customer_agent(customer_agent)

if __name__ == "__main__":
    main() 
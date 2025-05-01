from admin import views as admin_views
from hardware import models as hardware_models, utils as hardware_utils
from shared import views as shared_views, utils as shared_utils
from tickets import models as ticket_models, views as ticket_views
from game_queue.start import init_queue, cleanup_queue

def main():
    # Initialize databases
    ticket_models.init_db()  # Initialize tickets database
    hardware_models.init_db()  # Initialize hardware catalog database
    hardware_utils.migrate_hardware_catalog()  # Populate hardware catalog database
    
    # Initialize queue system
    queue_manager = init_queue()
    
    try:
        while True:
            shared_views.show_main_menu()
            
            choice = input("\nEnter your choice (1-3): ")
            
            if choice == '1':
                ticket_views.tickets_management_menu()
            elif choice == '2':
                admin_views.administrator_options()
            elif choice == ('q' or 'Q'):
                print("\nLogging out... Goodbye!")
                break
            else:
                print("\nInvalid choice. Please try again.")
                input("Press Enter to continue...")
    except KeyboardInterrupt:
        print("\n\nExiting program...")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        input("Press Enter to continue...")
    finally:
        # Clean up queue system
        cleanup_queue()

if __name__ == "__main__":
    main() 
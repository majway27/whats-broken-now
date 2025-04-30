from admin import views as admin_views
from hardware import models as hardware_models, utils as hardware_utils
from shared import views as shared_views, utils as shared_utils
from tickets import models as ticket_models, views as ticket_views

def main():
    ticket_models.init_db()  # Initialize tickets database
    hardware_models.init_db()  # Initialize hardware catalog database
    hardware_utils.migrate_hardware_catalog()  # Populate hardware catalog database
    while True:
        shared_views.print_menu()
        try:
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == '1':
                ticket_views.check_new_tickets()
            elif choice == '2':
                ticket_views.work_new_ticket()
            elif choice == '3':
                admin_views.administrator_options()
            elif choice == '4':
                print("\n" + shared_utils.generate_snarky_goodbye())
                break
            else:
                print("\nInvalid choice. Please try again.")
                input("Press Enter to continue...")
        except KeyboardInterrupt:
            print("\n\nExiting program...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main() 
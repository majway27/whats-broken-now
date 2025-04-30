import menu
from admin import views as admin_views
from hardware import models as hardware_models, utils as hardware_utils
from tickets import models as ticket_models, utils as ticket_utils

def main():
    ticket_models.init_db()  # Initialize tickets database
    hardware_models.init_db()  # Initialize hardware catalog database
    hardware_utils.migrate_hardware_catalog()  # Populate hardware catalog database
    while True:
        menu.print_menu()
        try:
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == '1':
                menu.check_new_tickets()
            elif choice == '2':
                menu.work_new_ticket()
            elif choice == '3':
                admin_views.administrator_options()
            elif choice == '4':
                print("\n" + ticket_utils.generate_snarky_goodbye())
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
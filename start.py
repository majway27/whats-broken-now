import menu
from hardware.hardware_catalog import init_hardware_db, migrate_hardware_catalog
from tickets import models, utils

def main():
    models.init_db()  # Initialize tickets database
    init_hardware_db()  # Initialize hardware catalog database
    migrate_hardware_catalog()  # Populate hardware catalog database
    while True:
        menu.print_menu()
        try:
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == '1':
                menu.check_new_tickets()
            elif choice == '2':
                menu.work_new_ticket()
            elif choice == '3':
                menu.administrator_options()
            elif choice == '4':
                print("\n" + utils.generate_snarky_goodbye())
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
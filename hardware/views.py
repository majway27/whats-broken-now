from . import models
from shared import views as shared_views
from shared.rich_ui import print_info, print_error, print_table, clear_screen, print_menu

def clear_screen():
    """Clear the terminal screen."""
    shared_views.clear_screen()

def print_hardware_categories():
    """Print all hardware categories."""
    categories = models.get_hardware_categories()
    print("\n=== Hardware Categories ===")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category['name']}")
    print("=========================")
    return categories

def print_hardware_items(category_id=None):
    """Print hardware items, optionally filtered by category."""
    items = models.get_hardware_items(category_id)
    print("\n=== Hardware Items ===")
    for i, item in enumerate(items, 1):
        print(f"{i}. {item['name']} ({item['model']}) by {item['manufacturer']}")
    print("=====================")
    return items

def show_hardware_details(hardware_id):
    """Show detailed information about a hardware item."""
    items = models.get_hardware_items()
    item = next((i for i in items if i['id'] == hardware_id), None)
    
    if not item:
        print_error("Hardware item not found.")
        return
    
    clear_screen()
    
    # Format basic information
    basic_info = f"Manufacturer: {item['manufacturer']}\n"
    basic_info += f"Model: {item['model']}\n"
    basic_info += f"Release Date: {item['release_date']}\n"
    basic_info += f"Repair Difficulty: {item['repair_difficulty']}/5\n"
    if item['operating_system']:
        basic_info += f"Operating System: {item['operating_system']}"
    
    print_info(f"{item['name']} Details", basic_info)
    
    # Print specifications
    specs = models.get_hardware_specs(hardware_id)
    if specs:
        spec_rows = [[name, value] for name, value in specs.items()]
        print_table("Specifications", ["Name", "Value"], spec_rows)
    
    # Print common failures
    failures = models.get_hardware_failures(hardware_id)
    if failures:
        failure_rows = [[str(i), failure] for i, failure in enumerate(failures, 1)]
        print_table("Common Failures", ["#", "Description"], failure_rows)
    
    # Print troubleshooting procedures
    procedures = models.get_troubleshooting_procedures(hardware_id)
    if procedures:
        for procedure in procedures:
            steps = "\n".join(f"{step['number']}. {step['description']}" for step in procedure['steps'])
            print_info(procedure['name'], steps)
    
    # Print special tools
    tools = models.get_special_tools(hardware_id)
    if tools:
        tool_rows = [[str(i), tool] for i, tool in enumerate(tools, 1)]
        print_table("Special Tools Required", ["#", "Tool"], tool_rows)
    
    input("\nPress Enter to continue...")

def main_menu():
    """Show the main hardware catalog menu."""
    while True:
        clear_screen()
        print("\n=== Hardware Catalog ===")
        print("1. Browse by Category")
        print("2. View All Hardware")
        print("3. Exit")
        print("=====================")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            browse_by_category()
        elif choice == '2':
            browse_all_hardware()
        elif choice == '3':
            return
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

def browse_by_category():
    """Browse hardware items by category."""
    while True:
        clear_screen()
        categories = print_hardware_categories()
        print(f"{len(categories) + 1}. Back to Main Menu")
        print("=========================")
        
        choice = input("\nEnter category number: ")
        
        try:
            choice = int(choice)
            if choice == len(categories) + 1:
                return
            elif 1 <= choice <= len(categories):
                browse_hardware_in_category(categories[choice - 1]['id'])
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")
        except ValueError:
            print("Please enter a valid number.")
            input("Press Enter to continue...")

def browse_hardware_in_category(category_id):
    """Browse hardware items in a specific category."""
    while True:
        clear_screen()
        items = print_hardware_items(category_id)
        print(f"{len(items) + 1}. Back to Categories")
        print("=========================")
        
        choice = input("\nEnter hardware item number: ")
        
        try:
            choice = int(choice)
            if choice == len(items) + 1:
                return
            elif 1 <= choice <= len(items):
                show_hardware_details(items[choice - 1]['id'])
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")
        except ValueError:
            print("Please enter a valid number.")
            input("Press Enter to continue...")

def browse_all_hardware():
    """Browse all hardware items."""
    while True:
        clear_screen()
        items = print_hardware_items()
        print(f"{len(items) + 1}. Back to Main Menu")
        print("=========================")
        
        choice = input("\nEnter hardware item number: ")
        
        try:
            choice = int(choice)
            if choice == len(items) + 1:
                return
            elif 1 <= choice <= len(items):
                show_hardware_details(items[choice - 1]['id'])
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")
        except ValueError:
            print("Please enter a valid number.")
            input("Press Enter to continue...")

def view_all_hardware():
    """Display all hardware items in the catalog."""
    clear_screen()
    print("\n=== All Hardware Items ===")
    
    conn = models.get_hardware_db()
    c = conn.cursor()
    
    c.execute("""
        SELECT hi.id, hi.name, hi.manufacturer, hi.model, hc.name as category
        FROM hardware_items hi
        JOIN hardware_categories hc ON hi.category_id = hc.id
        ORDER BY hi.name
    """)
    
    items = c.fetchall()
    if not items:
        print("\nNo hardware items found in the catalog.")
    else:
        for item in items:
            print(f"\nID: {item[0]}")
            print(f"Name: {item[1]}")
            print(f"Manufacturer: {item[2]}")
            print(f"Model: {item[3]}")
            print(f"Category: {item[4]}")
            print("-" * 30)
    
    conn.close()
    input("\nPress Enter to continue...") 

def add_hardware_item():
    """Display the UI for adding a new hardware item to the catalog."""
    clear_screen()
    
    # Get hardware categories
    conn = models.get_hardware_db()
    c = conn.cursor()
    c.execute("SELECT id, name FROM hardware_categories")
    categories = c.fetchall()
    conn.close()
    
    if not categories:
        print_error("No categories found. Please create categories first.")
        input("Press Enter to continue...")
        return False
    
    # Display categories
    category_rows = [[str(cat_id), cat_name] for cat_id, cat_name in categories]
    print_table("Available Categories", ["ID", "Name"], category_rows)
    
    try:
        category_id = int(input("\nSelect category ID: "))
        name = input("Enter hardware name: ")
        manufacturer = input("Enter manufacturer: ")
        model = input("Enter model: ")
        
        success, error = models.add_hardware_item(category_id, name, manufacturer, model)
        
        if success:
            print_info("Success", "Hardware item added successfully!")
        else:
            print_error(f"Error adding hardware item: {error}")
        return success
    except ValueError:
        print_error("Invalid category ID. Please enter a number.")
        return False
    finally:
        input("Press Enter to continue...")

def update_hardware_item():
    """Display the UI for updating an existing hardware item."""
    clear_screen()
    
    # Get all hardware items
    conn = models.get_hardware_db()
    c = conn.cursor()
    c.execute("""
        SELECT id, name, manufacturer, model
        FROM hardware_items
        ORDER BY name
    """)
    items = c.fetchall()
    conn.close()
    
    if not items:
        print_error("No hardware items found in the catalog.")
        input("Press Enter to continue...")
        return
    
    # Display hardware items
    item_rows = [[str(item[0]), f"{item[1]} ({item[2]} {item[3]})"] for item in items]
    print_table("Available Hardware Items", ["ID", "Details"], item_rows)
    
    try:
        item_id = int(input("\nSelect item ID to update: "))
        
        # Get new values
        name = input("Enter new name (press Enter to keep current): ")
        manufacturer = input("Enter new manufacturer (press Enter to keep current): ")
        model = input("Enter new model (press Enter to keep current): ")
        
        # Update the hardware item
        success, error = models.update_hardware_item(
            item_id,
            name if name else None,
            manufacturer if manufacturer else None,
            model if model else None
        )
        
        if success:
            if error == "No changes made":
                print_info("Update", "No changes made.")
            else:
                print_info("Success", "Hardware item updated successfully!")
        else:
            print_error(f"Error updating hardware item: {error}")
    except ValueError:
        print_error("Invalid item ID. Please enter a number.")
    finally:
        input("Press Enter to continue...")

def manage_hardware_catalog():
    """Manage the hardware catalog."""
    while True:
        clear_screen()
        print("\n=== Hardware Catalog Management ===")
        print("1. View All Hardware Items")
        print("2. Add New Hardware Item")
        print("3. Update Hardware Item")
        print("4. Return to Administrator Menu")
        print("================================")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            view_all_hardware()
        elif choice == '2':
            add_hardware_item()
        elif choice == '3':
            update_hardware_item()
        elif choice == '4':
            return
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

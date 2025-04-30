import os
from . import models
from shared import views as shared_views

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
        print("Hardware item not found.")
        return
    
    clear_screen()
    print(f"\n=== {item['name']} Details ===")
    print(f"Manufacturer: {item['manufacturer']}")
    print(f"Model: {item['model']}")
    print(f"Release Date: {item['release_date']}")
    print(f"Repair Difficulty: {item['repair_difficulty']}/5")
    if item['operating_system']:
        print(f"Operating System: {item['operating_system']}")
    
    # Print specifications
    specs = models.get_hardware_specs(hardware_id)
    print("\nSpecifications:")
    for spec_name, spec_value in specs.items():
        print(f"  {spec_name}: {spec_value}")
    
    # Print common failures
    failures = models.get_hardware_failures(hardware_id)
    print("\nCommon Failures:")
    for i, failure in enumerate(failures, 1):
        print(f"  {i}. {failure}")
    
    # Print troubleshooting procedures
    procedures = models.get_troubleshooting_procedures(hardware_id)
    print("\nTroubleshooting Procedures:")
    for procedure in procedures:
        print(f"\n  {procedure['name']}:")
        for step in procedure['steps']:
            print(f"    {step['number']}. {step['description']}")
    
    # Print special tools
    tools = models.get_special_tools(hardware_id)
    print("\nSpecial Tools Required:")
    for i, tool in enumerate(tools, 1):
        print(f"  {i}. {tool}")
    
    print("\nPress Enter to continue...")
    input()

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
    print("\n=== Add New Hardware Item ===")
    
    # Get hardware categories
    conn = models.get_hardware_db()
    c = conn.cursor()
    c.execute("SELECT id, name FROM hardware_categories")
    categories = c.fetchall()
    conn.close()
    
    if not categories:
        print("No categories found. Please create categories first.")
        input("Press Enter to continue...")
        return False
    
    print("\nAvailable Categories:")
    for cat_id, cat_name in categories:
        print(f"{cat_id}. {cat_name}")
    
    try:
        category_id = int(input("\nSelect category ID: "))
        name = input("Enter hardware name: ")
        manufacturer = input("Enter manufacturer: ")
        model = input("Enter model: ")
        
        success, error = models.add_hardware_item(category_id, name, manufacturer, model)
        
        if success:
            print("\nHardware item added successfully!")
        else:
            print(f"\nError adding hardware item: {error}")
        return success
    except ValueError:
        print("Invalid category ID. Please enter a number.")
        return False
    finally:
        input("Press Enter to continue...")

def update_hardware_item():
    """Display the UI for updating an existing hardware item."""
    clear_screen()
    print("\n=== Update Hardware Item ===")
    
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
        print("No hardware items found in the catalog.")
        input("Press Enter to continue...")
        return
    
    print("\nAvailable Hardware Items:")
    for item in items:
        print(f"{item[0]}. {item[1]} ({item[2]} {item[3]})")
    
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
                print("\nNo changes made.")
            else:
                print("\nHardware item updated successfully!")
        else:
            print(f"\nError updating hardware item: {error}")
    except ValueError:
        print("Invalid item ID. Please enter a number.")
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

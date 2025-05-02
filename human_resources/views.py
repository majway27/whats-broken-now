from datetime import date
from typing import Optional
from . import RoleRepository, EmployeeRepository, PerformanceRatingRepository
from shared.views import print_menu, print_common_header, clear_screen


def show_hr_menu():
    """Print the HR menu options and handle user choice."""
    while True:
        clear_screen()
        print_common_header()
        
        menu_options = [
            "1. Employee Management",
            "2. Role Management",
            "3. Performance Reviews",
            "Q. Back to Main Menu"
        ]
        print_menu("Human Resources", menu_options)
        
        choice = input("\nEnter your choice (1-3, Q): ")
        
        if choice == '1':
            employee_management_menu()
        elif choice == '2':
            role_management_menu()
        elif choice == '3':
            performance_reviews_menu()
        elif choice.upper() == 'Q':
            clear_screen()
            return
        else:
            print("\nInvalid choice. Please try again.")
            input("Press Enter to continue...")
            clear_screen()

def employee_management_menu():
    """Handle employee management operations."""
    while True:
        clear_screen()
        print_common_header()
        
        menu_options = [
            "1. List All Employees",
            "2. Add New Employee",
            "3. Update Employee Role",
            "Q. Back to HR Menu"
        ]
        print_menu("Employee Management", menu_options)
        
        choice = input("\nEnter your choice (1-3, Q): ")
        
        if choice == '1':
            list_employees()
        elif choice == '2':
            add_employee()
        elif choice == '3':
            update_employee_role()
        elif choice.upper() == 'Q':
            return
        else:
            print("\nInvalid choice. Please try again.")
            input("Press Enter to continue...")
            clear_screen()

def role_management_menu():
    """Handle role management operations."""
    while True:
        clear_screen()
        print_common_header()
        
        menu_options = [
            "1. List All Roles",
            "2. Add New Role",
            "Q. Back to HR Menu"
        ]
        print_menu("Role Management", menu_options)
        
        choice = input("\nEnter your choice (1-2, Q): ")
        
        if choice == '1':
            list_roles()
        elif choice == '2':
            add_role()
        elif choice.upper() == 'Q':
            return
        else:
            print("\nInvalid choice. Please try again.")
            input("Press Enter to continue...")
            clear_screen()

def performance_reviews_menu():
    """Handle performance review operations."""
    while True:
        clear_screen()
        print_common_header()
        
        menu_options = [
            "1. Add Performance Review",
            "2. View Employee Reviews",
            "Q. Back to HR Menu"
        ]
        print_menu("Performance Reviews", menu_options)
        
        choice = input("\nEnter your choice (1-2, Q): ")
        
        if choice == '1':
            add_performance_review()
        elif choice == '2':
            view_employee_reviews()
        elif choice.upper() == 'Q':
            return
        else:
            print("\nInvalid choice. Please try again.")
            input("Press Enter to continue...")
            clear_screen()

def list_employees():
    """Display all employees."""
    clear_screen()
    print_common_header()
    print("\nEmployee List:")
    print("-" * 80)
    
    employees = EmployeeRepository.get_all()
    if not employees:
        print("No employees found.")
    else:
        for emp in employees:
            role = RoleRepository.get_by_id(emp.role_id) if emp.role_id else None
            role_title = role.title if role else "No Role"
            print(f"{emp.id}. {emp.first_name} {emp.last_name} - {emp.email} - {role_title}")
    
    input("\nPress Enter to continue...")
    clear_screen()

def add_employee():
    """Add a new employee."""
    clear_screen()
    print_common_header()
    print("\nAdd New Employee")
    print("-" * 80)
    
    try:
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        email = input("Email: ")
        
        # Get available roles
        roles = RoleRepository.get_all()
        if roles:
            print("\nAvailable Roles:")
            for role in roles:
                print(f"{role.id}. {role.title}")
            role_id = input("\nEnter Role ID (or press Enter for no role): ")
            role_id = int(role_id) if role_id else None
        else:
            print("\nNo roles available. Please create a role first.")
            role_id = None
        
        # Get hire date
        hire_date_str = input("Hire Date (YYYY-MM-DD): ")
        hire_date = date.fromisoformat(hire_date_str)
        
        employee = EmployeeRepository.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            hire_date=hire_date,
            role_id=role_id
        )
        
        print(f"\nEmployee {employee.first_name} {employee.last_name} added successfully!")
    except ValueError as e:
        print(f"\nError: {str(e)}")
    except Exception as e:
        print(f"\nError adding employee: {str(e)}")
    
    input("\nPress Enter to continue...")
    clear_screen()

def update_employee_role():
    """Update an employee's role."""
    clear_screen()
    print_common_header()
    print("\nUpdate Employee Role")
    print("-" * 80)
    
    try:
        # List employees
        employees = EmployeeRepository.get_all()
        if not employees:
            print("No employees found.")
            input("\nPress Enter to continue...")
            return
        
        print("\nSelect Employee:")
        for emp in employees:
            print(f"{emp.id}. {emp.first_name} {emp.last_name}")
        
        employee_id = int(input("\nEnter Employee ID: "))
        employee = EmployeeRepository.get_by_id(employee_id)
        if not employee:
            print("Employee not found.")
            input("\nPress Enter to continue...")
            return
        
        # List roles
        roles = RoleRepository.get_all()
        if not roles:
            print("No roles available.")
            input("\nPress Enter to continue...")
            return
        
        print("\nAvailable Roles:")
        for role in roles:
            print(f"{role.id}. {role.title}")
        
        role_id = input("\nEnter Role ID (or press Enter to remove role): ")
        role_id = int(role_id) if role_id else None
        
        if EmployeeRepository.update_role(employee_id, role_id):
            print("\nRole updated successfully!")
        else:
            print("\nFailed to update role.")
    except ValueError as e:
        print(f"\nError: {str(e)}")
    except Exception as e:
        print(f"\nError updating role: {str(e)}")
    
    input("\nPress Enter to continue...")
    clear_screen()

def list_roles():
    """Display all roles."""
    clear_screen()
    print_common_header()
    print("\nRole List:")
    print("-" * 80)
    
    roles = RoleRepository.get_all()
    if not roles:
        print("No roles found.")
    else:
        for role in roles:
            print(f"{role.id}. {role.title}")
            if role.description:
                print(f"   Description: {role.description}")
            print()
    
    input("\nPress Enter to continue...")
    clear_screen()

def add_role():
    """Add a new role."""
    clear_screen()
    print_common_header()
    print("\nAdd New Role")
    print("-" * 80)
    
    try:
        title = input("Role Title: ")
        description = input("Description (optional): ")
        
        role = RoleRepository.create(title=title, description=description or None)
        print(f"\nRole '{role.title}' added successfully!")
    except Exception as e:
        print(f"\nError adding role: {str(e)}")
    
    input("\nPress Enter to continue...")
    clear_screen()

def add_performance_review():
    """Add a performance review for an employee."""
    clear_screen()
    print_common_header()
    print("\nAdd Performance Review")
    print("-" * 80)
    
    try:
        # List employees
        employees = EmployeeRepository.get_all()
        if not employees:
            print("No employees found.")
            input("\nPress Enter to continue...")
            return
        
        print("\nSelect Employee:")
        for emp in employees:
            print(f"{emp.id}. {emp.first_name} {emp.last_name}")
        
        employee_id = int(input("\nEnter Employee ID: "))
        employee = EmployeeRepository.get_by_id(employee_id)
        if not employee:
            print("Employee not found.")
            input("\nPress Enter to continue...")
            return
        
        rating = int(input("\nEnter Rating (1-5): "))
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        
        review_date_str = input("Review Date (YYYY-MM-DD): ")
        review_date = date.fromisoformat(review_date_str)
        
        comments = input("Comments (optional): ")
        
        review = PerformanceRatingRepository.create(
            employee_id=employee_id,
            rating=rating,
            review_date=review_date,
            comments=comments or None
        )
        
        print("\nPerformance review added successfully!")
    except ValueError as e:
        print(f"\nError: {str(e)}")
    except Exception as e:
        print(f"\nError adding review: {str(e)}")
    
    input("\nPress Enter to continue...")
    clear_screen()

def view_employee_reviews():
    """View performance reviews for an employee."""
    clear_screen()
    print_common_header()
    print("\nView Employee Reviews")
    print("-" * 80)
    
    try:
        # List employees
        employees = EmployeeRepository.get_all()
        if not employees:
            print("No employees found.")
            input("\nPress Enter to continue...")
            return
        
        print("\nSelect Employee:")
        for emp in employees:
            print(f"{emp.id}. {emp.first_name} {emp.last_name}")
        
        employee_id = int(input("\nEnter Employee ID: "))
        employee = EmployeeRepository.get_by_id(employee_id)
        if not employee:
            print("Employee not found.")
            input("\nPress Enter to continue...")
            return
        
        reviews = PerformanceRatingRepository.get_by_employee_id(employee_id)
        if not reviews:
            print(f"\nNo reviews found for {employee.first_name} {employee.last_name}.")
        else:
            print(f"\nPerformance Reviews for {employee.first_name} {employee.last_name}:")
            print("-" * 80)
            for review in reviews:
                print(f"Date: {review.review_date}")
                print(f"Rating: {review.rating}/5")
                if review.comments:
                    print(f"Comments: {review.comments}")
                print("-" * 40)
    except ValueError as e:
        print(f"\nError: {str(e)}")
    except Exception as e:
        print(f"\nError viewing reviews: {str(e)}")
    
    input("\nPress Enter to continue...")
    clear_screen() 
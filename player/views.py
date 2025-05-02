from datetime import date
from shared.views import print_menu, print_status, print_info, print_error, clear_screen
from shared.common_ui import print_common_header
from .repository import PlayerRepository
from human_resources.repository import RoleRepository, EmployeeRepository
from game_calendar.models import reset_game_days
import random

# Common first names and last names for random generation
FIRST_NAMES = [
    "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Quinn", "Avery",
    "Dakota", "Skyler", "Jamie", "Drew", "Blake", "Logan", "Cameron", "Parker",
    "Dylan", "Jordan", "Morgan", "Riley", "Avery", "Quinn", "Parker", "Drew",
    "Sam", "Robin", "Kai", "River", "Phoenix", "Sage", "Rowan", "Emerson",
    "Finley", "Reese", "Hayden", "Sawyer", "Ellis", "Rory", "Dallas", "Arden",
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
    "Thomas", "Charles", "Christopher", "Daniel", "Matthew", "Anthony", "Donald",
    "Mark", "Paul", "Steven", "Andrew", "Kenneth", "Joshua", "Kevin", "Brian",
    "George", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan",
    "Wei", "Ming", "Jing", "Hui", "Yong", "Xia", "Yan", "Jun", "Li", "Chen",
    "Hiroshi", "Kenji", "Takashi", "Yuki", "Akira", "Satoshi", "Kazuki", "Ryo",
    "Min-ji", "Soo-jin", "Ji-hoon", "Seung", "Min-ho", "Ji-won", "Hye-jin",
    "Arjun", "Vikram", "Rahul", "Priya", "Anjali", "Neha", "Raj", "Amit",
    "Deepak", "Sanjay", "Meera", "Kavita", "Ravi", "Sunil", "Vijay",
    "Mohammed", "Ahmed", "Ali", "Omar", "Yusuf", "Ibrahim", "Fatima", "Aisha",
    "Layla", "Zainab", "Noor", "Sara", "Hassan", "Karim", "Tariq",
    "Kwame", "Kofi", "Amani", "Zuri", "Amara", "Kai", "Zola", "Tendai",
    "Chidi", "Oluwaseun", "Ife", "Ade", "Babatunde", "Folake", "Oluwatobi",
    "Carlos", "Miguel", "Javier", "Ricardo", "Fernando", "Sofia", "Isabella",
    "Valentina", "Camila", "Gabriela", "Mariana", "Ana", "Luis", "Diego",
    "Lars", "Bjorn", "Ingrid", "Astrid", "Hans", "Klaus", "Greta", "Helena",
    "Vladimir", "Ivan", "Natasha", "Olga", "Dimitri", "Boris", "Anastasia"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez",
    "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright",
    "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green", "Adams",
    "Wang", "Li", "Zhang", "Liu", "Chen", "Yang", "Huang", "Zhao", "Wu",
    "Zhou", "Sun", "Ma", "Zhu", "Hu", "Guo", "Lin", "He", "Gao", "Luo",
    "Zheng", "Tanaka", "Sato", "Suzuki", "Takahashi", "Watanabe", "Ito",
    "Yamamoto", "Nakamura", "Kobayashi", "Kato", "Kim", "Lee", "Park", "Choi",
    "Jung", "Kang", "Cho", "Yoon", "Jang", "Lim",
    "Patel", "Kumar", "Singh", "Sharma", "Gupta", "Verma", "Mehta", "Chopra",
    "Reddy", "Kapoor", "Malhotra", "Nair", "Menon", "Iyer", "Kaur",
    "Khan", "Ali", "Hassan", "Hussein", "Ahmed", "Mohammed", "Ibrahim",
    "Abdullah", "Rahman", "Karim", "Malik", "Hassan", "Farah", "Omar",
    "Mensah", "Osei", "Owusu", "Kufuor", "Mbeki", "Mandela", "Tutu",
    "Nkrumah", "Kenyatta", "Mugabe", "Nyerere", "Kaunda", "Biko", "Lumumba",
    "Rodriguez", "Garcia", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Perez", "Sanchez", "Ramirez", "Torres", "Flores", "Rivera", "Morales",
    "Muller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner",
    "Becker", "Hoffmann", "Schulz", "Koch", "Bauer", "Richter", "Klein",
    "Wolf", "Schroder", "Neumann", "Schwarz", "Zimmermann", "Braun"
]

def generate_random_name() -> tuple[str, str]:
    """Generate a random first and last name."""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    return first_name, last_name

def generate_email(first_name: str, last_name: str) -> str:
    """Generate an email address from first and last name."""
    return f"{first_name.lower()}.{last_name.lower()}@company.com"

def handle_email_collision(first_name: str, last_name: str) -> str:
    """Handle email collision by adding a number suffix."""
    base_email = generate_email(first_name, last_name)
    email = base_email
    counter = 1
    
    # Check if email exists in either active or inactive employees
    while True:
        existing_employee = EmployeeRepository.get_by_email(email)
        if not existing_employee:
            break
        email = f"{first_name.lower()}.{last_name.lower()}{counter}@company.com"
        counter += 1
    
    return email

def handle_first_time_setup():
    """Handle first-time player setup and orientation."""
    clear_screen()
    print_common_header()
    
    print_info("Welcome to Whats Broken Now!", """
    Welcome to your first day at the company! Let's get you set up.
    
    We'll need some basic information to create your employee record.
    You will be joining the company as an IT Support Specialist.
    """)
    
    try:
        # Generate random name as default
        default_first, default_last = generate_random_name()
        
        # Get player information with defaults
        first_name = input(f"\nFirst Name [{default_first}]: ").strip()
        first_name = first_name if first_name else default_first
        
        last_name = input(f"Last Name [{default_last}]: ").strip()
        last_name = last_name if last_name else default_last
        
        # Generate email address
        email = handle_email_collision(first_name, last_name)
        
        # Create player record
        player = PlayerRepository.create(
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        
        # Get IT Support Specialist role
        role = RoleRepository.get_by_title("IT Support Specialist")
        if not role:
            raise ValueError("IT Support Specialist role not found. Please ensure the role exists in the system.")
        
        # Create employee record with IT Support Specialist role
        employee = EmployeeRepository.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            hire_date=date.today(),
            role_id=role.id,  # Force IT Support Specialist role
            employment_status='active'
        )
        
        # Update player with employee ID
        PlayerRepository.update_employee_id(player.id, employee.id)
        
        # Reset game days to day 1
        reset_game_days()
        
        # Show orientation message
        print_info("First Day Orientation", f"""
        Welcome to the IT Support team! As a new IT Support Specialist, you'll be responsible for:
        
        1. Handling support tickets from company.com customers.
        2. Troubleshooting hardware and software issues.
        3. Complying with the company's policies.
        
        Your first day will be focused on getting familiar with the systems and processes.
        When you are ready, try a ticket to help you learn the ropes.
        
        Your company email address is: [bold yellow]{email}[/]
        Remember to monitor your mailbox for important communications and updates.
        """)
        
        input("\nPress Enter to continue...")
        return True
        
    except ValueError as e:
        print_error(f"Setup Error: {str(e)}")
        input("\nPress Enter to continue...")
        return False
    except Exception as e:
        print_error(f"Setup Error: An unexpected error occurred: {str(e)}")
        input("\nPress Enter to continue...")
        return False 
from datetime import date

# Seed data for roles
ROLES = [
    {
        'title': 'Vice President, Operations',
        'description': 'The Vice President of Operations is a senior executive position responsible for overseeing and optimizing all operational aspects of the organization. This role requires strategic leadership, operational excellence, and the ability to drive organizational efficiency and growth.'
    },
    {
        'title': 'HR Manager',
        'description': 'Oversees all human resources operations and policies'
    },
    {
        'title': 'IT Manager',
        'description': 'Manages IT department operations and personnel'
    },
    {
        'title': 'IT Support Specialist',
        'description': 'Provides technical support and troubleshooting for hardware and software issues'
    },
    {
        'title': 'Hardware Technician',
        'description': 'Specializes in hardware repairs and maintenance'
    },
    {
        'title': 'Sales Representative',
        'description': 'Manages client relationships and drives product sales'
    }
]

# Seed data for employees
EMPLOYEES = [
    {
        'first_name': 'Sarah',
        'last_name': 'Chen',
        'email': 'sarah.chen@company.com',
        'role_title': 'Vice President, Operations',
        'hire_date': date(2019, 1, 1)
    },
    {
        'first_name': 'Joanna',
        'last_name': 'Flair',
        'email': 'joanna.flair@company.com',
        'role_title': 'HR Manager',
        'hire_date': date(2020, 1, 15)
    },
    {
        'first_name': 'Jill',
        'last_name': 'Crumburg',
        'email': 'jill.crumburg@company.com',
        'role_title': 'IT Manager',
        'hire_date': date(2020, 1, 15)
    },
    {
        'first_name': 'Hilton',
        'last_name': 'Adams',
        'email': 'hilton.adams@company.com',
        'role_title': 'Hardware Technician',
        'hire_date': date(2021, 3, 1)
    },
    {
        'first_name': 'Deter',
        'last_name': 'Ribbons',
        'email': 'deter.ribbons@company.com',
        'role_title': 'IT Support Specialist',
        'hire_date': date(2019, 6, 15)
    },
    {
        'first_name': 'Michael',
        'last_name': 'Colton',
        'email': 'michael.colton@company.com',
        'role_title': 'IT Support Specialist',
        'hire_date': date(2022, 9, 1)
    },
    {
        'first_name': 'Dom',
        'last_name': 'Limchowski',
        'email': 'dom.limchowski@company.com',
        'role_title': 'Sales Representative',
        'hire_date': date(2018, 4, 1)
    }
] 
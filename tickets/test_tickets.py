import unittest
from datetime import datetime
from . import models
from . import views
from shared.database import DatabaseConnection
from human_resources.repository import EmployeeRepository

class TestTickets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test database before running tests."""
        models.reset_db()
        # Create test employee
        cls.employee_repo = EmployeeRepository()
        cls.test_employee = cls.employee_repo.add_employee(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            role="Technician"
        )

    def setUp(self):
        """Set up test data before each test."""
        models.reset_db()
        # Add test product
        with DatabaseConnection.get_cursor('tickets') as c:
            c.execute("""
                INSERT INTO products (name, model, manufacturer)
                VALUES (?, ?, ?)
            """, ("Test Product", "Model X", "Test Manufacturer"))
            self.product_id = c.lastrowid

    def test_add_ticket(self):
        """Test adding a new ticket."""
        ticket = {
            'id': 'TEST-001',
            'title': 'Test Ticket',
            'status': 'Open',
            'description': 'Test description',
            'hardware': {
                'name': 'Test Product',
                'model': 'Model X',
                'manufacturer': 'Test Manufacturer'
            }
        }
        models.add_ticket(ticket)
        
        # Verify ticket was added
        tickets = models.get_all_tickets()
        self.assertEqual(len(tickets), 1)
        self.assertEqual(tickets[0]['id'], 'TEST-001')
        self.assertEqual(tickets[0]['title'], 'Test Ticket')
        self.assertEqual(tickets[0]['status'], 'Open')
        self.assertEqual(tickets[0]['description'], 'Test description')

    def test_get_active_tickets(self):
        """Test getting active tickets."""
        # Add test tickets
        ticket1 = {
            'id': 'TEST-001',
            'title': 'Active Ticket',
            'status': 'Open',
            'description': 'Test description',
            'hardware': {
                'name': 'Test Product',
                'model': 'Model X',
                'manufacturer': 'Test Manufacturer'
            }
        }
        ticket2 = {
            'id': 'TEST-002',
            'title': 'Resolved Ticket',
            'status': 'Resolved',
            'description': 'Test description',
            'hardware': {
                'name': 'Test Product',
                'model': 'Model X',
                'manufacturer': 'Test Manufacturer'
            }
        }
        models.add_ticket(ticket1)
        models.add_ticket(ticket2)

        active_tickets = models.get_active_tickets()
        self.assertEqual(len(active_tickets), 1)
        self.assertEqual(active_tickets[0]['id'], 'TEST-001')

    def test_get_unassigned_tickets(self):
        """Test getting unassigned tickets."""
        # Add test tickets
        ticket1 = {
            'id': 'TEST-001',
            'title': 'Unassigned Ticket',
            'status': 'Open',
            'description': 'Test description',
            'hardware': {
                'name': 'Test Product',
                'model': 'Model X',
                'manufacturer': 'Test Manufacturer'
            }
        }
        ticket2 = {
            'id': 'TEST-002',
            'title': 'Assigned Ticket',
            'status': 'Open',
            'description': 'Test description',
            'hardware': {
                'name': 'Test Product',
                'model': 'Model X',
                'manufacturer': 'Test Manufacturer'
            }
        }
        models.add_ticket(ticket1)
        models.add_ticket(ticket2)
        models.assign_ticket('TEST-002', self.test_employee.id)

        unassigned_tickets = models.get_unassigned_tickets()
        self.assertEqual(len(unassigned_tickets), 1)
        self.assertEqual(unassigned_tickets[0]['id'], 'TEST-001')

    def test_assign_ticket(self):
        """Test assigning a ticket to an employee."""
        # Add test ticket
        ticket = {
            'id': 'TEST-001',
            'title': 'Test Ticket',
            'status': 'Open',
            'description': 'Test description',
            'hardware': {
                'name': 'Test Product',
                'model': 'Model X',
                'manufacturer': 'Test Manufacturer'
            }
        }
        models.add_ticket(ticket)

        # Assign ticket
        models.assign_ticket('TEST-001', self.test_employee.id)

        # Verify assignment
        assignee = models.get_ticket_assignee('TEST-001')
        self.assertEqual(assignee['id'], self.test_employee.id)

    def test_update_ticket_status(self):
        """Test updating ticket status."""
        # Add test ticket
        ticket = {
            'id': 'TEST-001',
            'title': 'Test Ticket',
            'status': 'Open',
            'description': 'Test description',
            'hardware': {
                'name': 'Test Product',
                'model': 'Model X',
                'manufacturer': 'Test Manufacturer'
            }
        }
        models.add_ticket(ticket)

        # Update status
        models.update_ticket_status('TEST-001', 'In Progress')

        # Verify status update
        tickets = models.get_all_tickets()
        self.assertEqual(tickets[0]['status'], 'In Progress')

    def test_ticket_history(self):
        """Test ticket history tracking."""
        # Add test ticket
        ticket = {
            'id': 'TEST-001',
            'title': 'Test Ticket',
            'status': 'Open',
            'description': 'Test description',
            'hardware': {
                'name': 'Test Product',
                'model': 'Model X',
                'manufacturer': 'Test Manufacturer'
            }
        }
        models.add_ticket(ticket)

        # Make some changes
        models.update_ticket_status('TEST-001', 'In Progress')
        models.assign_ticket('TEST-001', self.test_employee.id)
        models.add_ticket_comment(ticket, 'Test comment')

        # Verify history
        history = models.get_ticket_history('TEST-001')
        self.assertGreater(len(history), 0)
        self.assertEqual(history[0]['status'], 'In Progress')

    def test_get_ticket_count(self):
        """Test getting ticket count."""
        # Add test tickets
        ticket1 = {
            'id': 'TEST-001',
            'title': 'Test Ticket 1',
            'status': 'Open',
            'description': 'Test description',
            'hardware': {
                'name': 'Test Product',
                'model': 'Model X',
                'manufacturer': 'Test Manufacturer'
            }
        }
        ticket2 = {
            'id': 'TEST-002',
            'title': 'Test Ticket 2',
            'status': 'Open',
            'description': 'Test description',
            'hardware': {
                'name': 'Test Product',
                'model': 'Model X',
                'manufacturer': 'Test Manufacturer'
            }
        }
        models.add_ticket(ticket1)
        models.add_ticket(ticket2)

        count = models.get_ticket_count()
        self.assertEqual(count, 2)

    def test_get_tickets_by_status(self):
        """Test getting ticket counts by status."""
        # Add test tickets
        ticket1 = {
            'id': 'TEST-001',
            'title': 'Open Ticket',
            'status': 'Open',
            'description': 'Test description',
            'hardware': {
                'name': 'Test Product',
                'model': 'Model X',
                'manufacturer': 'Test Manufacturer'
            }
        }
        ticket2 = {
            'id': 'TEST-002',
            'title': 'In Progress Ticket',
            'status': 'In Progress',
            'description': 'Test description',
            'hardware': {
                'name': 'Test Product',
                'model': 'Model X',
                'manufacturer': 'Test Manufacturer'
            }
        }
        models.add_ticket(ticket1)
        models.add_ticket(ticket2)

        status_counts = models.get_tickets_by_status()
        self.assertEqual(status_counts['Open'], 1)
        self.assertEqual(status_counts['In Progress'], 1)

if __name__ == '__main__':
    unittest.main() 
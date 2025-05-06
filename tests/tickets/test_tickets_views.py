import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from tickets.views import (
    work_new_ticket,
    view_all_tickets,
    view_ticket_history,
    add_ticket_comment,
    update_ticket_status,
    view_assigned_tickets,
    view_tickets_by_status
)
from tickets.models import *
from human_resources.utils import get_current_employee

class TestTicketViews(unittest.TestCase):
    def setUp(self):
        """Set up test data before each test."""
        # Mock the current employee
        self.mock_employee = MagicMock()
        self.mock_employee.id = 1
        self.mock_employee.first_name = "Test"
        self.mock_employee.last_name = "User"
        self.mock_employee.email = "test@example.com"

    @patch('tickets.views.get_current_employee')
    @patch('tickets.views.models.get_active_tickets')
    @patch('tickets.views.show_ticket_interaction')
    def test_work_new_ticket(self, mock_show_interaction, mock_get_tickets, mock_get_employee):
        """Test the work_new_ticket function."""
        # Mock the active tickets
        mock_tickets = [
            {
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
        ]
        mock_get_tickets.return_value = mock_tickets

        # Test selecting a ticket
        with patch('builtins.input', return_value='1'):
            work_new_ticket()
            mock_show_interaction.assert_called_once_with(mock_tickets[0])

        # Test returning to menu
        with patch('builtins.input', return_value='Q'):
            work_new_ticket()
            mock_show_interaction.assert_called_once()  # Should not be called again

    @patch('tickets.views.models.get_all_tickets')
    def test_view_all_tickets(self, mock_get_tickets):
        """Test the view_all_tickets function."""
        # Mock the tickets
        mock_tickets = [
            {
                'id': 'TEST-001',
                'title': 'Test Ticket',
                'status': 'Open',
                'description': 'Test description',
                'hardware': {
                    'name': 'Test Product',
                    'model': 'Model X',
                    'manufacturer': 'Test Manufacturer'
                },
                'created_at': '2024-03-20'
            }
        ]
        mock_get_tickets.return_value = mock_tickets

        with patch('builtins.input', return_value=''):
            view_all_tickets()
            mock_get_tickets.assert_called_once()

    @patch('tickets.views.models.get_ticket_history')
    def test_view_ticket_history(self, mock_get_history):
        """Test the view_ticket_history function."""
        # Mock the ticket
        mock_ticket = {
            'id': 'TEST-001',
            'title': 'Test Ticket'
        }

        # Mock the history
        mock_history = [
            {
                'changed_at': '2024-03-20',
                'status': 'Open',
                'assignee_name': 'Test User',
                'comment': 'Test comment'
            }
        ]
        mock_get_history.return_value = mock_history

        with patch('builtins.input', return_value=''):
            view_ticket_history(mock_ticket)
            mock_get_history.assert_called_once_with('TEST-001')

    @patch('tickets.views.models.append_ticket_comment')
    @patch('tickets.views.clear_screen')
    def test_add_ticket_comment(self, mock_clear_screen, mock_append_comment):
        """Test the add_ticket_comment function."""
        # Mock the ticket
        mock_ticket = {
            'id': 'TEST-001',
            'title': 'Test Ticket'
        }

        # Test adding a valid comment
        test_comment = 'Test comment'
        #with patch('builtins.input', return_value=test_comment):
        with patch('builtins.input', return_value=test_comment):
            add_ticket_comment(mock_ticket)
            mock_append_comment.assert_called_once_with(mock_ticket, test_comment)

        # Test empty comment
        mock_append_comment.reset_mock()
        with patch('builtins.input', return_value=''):
            add_ticket_comment(mock_ticket)
            mock_append_comment.assert_not_called()

        # Test comment with only whitespace
        mock_append_comment.reset_mock()
        with patch('builtins.input', return_value='   '):
            add_ticket_comment(mock_ticket)
            mock_append_comment.assert_not_called()

    @patch('tickets.views.models.mutate_ticket_status')
    def test_update_ticket_status(self, mock_mutate_status):
        """Test the update_ticket_status function."""
        # Mock the ticket
        mock_ticket = {
            'id': 'TEST-001',
            'title': 'Test Ticket',
            'status': 'Open'
        }

        # Test updating status to In Progress
        with patch('builtins.input', return_value='2'):
            update_ticket_status(mock_ticket)
            mock_mutate_status.assert_called_once_with('TEST-001', 'In Progress')

        # Test canceling
        mock_mutate_status.reset_mock()
        with patch('builtins.input', return_value='5'):
            update_ticket_status(mock_ticket)
            mock_mutate_status.assert_not_called()

        # Test invalid input
        mock_mutate_status.reset_mock()
        with patch('builtins.input', side_effect=['invalid', '5']):
            update_ticket_status(mock_ticket)
            mock_mutate_status.assert_not_called()

    @patch('tickets.views.models.get_assigned_tickets')
    def test_view_assigned_tickets(self, mock_get_assigned):
        """Test the view_assigned_tickets function."""
        # Mock the assigned tickets
        mock_tickets = [
            {
                'id': 'TEST-001',
                'title': 'Test Ticket',
                'status': 'Open',
                'hardware': {
                    'name': 'Test Product',
                    'model': 'Model X'
                },
                'created_at': '2024-03-20'
            }
        ]
        mock_get_assigned.return_value = mock_tickets

        with patch('builtins.input', return_value=''):
            view_assigned_tickets(1)
            mock_get_assigned.assert_called_once_with(1)

    @patch('tickets.views.models.get_tickets_by_status')
    def test_view_tickets_by_status(self, mock_get_by_status):
        """Test the view_tickets_by_status function."""
        # Mock the status counts
        mock_status_counts = {
            'Open': 2,
            'In Progress': 1
        }
        mock_get_by_status.return_value = mock_status_counts

        with patch('builtins.input', return_value=''):
            view_tickets_by_status()
            mock_get_by_status.assert_called_once()

if __name__ == '__main__':
    unittest.main() 
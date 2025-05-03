import os
import sys
import logging
import threading
import time
from datetime import datetime
from human_resources import models as hr_models
from human_resources.repository import RoleRepository, EmployeeRepository
from mailbox import models as mailbox_models

logger = logging.getLogger(__name__)

class RoleAgent:
    def __init__(self, role_id, interval_minutes=5):
        """Initialize a role agent."""
        self.role_id = role_id
        self.interval_minutes = interval_minutes
        self.thread = None
        self.running = False
        self._lock = threading.Lock()
        self.role = RoleRepository.get_by_id(role_id)
        if not self.role:
            raise ValueError(f"Role with ID {role_id} not found")

    def check_messages(self):
        """Check and respond to messages for employees with this role."""
        try:
            # Get all employees with this role
            employees = EmployeeRepository.get_all()
            role_employees = [emp for emp in employees if emp.role_id == self.role_id]

            for employee in role_employees:
                # Get unread messages for this employee
                messages = mailbox_models.get_messages(employee.email)
                unread_messages = [msg for msg in messages if not msg[5]]  # msg[5] is is_read flag

                for msg in unread_messages:
                    msg_id, sender, subject, content, timestamp, _ = msg
                    
                    # Generate response based on role and message content
                    response = self.generate_response(sender, subject, content)
                    if response:
                        mailbox_models.add_message(
                            sender=employee.email,
                            recipient=sender,
                            subject=f"Re: {subject}",
                            content=response
                        )
                        mailbox_models.mark_as_read(msg_id)
                        logger.info(f"Agent for {self.role.title} responded to message from {sender}")

        except Exception as e:
            logger.error(f"Error in check_messages for {self.role.title}: {e}")

    def generate_response(self, sender, subject, content):
        """Generate a response based on the role and message content."""
        # This is a placeholder for the LLM integration
        # In a real implementation, this would use the LLM to generate appropriate responses
        # based on the role's responsibilities and the message content
        return f"Thank you for your message. This is an automated response from the {self.role.title} role. Your message has been received and will be processed according to our standard procedures."

    def run(self):
        """Main agent loop."""
        logger.info(f"Role agent for {self.role.title} started")
        while self.running:
            try:
                self.check_messages()
                # Sleep for the specified interval
                time.sleep(self.interval_minutes * 60)
            except Exception as e:
                logger.error(f"Error in role agent for {self.role.title}: {e}")
                time.sleep(60)  # Sleep for a minute before retrying

    def start(self):
        """Start the role agent."""
        with self._lock:
            if self.running:
                logger.warning(f"Role agent for {self.role.title} is already running")
                return

            self.running = True
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()
            logger.info(f"Role agent for {self.role.title} started")

    def stop(self):
        """Stop the role agent."""
        with self._lock:
            if not self.running:
                logger.warning(f"Role agent for {self.role.title} is not running")
                return

            self.running = False
            if self.thread:
                self.thread.join(timeout=5)  # Wait up to 5 seconds for thread to finish
                self.thread = None
            logger.info(f"Role agent for {self.role.title} stopped")

class RoleAgentManager:
    def __init__(self):
        """Initialize the role agent manager."""
        self.agents = {}
        self._lock = threading.Lock()

    def start_all_agents(self):
        """Start agents for all roles."""
        roles = RoleRepository.get_all()
        for role in roles:
            self.start_agent(role.id)

    def stop_all_agents(self):
        """Stop all running agents."""
        with self._lock:
            for agent in self.agents.values():
                agent.stop()
            self.agents.clear()

    def start_agent(self, role_id):
        """Start an agent for a specific role."""
        with self._lock:
            if role_id in self.agents:
                logger.warning(f"Agent for role {role_id} is already running")
                return

            try:
                agent = RoleAgent(role_id)
                agent.start()
                self.agents[role_id] = agent
            except Exception as e:
                logger.error(f"Failed to start agent for role {role_id}: {e}")

    def stop_agent(self, role_id):
        """Stop an agent for a specific role."""
        with self._lock:
            if role_id not in self.agents:
                logger.warning(f"No agent running for role {role_id}")
                return

            self.agents[role_id].stop()
            del self.agents[role_id]

def init_role_agents():
    """Initialize and start all role agents."""
    manager = RoleAgentManager()
    manager.start_all_agents()
    return manager

def cleanup_role_agents():
    """Clean up all role agents."""
    manager = RoleAgentManager()
    manager.stop_all_agents() 
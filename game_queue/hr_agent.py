import os
import sys
import logging
import threading
import time
from datetime import datetime
import llm
from human_resources import models as hr_models
from human_resources.repository import RoleRepository, EmployeeRepository
from mailbox import models as mailbox_models

logger = logging.getLogger(__name__)

# Initialize LLM client
client = llm.get_model("mistral-7b-instruct-v0")

class HRAgent:
    def __init__(self, interval_minutes=5):
        """Initialize the HR agent."""
        self.interval_minutes = interval_minutes
        self.thread = None
        self.running = False
        self._lock = threading.Lock()
        self.role = RoleRepository.get_by_title("HR Manager")
        if not self.role:
            raise ValueError("HR Manager role not found")
        
        # Get the HR Manager employee
        employees = EmployeeRepository.get_all()
        hr_manager = next((emp for emp in employees if emp.role_id == self.role.id), None)
        if not hr_manager:
            raise ValueError("No employee found with HR Manager role")
        self.email = hr_manager.email

    def check_messages(self):
        """Check and respond to HR-related messages."""
        try:
            # Get all employees
            employees = EmployeeRepository.get_all()
            
            # Get unread messages for HR
            messages = mailbox_models.get_messages(self.email)
            unread_messages = [msg for msg in messages if not msg[5]]  # msg[5] is is_read flag

            for msg in unread_messages:
                msg_id, sender, subject, content, timestamp, _ = msg
                
                # Generate HR-appropriate response
                response = self.generate_hr_response(sender, subject, content)
                if response:
                    mailbox_models.add_message(
                        sender=self.email,
                        recipient=sender,
                        subject=f"Re: {subject}",
                        content=response
                    )
                    mailbox_models.mark_as_read(msg_id)
                    logger.info(f"HR Agent responded to message from {sender}")

        except Exception as e:
            logger.error(f"Error in HR agent check_messages: {e}")

    def generate_hr_response(self, sender, subject, content):
        """Generate an HR-appropriate response using LLM."""
        prompt = f"""As an HR Manager, respond to the following message from {sender}:
        Subject: {subject}
        Content: {content}
        
        Provide a professional, empathetic, and helpful response that:
        1. Addresses the employee's concerns
        2. Maintains confidentiality and professionalism
        3. Provides clear next steps or guidance
        4. Shows understanding of HR policies and procedures
        
        Keep the response concise and under 200 words."""
        
        try:
            response = client.prompt(prompt)
            return response.text()
        except Exception as e:
            logger.error(f"Error generating HR response: {e}")
            return "Thank you for your message. I apologize, but I'm currently experiencing technical difficulties. Please try again later or contact the IT department for assistance."

    def handle_employee_concerns(self):
        """Periodically check for employee concerns that need HR attention."""
        try:
            # Get all employees
            employees = EmployeeRepository.get_all()
            
            for employee in employees:
                # Check for any concerning patterns in employee data
                # This could include things like:
                # - Frequent absences
                # - Performance issues
                # - Work-life balance concerns
                # - Team conflicts
                
                # Generate proactive HR outreach if needed
                if self._should_reach_out(employee):
                    self._generate_proactive_outreach(employee)
                    
        except Exception as e:
            logger.error(f"Error in handle_employee_concerns: {e}")

    def _should_reach_out(self, employee):
        """Determine if HR should proactively reach out to an employee."""
        # This would implement logic to determine if an employee needs HR attention
        # For now, return False as a placeholder
        return False

    def _generate_proactive_outreach(self, employee):
        """Generate a proactive outreach message to an employee."""
        prompt = f"""As an HR Manager, create a supportive outreach message to {employee.name} about:
        - Checking in on their well-being
        - Offering support and resources
        - Maintaining confidentiality
        - Being professional yet empathetic
        
        Keep the message under 150 words."""
        
        try:
            response = client.prompt(prompt)
            mailbox_models.add_message(
                sender=self.email,
                recipient=employee.email,
                subject="HR Check-in",
                content=response.text()
            )
        except Exception as e:
            logger.error(f"Error generating proactive outreach: {e}")

    def run(self):
        """Main HR agent loop."""
        logger.info("HR agent started")
        while self.running:
            try:
                self.check_messages()
                self.handle_employee_concerns()
                time.sleep(self.interval_minutes * 60)
            except Exception as e:
                logger.error(f"Error in HR agent: {e}")
                time.sleep(60)  # Sleep for a minute before retrying

    def start(self):
        """Start the HR agent."""
        with self._lock:
            if self.running:
                logger.warning("HR agent is already running")
                return

            self.running = True
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()
            logger.info("HR agent started")

    def stop(self):
        """Stop the HR agent."""
        with self._lock:
            if not self.running:
                logger.warning("HR agent is not running")
                return

            self.running = False
            if self.thread:
                self.thread.join(timeout=5)  # Wait up to 5 seconds for thread to finish
                self.thread = None
            logger.info("HR agent stopped")

def init_hr_agent():
    """Initialize and start the HR agent."""
    agent = HRAgent()
    agent.start()
    return agent

def cleanup_hr_agent(agent):
    """Clean up the HR agent."""
    if agent:
        agent.stop() 

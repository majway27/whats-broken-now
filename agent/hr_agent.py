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

# Configure logging for HR agent
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Prevent propagation to root logger
logger.propagate = False

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Create file handler for HR agent logs
hr_handler = logging.FileHandler('logs/hr_agent.log')
hr_handler.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
hr_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(hr_handler)

# Initialize LLM client
client = llm.get_model("mistral-7b-instruct-v0")

class HRAgent:
    def __init__(self, interval_minutes=5):
        """Initialize the HR agent."""
        logger.info("Initializing HR agent with interval: %d minutes", interval_minutes)
        self.interval_minutes = interval_minutes
        self.thread = None
        self.running = False
        self._lock = threading.Lock()
        
        logger.debug("Fetching HR Manager role")
        self.role = RoleRepository.get_by_title("HR Manager")
        if not self.role:
            logger.error("HR Manager role not found in database")
            raise ValueError("HR Manager role not found")
        
        # Get the HR Manager employee
        logger.debug("Fetching all employees to find HR Manager")
        employees = EmployeeRepository.get_all()
        hr_manager = next((emp for emp in employees if emp.role_id == self.role.id), None)
        if not hr_manager:
            logger.error("No employee found with HR Manager role")
            raise ValueError("No employee found with HR Manager role")
        self.email = hr_manager.email
        logger.info("HR agent initialized with email: %s", self.email)

    def check_messages(self):
        """Check and respond to HR-related messages."""
        logger.info("Starting message check cycle")
        try:
            # Get all employees
            logger.debug("Fetching all employees")
            employees = EmployeeRepository.get_all()
            
            # Get unread messages for HR
            logger.debug("Fetching unread messages for HR")
            messages = mailbox_models.get_messages(self.email)
            unread_messages = [msg for msg in messages if not msg[5]]  # msg[5] is is_read flag
            logger.info("Found %d unread messages", len(unread_messages))

            for msg in unread_messages:
                msg_id, sender, subject, content, timestamp, _ = msg
                logger.info("Processing message from %s: %s", sender, subject)
                
                # Generate HR-appropriate response
                logger.debug("Generating HR response for message ID: %s", msg_id)
                response = self.generate_hr_response(sender, subject, content)
                if response:
                    logger.debug("Sending response to %s", sender)
                    mailbox_models.add_message(
                        sender=self.email,
                        recipient=sender,
                        subject=f"Re: {subject}",
                        content=response
                    )
                    mailbox_models.mark_as_read(msg_id)
                    logger.info("Successfully responded to message from %s", sender)
                else:
                    logger.warning("No response generated for message from %s", sender)

        except Exception as e:
            logger.error("Error in HR agent check_messages: %s", str(e), exc_info=True)

    def generate_hr_response(self, sender, subject, content):
        """Generate an HR-appropriate response using LLM."""
        logger.debug("Generating HR response for message from %s", sender)
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
            logger.debug("Sending prompt to LLM")
            response = client.prompt(prompt)
            logger.debug("Successfully generated response from LLM")
            return response.text()
        except Exception as e:
            logger.error("Error generating HR response: %s", str(e), exc_info=True)
            return "Thank you for your message. I apologize, but I'm currently experiencing technical difficulties. Please try again later or contact the IT department for assistance."

    def handle_employee_concerns(self):
        """Periodically check for employee concerns that need HR attention."""
        logger.info("Starting employee concerns check cycle")
        try:
            # Get all employees
            logger.debug("Fetching all employees for concern check")
            employees = EmployeeRepository.get_all()
            logger.info("Checking concerns for %d employees", len(employees))
            
            for employee in employees:
                logger.debug("Checking concerns for employee: %s", employee.name)
                # Check for any concerning patterns in employee data
                if self._should_reach_out(employee):
                    logger.info("Proactive outreach needed for employee: %s", employee.name)
                    self._generate_proactive_outreach(employee)
                else:
                    logger.debug("No concerns detected for employee: %s", employee.name)
                    
        except Exception as e:
            logger.error("Error in handle_employee_concerns: %s", str(e), exc_info=True)

    def _should_reach_out(self, employee):
        """Determine if HR should proactively reach out to an employee."""
        logger.debug("Evaluating if outreach needed for employee: %s", employee.name)
        # This would implement logic to determine if an employee needs HR attention
        # For now, return False as a placeholder
        return False

    def _generate_proactive_outreach(self, employee):
        """Generate a proactive outreach message to an employee."""
        logger.info("Generating proactive outreach for employee: %s", employee.name)
        prompt = f"""As an HR Manager, create a supportive outreach message to {employee.name} about:
        - Checking in on their well-being
        - Offering support and resources
        - Maintaining confidentiality
        - Being professional yet empathetic
        
        Keep the message under 150 words."""
        
        try:
            logger.debug("Sending outreach prompt to LLM")
            response = client.prompt(prompt)
            logger.debug("Successfully generated outreach message")
            mailbox_models.add_message(
                sender=self.email,
                recipient=employee.email,
                subject="HR Check-in",
                content=response.text()
            )
            logger.info("Sent proactive outreach to employee: %s", employee.name)
        except Exception as e:
            logger.error("Error generating proactive outreach: %s", str(e), exc_info=True)

    def run(self):
        """Main HR agent loop."""
        logger.info("Starting HR agent main loop")
        while self.running:
            try:
                logger.debug("Starting new agent cycle")
                self.check_messages()
                self.handle_employee_concerns()
                logger.debug("Agent cycle completed, sleeping for %d minutes", self.interval_minutes)
                time.sleep(self.interval_minutes * 60)
            except Exception as e:
                logger.error("Error in HR agent main loop: %s", str(e), exc_info=True)
                logger.info("Sleeping for 60 seconds before retrying")
                time.sleep(60)  # Sleep for a minute before retrying

    def start(self):
        """Start the HR agent."""
        with self._lock:
            if self.running:
                logger.warning("Attempted to start HR agent while already running")
                return

            logger.info("Starting HR agent")
            self.running = True
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()
            logger.info("HR agent thread started successfully")

    def stop(self):
        """Stop the HR agent."""
        with self._lock:
            if not self.running:
                logger.warning("Attempted to stop HR agent while not running")
                return

            logger.info("Stopping HR agent")
            self.running = False
            if self.thread:
                logger.debug("Waiting for HR agent thread to finish")
                self.thread.join(timeout=5)  # Wait up to 5 seconds for thread to finish
                self.thread = None
            logger.info("HR agent stopped successfully")

def init_hr_agent():
    """Initialize and start the HR agent."""
    logger.info("Initializing HR agent")
    agent = HRAgent()
    agent.start()
    logger.info("HR agent initialization complete")
    return agent

def cleanup_hr_agent(agent):
    """Clean up the HR agent."""
    if agent:
        logger.info("Cleaning up HR agent")
        agent.stop()
        logger.info("HR agent cleanup complete") 
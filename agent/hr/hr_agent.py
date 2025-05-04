import os
from typing import Optional
from ..base.agent_base import BaseAgent
from human_resources import models as hr_models
from human_resources.repository import RoleRepository, EmployeeRepository
from mailbox import models as mailbox_models
import llm

class HRAgent(BaseAgent):
    def __init__(self, config_path: str = "agent/hr/config/hr_agent_config.json"):
        """Initialize the HR agent with configuration."""
        super().__init__(config_path)
        self.role: Optional[hr_models.Role] = None
        self.email: Optional[str] = None
        self.llm_client = llm.get_model(self.config['llm_config']['model'])
        
    def initialize(self):
        """Initialize HR-specific resources."""
        self.logger.info("Initializing HR agent")
        
        # Get HR Manager role
        self.role = RoleRepository.get_by_title(self.config['role'])
        if not self.role:
            raise ValueError(f"{self.config['role']} role not found in database")
        
        # Get HR Manager employee
        employees = EmployeeRepository.get_all()
        hr_manager = next((emp for emp in employees if emp.role_id == self.role.id), None)
        if not hr_manager:
            raise ValueError(f"No employee found with {self.config['role']} role")
            
        self.email = hr_manager.email
        self.logger.info("HR agent initialized with email: %s", self.email)
    
    def process_tasks(self):
        """Process HR-specific tasks."""
        if self.config['capabilities']['message_handling']['enabled']:
            self._check_messages()
            
        if self.config['capabilities']['employee_concerns']['enabled']:
            self._handle_employee_concerns()
    
    def _check_messages(self):
        """Check and respond to HR-related messages."""
        self.logger.info("Starting message check cycle")
        try:
            employees = EmployeeRepository.get_all()
            hr_manager = next((emp for emp in employees if emp.role_id == self.role.id), None)
            if not hr_manager:
                self.logger.error("No employee found with HR Manager role")
                return
                
            messages = mailbox_models.get_messages(hr_manager.id)
            unread_messages = [msg for msg in messages if not msg[5]]
            self.logger.info("Found %d unread messages", len(unread_messages))

            for msg in unread_messages:
                msg_id, sender_name, subject, content, timestamp, _ = msg
                self.logger.info("Processing message from %s: %s", sender_name, subject)
                
                sender_employee = next((emp for emp in employees if f"{emp.first_name} {emp.last_name}" == sender_name), None)
                if not sender_employee:
                    self.logger.error("Could not find employee record for sender: %s", sender_name)
                    continue
                
                response = self._generate_hr_response(sender_name, subject, content)
                if response:
                    mailbox_models.add_message(
                        hr_manager.id,
                        sender_employee.id,
                        f"Re: {subject}",
                        response
                    )
                    mailbox_models.mark_as_read(msg_id)
                    self.logger.info("Successfully responded to message from %s", sender_name)
                else:
                    self.logger.warning("No response generated for message from %s", sender_name)

        except Exception as e:
            self.logger.error("Error in message check: %s", str(e), exc_info=True)
    
    def _generate_hr_response(self, sender: str, subject: str, content: str) -> Optional[str]:
        """Generate an HR-appropriate response using LLM."""
        try:
            prompt = self.config['llm_config']['prompt_templates']['message_response'].format(
                sender=sender,
                subject=subject,
                content=content
            )
            response = self.llm_client.prompt(prompt)
            return response.text()
        except Exception as e:
            self.logger.error("Error generating HR response: %s", str(e), exc_info=True)
            return None
    
    def _handle_employee_concerns(self):
        """Periodically check for employee concerns that need HR attention."""
        self.logger.info("Starting employee concerns check cycle")
        try:
            employees = EmployeeRepository.get_all()
            self.logger.info("Checking concerns for %d employees", len(employees))
            
            for employee in employees:
                if self._should_reach_out(employee):
                    self._generate_proactive_outreach(employee)
                    
        except Exception as e:
            self.logger.error("Error in employee concerns check: %s", str(e), exc_info=True)
    
    def _should_reach_out(self, employee) -> bool:
        """Determine if HR should proactively reach out to an employee."""
        # Implement logic based on config thresholds
        metrics = self.config['capabilities']['employee_concerns']['monitoring_metrics']
        thresholds = self.config['capabilities']['employee_concerns']['thresholds']
        
        # This is a placeholder - implement actual metric checking logic
        return False
    
    def _generate_proactive_outreach(self, employee):
        """Generate a proactive outreach message to an employee."""
        try:
            prompt = self.config['llm_config']['prompt_templates']['proactive_outreach'].format(
                employee_name=f"{employee.first_name} {employee.last_name}"
            )
            response = self.llm_client.prompt(prompt)
            
            mailbox_models.add_message(
                sender=self.email,
                recipient=employee.email,
                subject="HR Check-in",
                content=response.text()
            )
            self.logger.info("Sent proactive outreach to employee: %s %s", 
                           employee.first_name, employee.last_name)
        except Exception as e:
            self.logger.error("Error generating proactive outreach: %s", str(e), exc_info=True) 
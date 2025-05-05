import os
import sys
import logging
import threading
import time
import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from tickets import models as ticket_models

# Get logger for this module
logger = logging.getLogger(__name__)
logger.propagate = False  # Prevent propagation to root logger

@dataclass
class Customer:
    """Represents a customer in the system."""
    id: str
    name: str
    satisfaction_level: float  # 0.0 to 1.0
    last_ticket_time: Optional[datetime]
    ticket_frequency_hours: float  # Average hours between tickets
    priority_level: int  # 1-5, where 5 is highest priority

class CustomerAgent:
    def __init__(self, config_path: str = "agent/customer/config/customer_agent_config.json"):
        """Initialize the customer agent."""
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.interval_minutes = self.config['capabilities']['ticket_creation']['check_interval_minutes']
        self.thread = None
        self.running = False
        self._lock = threading.Lock()
        self.customers: Dict[str, Customer] = {}
        self._initialize_customers()

    def _load_config(self, config_path: str) -> Dict:
        """Load agent configuration from JSON file."""
        with open(config_path, 'r') as f:
            return json.load(f)

    def _setup_logging(self):
        """Configure logging based on agent config."""
        # Remove any existing handlers
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.handlers = []
        self.logger.propagate = False
        
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Create file handler
        handler = logging.FileHandler(self.config['logging']['file'])
        handler.setLevel(self.config['logging']['level'])
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(handler)
        self.logger.setLevel(self.config['logging']['level'])

    def _initialize_customers(self):
        """Initialize a set of default customers."""
        # Add some default customers with different characteristics
        self.customers = {
            "cust_001": Customer(
                id="cust_001",
                name="Enterprise Client A",
                satisfaction_level=0.8,
                last_ticket_time=None,
                ticket_frequency_hours=48.0,
                priority_level=5
            ),
            "cust_002": Customer(
                id="cust_002",
                name="Small Business B",
                satisfaction_level=0.6,
                last_ticket_time=None,
                ticket_frequency_hours=24.0,
                priority_level=3
            ),
            "cust_003": Customer(
                id="cust_003",
                name="Individual User C",
                satisfaction_level=0.9,
                last_ticket_time=None,
                ticket_frequency_hours=72.0,
                priority_level=1
            )
        }

    def _should_create_ticket(self, customer: Customer) -> bool:
        """Determine if a ticket should be created for this customer."""
        if not customer.last_ticket_time:
            return True
        
        hours_since_last_ticket = (datetime.now() - customer.last_ticket_time).total_seconds() / 3600
        return hours_since_last_ticket >= customer.ticket_frequency_hours

    def _adjust_satisfaction(self, customer: Customer, ticket_resolved: bool):
        """Adjust customer satisfaction based on ticket resolution."""
        if ticket_resolved:
            customer.satisfaction_level = min(1.0, customer.satisfaction_level + 0.1)
        else:
            customer.satisfaction_level = max(0.0, customer.satisfaction_level - 0.2)

    def check_and_create_tickets(self):
        """Check customers and create tickets as needed."""
        try:
            # Get current ticket counts
            status_counts = ticket_models.get_tickets_by_status()
            new_tickets_count = status_counts.get('New', 0)

            # Check each customer
            for customer in self.customers.values():
                if new_tickets_count >= 3:
                    break

                if self._should_create_ticket(customer):
                    new_ticket = ticket_models.check_new_tickets()
                    if new_ticket:
                        self.logger.info(f"Created new ticket for customer {customer.name}: {new_ticket['id']}")
                        customer.last_ticket_time = datetime.now()
                        new_tickets_count += 1
                    else:
                        self.logger.warning(f"Failed to create ticket for customer {customer.name}")

        except Exception as e:
            self.logger.error(f"Error in check_and_create_tickets: {e}")

    def run(self):
        """Main job loop."""
        self.logger.info("Customer agent started")
        while self.running:
            try:
                self.check_and_create_tickets()
                time.sleep(self.interval_minutes * 60)
            except Exception as e:
                self.logger.error(f"Error in customer agent: {e}")
                time.sleep(60)

    def start(self):
        """Start the customer agent."""
        with self._lock:
            if self.running:
                self.logger.warning("Customer agent is already running")
                return

            self.running = True
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()
            self.logger.info("Customer agent started")

    def stop(self):
        """Stop the customer agent."""
        with self._lock:
            if not self.running:
                self.logger.warning("Customer agent is not running")
                return

            self.running = False
            if self.thread:
                self.thread.join(timeout=5)
                self.thread = None
            self.logger.info("Customer agent stopped")

def init_customer_agent():
    """Initialize and start the customer agent."""
    agent = CustomerAgent()
    agent.start()
    return agent

def cleanup_customer_agent():
    """Clean up the customer agent."""
    agent = CustomerAgent()
    agent.stop() 
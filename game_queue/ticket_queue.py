import os
import sys
import logging
import threading
import time
from datetime import datetime
from tickets import models as ticket_models

logger = logging.getLogger(__name__)

class TicketQueueJob:
    def __init__(self, interval_minutes=2):
        """Initialize the ticket queue job."""
        self.interval_minutes = interval_minutes
        self.thread = None
        self.running = False
        self._lock = threading.Lock()

    def check_and_create_tickets(self):
        """Check the number of new tickets and create more if needed."""
        try:
            # Get ticket counts by status
            status_counts = ticket_models.get_tickets_by_status()
            new_tickets_count = status_counts.get('New', 0)

            # If we have less than 3 new tickets, create more
            while new_tickets_count < 3:
                new_ticket = ticket_models.check_new_tickets()
                if new_ticket:
                    logger.info(f"Created new ticket: {new_ticket['id']}")
                    new_tickets_count += 1
                else:
                    logger.warning("Did not create a new ticket this time.")
                    break

        except Exception as e:
            logger.error(f"Error in check_and_create_tickets: {e}")

    def run(self):
        """Main job loop."""
        logger.info("Ticket queue job started")
        while self.running:
            try:
                self.check_and_create_tickets()
                # Sleep for the specified interval
                time.sleep(self.interval_minutes * 60)
            except Exception as e:
                logger.error(f"Error in ticket queue job: {e}")
                time.sleep(60)  # Sleep for a minute before retrying

    def start(self):
        """Start the ticket queue job."""
        with self._lock:
            if self.running:
                logger.warning("Ticket queue job is already running")
                return

            self.running = True
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()
            logger.info("Ticket queue job started")

    def stop(self):
        """Stop the ticket queue job."""
        with self._lock:
            if not self.running:
                logger.warning("Ticket queue job is not running")
                return

            self.running = False
            if self.thread:
                self.thread.join(timeout=5)  # Wait up to 5 seconds for thread to finish
                self.thread = None
            logger.info("Ticket queue job stopped")

def init_ticket_queue():
    """Initialize and start the ticket queue job."""
    job = TicketQueueJob()
    job.start()
    return job

def cleanup_ticket_queue():
    """Clean up the ticket queue job."""
    job = TicketQueueJob()
    job.stop() 
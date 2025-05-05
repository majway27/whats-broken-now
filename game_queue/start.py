import os
import sys
import logging
from .simple_queue import GameEventQueue
import threading
import time
import queue as thread_queue

# Configure logging to write only to file
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'game_queue.log')

# Remove any existing handlers
logging.getLogger().handlers = []

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file)
    ]
)
logger = logging.getLogger(__name__)

class QueueManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QueueManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self.queue = GameEventQueue()
        self.processor_thread = None
        self.running = False
        self._initialized = True
        self.event_queue = thread_queue.Queue()  # Thread-safe queue for event processing

    def process_events(self):
        """Background thread to process events."""
        logger.info("Event processor started")
        while self.running:
            try:
                # Check for new events with a timeout
                try:
                    event = self.queue.get_next_event()
                    if event:
                        # Put event in thread-safe queue for processing
                        self.event_queue.put(event, timeout=0.1)
                except thread_queue.Full:
                    pass  # Queue is full, we'll process it next time

                # Process any events in the queue
                try:
                    while True:
                        event = self.event_queue.get_nowait()
                        logger.info(f"Processing event: {event['type']}")
                        self.handle_event(event)
                        self.queue.mark_event_processed(event['id'])
                        self.event_queue.task_done()
                except thread_queue.Empty:
                    pass  # No events to process

                # Short sleep to prevent CPU spinning
                time.sleep(0.1)
            except Exception as e:
                logger.error(f"Error processing event: {e}")
                time.sleep(1)

    def handle_event(self, event: dict):
        """Handle different types of game events."""
        event_type = event['type']
        data = event['data']
        
        try:
            if event_type == "ticket_submitted":
                logger.info(f"Processing ticket: {data['ticket_id']}")
                # Ticket processing will be handled by ticket_views
                
            elif event_type == "hardware_failure":
                logger.info(f"Processing hardware failure: {data['hardware_id']}")
                # Hardware failure will be handled by hardware_utils
                
            elif event_type == "admin_notification":
                logger.info(f"Processing admin notification: {data['message']}")
                # Admin notifications will be handled by admin_views
                
            else:
                logger.warning(f"Unknown event type: {event_type}")
        except Exception as e:
            logger.error(f"Error handling event {event_type}: {e}")

    def start(self):
        """Start the queue processor."""
        if self.processor_thread is not None:
            logger.warning("Queue processor is already running")
            return

        self.running = True
        self.processor_thread = threading.Thread(target=self.process_events, daemon=True)
        self.processor_thread.start()
        logger.info("Queue processor started")

    def stop(self):
        """Stop the queue processor."""
        if self.processor_thread is None:
            logger.warning("Queue processor is not running")
            return

        self.running = False
        # Wait for any remaining events to be processed
        try:
            self.event_queue.join(timeout=5)  # Wait up to 5 seconds for events to finish
        except Exception:
            pass
        self.processor_thread.join(timeout=1)  # Wait up to 1 second for thread to finish
        self.processor_thread = None
        logger.info("Queue processor stopped")

    def add_event(self, event_type: str, data: dict, priority: int = 0) -> int:
        """Add a new event to the queue."""
        return self.queue.add_event(event_type, data, priority)

def init_queue():
    """Initialize the queue system."""
    manager = QueueManager()
    manager.start()
    return manager

def cleanup_queue():
    """Clean up the queue system."""
    manager = QueueManager()
    manager.stop()
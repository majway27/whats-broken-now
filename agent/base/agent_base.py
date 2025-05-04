import json
import logging
import threading
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any

class BaseAgent(ABC):
    def __init__(self, config_path: str):
        """Initialize the base agent with configuration."""
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.thread = None
        self.running = False
        self._lock = threading.Lock()
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load agent configuration from JSON file."""
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def _setup_logging(self):
        """Configure logging based on agent config."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(self.config['logging']['level'])
        self.logger.propagate = False
        
        # Create logs directory if it doesn't exist
        Path('logs').mkdir(exist_ok=True)
        
        # Create file handler
        handler = logging.FileHandler(self.config['logging']['file'])
        handler.setLevel(self.config['logging']['level'])
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(handler)
    
    @abstractmethod
    def initialize(self):
        """Initialize agent-specific resources and connections."""
        pass
    
    @abstractmethod
    def process_tasks(self):
        """Process agent-specific tasks."""
        pass
    
    def run(self):
        """Main agent loop."""
        self.logger.info("Starting agent main loop")
        while self.running:
            try:
                self.logger.debug("Starting new agent cycle")
                self.process_tasks()
                self.logger.debug("Agent cycle completed")
                time.sleep(self.config['capabilities']['message_handling']['check_interval_minutes'] * 60)
            except Exception as e:
                self.logger.error("Error in agent main loop: %s", str(e), exc_info=True)
                time.sleep(60)
    
    def start(self):
        """Start the agent."""
        with self._lock:
            if self.running:
                self.logger.warning("Attempted to start agent while already running")
                return
            
            self.logger.info("Starting agent")
            self.running = True
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()
            self.logger.info("Agent thread started successfully")
    
    def stop(self):
        """Stop the agent."""
        with self._lock:
            if not self.running:
                self.logger.warning("Attempted to stop agent while not running")
                return
            
            self.logger.info("Stopping agent")
            self.running = False
            if self.thread:
                self.thread.join(timeout=5)
                self.thread = None
            self.logger.info("Agent stopped successfully") 
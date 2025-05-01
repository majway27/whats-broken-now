# WBN Game Queue System

A simple SQLite-based queue system for handling asynchronous game events. This system provides a lightweight way to manage game events without requiring additional services like Redis or Celery.

## Features

- SQLite-based event storage
- Priority-based event processing
- Thread-safe operations
- Automatic cleanup of old events
- Simple API for adding and processing events

## Usage

```python
from simple_queue import GameEventQueue

# Create queue
queue = GameEventQueue("game_events.db")

# Add an event
queue.add_event("ticket_submitted", {
    "ticket_id": "T123",
    "title": "Server Down",
    "priority": "high"
}, priority=2)

# Process events in background
def process_events():
    while True:
        event = queue.get_next_event()
        if event:
            # Handle the event
            handle_event(event)
            queue.mark_event_processed(event['id'])
        else:
            time.sleep(0.1)

# Start processor in background thread
import threading
processor = threading.Thread(target=process_events, daemon=True)
processor.start()
```

## Event Types

The system supports any type of game event. Common examples include:

1. **Player Actions**
   - Ticket submissions
   - Quest completions
   - NPC interactions

2. **Game Events**
   - World state changes
   - Quest updates
   - NPC behavior changes

3. **System Events**
   - Data cleanup
   - Periodic updates
   - State synchronization

## Priority Levels

Events can be assigned priority levels (higher numbers = higher priority):
- 2: Critical events (e.g., server issues)
- 1: Important events (e.g., NPC interactions)
- 0: Regular events (e.g., quest updates)

## Database Structure

Events are stored in a SQLite database with the following structure:
- `id`: Unique event identifier
- `event_type`: Type of event
- `priority`: Event priority
- `data`: JSON-encoded event data
- `created_at`: Event creation timestamp
- `processed_at`: Event processing timestamp
- `status`: Event status (pending/completed/failed)

## Error Handling

The system includes basic error handling:
- Thread-safe operations
- Event status tracking
- Failed event marking

## Maintenance

The system includes automatic cleanup of old events:
```python
# Clean up events older than 30 days
queue.cleanup_old_events(days=30)
``` 
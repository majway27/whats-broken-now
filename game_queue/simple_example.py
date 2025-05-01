from simple_queue import GameEventQueue
import time
import threading

def process_events(queue: GameEventQueue):
    """Background thread to process events."""
    while True:
        event = queue.get_next_event()
        if event:
            print(f"Processing event: {event['type']}")
            # Simulate event processing
            time.sleep(1)
            queue.mark_event_processed(event['id'])
        else:
            time.sleep(0.1)  # Wait a bit before checking again

def main():
    # Create queue
    queue = GameEventQueue("game_events.db")
    
    # Start event processor in background
    processor = threading.Thread(target=process_events, args=(queue,), daemon=True)
    processor.start()
    
    # Add some example events
    queue.add_event("ticket_submitted", {
        "ticket_id": "T123",
        "title": "Server Down",
        "priority": "high"
    }, priority=2)
    
    queue.add_event("npc_interaction", {
        "npc_id": "M456",
        "type": "performance_review",
        "rating": 4
    }, priority=1)
    
    queue.add_event("quest_update", {
        "quest_id": "Q789",
        "status": "in_progress",
        "progress": 50
    }, priority=0)
    
    # Wait for events to be processed
    time.sleep(5)
    
    # Show pending events
    print("\nPending events:")
    for event in queue.get_pending_events():
        print(f"- {event['type']} (Priority: {event['priority']})")
    
    # Cleanup old events
    queue.cleanup_old_events(days=30)

if __name__ == "__main__":
    main() 
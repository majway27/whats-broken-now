from tasks import (
    process_player_action,
    handle_npc_interaction,
    update_quest_status,
    process_ticket_update,
    cleanup_old_data,
    generate_world_events
)

def example_usage():
    """Example of how to use the queue system."""
    
    # Process a player action (high priority)
    result = process_player_action.delay(
        action_type="submit_ticket",
        player_id="player_123",
        ticket_data={"title": "Server Down", "priority": "high"}
    )
    print(f"Player action task ID: {result.id}")
    
    # Handle an NPC interaction (high priority)
    result = handle_npc_interaction.delay(
        npc_id="manager_456",
        interaction_type="performance_review",
        review_data={"rating": 4, "feedback": "Good work!"}
    )
    print(f"NPC interaction task ID: {result.id}")
    
    # Update a quest (default priority)
    result = update_quest_status.delay(
        quest_id="quest_789",
        status="in_progress",
        progress=50
    )
    print(f"Quest update task ID: {result.id}")
    
    # Process a ticket update (default priority)
    result = process_ticket_update.delay(
        ticket_id="ticket_101",
        update_type="status_change",
        new_status="resolved"
    )
    print(f"Ticket update task ID: {result.id}")
    
    # Schedule cleanup (low priority)
    result = cleanup_old_data.delay(days=30)
    print(f"Cleanup task ID: {result.id}")
    
    # Generate world events (low priority)
    result = generate_world_events.delay()
    print(f"World events task ID: {result.id}")

if __name__ == "__main__":
    example_usage() 
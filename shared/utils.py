def generate_snarky_goodbye():
    """Generate a snarky goodbye message from a coworker."""
    messages = [
        "Finally! I was starting to think you'd never leave.",
        "Don't let the door hit you on the way out! Just kidding... or am I?",
        "Leaving already? But who will I blame for all the bugs now?",
        "See you tomorrow! Unless you're working from home... again.",
        "Another day, another dollar... that you're taking home while I'm still here.",
        "Don't forget to take your coffee mug! (The one you never wash)",
        "Bye! Try not to break anything on your way out.",
    ]
    import random
    return random.choice(messages) 
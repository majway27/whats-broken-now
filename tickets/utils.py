import random
import llm
import sqlite3

# Initialize LLM client
client = llm.get_model("mistral-7b-instruct-v0")

def generate_reporter_comment(hardware_item):
    """Generate an entertaining reporter comment with a misunderstanding about the hardware."""
    # Get hardware specs from database
    conn = sqlite3.connect('hardware/hardware_catalog.db')
    c = conn.cursor()
    
    c.execute("""
        SELECT spec_name, spec_value
        FROM hardware_specs hs
        JOIN hardware_items hi ON hs.hardware_id = hi.id
        WHERE hi.name = ? AND hi.manufacturer = ? AND hi.model = ?
    """, (hardware_item['name'], hardware_item['manufacturer'], hardware_item['model']))
    
    specs = dict(c.fetchall())
    conn.close()
    
    prompt = f"""Create a short, entertaining report about a malfunctioning {hardware_item['name']} ({hardware_item['model']}).
    The reporter should misunderstand one of the technical specifications or features of the device.
    Include a brief history of how they acquired the device and their experience with it.
    Make it humorous but realistic.
    Keep it under 200 words."""
    
    try:
        response = client.prompt(prompt)
        return response.text()
    except Exception as e:
        return f"Error generating comment: {str(e)}"

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
        "Leaving at a reasonable hour? That's not like you.",
        "Don't worry about the tickets, I'll just... handle them all myself.",
        "See you tomorrow! Unless you're 'working from home' again.",
        "Another day, another ticket you didn't close.",
        "Don't let the bed bugs bite! (They're probably in your desk chair anyway)",
        "Bye! Try not to think about work... too much.",
        "Leaving already? But who will I steal snacks from now?",
        "Don't forget to set your out of office message... again."
    ]
    return random.choice(messages) 
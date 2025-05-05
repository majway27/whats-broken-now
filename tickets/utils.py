import random
import llm
import sqlite3
import os

# Get the directory where this module is located
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
HARDWARE_DB_PATH = os.path.join(MODULE_DIR, '..', 'hardware', 'hardware_catalog.db')

# Initialize LLM client
client = llm.get_model("mistral-7b-instruct-v0")

# TODO: Migrate this to customer_agent.py
def generate_reporter_comment(hardware_item):
    """Generate an entertaining reporter comment with a misunderstanding about the hardware."""
    # Get hardware specs from database
    conn = sqlite3.connect(HARDWARE_DB_PATH)
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

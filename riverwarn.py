import requests
from colorama import Fore, init
import json
import sqlite3
from datetime import datetime

# Initialize colorama for colored terminal output
init()

# Constants
CONFIG_FILE = "rivers.json"
DB_FILE = "river_data.db"

def setup_database():
    """Set up SQLite database to store river stage history."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS stages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            river TEXT NOT NULL,
            stage REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def load_config():
    """Load river configuration from JSON file."""
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading config: {e}")
        return []

def fetch_river_stage(gage_id):
    """Fetch current river stage from USGS NWIS API."""
    url = f"https://waterservices.usgs.gov/nwis/iv/?format=json&sites={gage_id}¶meterCd=00065"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        stage = data["value"]["timeSeries"][0]["values"][0]["value"][0]["value"]
        return float(stage)
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Error fetching data for gage {gage_id}: {e}")
        return None

def save_to_db(river, stage):
    """Save river stage data to SQLite database."""
    timestamp = datetime.now().isoformat()
    conn = sqlite3.connect(DB_FILE)
    conn.execute("INSERT INTO stages (river, stage, timestamp) VALUES (?, ?, ?)",
                 (river, stage, timestamp))
    conn.commit()
    conn.close()

def display_status(river, stage, flood_stage):
    """Display river status with color-coded output."""
    if stage is None:
        print(f"{Fore.WHITE}{river}: Data unavailable{Fore.RESET}")
    elif stage >= flood_stage:
        color = Fore.RED
        status = "FLOODING"
    elif stage >= flood_stage * 0.9:
        color = Fore.YELLOW
        status = "NEAR FLOOD"
    else:
        color = Fore.GREEN
        status = "SAFE"
    print(f"{color}{river}: {stage} ft (Flood: {flood_stage} ft) - {status}{Fore.RESET}")

def riverwarn():
    """Main function to run the river warning system."""
    # Set up database
    setup_database()

    # Load river configurations
    rivers = load_config()
    if not rivers:
        print("No rivers to monitor. Check rivers.json.")
        return

    # Process each river
    for river in rivers:
        stage = fetch_river_stage(river["gage_id"])
        if stage is not None:
            save_to_db(river["name"], stage)
        display_status(river["name"], stage, river["flood_stage"])

if __name__ == "__main__":
    riverwarn()
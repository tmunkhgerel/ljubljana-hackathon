import sys
from flask import Flask
import pandas as pd

app = Flask(__name__)

# This is your Digital Water Treaty Database
treaty_data = {
    "region": ["Dubai", "Al Ain", "Abu Dhabi"],
    "priority": ["Tourism", "Agriculture", "Groundwater"],
    "max_wind_threshold": [15, 25, 20] # km/h
}

df_treaty = pd.DataFrame(treaty_data)

@app.route('/')
def home():
    return "AI Rain-Mediator: System Online. Water Treaty Loaded."

if __name__ == "__main__":
    print(f"Using Python from: {sys.executable}")
    print("Treaty Rules Loaded:")
    print(df_treaty)

# The "Digital Water Treaty" Ruleset
REGIONS = {
    "Dubai": {"priority": "Tourism", "max_wind": 15, "risk_sector": "Urban Flooding"},
    "Al Ain": {"priority": "Agriculture", "max_wind": 30, "risk_sector": "Crop Damage"},
    "Abu Dhabi": {"priority": "Infrastructure", "max_wind": 20, "risk_sector": "Groundwater"}
}

def check_seeding_legality(source_region, wind_speed, wind_direction):
    """
    source_region: Where they want to seed (e.g., "Al Ain")
    wind_speed: current speed in km/h
    wind_direction: "NW", "SE", etc.
    """
    
    # Simple logic: If seeding in Al Ain and wind is North-West, it hits Dubai.
    if source_region == "Al Ain" and wind_direction == "NW":
        affected_region = "Dubai"
        
        # Check if the wind speed exceeds Dubai's Treaty threshold
        if wind_speed > REGIONS[affected_region]["max_wind"]:
            return {
                "status": "VETOED",
                "reason": f"Trans-boundary risk: Seeding in {source_region} will cause {REGIONS[affected_region]['risk_sector']} in {affected_region}.",
                "law_clause": "Article 4: Atmospheric Sovereignty"
            }
            
    return {"status": "APPROVED", "reason": "No trans-boundary conflict detected."}

# Test the AI
result = check_seeding_legality("Al Ain", 22, "NW")
print(f"AI DECISION: {result['status']} | {result['reason']}")
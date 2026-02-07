from flask import Flask, render_template_string, request
import datetime

app = Flask(__name__)

# --- THE TREATY DATABASE ---
LOGS = []

# --- THE UPGRADED DASHBOARD ---
@app.route('/')
def dashboard():
    # --- 1. PULL LIVE DATA ---
    API_KEY = "YOUR_ACTUAL_API_KEY" 
    city = "Al Ain"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        wind_speed_kmh = data['wind']['speed'] * 3.6
        wind_deg = data['wind']['deg']
    except Exception as e:
        # Fallback if API is down or Key is missing
        wind_speed_kmh, wind_deg = 18.5, 165 

    # --- 2. TREATY LOGIC ---
    # NW winds (270-360) blow from the Gulf; SE winds (135-225) blow toward the coast (Dubai)
    is_vetoed = (135 <= wind_deg <= 225) and (wind_speed_kmh > 15)
    decision = "VETOED" if is_vetoed else "APPROVED"
    color = "#ff4b2b" if is_vetoed else "#00c851"
    clause = "ARTICLE 7: TRANS-BOUNDARY RISK" if is_vetoed else "ARTICLE 1: RESOURCE ENHANCEMENT"

    # --- 3. THE UI (With SVG Compass) ---
    html = f'''
    <body style="font-family: 'Courier New', monospace; background: #0a0a0a; color: #00ff41; padding: 40px; text-align: center;">
        <h1 style="text-shadow: 0 0 10px #00ff41;">> RAIN-MEDIATOR_OS</h1>
        
        <div style="margin: 20px auto; width: 100px; height: 100px; border-radius: 50%; border: 2px solid #00ff41; position: relative; display: inline-block;">
            <div style="width: 2px; height: 50px; background: #ff4b2b; position: absolute; left: 49%; transform-origin: bottom; transform: rotate({wind_deg}deg);"></div>
            <p style="font-size: 10px; margin-top: 110px;">WIND VECTOR: {wind_deg}°</p>
        </div>

        <div style="margin-top: 20px; border: 1px solid #00ff41; padding: 20px; display: inline-block; background: rgba(0,255,65,0.05);">
            <h3>SENSORS: {city.upper()}</h3>
            <p>WIND VELOCITY: {wind_speed_kmh:.1f} KM/H</p>
            <hr style="border-color: #00ff41;">
            <h2 style="color: {color};">STATUS: {decision}</h2>
            <p style="font-size: 0.8em;">Citing: {clause}</p>
        </div>
    </body>
    '''
    return render_template_string(html)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

def mediator_logic(source_name, wind_speed, wind_deg):
    if source_name == "Al Ain" and (135 <= wind_deg <= 225):
        if wind_speed > 15:
            return {
                "status": "VETOED",
                "clause": "ARTICLE 7: TRANS-BOUNDARY FLOOD PREVENTION",
                "detail": "Projected precipitation path intersects Dubai Urban Zone."
            }
    return {
        "status": "APPROVED",
        "clause": "ARTICLE 1: SOVEREIGN RESOURCE ENHANCEMENT",
        "detail": "Atmospheric conditions stable for localized recharge."
    }

# 2. The "Pre-Law" UI with the SVG Compass
    html = f'''
    <body style="font-family: 'Courier New', Courier, monospace; background: #0f0f0f; color: #00ff41; padding: 40px; text-align: center;">
        <h1 style="text-shadow: 0 0 10px #00ff41;">> RAIN-MEDIATOR_OS v1.0.4</h1>
        
        <div style="margin: 20px auto; width: 100px; height: 100px; border-radius: 50%; border: 2px solid #00ff41; position: relative; display: inline-block;">
            <div style="width: 2px; height: 50px; background: #ff4b2b; position: absolute; left: 49%; transform-origin: bottom; transform: rotate({wind_deg}deg);"></div>
            <p style="font-size: 10px; margin-top: 110px;">WIND VECTOR</p>
        </div>

        <div style="display: flex; gap: 20px; justify-content: center; margin-top: 20px;">
            <div style="border: 1px solid #00ff41; padding: 20px; width: 400px; background: rgba(0,255,65,0.05);">
                <h3>LIVE SENSOR DATA</h3>
                <p>TARGET: Al Ain | WIND: {wind_speed}km/h at {wind_deg}°</p>
                <h2 style="color: {color};">STATUS: {decision}</h2>
            </div>
        </div>
    </body>
    '''
    return render_template_string(html)
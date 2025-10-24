import os
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()  # loads .env

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise RuntimeError("Please set OPENWEATHER_API_KEY in your .env file")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/weather")
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error":"Missing 'city' parameter"}), 400

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # use "imperial" for °F
    }

    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
    except requests.RequestException as e:
        return jsonify({"error":"Failed to reach weather service", "details": str(e)}), 502

    if resp.status_code != 200:
        # forward the message (city not found, etc.)
        try:
            data = resp.json()
        except Exception:
            data = {"message": resp.text}
        return jsonify({"error": "Weather API error", "details": data}), resp.status_code

    data = resp.json()
    # extract useful bits
    result = {
        "city": data.get("name"),
        "country": data.get("sys", {}).get("country"),
        "temp": data.get("main", {}).get("temp"),
        "feels_like": data.get("main", {}).get("feels_like"),
        "humidity": data.get("main", {}).get("humidity"),
        "pressure": data.get("main", {}).get("pressure"),
        "wind_speed": data.get("wind", {}).get("speed"),
        "description": data.get("weather", [{}])[0].get("description"),
        "icon": data.get("weather", [{}])[0].get("icon")  # icon code for OpenWeatherMap
    }
    return jsonify(result)

if __name__ == "__main__":
    # for local development only
    app.run(host="127.0.0.1", port=5000, debug=True)

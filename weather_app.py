import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Check if API key is missing
if not API_KEY:
    st.error("⚠️ Please set your OPENWEATHER_API_KEY in a .env file.")
    st.stop()

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Streamlit page setup
st.set_page_config(page_title="🌤️ Live Weather App", page_icon="🌦️", layout="centered")

st.markdown("<h1 style='text-align:center;'>🌤️ Live Weather App</h1>", unsafe_allow_html=True)

# City input
city = st.text_input("Enter City Name", placeholder="e.g. Karachi, London, Dubai")

# Fetch weather button
if st.button("Get Weather"):
    if not city:
        st.warning("Please enter a city name.")
    else:
        with st.spinner("Fetching weather data..."):
            params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }
            try:
                resp = requests.get(BASE_URL, params=params, timeout=10)
                if resp.status_code != 200:
                    st.error("City not found or invalid API key.")
                else:
                    data = resp.json()
                    st.success(f"✅ Weather in {data['name']}, {data['sys']['country']}")
                    icon = data["weather"][0]["icon"]
                    description = data["weather"][0]["description"].title()
                    temp = data["main"]["temp"]
                    feels = data["main"]["feels_like"]
                    humidity = data["main"]["humidity"]
                    wind = data["wind"]["speed"]

                    # Display weather info
                    st.image(f"https://openweathermap.org/img/wn/{icon}@2x.png")
                    st.markdown(f"### 🌡 Temperature: `{temp}°C` (Feels like `{feels}°C`)")
                    st.markdown(f"### 💧 Humidity: `{humidity}%`")
                    st.markdown(f"### 💨 Wind Speed: `{wind} m/s`")
                    st.markdown(f"### ☁️ Description: `{description}`")

            except requests.RequestException as e:
                st.error(f"Error fetching weather data: {e}")

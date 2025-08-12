import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Page setup
st.title("DelFloods")
st.write("🌧️ Welcome to our flood prediction model")

def train_model():
    df = pd.read_csv("new_csv.csv")
    X = df[['precip', 'River_Level', 'temp', 'humidity', 'windspeed']]
    y = df['Flood']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)
    return model, accuracy

# Train model
model, accuracy = train_model()
## st.write("✅ Model accuracy on test data:", accuracy)

# Input for river level
river_level = st.number_input("🌊 Enter current river level (in meters):", min_value=0.0, step=0.1)

# ✅ Function to safely fetch weather data
def fetch_weather_data():
    location = "Delhi,IN"
    today = datetime.now().strftime("%Y-%m-%d")
    api_key = "HC8QD5Y25CNY89PCZB3643W4X"

    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{today}/{today}"
    params = {
        "unitGroup": "metric",
        "include": "days",
        "key": api_key,
        "contentType": "json"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "days" in data and len(data["days"]) > 0:
            today_data = data["days"][0]
            return {
                "precip": today_data.get("precip") or 0.0,
                "temp": today_data.get("temp") or 0.0,
                "humidity": today_data.get("humidity") or 0.0,
                "windspeed": today_data.get("windspeed") or 0.0
            }
    return None

# Get weather
weather = fetch_weather_data()

# Make prediction if both inputs are ready
if weather and river_level:
    st.subheader("📊 Today's Weather Data:")
    st.json(weather)

    # Data for model prediction
    input_data = pd.DataFrame([{
        'precip': weather['precip'],
        'River_Level': river_level,
        'temp': weather['temp'],
        'humidity': weather['humidity'],
        'windspeed': weather['windspeed']
    }])

    # ----- Rule-based check -----
    if river_level > 205.55:
        rule_alert = "WILL occur"
        rule_flag = 2
    elif river_level > 202:
        rule_alert = "MAY occur"
        rule_flag = 1
    else:
        rule_alert = "NOT expected"
        rule_flag = 0

    # ----- Model prediction -----
    model_pred = model.predict(input_data)[0]  # 1 = flood likely, 0 = no flood

    # ----- Combined decision -----
    st.subheader("🚨 Final Flood Risk Decision:")
    if rule_flag == 1 or model_pred == 1 or rule_flag == 2 or model_pred == 2:
        st.error(f"Flood Likely! (Rule: {rule_alert}, Model: {'Likely' if model_pred == 1 or model_pred == 2 else 'Unlikely'})")
    else:
        st.success(f"No Flood Expected. (Rule: {rule_alert}, Model: {'Likely' if model_pred == 1 or model_pred == 2 else 'Unlikely'})")




















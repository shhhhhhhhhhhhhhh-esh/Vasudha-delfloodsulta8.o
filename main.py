import streamlit as st
st.title("DelFloods")
st.write("Welcome to our flood prediction model")

import pandas as pd
from meteostat import Point, Daily
from datetime import datetime
import os
import http.client

conn = http.client.HTTPSConnection("meteostat.p.rapidapi.com")


print("\n🔎 Enter today's weather details to predict flood risk:")


def fetch_weather_data():
    # Define location (Delhi)
    delhi = Point(28.61, 77.23)

    # Define the current date
    today = datetime.now()

    # Get daily weather data for today
    data = Daily(delhi, today, today)
    data = data.fetch()

    if data.empty:
        print("No weather data available for today.")
        return

    # Extract relevant weather information
    weather_row = {
        'datetime': today.isoformat(),
        'temp': data['tavg'].values[0],
        'precip': data['prcp'].values[0],
        'wind_speed': data['wspd'].values[0]
    }

    df = pd.DataFrame([weather_row])

    # Check if the file exists
    file_exists = os.path.isfile('weather_data.csv')

    # Save to CSV (append mode)
    df.to_csv('weather_data.csv', mode='a', header=not file_exists, index=False)

# Format the input as a DataFrame
new_data = pd.DataFrame([{
    'precip': prcp,
    'River_Level': river_level,
    'Temp': temp,
    'Humidity': humidity,
    'wind_speed': wind_speed
}])

# Predict
prediction = model.predict(new_data)

# Show result and button
if st.button("Submit"):
    st.write("\n📢 Prediction based on your input:")
    if prediction[0] == 2:
        st.write("➡️ FLOOD ⚠️")
    elif prediction[0] == 1:
        st.write("➡️ MAY FLOOD ⚠️")
    else:
        st.write("➡️ NO FLOOD ✅")













import streamlit as st
st.title("DelFloods")
st.write("Welcome to our flood prediction model")

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

from meteostat import Point, Daily
from datetime import datetime
import os
import http.client

conn = http.client.HTTPSConnection("meteostat.p.rapidapi.com")
# 2. Features and target
X = df[['Rainfall', 'River_Level', 'Temp', 'Humidity', 'Wind']]
y = df['Flood']

# 3. Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train the model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# 5. Predict and evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

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
    'precip': precip,
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










import streamlit as st
import numpy as np
import pickle

# Load your saved model
with open('random-forest.pkl', 'rb') as f:
    model = pickle.load(f)

st.title("🌿 Air Quality Index (AQI) Predictor")

st.write("""
Enter the pollutant levels below to get the predicted AQI.
""")

# Define pollutant features and their ranges (adjust as needed)
pollutants = {
    "PM2.5": (0, 500),
    "PM10": (0, 600),
    "NO": (0, 200),
    "NO2": (0, 300),
    "NOx": (0, 400),
    "NH3": (0, 200),
    "CO": (0, 20),
    "SO2": (0, 200)
}

# Create sliders for input with units added in label and decimal support
inputs = []
for pollutant, (min_val, max_val) in pollutants.items():
    default_val = (min_val + max_val) / 10  # default value as float
    val = st.slider(
        f"{pollutant} concentration (µg/m³)",
        float(min_val),
        float(max_val),
        float(default_val),
        step=0.1
    )
    inputs.append(val)

# Convert to numpy array and reshape for prediction
input_array = np.array(inputs).reshape(1, -1)

# Prediction button
if st.button("Predict AQI"):
    aqi = model.predict(input_array)[0]
    st.write(f"### Predicted AQI: {aqi:.2f}")

    # Color-coded message based on AQI ranges
    if aqi <= 50:
        st.success("Good — Air quality is satisfactory.")
    elif aqi <= 100:
        st.warning("Moderate — Acceptable, but sensitive people should be cautious.")
    elif aqi <= 150:
        st.error("Unhealthy for Sensitive Groups — People with health issues should limit exposure.")
    elif aqi <= 200:
        st.error("Unhealthy — Everyone may begin to experience health effects.")
    elif aqi <= 300:
        st.error("Very Unhealthy — Health alert, everyone should avoid prolonged exposure.")
    else:
        st.error("Hazardous — Emergency conditions, stay indoors.")

    # Optional: Show health tips based on AQI
    st.markdown("---")
    st.subheader("Health Tips")
    if aqi <= 50:
        st.write("Enjoy outdoor activities!")
    elif aqi <= 100:
        st.write("Consider reducing prolonged outdoor exertion.")
    elif aqi <= 150:
        st.write("Sensitive groups should limit outdoor activities.")
    elif aqi <= 200:
        st.write("Limit outdoor activities for everyone.")
    elif aqi <= 300:
        st.write("Avoid outdoor activities, especially strenuous ones.")
    else:
        st.write("Stay indoors and use air purifiers if possible.")

# Pollutant definitions toggle
with st.expander("Pollutant Definitions"):
    st.write("""
    - **PM2.5:** Fine particulate matter ≤2.5 micrometers.  
    - **PM10:** Particulate matter ≤10 micrometers.  
    - **NO:** Nitric oxide gas.  
    - **NO2:** Nitrogen dioxide gas.  
    - **NOx:** Nitrogen oxides (NO + NO2).  
    - **NH3:** Ammonia gas.  
    - **CO:** Carbon monoxide gas.  
    - **SO2:** Sulfur dioxide gas.  
    """)


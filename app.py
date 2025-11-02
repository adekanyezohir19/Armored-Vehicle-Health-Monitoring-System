import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Armored Vehicle Health Dashboard", layout="wide")

st.title("🛡️ Armored Vehicle Health Monitoring System")
st.subheader("Developed by: Adekanye Abdulzohir Oyetosade")

# Sidebar Inputs
st.sidebar.header("Vehicle Telemetry Input")
engine_temp = st.sidebar.slider("Engine Temperature (°C)", 50, 150, 80)
battery_voltage = st.sidebar.slider("Battery Voltage (V)", 10.0, 30.0, 24.0)
tire_pressure = st.sidebar.slider("Tire Pressure (PSI)", 20, 50, 35)
fuel_level = st.sidebar.slider("Fuel Level (%)", 0, 100, 60)

# Display Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Engine Temperature", f"{engine_temp} °C")
col2.metric("Battery Voltage", f"{battery_voltage} V")
col3.metric("Tire Pressure", f"{tire_pressure} PSI")
col4.metric("Fuel Level", f"{fuel_level} %")

st.divider()

# Status Logic
if engine_temp > 120:
    st.error("⚠️ Engine Overheating Detected!")
elif fuel_level < 15:
    st.warning("⛽ Low Fuel - Refill Required")
else:
    st.success("✅ Vehicle Status: Normal Operation")

# Data Simulation
data = pd.DataFrame({
    'Time': range(1, 11),
    'Engine Temp (°C)': np.random.randint(80, 130, 10),
    'Battery Voltage (V)': np.random.uniform(22, 26, 10)
})
st.line_chart(data.set_index('Time'))

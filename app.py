# app.py
# AVHMS Dashboard - styled to match the screenshot design (percent display for fuel)
# Developed by:  Adekanye Abdulzohir Oyetosade

import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="AVHMS Dashboard", layout="wide", initial_sidebar_state="expanded")

# -----------------------
# Header (title + credit)
# -----------------------
st.markdown("""
<div style="display:flex;align-items:center;gap:16px">
  <div style="font-size:28px;font-weight:700;color:#1a365d">🛡️ Armored Vehicle Health Monitoring System</div>
</div>
""", unsafe_allow_html=True)

st.markdown("**Developed by:**Adekanye Abdulzohir Oyetosade")
st.markdown("---")

# -----------------------
# Sidebar controls
# -----------------------
st.sidebar.header("Vehicle Controls")
vehicle_id = st.sidebar.text_input("Vehicle ID", value="AV-2025-01")
mission_status = st.sidebar.selectbox("Mission Status", ["Active", "Standby", "Maintenance"])
connection = st.sidebar.selectbox("Connection Type", ["Local", "GSM", "Satellite"])
auto_stream = st.sidebar.checkbox("Auto simulate stream", value=True)
refresh_seconds = st.sidebar.slider("Refresh rate (s)", 1, 10, 3)

# -----------------------
# Small CSS for cards
# -----------------------
card_css = """
<style>
.card {
  border-radius:8px;
  padding:18px;
  background-color: #ffffff;
  box-shadow: 0 1px 4px rgba(20,40,80,0.08);
  border: 1px solid rgba(20,40,80,0.06);
}
.kpi-title { color:#444; font-size:14px; }
.kpi-value { color:#1a365d; font-size:34px; font-weight:700; }
.status-box { border-radius:8px; padding:16px; background-color:#f7fbff; border:1px solid rgba(20,40,80,0.04);}
.small-muted { color:#666; font-size:13px; }
</style>
"""
st.markdown(card_css, unsafe_allow_html=True)

# -----------------------
# Generate (or get) telemetry
# -----------------------
def gen_telemetry(vehicle_id, connection):
    """Simulated telemetry record (replace with real data feed later)."""
    ts = datetime.utcnow().isoformat() + "Z"
    engine_temp = round(np.random.normal(loc=88, scale=6), 2)
    battery_v = round(np.random.normal(loc=12.4, scale=0.4), 2)
    tire_psi = round(np.random.normal(loc=33.2, scale=1.2), 2)
    fuel_pct = float(np.clip(np.random.normal(loc=60, scale=20), 0, 100))
    armor_integrity = float(np.clip(np.random.normal(loc=92, scale=6), 0, 100))
    conn = connection
    alerts = []
    if engine_temp > 110:
        alerts.append("ENGINE_OVERTEMP")
    if battery_v < 11.8:
        alerts.append("LOW_BATTERY")
    if fuel_pct < 15:
        alerts.append("LOW_FUEL")
    if armor_integrity < 80:
        alerts.append("ARMOR_IMPACT")
    return {
        "vehicleId": vehicle_id, "ts": ts,
        "metrics": {
            "engineTemp": engine_temp,
            "batteryV": battery_v,
            "tirePSI": tire_psi,
            "fuelPct": round(fuel_pct,2),
            "armorIntegrity": round(armor_integrity,2)
        },
        "alerts": alerts,
        "conn": conn
    }

# initialize history in session state
if "history" not in st.session_state:
    st.session_state.history = []

# auto-stream insert
if auto_stream:
    telemetry = gen_telemetry(vehicle_id, connection)
    st.session_state.history.insert(0, telemetry)
    st.session_state.history = st.session_state.history[:300]
else:
    if not st.session_state.history:
        # pre-seed a few records for chart
        for _ in range(6):
            st.session_state.history.insert(0, gen_telemetry(vehicle_id, connection))

# -----------------------
# Layout: KPI row (4 cards)
# -----------------------
kpi_row = st.container()
with kpi_row:
    col1, col2, col3, col4 = st.columns(4, gap="large")
    latest = st.session_state.history[0] if st.session_state.history else gen_telemetry(vehicle_id, connection)
    m = latest["metrics"]
    # Engine Temp
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-title">Engine Temperature</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-value">{m["engineTemp"]:.2f} °C</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    # Battery
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-title">Battery Voltage (V)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-value">{m["batteryV"]:.2f} V</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    # Tire Pressure
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-title">Tire Pressure (PSI)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-value">{m["tirePSI"]:.2f}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    # Fuel percent (show as percent + progress bar)
    with col4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-title">Fuel Level (%)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-value">{m["fuelPct"]:.2f} %</div>', unsafe_allow_html=True)
        st.progress(int(m["fuelPct"]))
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# -----------------------
# Main content (status left / chart right)
# -----------------------
left_col, right_col = st.columns([1.6, 1], gap="large")

# Left: Status block (alerts + details)
with left_col:
    st.markdown('<div class="status-box">', unsafe_allow_html=True)
    st.markdown("### Vehicle status")
    if latest["alerts"]:
        for a in latest["alerts"]:
            st.error(f"• {a}")
    else:
        st.success("✅ Vehicle operating normally")
    st.markdown("#### Latest telemetry (summary)")
    st.markdown(f"- **Vehicle ID:** {latest['vehicleId']}")
    st.markdown(f"- **Timestamp (UTC):** {latest['ts']}")
    st.markdown(f"- **Connection:** {latest['conn']}")
    st.markdown(f"- **Armor Integrity:** {m['armorIntegrity']:.2f} %")
    st.markdown('</div>', unsafe_allow_html=True)

# Right: Live chart
with right_col:
    st.markdown("### Live Telemetry (Engine Temp trend)")
    # Build DataFrame for last N points
    hist = st.session_state.history[:50][::-1]  # oldest -> newest
    df = pd.DataFrame([{
        "ts": item["ts"],
        "engineTemp": item["metrics"]["engineTemp"],
        "batteryV": item["metrics"]["batteryV"],
        "fuelPct": item["metrics"]["fuelPct"]
    } for item in hist])
    if not df.empty:
        df["ts_parsed"] = pd.to_datetime(df["ts"])
        df = df.set_index("ts_parsed")
        # Plot with plotly for nicer styling
        fig = px.line(df, y=["engineTemp", "batteryV", "fuelPct"],
                      labels={"value":"Reading", "variable":"Metric", "ts_parsed":"Time"},
                      template="plotly_white")
        fig.update_layout(height=360, margin=dict(l=10,r=10,t=30,b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No historical data yet.")
      # Armored Vehicle Health Monitoring System

Developed by **Adekanye Abdulzohir**

## 🚘 Dashboard Preview
![Dashboard Preview](file_00000000af48624389f3093cc8afc36e.png)

## 🛡️ Armored Vehicle
![Armored Vehicle](file_000000002088620cab00446a50df68c7.png)

# -----------------------
# Footer & throttling
# -----------------------
st.markdown("---")
st.caption("AVHMS Dashboard • Developed by Adekanye Abdulzohir Oyetosade")

# Sleep to honor refresh rate when auto streaming
if auto_stream:
    time.sleep(refresh_seconds)
    import time

# Auto-refresh every 5 seconds (safe alternative)
time.sleep(5)
st.experimental_set_query_params(updated=int(time.time()))

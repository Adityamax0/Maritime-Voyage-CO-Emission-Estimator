import streamlit as st
import pandas as pd
import joblib

# 1. Page Configuration
st.set_page_config(
    page_title="Maritime CO₂ Emission Estimator",
    page_icon="🚢",
    layout="centered"
)

# 2. Header & Overview
st.title("🚢 Maritime CO₂ Emission Estimator")
st.markdown(
    """
    Predict vessel Scope 1 greenhouse gas emissions for short-haul sea voyages.
    Configure the operational parameters below to generate an estimate.
    """
)

# 3. Model Loading with Caching
@st.cache_resource
def load_pipeline():
    return joblib.load("ship_emission_pipeline.pkl")

try:
    pipeline = load_pipeline()
except FileNotFoundError:
    st.error("Model file 'ship_emission_pipeline.pkl' not found. Ensure it is placed in the root directory.")
    st.stop()

# 4. Form Layout
with st.form("emission_form"):
    st.subheader("1. Vessel & Voyage Specifications")
    col1, col2 = st.columns(2)

    with col1:
        ship_type = st.selectbox(
            "Ship Type",
            options=['Fishing Trawler', 'Oil Service Boat', 'Surfer Boat', 'Tanker Ship'],
            index=1
        )
        fuel_type = st.selectbox(
            "Fuel Type",
            options=['Diesel', 'HFO'],
            index=1
        )
        weather = st.selectbox(
            "Weather Conditions",
            options=['Calm', 'Moderate', 'Stormy'],
            index=2
        )

    with col2:
        month = st.selectbox(
            "Voyage Month",
            options=[
                'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'
            ],
            index=0
        )
        distance = st.slider(
            "Voyage Distance (nautical miles)",
            min_value=20.0,
            max_value=500.0,
            value=100.0,
            step=10.0,
            help="Trained on short-haul maritime routes up to 500 nm."
        )
        engine_eff = st.slider(
            "Engine Efficiency Factor",
            min_value=0.50,
            max_value=1.00,
            value=0.85,
            step=0.01,
            help="Ratio representing relative operational thermal efficiency."
        )

    submitted = st.form_submit_button("Calculate CO₂ Emissions", use_container_width=True)

# 5. Prediction Execution
if submitted:
    input_df = pd.DataFrame([{
        'ship_type': ship_type,
        'fuel_type': fuel_type,
        'weather_conditions': weather,
        'month': month,
        'distance': float(distance),
        'engine_efficiency': float(engine_eff)
    }])

    prediction = pipeline.predict(input_df)[0]
    intensity = prediction / distance

    st.divider()
    st.subheader("Emission Forecast Results")

    metric_col1, metric_col2 = st.columns(2)
    metric_col1.metric(
        label="Predicted Scope 1 CO₂",
        value=f"{prediction:,.2f} MT",
        help="Total estimated metric tons of CO2 released."
    )
    metric_col2.metric(
        label="Emission Intensity",
        value=f"{intensity:.2f} MT / nm",
        help="Metric tons of CO2 per nautical mile."
    )

    if prediction > 20000:
        st.warning("High emission profile: Heavy fuel oil or large displacement vessel detected.")
    else:
        st.success("Standard operational profile within expected baseline parameters.")
        
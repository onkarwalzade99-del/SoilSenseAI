
import streamlit as st
import pandas as pd

from src.predictor import predict_crop
from src.report_generator import generate_pdf_report

# Page configuration
st.set_page_config(
    page_title="SoilSense AI",
    page_icon="🌱",
    layout="wide",
)

# Header
st.title("🌱 SoilSense AI")
st.subheader("Soil Test Analyzer & Crop Recommendation System")

st.write(
    "Enter your soil and environmental measurements to obtain "
    "a machine-learning-based crop prediction."
)

st.info(
    "This is a data-driven prediction, not a guarantee of crop suitability. "
    "Confirm your decision with local agricultural guidance."
)

# Sidebar navigation
page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Soil Data Input",
        "Crop Recommendation",
        "Soil Analysis",
    ],
)

# Keep the submitted soil data available between pages
if "soil_data" not in st.session_state:
    st.session_state.soil_data = None

if "predicted_crop" not in st.session_state:
    st.session_state.predicted_crop = None

# Home page
if page == "Home":
    st.header("Welcome to SoilSense AI")

    st.write(
        "SoilSense AI uses a trained Random Forest classifier to predict "
        "a crop category from soil nutrients and environmental measurements."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("ML Model", "Random Forest")
    col2.metric("Input Features", "7")
    col3.metric("Prediction Type", "Crop Classification")

    st.markdown("### How it works")
    st.markdown(
        """
        1. Enter soil and environmental measurements.
        2. Validate the supplied values.
        3. Generate a crop prediction using the trained model.
        4. Review the measurements and analysis.
        """
    )

# Soil input page
elif page == "Soil Data Input":
    st.header("Enter Soil Data")

    with st.form("soil_input_form"):
        col1, col2 = st.columns(2)

        with col1:
            nitrogen = st.number_input(
                "Nitrogen (N)",
                min_value=0.0,
                max_value=140.0,
                value=90.0,
            )
            phosphorus = st.number_input(
                "Phosphorus (P)",
                min_value=0.0,
                max_value=145.0,
                value=42.0,
            )
            potassium = st.number_input(
                "Potassium (K)",
                min_value=0.0,
                max_value=205.0,
                value=43.0,
            )
            soil_ph = st.number_input(
                "Soil pH",
                min_value=0.0,
                max_value=14.0,
                value=6.5,
            )

        with col2:
            temperature = st.number_input(
                "Temperature (°C)",
                min_value=-10.0,
                max_value=60.0,
                value=25.0,
            )
            humidity = st.number_input(
                "Humidity (%)",
                min_value=0.0,
                max_value=100.0,
                value=80.0,
            )
            rainfall = st.number_input(
                "Rainfall (mm)",
                min_value=0.0,
                max_value=5000.0,
                value=200.0,
            )

        submitted = st.form_submit_button(
            "Save Soil Measurements",
            use_container_width=True,
        )

    if submitted:
        st.session_state.soil_data = {
            "N": nitrogen,
            "P": phosphorus,
            "K": potassium,
            "temperature": temperature,
            "humidity": humidity,
            "ph": soil_ph,
            "rainfall": rainfall,
        }

        st.session_state.predicted_crop = None

        st.success(
            "Soil measurements saved. Open Crop Recommendation "
            "to generate a prediction."
        )

# Crop recommendation page
elif page == "Crop Recommendation":
    st.header("Crop Recommendation")

    soil_data = st.session_state.soil_data

    if soil_data is None:
        st.warning(
            "Please enter and save your soil measurements "
            "on the Soil Data Input page first."
        )
    else:
        st.markdown("### Submitted measurements")
        st.dataframe(
            pd.DataFrame([soil_data]),
            use_container_width=True,
            hide_index=True,
        )

        if st.button("Get Crop Recommendation", type="primary"):
            try:
                crop = predict_crop(soil_data)
                st.session_state.predicted_crop = crop
            except Exception as error:
                st.error(f"Prediction failed: {error}")

        if st.session_state.predicted_crop:
            st.success(
                f"Predicted crop: {st.session_state.predicted_crop.title()}"
            )

            st.caption(
                "This prediction reflects the training dataset. "
                "It is not a guarantee of yield or local suitability."
            )
            
            pdf_bytes = generate_pdf_report(
                st.session_state.soil_data,
                st.session_state.predicted_crop,
            )

            st.download_button(
                label="Download PDF Report",
                data=pdf_bytes,
                file_name="SoilSense_AI_Report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )


# Soil analysis page
elif page == "Soil Analysis":
    st.header("Soil Analysis")

    soil_data = st.session_state.soil_data

    if soil_data is None:
        st.warning(
            "Enter and save soil measurements before viewing analysis."
        )
    else:
        col1, col2, col3 = st.columns(3)

        col1.metric("Nitrogen (N)", f"{soil_data['N']:g}")
        col2.metric("Phosphorus (P)", f"{soil_data['P']:g}")
        col3.metric("Potassium (K)", f"{soil_data['K']:g}")

        col4, col5, col6 = st.columns(3)

        col4.metric("Soil pH", f"{soil_data['ph']:.2f}")
        col5.metric("Temperature", f"{soil_data['temperature']:.1f} °C")
        col6.metric("Humidity", f"{soil_data['humidity']:.1f}%")

        st.markdown("### Nutrient measurements")

        nutrient_data = pd.DataFrame(
            {
                "Nutrient": ["Nitrogen (N)", "Phosphorus (P)", "Potassium (K)"],
                "Value": [
                    soil_data["N"],
                    soil_data["P"],
                    soil_data["K"],
                ],
            }
        )

        st.bar_chart(
            nutrient_data.set_index("Nutrient"),
            y="Value",
        )

        st.metric("Rainfall", f"{soil_data['rainfall']:.1f} mm")

        st.caption(
            "NPK values use the input units expected by the dataset. "
            "The chart compares the entered numbers; it does not by itself "
            "determine whether nutrient levels are agronomically adequate."
        )

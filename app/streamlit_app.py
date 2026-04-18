import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# # Import utility functions (utils is in same directory)
# from utils.model_loader import load_advanced_model, load_baseline_model
# from utils.feature_engineering import engineer_advanced_features, engineer_baseline_features
# from utils.rag_search import search_rbi_guidelines
# from utils.translator import translate_to_hindi

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Try imports with error messages
try:
    from utils.model_loader import load_advanced_model, load_baseline_model
    st.write("✓ model_loader imported")
except Exception as e:
    st.error(f"model_loader import failed: {e}")

try:
    from utils.feature_engineering import engineer_advanced_features, engineer_baseline_features
    st.write("✓ feature_engineering imported")
except Exception as e:
    st.error(f"feature_engineering import failed: {e}")

# Page configuration
st.set_page_config(
    page_title="Suraksha - UPI Fraud Detection",
    page_icon="🛡️",
    layout="wide"
)

# Title
st.title("🛡️ Suraksha: UPI Fraud Detection System")
st.markdown("---")

# Sidebar
st.sidebar.header("⚙️ Configuration")

mode = st.sidebar.selectbox(
    "Detection Mode",
    ["Advanced", "Baseline"]
)

language = st.sidebar.selectbox(
    "Language / भाषा",
    ["English", "Hindi"]
)

st.sidebar.markdown("---")
st.sidebar.info(f"Mode: {mode}\nLanguage: {language}")

# Input Form
st.header("📊 Transaction Details")

with st.form("fraud_detection_form"):
    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("Amount (₹)", 0.0, 100000.0, 1000.0)
        hour = st.slider("Hour of Transaction", 0, 23, 14)
        merchant_category = st.selectbox("Merchant Category", [
            "Grocery", "Shopping", "Entertainment", "Electronics",
            "Fuel", "Travel", "Food", "Healthcare", "Education",
            "Utilities", "Jewelry", "Luxury"
        ])
        failed_transactions = st.number_input("Failed Transactions", 0, 50, 0)

    with col2:
        if mode == "Advanced":
            device_id = st.text_input("Device ID", "DEVICE_001")
            new_device = st.radio("New Device?", ["No", "Yes"])
            sim_changed = st.radio("SIM Changed?", ["No", "Yes"])
            recent_txn_count = st.number_input("Recent Txn Count", 0, 100, 5)

    submitted = st.form_submit_button("🔍 Detect Fraud")

# Prediction
if submitted:
    with st.spinner("Analyzing transaction..."):
        try:
            # Input dictionary
            input_data = {
                "amount_inr": amount,
                "hour": hour,
                "merchant_category": merchant_category,
                "failed_txn_count": failed_transactions,
                "timestamp": datetime.now()
            }
            if mode == "Advanced":
                input_data.update({
                    "device_id": device_id,
                    "is_new_device": 1 if new_device == "Yes" else 0,
                    "sim_changed": 1 if sim_changed == "Yes" else 0,
                    "recent_txn_count": recent_txn_count
                })

            # Feature engineering
            if mode == "Advanced":
                features = engineer_advanced_features(input_data)
                model = load_advanced_model()
            else:
                features = engineer_baseline_features(input_data)
                model = load_baseline_model()

            # Convert numpy array to DataFrame properly
            if isinstance(features, np.ndarray):
                features = pd.DataFrame(features)

            # Prediction
            prediction = model.predict(features)
            fraud_type = prediction[0]

            # Convert safely
            try:
                fraud_type = int(fraud_type)
            except:
                pass

            # Confidence
            confidence = None
            try:
                proba = model.predict_proba(features)
                confidence = float(max(proba[0]) * 100)
            except:
                pass

            # Mapping
            fraud_type_map = {
                0: "Legitimate",
                1: "Amount Anomaly",
                2: "Temporal Anomaly",
                3: "Merchant Fraud",
                4: "High-Risk Pattern",
                5: "Device Fraud",
                6: "SIM Swap Fraud",
                7: "Velocity Fraud"
            }

            fraud_label = fraud_type_map.get(fraud_type, str(fraud_type))

            # RAG
            explanation = search_rbi_guidelines(fraud_label)

            # Translation
            if language == "Hindi":
                fraud_label = translate_to_hindi(fraud_label)
                explanation = translate_to_hindi(explanation)

            # Output
            st.markdown("---")
            st.header("🎯 Detection Results")
            if fraud_type == 0:
                st.success(f"✅ {fraud_label}")
            else:
                st.error(f"⚠️ {fraud_label}")

            if confidence:
                st.metric("Confidence", f"{confidence:.2f}%")
            st.subheader("📋 Explanation")
            st.info(explanation)

            with st.expander("Details"):
                st.json(input_data)
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.exception(e)

# Footer
st.markdown("---")
st.caption("🛡️ Suraksha - Databricks Hackathon Project")

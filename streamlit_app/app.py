import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime

st.set_page_config(page_title="🛡️ Suraksha Fraud Detection", layout="wide")

# Title
st.title("🛡️ Suraksha: UPI Fraud Detection System")
st.markdown("AI-Powered Real-time Fraud Detection for Digital Payments")
st.markdown("---")

# Fraud type mapping
FRAUD_TYPES = {
    0: "Legitimate", 1: "Velocity Fraud", 2: "Mule Account", 
    3: "SIM Swap", 4: "Device Takeover", 5: "Beneficiary Manipulation",
    6: "Amount Anomaly", 7: "Temporal Anomaly", 8: "Merchant Fraud", 
    9: "Failed-Then-Success"
}

@st.cache_resource
def load_models():
    try:
        adv = joblib.load("/Workspace/Users/vinodekdhoke@gmail.com/Suraksha/models/suraksha_advanced.pkl")
        base = joblib.load("/Workspace/Users/vinodekdhoke@gmail.com/Suraksha/baseline_solution/suraksha_baseline_model.pkl")
        feat = joblib.load("/Workspace/Users/vinodekdhoke@gmail.com/Suraksha/models/feature_names.pkl")
        return adv, base, feat
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None, None

st.sidebar.header("⚙️ Configuration")
model_type = st.sidebar.radio("Model", ["Advanced (10-class)", "Baseline (Binary)"])

adv_model, base_model, features = load_models()

if adv_model is None:
    st.stop()

st.sidebar.success("✅ Models loaded")

# Input form
st.header("📊 Transaction Details")

col1, col2 = st.columns(2)

with col1:
    txn_id = st.text_input("Transaction ID", "TXN_001")
    amount = st.number_input("Amount (₹)", 100, 100000, 5000)
    txn_type = st.selectbox("Type", ["P2P", "P2M", "Bill Payment", "Recharge"])
    device = st.selectbox("Device", ["Android", "iOS", "Web"])

with col2:
    timestamp = st.text_input("Time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    age_group = st.selectbox("Age", ["18-25", "26-35", "36-45", "46-55", "56+"])
    bank = st.selectbox("Bank", ["SBI", "HDFC", "ICICI", "Axis", "PNB"])
    network = st.selectbox("Network", ["4G", "5G", "WiFi"])

st.markdown("### Optional Fraud Indicators")
col3, col4, col5 = st.columns(3)

with col3:
    txn_count = st.number_input("Txns/hour", 0, 50, 2)
with col4:
    device_changed = st.checkbox("Device Changed")
with col5:
    sim_changed = st.checkbox("SIM Changed")

if st.button("🔍 Analyze Transaction", type="primary", use_container_width=True):
    
    # Simple feature engineering for demo
    hour = pd.to_datetime(timestamp).hour
    is_night = 1 if hour < 6 or hour > 22 else 0
    
    # Create feature dict
    txn_data = {
        'hour': hour, 'amount_inr': amount, 'is_night': is_night,
        'sender_txn_count_1hour': txn_count,
        'device_changed_flag': int(device_changed),
        'sim_change_recent': int(sim_changed)
    }
    
    # For demo - create dummy features matching model expectations
    if model_type == "Advanced (10-class)":
        # Create basic feature array
        X = pd.DataFrame([[hour, amount, txn_count, int(device_changed), int(sim_changed)] + [0]*33])
        X.columns = features if len(features) == 38 else [f'f{i}' for i in range(38)]
        
        pred = adv_model.predict(X)[0]
        proba = adv_model.predict_proba(X)[0]
        
        st.markdown("---")
        st.header("🎯 Results")
        
        if pred == 0:
            st.success(f"✅ **LEGITIMATE TRANSACTION**")
            st.metric("Confidence", f"{max(proba)*100:.1f}%")
        else:
            st.error(f"🚨 **FRAUD DETECTED: {FRAUD_TYPES[pred]}**")
            st.metric("Confidence", f"{max(proba)*100:.1f}%")
        
        # Show top predictions
        st.subheader("Top Predictions")
        top_indices = np.argsort(proba)[::-1][:5]
        for idx in top_indices:
            if proba[idx] > 0.01:
                st.write(f"- {FRAUD_TYPES[idx]}: {proba[idx]*100:.1f}%")
    
    else:
        # Baseline model
        X = pd.DataFrame([[amount, hour, pd.to_datetime(timestamp).dayofweek, pd.to_datetime(timestamp).month]])
        pred = base_model.predict(X)[0]
        proba = base_model.predict_proba(X)[0]
        
        st.markdown("---")
        st.header("🎯 Results")
        
        if pred == 0:
            st.success(f"✅ **LEGITIMATE TRANSACTION**")
        else:
            st.error(f"🚨 **FRAUD DETECTED**")
        
        st.metric("Confidence", f"{max(proba)*100:.1f}%")

# Footer
st.markdown("---")
st.caption("🛡️ Suraksha Fraud Detection | Databricks Hackathon 2024")

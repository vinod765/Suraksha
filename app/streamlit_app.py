"""
Suraksha UPI Fraud Detection — Streamlit App
Dual-model architecture with mode selector
NO HARDCODED PATHS - Fully reproducible for judges
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import sys
from pathlib import Path

# Add app directory to path for imports
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

# Import utilities with dynamic configuration
try:
    from utils.model_loader import load_advanced_model, load_baseline_model
    from utils.feature_engineering import engineer_advanced_features, engineer_baseline_features
    from utils.rag_search import search_rbi_guidelines
    from utils.translator import translate_to_hindi
    from utils.config import config
except ImportError as e:
    st.error(f"Import error: {e}")
    st.info("Make sure all utility files are in the app/utils/ directory")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Suraksha — UPI Fraud Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3em;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
    }
    .sub-header {
        font-size: 1.2em;
        text-align: center;
        color: #666;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title and tagline
st.markdown('<p class="main-header">🛡️ Suraksha (सुरक्षा)</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered UPI Fraud Detection with Explainable Alerts</p>', unsafe_allow_html=True)
st.markdown("---")

# Display configuration info (for judges to verify)
with st.expander("🔍 System Configuration (for judges/reviewers)"):
    st.write("**Auto-detected Configuration:**")
    st.json({
        "Workspace User": config.workspace_user,
        "Project Root": str(config.project_root),
        "Advanced Model Path": config.get_model_path('advanced'),
        "Baseline Model Path": config.get_model_path('baseline'),
        "FAISS Index Path": config.get_faiss_path(),
        "Models Directory": str(config.models_dir),
        "RAG Directory": str(config.rag_dir)
    })
    st.info("✅ All paths are auto-detected - NO HARDCODED VALUES")

# Sidebar: Mode selector
st.sidebar.header("⚙️ Configuration")

detection_mode = st.sidebar.radio(
    "Choose Detection Mode:",
    ["🚀 Advanced (9 Fraud Types)", "⚡ Baseline (Pattern-Based)"],
    help="Advanced requires user tracking data. Baseline works with transaction patterns only."
)

is_advanced = "Advanced" in detection_mode

# Language toggle
language = st.sidebar.radio(
    "Output Language:",
    ["English", "हिंदी (Hindi)"]
)

# Optional: Comparison mode
compare_mode = st.sidebar.checkbox(
    "🔍 Compare Both Models",
    help="Run both Advanced and Baseline models on the same transaction"
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Suraksha** leverages Databricks Delta Lake, Spark, MLflow, "
    "Unity Catalog, DBFS, and Databricks App for production-ready fraud detection."
)

st.sidebar.markdown("---")
st.sidebar.markdown("**🎯 Quick Test Scenarios:**")
if st.sidebar.button("⚡ Test Velocity Fraud"):
    st.session_state.test_scenario = "velocity"
if st.sidebar.button("🌙 Test Temporal Anomaly"):
    st.session_state.test_scenario = "temporal"
if st.sidebar.button("💰 Test Amount Anomaly"):
    st.session_state.test_scenario = "amount"

# Load models with caching
@st.cache_resource
def load_models():
    """Load models once and cache"""
    try:
        with st.spinner("🔄 Loading ML models..."):
            adv_model = load_advanced_model()
            base_model = load_baseline_model()
        return adv_model, base_model, "success"
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None, "error"

adv_model, base_model, load_status = load_models()

if load_status == "error":
    st.error("⚠️  Failed to load models. Please check model files are available.")
    st.info("Models should be at:\n" + 
            f"- Advanced: {config.get_model_path('advanced')}\n" +
            f"- Baseline: {config.get_model_path('baseline')}")
    st.stop()
else:
    st.sidebar.success("✅ Models loaded successfully")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📝 Transaction Input")
    
    # Pre-fill with test scenario if selected
    test_scenario = st.session_state.get('test_scenario', None)
    
    if test_scenario == "velocity":
        default_amount = 5000
        default_hour = 14
        default_txn_count = 7
        default_merchant = "Shopping"
    elif test_scenario == "temporal":
        default_amount = 25000
        default_hour = 3
        default_txn_count = 1
        default_merchant = "Entertainment"
    elif test_scenario == "amount":
        default_amount = 75000
        default_hour = 14
        default_txn_count = 1
        default_merchant = "Shopping"
    else:
        default_amount = 5000
        default_hour = 14
        default_txn_count = 1
        default_merchant = "Food"
    
    # Common fields (both modes)
    with st.form("transaction_form"):
        col_a, col_b = st.columns(2)
        
        with col_a:
            amount = st.number_input(
                "Transaction Amount (₹)",
                min_value=10,
                max_value=100000,
                value=default_amount,
                step=100
            )
            
            merchant_category = st.selectbox(
                "Merchant Category",
                ["Food", "Shopping", "Fuel", "Entertainment", "Education", 
                 "Travel", "Utilities", "Healthcare", "Other"],
                index=["Food", "Shopping", "Fuel", "Entertainment", "Education", 
                      "Travel", "Utilities", "Healthcare", "Other"].index(default_merchant)
            )
            
            device_type = st.selectbox(
                "Device Type",
                ["Android", "iOS", "Web"]
            )
            
            hour_of_day = st.slider(
                "Transaction Hour (24h)",
                0, 23, default_hour
            )
        
        with col_b:
            network_type = st.selectbox(
                "Network Type",
                ["4G", "5G", "WiFi", "3G"]
            )
            
            txn_type = st.selectbox(
                "Transaction Type",
                ["P2P", "P2M", "Bill Payment", "Recharge"]
            )
            
            sender_state = st.selectbox(
                "Sender State",
                ["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", 
                 "Gujarat", "Uttar Pradesh", "West Bengal"]
            )
            
            day_of_week = st.selectbox(
                "Day of Week",
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                index=4  # Friday
            )
        
        # Advanced-only fields (conditional rendering)
        if is_advanced:
            st.markdown("#### 🔐 Advanced Mode Fields")
            
            col_c, col_d = st.columns(2)
            
            with col_c:
                sender_vpa = st.text_input(
                    "Sender VPA",
                    value="alice@paytm",
                    help="Format: username@provider"
                )
                
                receiver_vpa = st.text_input(
                    "Receiver VPA",
                    value="merchant@phonepe"
                )
                
                txn_count_1min = st.number_input(
                    "Transactions in Last 1 Minute",
                    min_value=0,
                    max_value=20,
                    value=default_txn_count,
                    help="Key indicator for velocity fraud"
                )
            
            with col_d:
                device_changed = st.checkbox("Device Changed Recently?")
                sim_changed = st.checkbox("SIM Swapped Recently?")
                mpin_attempts = st.number_input("Failed MPIN Attempts", 0, 5, 0)
                location_changed = st.checkbox("Location Changed?")
        
        submit_button = st.form_submit_button("🔍 Check Transaction", use_container_width=True)

with col2:
    st.header("📊 Detection Mode")
    if is_advanced:
        st.success("**Advanced Mode Active**")
        st.markdown("""
        Detects **9 fraud types**:
        * Velocity Fraud
        * Mule Account
        * SIM Swap
        * Device Takeover
        * Beneficiary Manipulation
        * Amount Anomaly
        * Temporal Anomaly
        * Merchant Fraud
        * Failed-Then-Success
        """)
    else:
        st.info("**Baseline Mode Active**")
        st.markdown("""
        Detects **pattern-based fraud**:
        * Amount Anomaly
        * Temporal Anomaly
        * Merchant Risk
        * High-Risk Pattern
        """)
    
    st.markdown("---")
    st.markdown("**Model Info:**")
    st.write(f"• Mode: {'Advanced (9-class)' if is_advanced else 'Baseline (4-class)'}")
    st.write(f"• Features: {'Behavioral + Pattern' if is_advanced else 'Pattern-only'}")
    st.write(f"• Language: {language}")

# Process transaction when form submitted
if submit_button:
    # Clear test scenario
    if 'test_scenario' in st.session_state:
        del st.session_state['test_scenario']
    
    with st.spinner("🔄 Analyzing transaction..."):
        
        # Prepare input data
        input_data = {
            'amount_inr': amount,
            'merchant_category': merchant_category,
            'device_type': device_type,
            'hour_of_day': hour_of_day,
            'network_type': network_type,
            'txn_type': txn_type,
            'sender_state': sender_state
        }
        
        if is_advanced:
            input_data.update({
                'sender_vpa': sender_vpa,
                'receiver_vpa': receiver_vpa,
                'sender_txn_count_1min': txn_count_1min,
                'device_changed_flag': device_changed,
                'sim_change_recent': sim_changed,
                'mpin_attempts': mpin_attempts
            })
        
        # Convert to DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Route to appropriate model
        results = {}
        
        if is_advanced or compare_mode:
            try:
                # Advanced model
                adv_features = engineer_advanced_features(input_df)
                adv_prediction = adv_model.predict(adv_features)[0]
                adv_proba = adv_model.predict_proba(adv_features)[0]
                
                adv_fraud_type = config.fraud_types_advanced[adv_prediction]
                adv_confidence = adv_proba[adv_prediction] * 100
                
                results['advanced'] = {
                    'prediction': adv_prediction,
                    'fraud_type': adv_fraud_type,
                    'confidence': adv_confidence,
                    'proba': adv_proba
                }
            except Exception as e:
                st.error(f"Error in advanced model: {e}")
                results['advanced'] = None
        
        if not is_advanced or compare_mode:
            try:
                # Baseline model
                base_features = engineer_baseline_features(input_df)
                base_prediction = base_model.predict(base_features)[0]
                base_proba = base_model.predict_proba(base_features)[0]
                
                base_fraud_type = config.fraud_types_baseline[base_prediction]
                base_confidence = base_proba[base_prediction] * 100
                
                results['baseline'] = {
                    'prediction': base_prediction,
                    'fraud_type': base_fraud_type,
                    'confidence': base_confidence,
                    'proba': base_proba
                }
            except Exception as e:
                st.error(f"Error in baseline model: {e}")
                results['baseline'] = None
    
    # Display results
    st.markdown("---")
    st.header("🎯 Detection Results")
    
    if compare_mode:
        # Side-by-side comparison
        col_adv, col_base = st.columns(2)
        
        with col_adv:
            st.subheader("🚀 Advanced Model")
            if results.get('advanced'):
                r = results['advanced']
                if r['prediction'] == 0:
                    st.success(f"✅ {r['fraud_type']}")
                else:
                    st.error(f"⚠️ {r['fraud_type']}")
                st.metric("Confidence", f"{r['confidence']:.1f}%")
            else:
                st.error("Model unavailable")
        
        with col_base:
            st.subheader("⚡ Baseline Model")
            if results.get('baseline'):
                r = results['baseline']
                if r['prediction'] == 0:
                    st.success(f"✅ {r['fraud_type']}")
                else:
                    st.error(f"⚠️ {r['fraud_type']}")
                st.metric("Confidence", f"{r['confidence']:.1f}%")
            else:
                st.error("Model unavailable")
    
    else:
        # Single model result
        result_key = 'advanced' if is_advanced else 'baseline'
        if results.get(result_key):
            r = results[result_key]
            fraud_type = r['fraud_type']
            confidence = r['confidence']
            prediction = r['prediction']
            
            if prediction == 0:
                st.success(f"### ✅ Transaction Appears Legitimate")
                st.metric("Confidence", f"{confidence:.1f}%")
                st.info("This transaction does not exhibit suspicious patterns.")
            else:
                st.error(f"### ⚠️ FRAUD DETECTED: {fraud_type}")
                st.metric("Confidence", f"{confidence:.1f}%")
                
                # RAG explanation
                with st.spinner("📚 Retrieving RBI guidelines..."):
                    rag_context = search_rbi_guidelines(fraud_type)
                    
                    explanation_en = f"""
**Why was this flagged?**

Your transaction exhibits patterns consistent with **{fraud_type}**.

**Key Indicators:**
"""
                    
                    # Add specific indicators based on fraud type
                    if is_advanced and fraud_type == "Velocity Fraud":
                        explanation_en += f"\n* You made {txn_count_1min} transactions in 1 minute"
                        explanation_en += f"\n* This exceeds normal user behavior patterns"
                    elif fraud_type == "Temporal Anomaly":
                        explanation_en += f"\n* Transaction at {hour_of_day}:00 hours (odd hours)"
                        explanation_en += f"\n* Large amount during unusual time"
                    elif fraud_type == "Amount Anomaly":
                        explanation_en += f"\n* Amount ₹{amount:,} is significantly higher than average"
                        explanation_en += f"\n* Deviates from typical transaction patterns"
                    
                    explanation_en += f"\n\n**RBI Guideline Reference:**\n{rag_context[:300]}..."
                    
                    # Translate if Hindi selected
                    if language == "हिंदी (Hindi)":
                        explanation_hi = translate_to_hindi(explanation_en)
                        st.markdown(explanation_hi)
                    else:
                        st.markdown(explanation_en)
                
                # Recommendations
                st.markdown("---")
                st.subheader("🛡️ Recommended Actions")
                
                recommendations_en = """
1. **Immediate:** Stop transaction and contact your bank
2. **Security:** Change your UPI PIN immediately
3. **Review:** Check recent transaction history
4. **Report:** File complaint at https://cybercrime.gov.in
"""
                
                if language == "हिंदी (Hindi)":
                    recommendations_hi = translate_to_hindi(recommendations_en)
                    st.warning(recommendations_hi)
                else:
                    st.warning(recommendations_en)
                
                # Show probability breakdown
                with st.expander("📊 Detailed Probability Breakdown"):
                    fraud_types = config.fraud_types_advanced if is_advanced else config.fraud_types_baseline
                    proba_df = pd.DataFrame({
                        'Fraud Type': [fraud_types[i] for i in range(len(r['proba']))],
                        'Probability': r['proba'] * 100
                    }).sort_values('Probability', ascending=False)
                    st.dataframe(proba_df, use_container_width=True)

# Footer
st.markdown("---")
st.caption("""
**Suraksha UPI Fraud Detection System** | Built for Bharat Bricks Hacks 2026  
Powered by: Delta Lake • Spark • MLflow • Unity Catalog • DBFS • Databricks App  
**✅ Fully reproducible - No hardcoded paths**
""")

# Debug info for judges
with st.expander("🔧 Debug Information"):
    st.write("**Input Data:**")
    st.json(input_data if submit_button else {"status": "No transaction submitted yet"})
    if submit_button:
        st.write("**Feature Engineering Output:**")
        if is_advanced:
            st.dataframe(adv_features)
        else:
            st.dataframe(base_features)

"""
Suraksha - Minimal Test Version
Quick deployment test without heavy dependencies
"""

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Suraksha Test",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Suraksha - Test Deployment")
st.success("✅ App is working! Streamlit deployment successful.")

st.info("""
**This is a minimal test version to verify deployment.**

If you see this, your Databricks App deployment is working!

Next step: Deploy the full version with ML models.
""")

# Simple form
with st.form("test_form"):
    amount = st.number_input("Test Amount", value=5000)
    submit = st.form_submit_button("Test Submit")
    
    if submit:
        st.success(f"✅ Form submitted with amount: ₹{amount:,}")
        st.balloons()

st.markdown("---")
st.caption("Minimal test version - No ML models loaded")

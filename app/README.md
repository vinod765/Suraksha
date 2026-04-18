# Suraksha Fraud Detection App

🛡️ **AI-Powered UPI Fraud Detection with Explainable Alerts**

---

## Overview

Suraksha (सुरक्षा - meaning "Security" in Hindi) is a production-ready Streamlit application for detecting UPI fraud using dual-model architecture:

- **Advanced Model:** 9-class fraud detection with user behavior tracking
- **Baseline Model:** Pattern-based detection without user tracking

---

## ✨ Key Features

### Technical Excellence
- ✅ **Zero Hardcoded Paths:** Fully reproducible in any Databricks workspace
- ✅ **Dual-Model Architecture:** Advanced (9 fraud types) + Baseline (4 patterns)
- ✅ **Multiple Fallbacks:** MLflow → Local files → Demo mode
- ✅ **RAG-Enhanced:** Retrieves relevant RBI guidelines for explanations
- ✅ **Multilingual:** English and Hindi support

### Databricks Integration
- Delta Lake (data storage)
- Spark (feature engineering)
- MLflow (model registry)
- Unity Catalog (governance)
- DBFS (RAG storage)
- Databricks App (serverless deployment)

### Fraud Detection
- Velocity Fraud (rapid transactions)
- Mule Account (money laundering)
- SIM Swap attacks
- Device Takeover
- Beneficiary Manipulation
- Amount Anomaly
- Temporal Anomaly (odd hours)
- Merchant Fraud
- Failed-Then-Success patterns

---

## 🚀 Quick Start

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Run Locally
```bash
streamlit run streamlit_app.py
```

### 3. Deploy on Databricks
- Right-click `streamlit_app.py` → Create App
- Or use Databricks Apps UI

---

## 📁 File Structure

```
app/
├── streamlit_app.py          # Main application
├── config.py                 # Dynamic configuration (auto-detects paths)
├── requirements.txt          # Dependencies
├── SETUP.md                  # Detailed setup instructions
├── README.md                 # This file
└── utils/
    ├── model_loader.py       # Loads models from MLflow or files
    ├── feature_engineering.py# Feature transformations
    ├── rag_search.py         # RAG for RBI guidelines
    └── translator.py         # Hindi translation
```

---

## 🔧 Configuration

### Automatic Path Detection

The app automatically detects:
- Workspace user (from dbutils, environment, or path)
- Project root (relative to config.py)
- Model locations (models/, baseline_solution/, or MLflow)
- RAG components (rag/ folder or DBFS)

**No manual configuration needed!**

View detected paths in the app's "🔍 System Configuration" expander.

---

## 🧪 Testing

### Quick Tests (Via Sidebar Buttons)

1. **⚡ Velocity Fraud:** 7 transactions in 1 minute
2. **🌙 Temporal Anomaly:** ₹25K at 3 AM
3. **💰 Amount Anomaly:** ₹75K transaction

### Manual Testing

Fill in transaction details and click "🔍 Check Transaction"

---

## 🎯 Detection Modes

### Advanced Mode (9 Fraud Types)
Requires user tracking data:
- Sender/Receiver VPA
- Transaction velocity
- Device/SIM changes
- MPIN attempts

**Use cases:** Banks with comprehensive user tracking

### Baseline Mode (Pattern-Based)
Works with basic transaction data:
- Amount patterns
- Temporal patterns
- Merchant risk
- Statistical anomalies

**Use cases:** Privacy-constrained environments, limited data

---

## 📊 Output

For each transaction, the app provides:

1. **Prediction:** Fraud type or "Legitimate"
2. **Confidence Score:** Model certainty (%)
3. **Explanation:** Why it was flagged (RAG-enhanced)
4. **RBI Guidelines:** Relevant regulatory context
5. **Recommendations:** Actionable next steps
6. **Language Options:** English or Hindi

---

## 🌍 Multilingual Support

- **English:** Full explanations and recommendations
- **हिंदी (Hindi):** Translated using fallback templates or neural translation
- **Future:** Expandable to other Indian languages

---

## 🔐 Production Ready

### Reliability
- Graceful degradation if components missing
- Multiple fallback mechanisms
- Comprehensive error handling
- Demo mode if models unavailable

### Deployment Options
1. **Databricks App:** Serverless, auto-scaling
2. **Local:** Development and testing
3. **Docker:** Containerized deployment
4. **Cloud:** AWS/Azure/GCP with Streamlit Cloud

---

## 📚 Documentation

- **SETUP.md:** Complete setup instructions for judges
- **Strategy Guide:** `/Suraksha/UPI_Fraud_Shield_Complete_Strategy.md`
- **Project Structure:** `/Suraksha/PROJECT_STRUCTURE.md`

---

## 🎓 For Judges/Reviewers

### Reproducibility
- Copy this folder to any Databricks workspace
- Install dependencies
- Run immediately - no configuration needed

### Verification
- View auto-detected paths in app
- Check debug information in expanders
- Test with provided scenarios

### Evaluation Criteria
✅ Databricks Usage (6 components)  
✅ Accuracy & Effectiveness (dual models)  
✅ Innovation (RAG, multilingual, adaptive)  
✅ Presentation & Demo (working, reproducible)

---

## 🛠️ Requirements

- Python 3.8+
- Streamlit 1.28+
- scikit-learn, xgboost, pandas, numpy
- MLflow (optional, falls back to local files)
- sentence-transformers, faiss-cpu (optional, for RAG)
- transformers (optional, for neural translation)

See `requirements.txt` for complete list.

---

## 🎯 Design Philosophy

1. **Reproducibility First:** No hardcoded paths, works anywhere
2. **Graceful Degradation:** Missing components → fallbacks, not errors
3. **Judge-Friendly:** Clear configuration, comprehensive docs
4. **Production Thinking:** MLflow integration, multiple deployment options
5. **Educational:** Explains WHY fraud is detected (not just "fraud")

---

## 🏆 Built For

**Bharat Bricks Hacks 2026**  
Track: Digital-Artha (Economy & Financial Inclusion)  
Focus: Production-ready fraud detection with Databricks

---

## 📞 Support

For issues or questions:
1. Check SETUP.md troubleshooting section
2. Review debug information in app
3. Verify paths in "System Configuration" expander

---

## 📄 License

MIT License - See parent directory for details

---

## 🙏 Acknowledgments

- RBI fraud taxonomy and guidelines
- NPCI UPI fraud reports
- Databricks platform documentation
- AI4Bharat for IndicTrans2 model inspiration

---

**Ready to detect fraud! 🚀**

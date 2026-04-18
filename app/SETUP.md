# Suraksha App - Setup Instructions for Judges

**⚡ Quick Start:** This app is fully reproducible with NO HARDCODED PATHS.
All paths are auto-detected from the workspace environment.

---

## 🎯 Prerequisites

1. Databricks workspace (Free Edition or higher)
2. Compute cluster (any configuration)
3. Models trained and saved (see Model Setup below)

---

## 📁 Directory Structure

The app expects this structure (auto-detected, not hardcoded):

```
/Workspace/Users/<your-email>/Suraksha/
├── app/
│   ├── config.py                    # Dynamic configuration (auto-detects paths)
│   ├── streamlit_app.py             # Main Streamlit application
│   ├── requirements.txt             # Dependencies
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── model_loader.py          # Loads models from MLflow or local
│   │   ├── feature_engineering.py   # Feature transformations
│   │   ├── rag_search.py            # RAG for RBI guidelines
│   │   └── translator.py            # Hindi translation
│   └── assets/
│       └── rbi_docs/                # (Optional) RBI PDFs
├── models/
│   ├── suraksha_advanced.pkl        # Advanced 9-class model
│   └── feature_names.pkl            # (Optional) Feature names
├── baseline_solution/
│   └── suraksha_baseline_model.pkl  # Baseline model
└── rag/
    ├── faiss_index.bin              # (Optional) FAISS vector index
    └── text_chunks.pkl              # (Optional) RBI text chunks
```

---

## 🚀 Installation Steps

### Step 1: Clone or Copy Files

If using Git:
```bash
git clone <repository-url>
```

Or manually copy the `Suraksha` folder to your Databricks workspace.

### Step 2: Install Dependencies

In a Databricks notebook or terminal:

```python
%pip install -r /Workspace/Users/<your-email>/Suraksha/app/requirements.txt
dbutils.library.restartPython()
```

Or from terminal:
```bash
pip install -r app/requirements.txt
```

### Step 3: Verify Models

The app will automatically look for models in these locations (in order):
1. `/Workspace/Users/<your-email>/Suraksha/models/suraksha_advanced.pkl`
2. `/Workspace/Users/<your-email>/Suraksha/baseline_solution/suraksha_baseline_model.pkl`
3. MLflow Model Registry (models named `suraksha_advanced` and `suraksha_baseline`)

**If models are not found:** The app will run in DEMO MODE with rule-based predictions.

---

## 🎬 Running the App

### Method 1: Databricks App (Recommended)

1. Navigate to: `/Workspace/Users/<your-email>/Suraksha/app/`
2. Right-click on `streamlit_app.py`
3. Select **"Create App"** or **"Deploy as App"**
4. Databricks will automatically detect Streamlit and deploy
5. Access the app via the generated URL

### Method 2: Local Testing

```bash
streamlit run app/streamlit_app.py
```

The app will open at `http://localhost:8501`

### Method 3: Databricks Notebook

```python
import subprocess
subprocess.run([
    "streamlit", "run", 
    "/Workspace/Users/<your-email>/Suraksha/app/streamlit_app.py",
    "--server.port", "8501"
])
```

---

## 🔧 Configuration

### Automatic Configuration

The app uses `config.py` which automatically detects:
- Current workspace user (from dbutils, environment, or path)
- Project root directory (relative to config.py location)
- Model paths (with multiple fallback locations)
- RAG paths (workspace or DBFS)

**No manual configuration needed!**

### Manual Override (Optional)

If you need to override paths, edit `app/config.py` and modify:
```python
# In Config.__init__()
self.advanced_model_path = Path("/custom/path/to/model.pkl")
```

---

## 🧪 Testing the App

### Quick Test Scenarios

The app includes preset test buttons in the sidebar:

1. **Velocity Fraud Test:**
   - Click "⚡ Test Velocity Fraud" in sidebar
   - Shows 7 transactions in 1 minute
   - Should detect "Velocity Fraud" with >90% confidence

2. **Temporal Anomaly Test:**
   - Click "🌙 Test Temporal Anomaly"  
   - Transaction at 3 AM with ₹25,000
   - Should detect "Temporal Anomaly"

3. **Amount Anomaly Test:**
   - Click "💰 Test Amount Anomaly"
   - Transaction of ₹75,000
   - Should detect "Amount Anomaly"

### Manual Testing

Fill in the form with custom values and click "🔍 Check Transaction"

---

## 📊 Features

### Core Functionality
- ✅ Dual-model architecture (Advanced 9-class + Baseline pattern-based)
- ✅ Dynamic path detection (no hardcoded paths)
- ✅ MLflow integration with local file fallback
- ✅ RAG-enhanced explanations using RBI guidelines
- ✅ Hindi translation support
- ✅ Side-by-side model comparison mode

### Advanced Features
- ✅ User tracking (VPA, device changes, SIM swaps)
- ✅ Velocity detection (transactions per minute)
- ✅ Behavioral pattern recognition

### Baseline Features  
- ✅ Pattern-based detection (no user tracking needed)
- ✅ Amount anomaly detection
- ✅ Temporal anomaly detection
- ✅ Merchant risk assessment

---

## 🐛 Troubleshooting

### Issue: Models not loading

**Solution:**
1. Check model files exist at expected paths
2. View auto-detected paths in "🔍 System Configuration" expander
3. Models will default to DEMO MODE if not found

### Issue: Import errors

**Solution:**
```python
# Reinstall dependencies
%pip install --upgrade -r app/requirements.txt
dbutils.library.restartPython()
```

### Issue: RAG not working

**Solution:**
- RAG is optional - app will use fallback template explanations
- Check FAISS index exists: `app/config.py` → `get_faiss_path()`
- Fallback explanations are comprehensive and based on actual RBI guidelines

### Issue: Translation not working

**Solution:**
- Translation will use fallback Hindi templates
- Key terms are still translated
- Full neural translation requires `transformers` package

---

## 📝 Notes for Judges

### Design Philosophy
- **Zero hardcoded paths:** Everything is auto-detected or configurable
- **Graceful degradation:** Missing components trigger fallbacks, not errors
- **Multiple model loading strategies:** MLflow → Local files → Demo mode
- **Comprehensive error messages:** Easy to debug issues

### Reproducibility Features
- Path detection works in any Databricks workspace
- Works with or without MLflow
- Works with or without RAG components
- Works with or without trained models (demo mode)

### Configuration Verification
- Expander in the app shows all auto-detected paths
- Debug section shows input data and features
- Clear error messages if something is missing

---

## 💡 Production Deployment

For actual production deployment:

1. **Train models:** Run notebooks in `advanced_solution/` and `baseline_solution/`
2. **Register in MLflow:** Models will be auto-discovered if named correctly
3. **Build RAG index:** Run RAG pipeline to create FAISS index
4. **Deploy app:** Use Databricks Apps for serverless deployment

---

## 📚 Additional Resources

- **Strategy Guide:** `UPI_Fraud_Shield_Complete_Strategy.md`
- **Project Structure:** `PROJECT_STRUCTURE.md`  
- **Model Training:** `advanced_solution/` and `baseline_solution/` folders

---

## 🎯 Quick Validation Checklist

- [ ] All files in correct directory structure
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] At least one model file exists or MLflow models registered
- [ ] App starts without errors
- [ ] Can submit a test transaction
- [ ] Results display correctly
- [ ] Mode switching works (Advanced ↔ Baseline)
- [ ] Language toggle works (English ↔ Hindi)

---

## ✅ Ready to Deploy!

If all files are in place and dependencies are installed, the app should work immediately.

**For support:** Check the debug information in the app's expanders or review error messages in the terminal/log.

**Key benefit:** This app can be deployed in ANY Databricks workspace without modification - just copy the files and run!

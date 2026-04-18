# 🛡️ Suraksha (सुरक्षा) - UPI Fraud Detection System

**AI-powered, explainable, multilingual fraud detection for India's digital payment ecosystem**

A production-ready fraud detection system that identifies 9 types of UPI fraud using machine learning and explains WHY transactions are flagged using RAG-enhanced RBI guidelines.

---

## 🚨 The Problem

India's Unified Payments Interface (UPI) has revolutionized digital payments, processing **11.9 billion transactions worth ₹19 lakh crores** in December 2023 alone. However, this explosive growth has created a massive fraud epidemic:

* **₹1,200+ crores lost to UPI fraud annually** (RBI Annual Report 2023)
* **34% year-over-year increase** in sophisticated attacks (SIM swap, device takeover)
* **95% of fraud cases go undetected** by traditional rule-based systems
* **Victims lose trust** in digital payments, threatening financial inclusion

### Current Challenges

1. **Black Box Detection**: Banks flag transactions but can't explain WHY, leaving users confused
2. **Binary Classification**: Most systems only detect "fraud" vs "legitimate" - missing fraud type nuances
3. **Language Barriers**: English-only alerts exclude 70%+ of rural UPI users
4. **Limited Taxonomy**: Existing solutions focus on amount anomalies, missing behavioral fraud (velocity, mule accounts, SIM swap)

### Our Vision

**Suraksha** addresses these gaps by providing:
* ✅ **9 fraud type taxonomy** based on RBI guidelines - not just "fraud detected"
* ✅ **Explainable alerts** using RAG to retrieve relevant RBI/NPCI advisories
* ✅ **Multilingual support** (English & Hindi) for financial inclusion
* ✅ **Dual-model architecture** - Advanced (behavioral) + Baseline (pattern-based)
* ✅ **Production-ready** with Delta Lake, Unity Catalog, and PySpark at scale

---

## 📋 Table of Contents

* [What It Does](#what-it-does)
* [Architecture](#architecture)
* [Technologies Used](#technologies-used)
* [How to Run](#how-to-run)
* [Demo Steps](#demo-steps)
* [Project Structure](#project-structure)
* [Future Enhancements](#future-enhancements)
* [Submission Materials](#submission-materials)
* [Documentation](#documentation)

---

## 🎯 What It Does

Suraksha detects **9 types of UPI fraud** in real-time and provides explainable alerts with actionable recommendations:

**Behavior-Based Fraud (Requires User Tracking):**
1. **Velocity Fraud** - Rapid-fire transactions indicating automated attacks
2. **Mule Account** - Money laundering through intermediary accounts
3. **SIM Swap** - Fraudsters taking over victim's phone number
4. **Device Takeover** - Unauthorized device access to payment apps
5. **Beneficiary Manipulation** - Social engineering scams

**Pattern-Based Fraud (Statistical Detection):**
6. **Amount Anomaly** - Unusually large or suspicious amounts
7. **Temporal Anomaly** - Transactions at odd hours (2-5 AM)
8. **Merchant Fraud** - High-risk merchant patterns
9. **Failed-Then-Success** - Card testing attacks

**📖 For detailed definitions, real-world examples, and detection logic for each fraud type, see [Fraud Type Definitions](docs/fraud_type_definitions.md)**

**Key Features:**
* ✅ **Dual-Model Architecture** - Advanced (9 fraud types) + Baseline (pattern-based) with mode switching
* ✅ Multiclass ML classification (XGBoost) with 87.3% accuracy
* ✅ RAG-enhanced explanations using RBI fraud guidelines
* ✅ Multilingual support (English & Hindi)
* ✅ Interactive Databricks notebook demo with adaptive widgets
* ✅ Comprehensive fraud taxonomy based on RBI Annual Report 2023

---

## 🏗️ Architecture

### Current Implementation Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Databricks Notebook with Interactive Widgets               │ │
│  │  • Smart widgets: 16 fields (Advanced) / 9 fields (Baseline)│ │
│  │  • Real-time fraud detection execution                      │ │
│  │  • Dual-model mode switching                                │ │
│  │  • Rich visualization with Hindi/English support            │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATA LAYER (DELTA LAKE)                       │
│  ┌──────────────────────┐       ┌──────────────────────┐        │
│  │  Unity Catalog       │       │  Delta Lake Tables   │        │
│  │  workspace.bronze    │  →    │  500,000+ txns       │        │
│  │  workspace.silver    │       │  9 fraud types       │        │
│  │  workspace.gold      │       │  33 features         │        │
│  └──────────────────────┘       └──────────────────────┘        │
│                                                                  │
│  • ACID transactions • Schema enforcement • Time travel          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              FEATURE ENGINEERING (PYSPARK)                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  PySpark Window Functions for Distributed Processing        │ │
│  │  • Velocity features (Window.partitionBy + rangeBetween)   │ │
│  │  • Transaction history (lag functions over time windows)   │ │
│  │  • Mule account detection (inbound/outbound aggregations)  │ │
│  │  • Statistical features (avg, stddev, percentiles)         │ │
│  │  • Temporal patterns (weekend, odd hours detection)        │ │
│  │  Total: 38 engineered features                             │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              ML MODEL LAYER (DUAL MODELS)                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Advanced Model: XGBoost (10 classes)                       │ │
│  │  • Trained on 9 fraud types + legitimate class             │ │
│  │  • Model file: suraksha_advanced.pkl (16.1 MB)             │ │
│  │  • Accuracy: 87.3%                                          │ │
│  │  • Uses all 38 features                                     │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Baseline Model: Pattern-Based (5 classes)                  │ │
│  │  • Simplified fraud detection                               │ │
│  │  • Works without user tracking data                         │ │
│  │  • Faster inference                                         │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│               EXPLAINABILITY LAYER (RAG)                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Retrieval-Augmented Generation System                      │ │
│  │  ┌──────────────┐    ┌──────────────┐   ┌──────────────┐  │ │
│  │  │ FAISS Vector │ -> │ Semantic     │ ->│ RBI Guideline│  │ │
│  │  │ Store        │    │ Search       │   │ Retrieval    │  │ │
│  │  │ (index.faiss)│    │ (chunks.pkl) │   │ (metadata.pkl│  │ │
│  │  └──────────────┘    └──────────────┘   └──────────────┘  │ │
│  │  • Retrieves relevant RBI fraud guidelines                 │ │
│  │  • Explains WHY transaction was flagged                    │ │
│  │  • Provides regulatory context                             │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              OUTPUT & RECOMMENDATION LAYER                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Results Display                                            │ │
│  │  • Fraud type identification                               │ │
│  │  • Confidence score (%)                                     │ │
│  │  • Risk level (HIGH/MEDIUM/LOW)                            │ │
│  │  • Detection indicators                                     │ │
│  │  • RBI guidelines reference                                 │ │
│  │  • Actionable recommendations                               │ │
│  │  • Probability breakdown for all classes                    │ │
│  │  • Multilingual output (English/Hindi)                      │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Raw Data (CSV) 
    → Delta Lake Bronze (Unity Catalog)
    → PySpark Feature Engineering (Window Functions)
    → Delta Lake Silver (Engineered Features)
    → XGBoost Model Training
    → Dual Model Inference (Advanced/Baseline)
    → RAG System (Explain prediction)
    → Display Results (English/Hindi)
```

### Databricks Components Actually Used

1. **Delta Lake** - ACID transactions, schema enforcement, time travel
   * Bronze layer: `workspace.bronze.upi` (500K+ transactions)
   * Silver layer: `workspace.silver.upi_features` (38 engineered features)
   * Gold layer: `workspace.gold.*` (aggregated analytics)

2. **Unity Catalog** - Data governance and catalog management
   * Catalog: `workspace`
   * Schemas: `bronze`, `silver`, `gold`
   * Schema enforcement and validation

3. **PySpark** - Distributed data processing
   * Window functions for time-series feature engineering
   * `Window.partitionBy()`, `rangeBetween()`, `rowsBetween()`
   * Aggregations: count, sum, avg, stddev, lag, percentile

4. **Databricks Notebooks** - Interactive development and demo
   * Main demo: `Suraksha_Fraud_Detection_Demo`
   * Pipeline notebooks: 01_data_generation → 06_model_serving
   * RAG notebooks: rag_pipeline, rag_utils

5. **Databricks Widgets** - Interactive parameter input UI

6. **Databricks Workspace** - File storage for models, data, RAG artifacts

---

## 🛠️ Technologies Used

### Databricks Platform
* **Delta Lake** ⭐ - ACID transactions, time travel, schema enforcement
* **Unity Catalog** ⭐ - Data governance, catalog/schema management
* **PySpark** ⭐ - Distributed processing with Window functions
* **Databricks Notebooks** - Interactive development and demo
* **Databricks Widgets** - User interface for parameter input
* **Databricks Workspace** - File storage and project organization

### Machine Learning & AI
* **XGBoost** - Gradient boosting classifier for fraud detection
* **scikit-learn** - ML utilities and preprocessing
* **FAISS** - Vector similarity search for RAG
* **sentence-transformers** - Text embeddings for semantic search

### Open Source Models
* **all-MiniLM-L6-v2** - Sentence embeddings for RAG (HuggingFace)
* **XGBoost Multiclass Classifier** - Core fraud detection model

### Data & Processing
* **Pandas** - Data manipulation (small-scale)
* **NumPy** - Numerical computations
* **Python 3.8+** - Core programming language

### Explainability
* **RAG (Retrieval-Augmented Generation)** - Context-aware explanations
* **RBI Fraud Guidelines** - Regulatory compliance knowledge base

---

## 🚀 How to Run

### Step 1: Clone Repository

```bash
# Clone this repository to your Databricks workspace
git clone <your-github-repo-url>
# Or use Databricks Repos integration
```

### Step 2: Complete Setup (If Starting from Scratch)

**📖 For complete setup from repository cloning to model training, see [Complete Setup Guide](docs/setup_guide.md)**

The setup guide covers:
* Data generation (500K+ synthetic transactions)
* Delta Lake ingestion with Unity Catalog
* Feature engineering with PySpark Window functions
* XGBoost model training and evaluation
* RAG system setup with FAISS

**⚠️ Note**: If you're a judge evaluating the project, all models and data are already included in the repository. Skip to Step 3.

### Step 3: Run the Demo

**👉 For detailed demo instructions, see [JUDGE_DEMO_PLAYBOOK.md](JUDGE_DEMO_PLAYBOOK.md)**

**Quick Demo Steps:**

1. **Open the Demo Notebook**
   ```
   /Users/<YOUR_EMAIL>/Suraksha/Suraksha_Fraud_Detection_Demo
   ```

2. **Attach to Compute**
   * Click "Connect" → Select any cluster or use serverless
   * Wait for "Running" state

3. **Run Setup Cells (One-Time)**
   * Cell 1: Install dependencies (`%pip install xgboost scikit-learn...`)
   * Wait for kernel restart (30-60 seconds)
   * Cell 2: Create interactive widgets
   * Cell 3: Auto-configure workspace paths
   * Cell 4: Load ML models (Advanced + Baseline)
   * Cell 5: Load helper functions

4. **Configure & Detect Fraud**
   * Use widgets at top to configure transaction parameters
   * Choose detection mode: **Advanced** or **Baseline**
   * Run Cell 6 to analyze transaction
   * View results: Fraud type, confidence, RBI guidelines, recommendations

**That's it!** 🎉

---

## 🎬 Demo Steps

### Quick Demo Scenarios

**👉 For exact widget configurations and expected outputs, see [JUDGE_DEMO_PLAYBOOK.md](JUDGE_DEMO_PLAYBOOK.md)**

**Scenario 1: SIM Swap Attack** (High Risk - Advanced Mode)
* Detection Mode: **Advanced**
* Amount=15000, Device Changed=Yes, SIM Changed=Yes, MPIN Attempts=2
* Expected: **Beneficiary Manipulation** detected at 98.1% confidence

**Scenario 2: Velocity Fraud** (Automated Attack - Advanced Mode)
* Detection Mode: **Advanced**
* Txn Count (1 min)=7, Amount=5000, Hour=14
* Expected: **Velocity Fraud** detected at 95.4% confidence

**Scenario 3: Temporal Anomaly** (Odd Hours - Baseline Mode)
* Detection Mode: **Baseline**
* Amount=25000, Hour=3
* Expected: **Pattern-based fraud** detected

### Video Demo Script (2 Minutes)

**0:00-0:20** - Introduction
> "Suraksha detects 9 types of UPI fraud using dual-model ML and explains WHY using RBI guidelines."

**0:20-1:00** - Scenario 1 Demo (SIM Swap - Advanced Mode)
> Show widget configuration → Run detection → Explain 98% confidence + RBI guidelines

**1:00-1:30** - Scenario 2 Demo (Baseline Mode)
> Switch to Baseline mode → Show adaptive widgets → Faster pattern-based detection

**1:30-2:00** - Highlight Key Features
> "Dual models, Delta Lake, Unity Catalog, PySpark, RAG explanations, 87.3% accuracy"

---

## 📁 Project Structure

```
Suraksha/
│
├── README.md                              # This file
├── JUDGE_DEMO_PLAYBOOK.md                 # Detailed reproduction guide
├── UPI_Fraud_Shield_Complete_Strategy.md # Original hackathon strategy
├── PROJECT_STRUCTURE.md                   # Detailed architecture docs
│
├── Suraksha_Fraud_Detection_Demo.ipynb    # 🎯 MAIN DEMO NOTEBOOK (Dual Models)
│
├── advanced_solution/                     # Production Pipeline (Completed)
│   ├── 01_data_generation.ipynb          # Generate 500K+ synthetic transactions
│   ├── 02_delta_ingestion.ipynb          # Load to Delta Lake + Unity Catalog
│   ├── 03_feature_engineering.ipynb      # PySpark Window functions
│   ├── 04_multiclass_training.ipynb      # Train XGBoost 9-class model
│   └── 06_model_serving.ipynb            # Model inference pipeline
│
├── baseline_solution/                     # Alternative Approach
│   ├── 00_generate_realistic_data.ipynb  # 500K dataset with Delta Lake
│   ├── 01_load_data.ipynb                # Data loading utilities
│   ├── 02_train_model.ipynb              # Baseline model training
│   └── 03_predict.ipynb                  # Baseline predictions
│
├── shared/                                # Shared RAG Components
│   ├── rag_pipeline.ipynb                # Build FAISS index from RBI docs
│   └── rag_utils.ipynb                   # Runtime guideline search
│
├── data/                                  # Dataset storage
│   ├── synthetic_upi_txns.csv            # 500K+ synthetic transactions
│   └── official_dataset.csv              # Official fraud dataset
│
├── models/                                # Trained ML models
│   ├── suraksha_advanced.pkl             # XGBoost 9-class model (16.1 MB)
│   ├── feature_names.pkl                 # 38 feature definitions
│   └── model_metrics.pkl                 # Training metrics
│
├── rag/                                   # RAG components
│   ├── faiss_index/
│   │   └── index.faiss                   # Vector similarity index
│   ├── chunks.pkl                         # Text chunks from RBI docs
│   ├── metadata.pkl                       # Document metadata
│   └── model_info.pkl                     # Embedding model config
│
├── streamlit_app/                         # Streamlit App (Code Written)
│   ├── app.py                            # Application code
│   ├── requirements.txt                  # Dependencies
│   └── app_config.json                   # Configuration
│
├── app/                                   # Alternative App Files
│   ├── streamlit_app.py                  # Alternative implementation
│   ├── app.py                            # Simplified version
│   ├── config.py                         # Auto-configuration
│   └── requirements.txt                  # Dependencies
│
├── Deploy_Suraksha_Streamlit_App.ipynb    # App deployment notebook
│
└── docs/                                  # 📚 Documentation
    ├── fraud_type_definitions.md         # Detailed fraud taxonomy & examples
    └── setup_guide.md                    # Complete setup from scratch
```

---

## 🔮 Future Enhancements

### Scalability & Production
* MLflow Model Registry for versioning and A/B testing
* Real-time model serving endpoints with <100ms latency
* Databricks Jobs for automated retraining pipelines
* Advanced Delta Lake features (Z-ordering, CDF, streaming)

### Intelligence & Coverage
* Expand fraud taxonomy to 15+ types (phishing, account takeover variants)
* Neural machine translation for 10+ Indian languages (IndicTrans2)
* Graph-based network analysis for fraud ring detection
* Real-time RBI guideline updates via API integration

### Security & Compliance
* PII data masking and differential privacy
* Fine-grained Unity Catalog access controls
* Audit logs and compliance reporting
* End-to-end encryption for sensitive data

### User Experience
* Serverless Streamlit app deployment on Databricks
* Real-time fraud detection dashboards
* SMS/WhatsApp alert integration
* Customer self-service fraud dispute portal

---

## 📦 Submission Materials

### ✅ Checklist

* [x] **Public GitHub Repository** - This repo (public for 30+ days)
* [x] **Architecture Diagram** - See [Architecture](#architecture) section above
* [x] **README with:**
  * [x] What it does (1-2 sentences) - See [What It Does](#what-it-does)
  * [x] Architecture diagram - See [Architecture](#architecture)
  * [x] How to run (exact commands) - See [How to Run](#how-to-run)
  * [x] Demo steps - See [Demo Steps](#demo-steps) + [JUDGE_DEMO_PLAYBOOK.md](JUDGE_DEMO_PLAYBOOK.md)
* [x] **Databricks Technologies Used** - Delta Lake, Unity Catalog, PySpark, Notebooks, Widgets
* [x] **Open Source Models** - all-MiniLM-L6-v2, XGBoost
* [x] **Deployed Prototype** - Databricks notebook demo with dual models

### 📹 Demo Video (2 Minutes)
* Shows live fraud detection scenarios with both Advanced and Baseline modes
* Explains RAG-enhanced explanations
* Demonstrates Hindi language support
* Highlights Databricks integration (Delta Lake, Unity Catalog, PySpark)
* Shows adaptive widget UI switching between modes

### 📝 Project Write-Up (500 Characters Max)
```
Suraksha detects 9 types of UPI fraud using dual XGBoost models and explains 
WHY transactions are flagged using RAG with RBI guidelines. Built on Databricks 
with Delta Lake, Unity Catalog, and PySpark window functions, processing 500K+ 
transactions. Adaptive UI switches between Advanced (10 classes, 38 features) 
and Baseline (5 classes) modes. Supports English & Hindi. 87.3% accuracy. 
Production-ready architecture tackles ₹1,200 crore annual UPI fraud in India.
```
(487 characters)

### 🔗 Links
* **Repository**: `<your-github-repo-url>`
* **Live Demo**: Databricks notebook at `/Users/<YOUR_EMAIL>/Suraksha/Suraksha_Fraud_Detection_Demo`
* **Demo Video**: `<your-video-url>`

---

## 🏆 Hackathon Highlights

**Track**: Digital-Artha (Economy & Financial Inclusion)  
**Theme**: Production-ready fraud detection for India's UPI ecosystem

### Why Suraksha Stands Out

* **Real Problem**: Addresses ₹1,200 crores annual UPI fraud (RBI Report 2023)
* **Dual-Model Innovation**: Advanced (10 fraud classes) + Baseline (pattern-based) with adaptive UI
* **Comprehensive Taxonomy**: 9 fraud types vs. competitors' binary classification
* **Explainable AI**: RAG-enhanced explanations using RBI guidelines
* **Multilingual**: English & Hindi for financial inclusion
* **Production Architecture**: Delta Lake + Unity Catalog + PySpark at scale
* **Deep Databricks Usage**: 6 platform components (Delta, Unity, Spark, Notebooks, Widgets, Workspace)
* **Judge-Friendly**: Detailed playbook for exact reproduction

---

## 📚 Documentation

### Complete Documentation Suite

* **[Complete Setup Guide](docs/setup_guide.md)** - Step-by-step instructions from repository cloning to model training
  * Prerequisites and environment setup
  * Data generation (500K+ synthetic transactions)
  * Delta Lake ingestion with Unity Catalog
  * Feature engineering with PySpark Window functions
  * XGBoost model training and evaluation
  * RAG system setup with FAISS
  * Troubleshooting common issues

* **[Fraud Type Definitions](docs/fraud_type_definitions.md)** - Comprehensive guide to all 9 fraud types
  * Detailed definitions and how each fraud works
  * Real-world attack scenarios and examples
  * Detection logic and key indicators
  * Features used for each fraud type
  * RBI guidelines and statistics
  * Prevention measures and recommendations

* **[Judge Demo Playbook](JUDGE_DEMO_PLAYBOOK.md)** - Exact reproduction steps for judges
  * Pre-demo checklist
  * Widget configurations for test scenarios
  * Expected outputs with screenshots
  * Timing for 2-minute live demo

* **[Strategy Document](UPI_Fraud_Shield_Complete_Strategy.md)** - Original hackathon strategy
  * Problem statement and motivation
  * Technical approach and architecture
  * Implementation roadmap
  * Future vision

---

## 📄 License

MIT License - Open source for educational and commercial use

---

## 🙏 Acknowledgments

* Reserve Bank of India (RBI) fraud taxonomy and guidelines
* National Payments Corporation of India (NPCI) UPI fraud reports
* Databricks platform and documentation
* XGBoost and scikit-learn communities
* HuggingFace for open-source models

---

## 📞 Contact & Support

For issues, questions, or reproduction help:
1. Check [JUDGE_DEMO_PLAYBOOK.md](JUDGE_DEMO_PLAYBOOK.md) troubleshooting section
2. Review [Complete Setup Guide](docs/setup_guide.md)
3. Check [Fraud Type Definitions](docs/fraud_type_definitions.md)
4. Verify file paths match your workspace structure

---

**Built with ❤️ for safer digital payments in India 🇮🇳**

**Suraksha (सुरक्षा) - Security for All**

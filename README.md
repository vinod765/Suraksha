# Suraksha: UPI Fraud Detection System


## 👥 Team - Suraksha

* Dhoke Vinod Eknath - (240001025)
* Chetan Verma - (240001022)

## 🚀 What it does

Suraksha is an AI-powered UPI fraud detection system that classifies transactions into multiple fraud types and provides RBI-backed explanations with optional Hindi translation for better financial awareness.

---

## 🏗️ Architecture 

```text
                        ┌────────────────────────────┐
                        │        User (UI)           │
                        │  Streamlit Web Interface   │
                        └────────────┬───────────────┘
                                     │
                                     ▼
                     ┌────────────────────────────────┐
                     │   Input Processing Layer       │
                     │  (Transaction Details Form)    │
                     └────────────┬───────────────────┘
                                  │
                                  ▼
                ┌────────────────────────────────────┐
                │ Feature Engineering Layer          │
                │ (Spark / Pandas Transformations)   │
                └────────────┬───────────────────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
┌──────────────────────────┐      ┌──────────────────────────┐
│  Advanced Model Pipeline │      │ Baseline Model Pipeline  │
│  (Behavioral Features)   │      │ (Pattern Features)       │
│  XGBoost + MLflow        │      │ XGBoost + MLflow         │
└────────────┬─────────────┘      └────────────┬─────────────┘
             │                                 │
             └──────────────┬──────────────────┘
                            ▼
                ┌──────────────────────────────┐
                │   Fraud Classification Layer │
                │   (Multi-class Prediction)   │
                └────────────┬─────────────────┘
                             │
                             ▼
                ┌──────────────────────────────┐
                │   RAG Layer (Explainability) │
                │ RBI / NPCI / FATF Documents  │
                │ FAISS + Embeddings           │
                └────────────┬─────────────────┘
                             │
                             ▼
                ┌──────────────────────────────┐
                │ Translation Layer            │
                │ (IndicTrans2 - Hindi)        │
                └────────────┬─────────────────┘
                             │
                             ▼
                ┌──────────────────────────────┐
                │   Output Layer               │
                │ Fraud Type + Confidence      │
                │ RBI Explanation              │
                │ Hindi Translation            │
                └──────────────────────────────┘
```

---

## 🧠 Databricks Integration

```text
Data Layer:
- Delta Lake (transaction storage)

Processing:
- Apache Spark (feature engineering)

ML Layer:
- MLflow (model training & tracking)
- XGBoost (classification)

Serving:
- Databricks Apps (Streamlit deployment)
- DBFS (data + documents)

Explainability:
- RAG pipeline using RBI/NPCI documents
```

---


### Databricks Components Used

* Delta Lake (data storage)
* Apache Spark (feature engineering)
* MLflow (model tracking & training)
* Databricks Workspace (development)
* Databricks Apps (deployment)

---

## 🛠️ Tech Stack

### Databricks

* Apache Spark
* Delta Lake
* MLflow

### Machine Learning

* XGBoost (fraud classification)

### Open Source

* Streamlit (frontend)
* Pandas, NumPy (data handling)
* FAISS (vector search - RAG)
* Sentence Transformers (embeddings)
* IndicTrans2 (Hindi translation)

---

## 📊 Features

* Multi-class fraud detection (9 fraud types)
* Explainable AI using RBI/NPCI guidelines (RAG)
* Dual mode:

  * Advanced (behavior-based)
  * Baseline (pattern-based)
* Hindi language support


---

## ⚙️ How to Run

### 1. Clone the repo

```bash
git clone <your-repo-link>
cd Suraksha
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Streamlit app

```bash
cd app
streamlit run streamlit_app.py
```

---


## 📓 Notebook Demo (Fallback)

**Notebook Path / Link:** 

`<Add Databricks Notebook Link Here>`

## 🎮 Demo Steps

1. Open the Streamlit app
2. Select mode:

   * Advanced OR Baseline
3. Enter transaction details:

   * Amount
   * Time
   * Merchant category
4. Click **Detect Fraud**
5. View:

   * Fraud type
   * Confidence
   * RBI-based explanation
6. Toggle Hindi for translated output

---

## 📌 Notes

* MLflow is used for model training and tracking
* Lightweight model/dummy inference used in app for stable deployment
* RBI/NPCI documents used for explainable outputs

---

## 🏁 Future Improvements

* Real-time inference UI
* Improved multilingual support
* Enhanced fraud detection accuracy
---

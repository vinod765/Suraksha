# Suraksha Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                          SURAKSHA ARCHITECTURE                           │
│              UPI Fraud Detection with Explainable AI                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Component Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        📱 USER INTERFACE LAYER                            │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  │
│  ┃       Databricks Notebook with Interactive Widgets               ┃  │
│  ┃                                                                   ┃  │
│  ┃  • 16 configurable transaction parameters                        ┃  │
│  ┃  • Real-time fraud detection execution                           ┃  │
│  ┃  • Rich HTML/CSS visualization                                   ┃  │
│  ┃  • Language toggle (English/Hindi)                               ┃  │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  │
└──────────────────────────────┬───────────────────────────────────────────┘
                               │ User inputs transaction details
                               ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                          💾 DATA LAYER                                    │
│  ┌────────────────────────────┐    ┌────────────────────────────┐       │
│  │   Synthetic Dataset        │    │   Official Dataset         │       │
│  │   (120,000 transactions)   │    │   (Labeled fraud data)     │       │
│  ├────────────────────────────┤    ├────────────────────────────┤       │
│  │ • User identifiers (VPAs)  │    │ • 9 fraud type labels      │       │
│  │ • Device/SIM metadata      │    │ • Realistic patterns       │       │
│  │ • Behavioral patterns      │    │ • Training data source     │       │
│  │ • 38 feature columns       │    │ • CSV format               │       │
│  └────────────────────────────┘    └────────────────────────────┘       │
│                                                                           │
│  Storage: /Workspace/Users/<username>/Suraksha/data/                     │
└──────────────────────────────┬───────────────────────────────────────────┘
                               │ Load and transform
                               ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                     ⚙️  FEATURE ENGINEERING                               │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  │
│  ┃           Python/Pandas Feature Transformations                  ┃  │
│  ┃                                                                   ┃  │
│  ┃  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ ┃  │
│  ┃  │  Behavioral     │  │  Temporal       │  │  Statistical    │ ┃  │
│  ┃  │  Features       │  │  Features       │  │  Features       │ ┃  │
│  ┃  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤ ┃  │
│  ┃  │ • Velocity      │  │ • Hour of day   │  │ • Z-scores      │ ┃  │
│  ┃  │ • Txn history   │  │ • Day of week   │  │ • Percentiles   │ ┃  │
│  ┃  │ • Receiver flow │  │ • Odd hours     │  │ • Anomaly scores│ ┃  │
│  ┃  │ • Device change │  │ • Weekend flag  │  │ • Amount ratios │ ┃  │
│  ┃  └─────────────────┘  └─────────────────┘  └─────────────────┘ ┃  │
│  ┃                                                                   ┃  │
│  ┃  Total: 38 engineered features → Feature vector                  ┃  │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  │
└──────────────────────────────┬───────────────────────────────────────────┘
                               │ Feature vector (38 dimensions)
                               ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                      🤖 MACHINE LEARNING LAYER                            │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  │
│  ┃             XGBoost Multiclass Classifier                         ┃  │
│  ┃                                                                   ┃  │
│  ┃  Model: suraksha_advanced.pkl (16.1 MB)                          ┃  │
│  ┃  Algorithm: Gradient Boosting (XGBoost)                          ┃  │
│  ┃  Classes: 10 (9 fraud types + legitimate)                        ┃  │
│  ┃  Accuracy: 87.3%                                                  ┃  │
│  ┃                                                                   ┃  │
│  ┃  Output: Probability distribution across all classes             ┃  │
│  ┃  ┌──────────────────────────────────────────────────────────┐   ┃  │
│  ┃  │ Class 0: Legitimate               → 2.1%                 │   ┃  │
│  ┃  │ Class 1: Velocity Fraud          → 3.2%                 │   ┃  │
│  ┃  │ Class 2: Mule Account            → 1.5%                 │   ┃  │
│  ┃  │ Class 3: SIM Swap                → 95.3% ✓ DETECTED     │   ┃  │
│  ┃  │ Class 4: Device Takeover         → 4.7%                 │   ┃  │
│  ┃  │ Class 5: Beneficiary Manipulation→ 8.9%                 │   ┃  │
│  ┃  │ ...                                                       │   ┃  │
│  ┃  └──────────────────────────────────────────────────────────┘   ┃  │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  │
└──────────────────────────────┬───────────────────────────────────────────┘
                               │ Predicted fraud type
                               ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                   📚 EXPLAINABILITY LAYER (RAG)                           │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  │
│  ┃        Retrieval-Augmented Generation (RAG) System               ┃  │
│  ┃                                                                   ┃  │
│  ┃  ┌────────────────┐      ┌────────────────┐     ┌────────────┐  ┃  │
│  ┃  │  FAISS Vector  │      │  Semantic      │     │   RBI      │  ┃  │
│  ┃  │  Store         │  →   │  Search        │  →  │ Guidelines │  ┃  │
│  ┃  │  (index.faiss) │      │  (Top-K)       │     │ Retrieval  │  ┃  │
│  ┃  └────────────────┘      └────────────────┘     └────────────┘  ┃  │
│  ┃           ↑                                                       ┃  │
│  ┃           │                                                       ┃  │
│  ┃  ┌────────────────┐      ┌────────────────┐                     ┃  │
│  ┃  │  Embeddings    │      │  Text Chunks   │                     ┃  │
│  ┃  │  (MiniLM-L6)   │      │  (chunks.pkl)  │                     ┃  │
│  ┃  └────────────────┘      └────────────────┘                     ┃  │
│  ┃                                                                   ┃  │
│  ┃  Knowledge Base: RBI Fraud Reports, NPCI Guidelines              ┃  │
│  ┃  Purpose: Explain WHY transaction was flagged as fraud           ┃  │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  │
└──────────────────────────────┬───────────────────────────────────────────┘
                               │ Retrieved guidelines + explanations
                               ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                    📊 OUTPUT & RECOMMENDATION LAYER                       │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  │
│  ┃                    Results Display                                ┃  │
│  ┃  ┌──────────────────────────────────────────────────────────┐    ┃  │
│  ┃  │  ⚠️  FRAUD DETECTED                                       │    ┃  │
│  ┃  │  Fraud Type: SIM Swap Attack                            │    ┃  │
│  ┃  │  Confidence: 95.3%                                       │    ┃  │
│  ┃  │  Risk Level: 🔴 HIGH                                     │    ┃  │
│  ┃  ├──────────────────────────────────────────────────────────┤    ┃  │
│  ┃  │  🔍 Detection Indicators:                                │    ┃  │
│  ┃  │  • SIM card swap detected                               │    ┃  │
│  ┃  │  • Device change detected                               │    ┃  │
│  ┃  │  • Multiple MPIN attempts (2)                           │    ┃  │
│  ┃  ├──────────────────────────────────────────────────────────┤    ┃  │
│  ┃  │  📚 RBI Guidelines Reference:                            │    ┃  │
│  ┃  │  "SIM swap fraud increased 34% YoY (NPCI 2023)..."      │    ┃  │
│  ┃  ├──────────────────────────────────────────────────────────┤    ┃  │
│  ┃  │  💡 Recommended Actions:                                 │    ┃  │
│  ┃  │  1. 🚫 BLOCK transaction immediately                     │    ┃  │
│  ┃  │  2. 📞 Contact customer via registered phone             │    ┃  │
│  ┃  │  3. 🔒 Freeze account temporarily                        │    ┃  │
│  ┃  │  4. 🔍 Investigate recent activity                       │    ┃  │
│  ┃  └──────────────────────────────────────────────────────────┘    ┃  │
│  ┃                                                                   ┃  │
│  ┃  🌐 Language: English / हिंदी                                    ┃  │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  │
└──────────────────────────────────────────────────────────────────────────┘
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────────────┐
│                       DATABRICKS PLATFORM                            │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐       │
│  │   Notebooks    │  │   Workspace    │  │     Python     │       │
│  │   (Demo UI)    │  │  (File Store)  │  │   (Compute)    │       │
│  └────────────────┘  └────────────────┘  └────────────────┘       │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                     MACHINE LEARNING STACK                           │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐       │
│  │    XGBoost     │  │  scikit-learn  │  │     Pandas     │       │
│  │ (Classifier)   │  │  (Utilities)   │  │  (Features)    │       │
│  └────────────────┘  └────────────────┘  └────────────────┘       │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                       RAG & EMBEDDINGS                               │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐       │
│  │     FAISS      │  │ sentence-trans │  │   HuggingFace  │       │
│  │ (Vector Store) │  │   (Embeddings) │  │  (all-MiniLM)  │       │
│  └────────────────┘  └────────────────┘  └────────────────┘       │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌─────────────┐
│ User Input  │
│ (16 params) │
└──────┬──────┘
       │
       ▼
┌────────────────────┐
│ Feature Engineering│
│ (38 features)      │
└──────┬─────────────┘
       │
       ▼
┌────────────────────┐        ┌──────────────────┐
│  XGBoost Model     │───────▶│ Fraud Type       │
│  Prediction        │        │ + Confidence (%) │
└────────────────────┘        └──────┬───────────┘
                                     │
                                     ▼
                              ┌──────────────────┐
                              │ RAG System       │
                              │ (FAISS Search)   │
                              └──────┬───────────┘
                                     │
                                     ▼
                              ┌──────────────────┐
                              │ RBI Guidelines   │
                              │ + Explanations   │
                              └──────┬───────────┘
                                     │
                                     ▼
                              ┌──────────────────┐
                              │ Display Results  │
                              │ (EN/HI)          │
                              └──────────────────┘
```

---

## Fraud Detection Types

```
┌────────────────────────────────────────────────────────────────┐
│                   9 FRAUD TYPES DETECTED                        │
├────────────────────────────────────────────────────────────────┤
│  Behavior-Based (Requires User Tracking)                       │
│  ├─ 1. Velocity Fraud          (7+ txns/min)                  │
│  ├─ 2. Mule Account            (rapid in/out flows)           │
│  ├─ 3. SIM Swap                (SIM change + transactions)    │
│  ├─ 4. Device Takeover         (new device + location)        │
│  └─ 5. Beneficiary Manipulation(social engineering)           │
│                                                                 │
│  Pattern-Based (Statistical Detection)                         │
│  ├─ 6. Amount Anomaly          (z-score > 3)                  │
│  ├─ 7. Temporal Anomaly        (odd hours: 2-5 AM)            │
│  ├─ 8. Merchant Fraud          (high-risk patterns)           │
│  └─ 9. Failed-Then-Success     (card testing)                 │
└────────────────────────────────────────────────────────────────┘
```

---

**Note**: This diagram represents the current implementation. See README.md "Future Improvements" section for planned enhancements (Delta Lake, Unity Catalog, MLflow Registry, etc.).

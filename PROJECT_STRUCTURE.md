# Suraksha Project Structure

```
suraksha/
│
├── README.md                               # Project overview
├── UPI_Fraud_Shield_Complete_Strategy.md  # Complete hackathon strategy
├── PROJECT_STRUCTURE.md                   # This file
├── .gitignore                             # Git ignore rules
│
├── app/                                   # Frontend Layer
│   ├── streamlit_app.py                   # PRIMARY: Streamlit app with dual-mode
│   ├── gradio_app.py                      # BACKUP: Alternative UI (if Streamlit fails)
│   ├── requirements.txt                   # Python dependencies
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── model_loader.py                # MLflow model loading utilities
│   │   ├── rag_search.py                  # RAG search wrapper (calls shared/rag_utils)
│   │   ├── translator.py                  # IndicTrans2 Hindi translation
│   │   └── feature_engineering.py         # Dynamic feature generation
│   └── assets/
│       ├── .gitkeep
│       └── rbi_docs/                      # RBI/NPCI PDFs for RAG
│
├── shared/                                # 🆕 SHARED COMPONENTS (Both Models Use)
│   ├── __init__.py
│   ├── README.md                          # Explains why RAG is shared
│   ├── rag_pipeline.py                    # FAISS vector store creation (run once)
│   └── rag_utils.py                       # Runtime guideline search (used by both)
│
├── advanced_solution/                     # Advanced ML Pipeline (9 fraud types)
│   ├── __init__.py
│   ├── 01_data_generation.py              # Synthetic dataset with user IDs
│   ├── 02_delta_ingestion.py              # Delta Lake Bronze layer
│   ├── 03_feature_engineering.py          # Spark window functions for behavior
│   ├── 04_multiclass_training.py          # XGBoost 9-class model → MLflow
│   └── 06_model_serving.py                # Inference endpoint (uses shared/rag_utils)
│
├── baseline_solution/                     # Baseline ML Pipeline (4 fraud patterns)
│   ├── __init__.py
│   ├── 01_data_ingestion.py               # Official dataset ingestion
│   ├── 02_pattern_features.py             # Pattern-based features
│   ├── 03_binary_training.py              # XGBoost 4-class model → MLflow
│   └── 04_model_serving.py                # Inference endpoint (uses shared/rag_utils)
│
├── data/                                  # Data Directory
│   ├── .gitkeep
│   └── rbi_documents/                     # RBI/NPCI PDF storage
│       └── .gitkeep
│
└── docs/                                  # Documentation
    ├── fraud_type_definitions.md          # Detailed fraud taxonomy
    └── setup_guide.md                     # Installation & setup instructions
```

## Key Architecture Decisions

### 1. Why `shared/` Folder?
**Both** Advanced and Baseline models need RAG for explanations:
- Advanced detects **9 specific fraud types** → RAG explains each type
- Baseline detects **4 pattern-based types** → RAG explains each pattern
- **Same FAISS index**, same RBI guidelines, different fraud taxonomies
- Avoids code duplication and ensures consistent explanations

### 2. Why Gradio + Streamlit?
Per strategy document (Section 4: Frontend Tech Stack):
- **Streamlit** = Primary (professional, works on Databricks Free Edition)
- **Gradio** = Backup (if Streamlit has issues during hackathon)
- Demo uses `streamlit_app.py` unless issues arise

### 3. Model Serving Flow
```
[Transaction Input]
        ↓
[app/streamlit_app.py]
        ↓
[MLflow Model: suraksha_advanced OR suraksha_baseline]
        ↓
[Predicted Fraud Type]
        ↓
[shared/rag_utils.search_guidelines()]  ← Same for both models
        ↓
[RBI Guideline Explanation]
        ↓
[app/utils/translator.py] (if Hindi selected)
        ↓
[Display to User]
```

## Databricks Components Used

1. **Delta Lake** - Bronze/Silver/Gold data architecture
2. **Spark** - Distributed feature engineering
3. **MLflow** - Model tracking and registry (2 models)
4. **Unity Catalog** - Data governance
5. **DBFS** - Vector store (`/dbfs/suraksha/rag/`) and artifacts
6. **Databricks App** - Serverless Streamlit deployment

## Quick Start

See [docs/setup_guide.md](docs/setup_guide.md) for detailed setup instructions.

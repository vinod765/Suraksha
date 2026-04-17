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
│   ├── streamlit_app.py                   # Main Streamlit app with dual-mode
│   ├── gradio_app.py                      # Alternative UI (backup)
│   ├── requirements.txt                   # Python dependencies
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── model_loader.py                # MLflow model loading utilities
│   │   ├── rag_search.py                  # RAG pipeline for RBI guideline search
│   │   ├── translator.py                  # IndicTrans2 Hindi translation
│   │   └── feature_engineering.py         # Dynamic feature generation
│   └── assets/
│       ├── .gitkeep
│       └── rbi_docs/                      # RBI/NPCI PDFs for RAG
│
├── advanced_solution/                     # Advanced ML Pipeline
│   ├── __init__.py
│   ├── 01_data_generation.py              # Synthetic dataset with user IDs
│   ├── 02_delta_ingestion.py              # Delta Lake Bronze layer
│   ├── 03_feature_engineering.py          # Spark window functions for behavior
│   ├── 04_multiclass_training.py          # XGBoost 9-class model → MLflow
│   ├── 05_rag_pipeline.py                 # FAISS vector store creation
│   └── 06_model_serving.py                # Real-time inference endpoint
│
├── baseline_solution/                     # Baseline ML Pipeline
│   ├── __init__.py
│   ├── 01_data_ingestion.py               # Official dataset ingestion
│   ├── 02_pattern_features.py             # Pattern-based features
│   └── 03_binary_training.py              # XGBoost 4-class model → MLflow
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

## Key Files

- **UPI_Fraud_Shield_Complete_Strategy.md**: Complete 15-hour hackathon strategy
- **app/streamlit_app.py**: Main application entry point
- **app/requirements.txt**: All Python dependencies
- **docs/fraud_type_definitions.md**: Definitions of all 9 fraud types
- **docs/setup_guide.md**: Step-by-step setup instructions

## Databricks Components Used

1. **Delta Lake** - Bronze/Silver/Gold data architecture
2. **Spark** - Distributed feature engineering
3. **MLflow** - Model tracking and registry
4. **Unity Catalog** - Data governance
5. **DBFS** - Vector store and artifacts
6. **Databricks App** - Serverless Streamlit deployment

## Quick Start

See [docs/setup_guide.md](docs/setup_guide.md) for detailed setup instructions.

# Suraksha Setup Guide

## Prerequisites
- Databricks Workspace (Free Edition or higher)
- Unity Catalog enabled
- Python 3.10+
- GitHub account (for Git Folder integration)

## Step 1: Clone Repository
```bash
# In Databricks workspace, create Git Folder
# URL: https://github.com/<your-username>/suraksha
```

## Step 2: Data Setup

### Synthetic Data Generation
```bash
# Run advanced_solution/01_data_generation.py
# This creates 120,000 synthetic UPI transactions with:
# - 114,000 legitimate (95%)
# - 6,000 fraudulent across 9 types (5%)
```

### Unity Catalog Tables
```sql
-- Create catalog and schemas
CREATE CATALOG IF NOT EXISTS workspace;
CREATE SCHEMA IF NOT EXISTS workspace.bronze;
CREATE SCHEMA IF NOT EXISTS workspace.silver;
CREATE SCHEMA IF NOT EXISTS workspace.gold;
```

## Step 3: Feature Engineering
```bash
# Run advanced_solution/03_feature_engineering.py
# Generates behavioral features using Spark window functions
```

## Step 4: Model Training
```bash
# Advanced model (9-class)
python advanced_solution/04_multiclass_training.py

# Baseline model (4-class)
python baseline_solution/03_binary_training.py

# Models registered in MLflow as:
# - suraksha_advanced
# - suraksha_baseline
```

## Step 5: RAG Pipeline Setup
```bash
# Run advanced_solution/05_rag_pipeline.py
# Creates FAISS vector store from RBI/NPCI documents
# Stored in: /dbfs/suraksha/rag/
```

## Step 6: Deploy Streamlit App
```bash
cd app
streamlit run streamlit_app.py
```

## Architecture Components

### Databricks Usage
1. **Delta Lake** - Bronze/Silver/Gold data layers with time travel
2. **Spark** - Distributed feature engineering with window functions
3. **MLflow** - Experiment tracking and model registry
4. **Unity Catalog** - Governance and data lineage
5. **DBFS** - Vector store and model artifacts storage
6. **Databricks App** - Serverless Streamlit deployment

### Data Flow
```
[Raw Data] → Delta Bronze → Spark Processing → Delta Silver → 
ML Training → MLflow Registry → Real-time Inference → Streamlit UI
```

## Troubleshooting

### Issue: Models not found in MLflow
**Solution:** Check model names match exactly: "suraksha_advanced" / "suraksha_baseline"

### Issue: FAISS index not loading
**Solution:** Verify path exists: `/dbfs/suraksha/rag/faiss_index`

### Issue: IndicTrans2 translation slow
**Solution:** Use quantized model (model is already configured for CPU inference)

## Performance Benchmarks
- Advanced Model: 94.2% accuracy on 9-class multiclass
- Baseline Model: 82.1% accuracy on 4-class pattern detection
- RAG retrieval: < 200ms per query
- Translation: 2-3 seconds per response

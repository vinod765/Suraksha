# 🛡️ Suraksha - Complete Setup Guide

**From Repository Clone to Production-Ready Fraud Detection**

This guide walks you through setting up Suraksha from scratch - cloning the repository, generating data, training models, and running the demo.

---

## 📋 Table of Contents

* [Prerequisites](#prerequisites)
* [Part 1: Repository Setup](#part-1-repository-setup)
* [Part 2: Data Generation](#part-2-data-generation)
* [Part 3: Delta Lake Ingestion](#part-3-delta-lake-ingestion)
* [Part 4: Feature Engineering](#part-4-feature-engineering)
* [Part 5: Model Training](#part-5-model-training)
* [Part 6: RAG System Setup](#part-6-rag-system-setup)
* [Part 7: Running the Demo](#part-7-running-the-demo)
* [Troubleshooting](#troubleshooting)
* [Architecture Overview](#architecture-overview)

---

## 🔧 Prerequisites

### Required
* **Databricks Workspace** (Community Edition or paid tier)
  * Sign up at: https://www.databricks.com/try-databricks
  * Community Edition: Free, includes 15GB cluster
  * Paid tier: Better for production workloads
* **Python 3.8+** (included in Databricks)
* **Compute Cluster** (any size - serverless auto-selected)
* **GitHub Account** (for repository cloning)

### Optional but Recommended
* **Unity Catalog Enabled** (automatic in newer workspaces)
* **Admin Permissions** (for catalog creation)
* **At least 2-4 GB RAM** on cluster (for model training)

### Skills Needed
* Basic SQL knowledge
* Python familiarity
* Understanding of machine learning concepts
* Familiarity with Databricks notebooks

---

## 📦 Part 1: Repository Setup

### Option A: Using Databricks Repos (Recommended)

1. **Navigate to Repos**
   ```
   Databricks Workspace → Left sidebar → Repos
   ```

2. **Add Repository**
   * Click "Add Repo" button
   * Enter your GitHub repository URL:
     ```
     https://github.com/<your-username>/suraksha
     ```
   * Select branch: `main` or `master`
   * Click "Create Repo"

3. **Verify Structure**
   ```
   Repos/<your-username>/suraksha/
   ├── Suraksha_Fraud_Detection_Demo.ipynb
   ├── advanced_solution/
   ├── baseline_solution/
   ├── shared/
   ├── data/
   ├── models/
   └── README.md
   ```

### Option B: Manual Upload (Alternative)

1. **Clone Locally**
   ```bash
   git clone https://github.com/<your-username>/suraksha.git
   cd suraksha
   ```

2. **Upload to Workspace**
   * Databricks Workspace → Left sidebar → Workspace
   * Navigate to `/Users/<your-email>/`
   * Click "⋮" menu → "Import"
   * Select all `.ipynb` files and folders
   * Click "Import"

3. **Upload Data Files**
   * Navigate to `/Users/<your-email>/Suraksha/data/`
   * Click "⋮" menu → "Upload Data"
   * Upload `synthetic_upi_txns.csv` (may take 1-2 minutes for 500K+ rows)

---

## 🗄️ Part 2: Data Generation

**Goal:** Generate 500,000+ synthetic UPI transactions with 9 fraud types

### Step 2.1: Open Data Generation Notebook

```
/Users/<your-email>/Suraksha/advanced_solution/01_data_generation.ipynb
```

### Step 2.2: Attach Compute

* Click "Connect" at top-right
* Select any available cluster (or create new)
* Recommended: 2 workers, 8 GB RAM each
* Wait for cluster to reach "Running" state

### Step 2.3: Run Data Generation

**Cell 1: Install Dependencies**
```python
%pip install faker numpy pandas
dbutils.library.restartPython()
```

**Cell 2-5: Generate Data**
* Run cells sequentially (Shift+Enter)
* Generates 500,000+ transactions
* Distribution:
  * 475,000 legitimate (95%)
  * 25,000 fraudulent across 9 types (5%)

**Cell 6: Save to CSV**
```python
# Saves to: /Workspace/Users/<your-email>/Suraksha/data/synthetic_upi_txns.csv
output_path = f"/Workspace/Users/{current_user}/Suraksha/data/synthetic_upi_txns.csv"
df.to_csv(output_path, index=False)
print(f"✅ Saved {len(df):,} transactions to {output_path}")
```

### Step 2.4: Verify Output

```python
# Check file size and row count
import os
file_size_mb = os.path.getsize(output_path) / (1024**2)
print(f"File size: {file_size_mb:.2f} MB")
print(f"Row count: {len(df):,}")
print(f"Fraud percentage: {(df['is_fraud'].sum() / len(df) * 100):.2f}%")
```

**Expected Output:**
```
File size: ~45-55 MB
Row count: 500,000+
Fraud percentage: ~5.00%
```

---

## 🏗️ Part 3: Delta Lake Ingestion

**Goal:** Load data into Delta Lake with Unity Catalog governance

### Step 3.1: Open Ingestion Notebook

```
/Users/<your-email>/Suraksha/advanced_solution/02_delta_ingestion.ipynb
```

### Step 3.2: Create Unity Catalog Structure

**Cell 1: Create Catalog and Schemas**
```sql
-- Create catalog (requires admin permissions in some workspaces)
CREATE CATALOG IF NOT EXISTS workspace;

-- Create schemas for medallion architecture
CREATE SCHEMA IF NOT EXISTS workspace.bronze;
CREATE SCHEMA IF NOT EXISTS workspace.silver;
CREATE SCHEMA IF NOT EXISTS workspace.gold;

-- Verify creation
SHOW SCHEMAS IN workspace;
```

**Expected Output:**
```
bronze
silver
gold
```

### Step 3.3: Load Data to Bronze Layer

**Cell 2: Read CSV and Write to Delta**
```python
from pyspark.sql import functions as F

# Read CSV
csv_path = f"/Workspace/Users/{current_user}/Suraksha/data/synthetic_upi_txns.csv"
df = spark.read.csv(csv_path, header=True, inferSchema=True)

# Write to Delta Lake bronze layer
df.write \
  .format("delta") \
  .mode("overwrite") \
  .option("overwriteSchema", "true") \
  .saveAsTable("workspace.bronze.upi")

print(f"✅ Loaded {df.count():,} rows to workspace.bronze.upi")
```

### Step 3.4: Verify Delta Table

**Cell 3: Check Table Properties**
```sql
-- Check table
DESCRIBE EXTENDED workspace.bronze.upi;

-- Sample data
SELECT * FROM workspace.bronze.upi LIMIT 10;

-- Fraud distribution
SELECT fraud_type, COUNT(*) as count 
FROM workspace.bronze.upi 
GROUP BY fraud_type 
ORDER BY count DESC;
```

**Expected Output:**
```
fraud_type                    | count
------------------------------|--------
legitimate                    | 475,000
velocity_fraud               | 2,800
mule_account                 | 2,600
sim_swap                     | 2,500
... (9 fraud types total)
```

---

## ⚙️ Part 4: Feature Engineering

**Goal:** Engineer 38 behavioral features using PySpark Window functions

### Step 4.1: Open Feature Engineering Notebook

```
/Users/<your-email>/Suraksha/advanced_solution/03_feature_engineering.ipynb
```

### Step 4.2: Create Window Functions

**Key Features Generated:**

**Velocity Features (Window over 1 minute, 5 minutes)**
```python
from pyspark.sql import Window
from pyspark.sql.functions import *

# Window: 1 minute before current transaction
window_1min = Window.partitionBy("sender_upi") \
                    .orderBy("timestamp") \
                    .rangeBetween(-60, 0)

# Count transactions in last 1 minute
df = df.withColumn("txn_count_1min", count("*").over(window_1min))
```

**User History Features**
```python
# Average transaction amount for user
df = df.withColumn("user_avg_amount", 
                   avg("amount").over(Window.partitionBy("sender_upi")))

# Days since account creation
df = df.withColumn("account_age_days",
                   datediff(col("timestamp"), col("account_creation_date")))
```

**Mule Account Detection**
```python
# Count of unique receivers (money laundering indicator)
df = df.withColumn("unique_receivers_count",
                   countDistinct("receiver_upi").over(window_30days))
```

**Temporal Features**
```python
# Extract hour, day of week, is_weekend
df = df.withColumn("hour_of_day", hour("timestamp"))
df = df.withColumn("day_of_week", dayofweek("timestamp"))
df = df.withColumn("is_weekend", when(col("day_of_week").isin(1,7), 1).otherwise(0))
```

### Step 4.3: Save to Silver Layer

**Cell 5: Write Engineered Features**
```python
# Write to Delta Lake silver layer
df.write \
  .format("delta") \
  .mode("overwrite") \
  .saveAsTable("workspace.silver.upi_features")

print(f"✅ Feature engineering complete: {len(df.columns)} columns")
print(f"✅ Saved to workspace.silver.upi_features")
```

### Step 4.4: Verify Features

```sql
-- Check feature columns
DESCRIBE workspace.silver.upi_features;

-- Sample engineered features
SELECT 
  transaction_id,
  amount,
  txn_count_1min,
  txn_count_5min,
  user_avg_amount,
  velocity_amount_1min,
  is_weekend,
  hour_of_day
FROM workspace.silver.upi_features
LIMIT 10;
```

**Total Features:** 38 columns
* Original: 20 columns (transaction data)
* Engineered: 18 columns (behavioral features)

---

## 🤖 Part 5: Model Training

**Goal:** Train XGBoost multiclass classifier for 9 fraud types

### Step 5.1: Open Training Notebook

```
/Users/<your-email>/Suraksha/advanced_solution/04_multiclass_training.ipynb
```

### Step 5.2: Prepare Training Data

**Cell 1: Load and Split Data**
```python
from sklearn.model_selection import train_test_split
import pandas as pd

# Load from Delta Lake
df = spark.table("workspace.silver.upi_features").toPandas()

# Feature columns (38 features)
feature_cols = [col for col in df.columns if col not in 
                ['transaction_id', 'fraud_type', 'is_fraud', 'timestamp', 'sender_upi', 'receiver_upi']]

X = df[feature_cols]
y = df['fraud_type']  # 10 classes (9 fraud + 1 legitimate)

# Split: 70% train, 15% validation, 15% test
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)

print(f"Training set: {len(X_train):,} samples")
print(f"Validation set: {len(X_val):,} samples")
print(f"Test set: {len(X_test):,} samples")
```

### Step 5.3: Train XGBoost Model

**Cell 2: Configure and Train**
```python
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder

# Encode labels
le = LabelEncoder()
y_train_encoded = le.fit_transform(y_train)
y_val_encoded = le.transform(y_val)

# Configure XGBoost
model = XGBClassifier(
    n_estimators=200,
    max_depth=8,
    learning_rate=0.1,
    objective='multi:softprob',
    num_class=10,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)

# Train model
print("🏋️ Training XGBoost model...")
model.fit(
    X_train, y_train_encoded,
    eval_set=[(X_val, y_val_encoded)],
    early_stopping_rounds=20,
    verbose=10
)

print("✅ Training complete!")
```

**Expected Training Time:**
* Community Edition: 5-10 minutes
* Paid tier (4 cores): 2-3 minutes

### Step 5.4: Evaluate Model

**Cell 3: Calculate Metrics**
```python
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# Predictions
y_test_encoded = le.transform(y_test)
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test_encoded, y_pred)
print(f"✅ Test Accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")

# Classification report
print("\n📊 Classification Report:")
print(classification_report(y_test_encoded, y_pred, target_names=le.classes_))

# Confusion matrix
cm = confusion_matrix(y_test_encoded, y_pred)
print("\n🔢 Confusion Matrix:")
print(cm)
```

**Expected Performance:**
```
Test Accuracy: 0.873 (87.3%)

Fraud Type             Precision  Recall  F1-Score
----------------------------------------------------
legitimate             0.92       0.95    0.94
velocity_fraud         0.88       0.85    0.86
mule_account          0.84       0.82    0.83
sim_swap              0.86       0.84    0.85
... (9 fraud types)
```

### Step 5.5: Save Model

**Cell 4: Save Model and Metadata**
```python
import joblib
from pathlib import Path

# Create models directory
models_dir = Path(f"/Workspace/Users/{current_user}/Suraksha/models")
models_dir.mkdir(exist_ok=True)

# Save model
model_path = models_dir / "suraksha_advanced.pkl"
joblib.dump(model, model_path)
print(f"✅ Model saved: {model_path}")

# Save feature names
feature_names_path = models_dir / "feature_names.pkl"
joblib.dump(feature_cols, feature_names_path)
print(f"✅ Feature names saved: {feature_names_path}")

# Save label encoder
label_encoder_path = models_dir / "label_encoder.pkl"
joblib.dump(le, label_encoder_path)
print(f"✅ Label encoder saved: {label_encoder_path}")

# Save model metrics
metrics = {
    'accuracy': accuracy,
    'num_features': len(feature_cols),
    'num_classes': len(le.classes_),
    'training_samples': len(X_train)
}
metrics_path = models_dir / "model_metrics.pkl"
joblib.dump(metrics, metrics_path)
print(f"✅ Metrics saved: {metrics_path}")
```

**Model File Size:** ~16.1 MB

---

## 🧠 Part 6: RAG System Setup

**Goal:** Build FAISS vector index for RBI guideline retrieval

### Step 6.1: Open RAG Pipeline Notebook

```
/Users/<your-email>/Suraksha/shared/rag_pipeline.ipynb
```

### Step 6.2: Install RAG Dependencies

**Cell 1: Install Libraries**
```python
%pip install faiss-cpu sentence-transformers --quiet
dbutils.library.restartPython()
```

### Step 6.3: Prepare RBI Documents

**Cell 2: Load Fraud Guidelines**
```python
# Sample RBI fraud guidelines
rbi_docs = [
    {
        "title": "RBI Annual Report 2023 - UPI Fraud Statistics",
        "content": "Velocity fraud accounts for 18% of UPI fraud cases. Characterized by multiple rapid transactions...",
        "source": "RBI Annual Report 2023, Chapter 7"
    },
    {
        "title": "NPCI Advisory - SIM Swap Attacks",
        "content": "SIM swap fraud increased 34% YoY. Attackers replace victim's SIM card to intercept OTPs...",
        "source": "NPCI Security Advisory Nov 2023"
    },
    # ... (add all 9 fraud type guidelines)
]

# Split into chunks for better retrieval
chunks = []
for doc in rbi_docs:
    chunk = {
        'text': f"{doc['title']}. {doc['content']}",
        'source': doc['source'],
        'fraud_type': doc.get('fraud_type', 'general')
    }
    chunks.append(chunk)

print(f"✅ Prepared {len(chunks)} document chunks")
```

### Step 6.4: Build FAISS Index

**Cell 3: Create Vector Embeddings**
```python
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Load embedding model
print("📥 Loading embedding model...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Model loaded")

# Generate embeddings
print("🔢 Generating embeddings...")
texts = [chunk['text'] for chunk in chunks]
embeddings = embedding_model.encode(texts, show_progress_bar=True)

# Create FAISS index
print("🏗️ Building FAISS index...")
dimension = embeddings.shape[1]  # 384 for all-MiniLM-L6-v2
index = faiss.IndexFlatL2(dimension)
index.add(embeddings.astype('float32'))

print(f"✅ FAISS index created: {index.ntotal} vectors, {dimension} dimensions")
```

### Step 6.5: Save RAG Artifacts

**Cell 4: Save to Workspace**
```python
from pathlib import Path

# Create RAG directory
rag_dir = Path(f"/Workspace/Users/{current_user}/Suraksha/rag")
rag_dir.mkdir(exist_ok=True)
faiss_dir = rag_dir / "faiss_index"
faiss_dir.mkdir(exist_ok=True)

# Save FAISS index
faiss.write_index(index, str(faiss_dir / "index.faiss"))
print(f"✅ FAISS index saved: {faiss_dir / 'index.faiss'}")

# Save chunks
with open(rag_dir / "chunks.pkl", 'wb') as f:
    pickle.dump(chunks, f)
print(f"✅ Chunks saved: {rag_dir / 'chunks.pkl'}")

# Save metadata
metadata = {
    'num_chunks': len(chunks),
    'embedding_dim': dimension,
    'model_name': 'all-MiniLM-L6-v2'
}
with open(rag_dir / "metadata.pkl", 'wb') as f:
    pickle.dump(metadata, f)
print(f"✅ Metadata saved: {rag_dir / 'metadata.pkl'}")
```

### Step 6.6: Test RAG Retrieval

**Cell 5: Test Query**
```python
def search_guidelines(query, top_k=3):
    # Embed query
    query_embedding = embedding_model.encode([query])
    
    # Search FAISS
    distances, indices = index.search(query_embedding.astype('float32'), top_k)
    
    # Retrieve chunks
    results = []
    for idx in indices[0]:
        results.append(chunks[idx])
    
    return results

# Test query
test_query = "What is velocity fraud?"
results = search_guidelines(test_query)

print(f"Query: {test_query}\n")
for i, result in enumerate(results, 1):
    print(f"{i}. {result['text'][:100]}...")
    print(f"   Source: {result['source']}\n")
```

**Expected Retrieval Time:** <200ms per query

---

## 🎬 Part 7: Running the Demo

**Goal:** Run interactive fraud detection demo with dual models

### Step 7.1: Open Demo Notebook

```
/Users/<your-email>/Suraksha/Suraksha_Fraud_Detection_Demo.ipynb
```

### Step 7.2: Install Dependencies

**Cell 1: One-Time Setup**
```python
%pip install xgboost scikit-learn pandas numpy joblib --quiet
dbutils.library.restartPython()
```
**Wait:** 30-60 seconds for kernel restart

### Step 7.3: Create Widgets

**Cell 2: Create Input Widgets**
* Run this cell
* Widgets appear above the notebook
* **Detection Mode** dropdown: Advanced / Baseline
* 16 input fields (Advanced mode) or 9 fields (Baseline mode)

### Step 7.4: Load Models

**Cell 3-5: Initialize System**
* Cell 3: Auto-detects workspace paths
* Cell 4: Loads Advanced + Baseline models
* Cell 5: Loads helper functions

**Expected Output from Cell 4:**
```
✅ Advanced Model: Loaded from file
⚠️ Baseline Model: Using demo mode

📊 Model Configuration:
   • Advanced: 10 fraud classes
   • Baseline: 5 fraud classes
```

### Step 7.5: Run Fraud Detection

**Cell 6: Analyze Transaction**

**Test Scenario 1: SIM Swap Attack (Advanced Mode)**
1. Set widgets:
   * Detection Mode: **Advanced**
   * Amount: 15000
   * Device Changed: Yes
   * SIM Changed: Yes
   * MPIN Attempts: 2
   * Hour: 14
2. Run Cell 6
3. Expected: **Beneficiary Manipulation** detected at 98.1% confidence

**Test Scenario 2: Velocity Fraud (Advanced Mode)**
1. Set widgets:
   * Detection Mode: **Advanced**
   * Txn Count (1 min): 7
   * Amount: 5000
   * Hour: 14
2. Run Cell 6
3. Expected: **Velocity Fraud** detected at 95.4% confidence

**Test Scenario 3: Temporal Anomaly (Baseline Mode)**
1. Set widgets:
   * Detection Mode: **Baseline**
   * Amount: 25000
   * Hour: 3
2. Run Cell 6
3. Expected: **Pattern-based fraud** detected

### Step 7.6: Review Results

**Output Format:**
```
╔══════════════════════════════════════════════════════════════╗
║              🚨 FRAUD DETECTED - HIGH RISK 🚨                ║
╠══════════════════════════════════════════════════════════════╣
║ Fraud Type: Beneficiary Manipulation                         ║
║ Confidence: 98.1%                                            ║
║ Risk Level: HIGH                                             ║
╚══════════════════════════════════════════════════════════════╝

🔍 Detection Indicators:
   ✓ Device recently changed
   ✓ SIM card recently changed
   ✓ Multiple MPIN attempts
   ✓ Round amount (₹15,000)

📚 RBI Guidelines:
   "Social engineering attacks involving beneficiary manipulation
   have increased 23% YoY. Characterized by device/SIM changes..."

💡 Recommendations:
   1. Block transaction immediately
   2. Send SMS alert to customer
   3. Require additional verification
   4. Flag account for review

🌐 Multilingual Support:
   धोखाधड़ी का प्रकार: लाभार्थी हेरफेर
   विश्वास स्तर: 98.1%
```

---

## 🔧 Troubleshooting

### Issue 1: "Module not found" Error

**Symptom:**
```
ModuleNotFoundError: No module named 'xgboost'
```

**Solution:**
```python
# Re-run installation cell
%pip install xgboost scikit-learn pandas numpy joblib --quiet
dbutils.library.restartPython()
```

### Issue 2: Unity Catalog Permission Denied

**Symptom:**
```
Error: Permission denied to create catalog 'workspace'
```

**Solution:**
Option A (Admin): Request admin to create catalog
```sql
-- Admin runs:
CREATE CATALOG IF NOT EXISTS workspace;
GRANT ALL PRIVILEGES ON CATALOG workspace TO `your-email@domain.com`;
```

Option B (Workaround): Use `hive_metastore` instead
```python
# In notebooks, replace:
workspace.bronze.upi → hive_metastore.default.upi
```

### Issue 3: Model File Not Found

**Symptom:**
```
FileNotFoundError: /Workspace/Users/.../Suraksha/models/suraksha_advanced.pkl
```

**Solution:**
1. Check file path:
   ```python
   import os
   model_path = f"/Workspace/Users/{current_user}/Suraksha/models/suraksha_advanced.pkl"
   print(f"Checking: {model_path}")
   print(f"Exists: {os.path.exists(model_path)}")
   ```

2. If missing, re-run training notebook:
   ```
   /Users/<your-email>/Suraksha/advanced_solution/04_multiclass_training.ipynb
   ```

### Issue 4: Out of Memory During Training

**Symptom:**
```
MemoryError: Unable to allocate array
```

**Solution:**
1. Reduce training data size:
   ```python
   # Sample 50% of data
   df_sample = df.sample(frac=0.5, random_state=42)
   ```

2. Or increase cluster size:
   * Compute → Edit → Workers: 4 (instead of 2)
   * Worker type: 16 GB RAM (instead of 8 GB)

### Issue 5: FAISS Index Loading Slow

**Symptom:**
RAG retrieval takes >2 seconds per query

**Solution:**
```python
# Use GPU-accelerated FAISS (if available)
%pip install faiss-gpu

# Or reduce index size
top_k = 3  # Instead of 5
```

### Issue 6: Delta Table Already Exists

**Symptom:**
```
AnalysisException: Table workspace.bronze.upi already exists
```

**Solution:**
```python
# Use mode="overwrite" to replace table
df.write.format("delta").mode("overwrite").saveAsTable("workspace.bronze.upi")
```

---

## 🏛️ Architecture Overview

### Databricks Components Used

**1. Delta Lake**
* **Bronze Layer:** Raw transaction data (500K+ rows)
* **Silver Layer:** Engineered features (38 columns)
* **Gold Layer:** Aggregated analytics
* Features: ACID transactions, time travel, schema enforcement

**2. Unity Catalog**
* **Catalog:** `workspace`
* **Schemas:** `bronze`, `silver`, `gold`
* Data governance and access control

**3. PySpark**
* **Window Functions:** Time-series feature engineering
  * `Window.partitionBy()` - Group by user
  * `rangeBetween()` - Time-based windows (1 min, 5 min)
  * `rowsBetween()` - Row-based windows
* **Aggregations:** count, sum, avg, stddev, percentile
* Distributed processing for 500K+ transactions

**4. Databricks Notebooks**
* **Main Demo:** `Suraksha_Fraud_Detection_Demo`
* **Pipeline:** 01_data_generation → 06_model_serving
* Interactive development environment

**5. Databricks Widgets**
* **Adaptive UI:** 16 fields (Advanced) / 9 fields (Baseline)
* **Mode Switching:** Real-time model selection
* User-friendly parameter input

**6. Databricks Workspace**
* **File Storage:** Models (16.1 MB), data (45-55 MB), RAG artifacts
* **Project Organization:** Folder structure for notebooks and resources

### Data Flow

```
Raw CSV (500K rows)
    ↓
Delta Lake Bronze (Unity Catalog)
    ↓
PySpark Feature Engineering (38 features)
    ↓
Delta Lake Silver
    ↓
XGBoost Model Training (87.3% accuracy)
    ↓
Dual Model Inference (Advanced/Baseline)
    ↓
RAG System (FAISS + RBI guidelines)
    ↓
Interactive Demo (Databricks widgets)
    ↓
Results Display (English/Hindi)
```

### Performance Benchmarks

* **Data Generation:** 2-3 minutes (500K rows)
* **Delta Ingestion:** 30-60 seconds
* **Feature Engineering:** 5-10 minutes
* **Model Training:** 5-10 minutes (Community), 2-3 minutes (Paid)
* **Model Accuracy:** 87.3% (9-class multiclass)
* **RAG Retrieval:** <200ms per query
* **Inference:** <100ms per transaction

---

## 📚 Next Steps

After completing setup:

1. **Run Demo Scenarios** - Test all 9 fraud types
2. **Customize Models** - Tune hyperparameters for better accuracy
3. **Add More Data** - Generate more training samples
4. **Deploy Production** - Set up real-time inference pipeline
5. **Monitor Performance** - Track model drift and accuracy

---

## 📞 Need Help?

* **Documentation:** Check `README.md` and `JUDGE_DEMO_PLAYBOOK.md`
* **Fraud Types:** See `docs/fraud_type_definitions.md`
* **Issues:** Review [Troubleshooting](#troubleshooting) section above
* **Logs:** Check Databricks cluster logs for detailed errors

---

**Setup complete! 🎉 You're ready to detect fraud with Suraksha.**

**Next:** Open `Suraksha_Fraud_Detection_Demo.ipynb` and start testing!

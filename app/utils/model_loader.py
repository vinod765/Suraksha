"""
Model Loader for Suraksha
Loads trained ML models with multiple fallback options
"""

import os
import pickle
import warnings
warnings.filterwarnings('ignore')

try:
    import mlflow
    import mlflow.xgboost
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False

from config import config  # FIXED: was 'from app.config import config'

def load_advanced_model():
    """
    Load advanced 9-class fraud detection model
    
    Tries in order:
    1. MLflow Model Registry
    2. Local file system
    3. Demo mode (rule-based predictions)
    
    Returns:
        model: Trained XGBoost model or demo fallback
    """
    
    # Try MLflow first
    if MLFLOW_AVAILABLE:
        try:
            print(f"   Trying MLflow Model Registry: {config.advanced_model_name}...")
            model = mlflow.xgboost.load_model(f"models:/{config.advanced_model_name}/Production")
            print(f"   ✓ Loaded from MLflow")
            return model
        except Exception as e:
            print(f"   ⚠️  MLflow load failed: {e}")
    
    # Try local file
    model_path = config.get_model_path('advanced')
    if os.path.exists(model_path):
        try:
            print(f"   Trying local file: {model_path}...")
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            print(f"   ✓ Loaded from local file")
            return model
        except Exception as e:
            print(f"   ⚠️  File load failed: {e}")
    
    # Fallback to demo mode
    print("   ⚠️  Using DEMO MODE (rule-based predictions)")
    return DemoAdvancedModel()

def load_baseline_model():
    """
    Load baseline pattern-based fraud detection model
    
    Tries in order:
    1. MLflow Model Registry
    2. Local file system
    3. Demo mode (simple rules)
    
    Returns:
        model: Trained model or demo fallback
    """
    
    # Try MLflow first
    if MLFLOW_AVAILABLE:
        try:
            print(f"   Trying MLflow Model Registry: {config.baseline_model_name}...")
            model = mlflow.sklearn.load_model(f"models:/{config.baseline_model_name}/Production")
            print(f"   ✓ Loaded from MLflow")
            return model
        except Exception as e:
            print(f"   ⚠️  MLflow load failed: {e}")
    
    # Try local file
    model_path = config.get_model_path('baseline')
    if os.path.exists(model_path):
        try:
            print(f"   Trying local file: {model_path}...")
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            print(f"   ✓ Loaded from local file")
            return model
        except Exception as e:
            print(f"   ⚠️  File load failed: {e}")
    
    # Fallback to demo mode
    print("   ⚠️  Using DEMO MODE (rule-based predictions)")
    return DemoBaselineModel()

class DemoAdvancedModel:
    """Demo model that uses rules to simulate advanced fraud detection"""
    
    def predict(self, X):
        """Rule-based prediction for demo purposes"""
        import numpy as np
        predictions = []
        
        for _, row in X.iterrows():
            # Check for SIM Swap (class 3)
            if row.get('sim_change_recent', False) and row.get('device_changed_flag', False):
                predictions.append(3)  # SIM Swap
            # Check for Temporal Anomaly (class 7)
            elif row.get('is_odd_hours', False) and row.get('amount_inr', 0) > 10000:
                predictions.append(7)  # Temporal Anomaly
            # Check for Amount Anomaly (class 6)
            elif row.get('amount_zscore', 0) > 3:
                predictions.append(6)  # Amount Anomaly
            # Check for Merchant Fraud (class 8)
            elif row.get('high_risk_merchant', False):
                predictions.append(8)  # Merchant Fraud
            # Legitimate (class 0)
            else:
                predictions.append(0)
        
        return np.array(predictions)
    
    def predict_proba(self, X):
        """Generate probability distributions for demo"""
        import numpy as np
        predictions = self.predict(X)
        probas = []
        
        for pred in predictions:
            proba = np.zeros(10)
            proba[pred] = 0.85  # High confidence for detected class
            proba[0] = 0.15 if pred != 0 else 0.85  # Baseline legitimate probability
            # Normalize
            proba = proba / proba.sum()
            probas.append(proba)
        
        return np.array(probas)

class DemoBaselineModel:
    """Demo model that uses simple rules for baseline detection"""
    
    def predict(self, X):
        """Rule-based prediction for baseline demo"""
        import numpy as np
        predictions = []
        
        for _, row in X.iterrows():
            # Temporal Anomaly (class 2)
            if row.get('is_odd_hours', False):
                predictions.append(2)
            # Amount Anomaly (class 1)
            elif row.get('amount_inr', 0) > 50000:
                predictions.append(1)
            # Merchant Risk (class 3)
            elif row.get('high_risk_merchant', False):
                predictions.append(3)
            # Legitimate (class 0)
            else:
                predictions.append(0)
        
        return np.array(predictions)
    
    def predict_proba(self, X):
        """Generate probability distributions for baseline demo"""
        import numpy as np
        predictions = self.predict(X)
        probas = []
        
        for pred in predictions:
            proba = np.zeros(5)
            proba[pred] = 0.80
            proba[0] = 0.20 if pred != 0 else 0.80
            proba = proba / proba.sum()
            probas.append(proba)
        
        return np.array(probas)

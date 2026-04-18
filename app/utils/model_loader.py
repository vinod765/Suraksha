"""
Model Loader Utility
Loads trained models from MLflow Registry
"""

import warnings
warnings.filterwarnings('ignore')

class DummyModel:
    """Fallback dummy model when MLflow models are unavailable"""
    
    def predict(self, X):
        """Returns low risk prediction"""
        if hasattr(X, '__len__'):
            return [0] * len(X)  # 0 = Legitimate
        return [0]
    
    def predict_proba(self, X):
        """Returns low risk probability"""
        if hasattr(X, '__len__'):
            n = len(X)
            return [[0.9, 0.1] for _ in range(n)]  # 90% legitimate, 10% fraud
        return [[0.9, 0.1]]


def load_advanced_model():
    """
    Load the advanced fraud detection model from MLflow.
    Falls back to dummy model if loading fails.
    
    Returns:
        model: Loaded MLflow model or DummyModel
    """
    try:
        import mlflow
        import mlflow.xgboost
        
        model_name = "suraksha_advanced"
        model_uri = f"models:/{model_name}/latest"
        
        print(f"Loading advanced model: {model_name}")
        model = mlflow.xgboost.load_model(model_uri)
        print(f"✓ Advanced model loaded successfully")
        return model
        
    except Exception as e:
        print(f"⚠️ Failed to load advanced model: {str(e)}")
        print("Using dummy model as fallback")
        return DummyModel()


def load_baseline_model():
    """
    Load the baseline fraud detection model from MLflow.
    Falls back to dummy model if loading fails.
    
    Returns:
        model: Loaded MLflow model or DummyModel
    """
    try:
        import mlflow
        import mlflow.xgboost
        
        model_name = "suraksha_baseline"
        model_uri = f"models:/{model_name}/latest"
        
        print(f"Loading baseline model: {model_name}")
        model = mlflow.xgboost.load_model(model_uri)
        print(f"✓ Baseline model loaded successfully")
        return model
        
    except Exception as e:
        print(f"⚠️ Failed to load baseline model: {str(e)}")
        print("Using dummy model as fallback")
        return DummyModel()


# Cache loaded models to avoid reloading
_advanced_model_cache = None
_baseline_model_cache = None


def get_advanced_model():
    """Get cached advanced model or load it"""
    global _advanced_model_cache
    if _advanced_model_cache is None:
        _advanced_model_cache = load_advanced_model()
    return _advanced_model_cache


def get_baseline_model():
    """Get cached baseline model or load it"""
    global _baseline_model_cache
    if _baseline_model_cache is None:
        _baseline_model_cache = load_baseline_model()
    return _baseline_model_cache

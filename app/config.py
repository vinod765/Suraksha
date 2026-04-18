"""
Configuration file for Suraksha App
Auto-detects paths dynamically - NO HARDCODED PATHS
"""

import os
from pathlib import Path

class Config:
    """Dynamic configuration that adapts to any workspace environment"""
    
    def __init__(self):
        # Auto-detect current workspace user
        self.workspace_user = self._get_workspace_user()
        
        # Auto-detect project root (where this config.py is located)
        self.app_dir = Path(__file__).parent.absolute()
        self.project_root = self.app_dir.parent
        
        # Model paths (relative to project root)
        self.models_dir = self.project_root / "models"
        self.advanced_model_path = self.models_dir / "suraksha_advanced.pkl"
        self.baseline_model_path = self.project_root / "baseline_solution" / "suraksha_baseline_model.pkl"
        self.feature_names_path = self.models_dir / "feature_names.pkl"
        
        # RAG paths (relative to project root)
        self.rag_dir = self.project_root / "rag"
        self.faiss_index_path = self.rag_dir / "faiss_index.bin"
        self.text_chunks_path = self.rag_dir / "text_chunks.pkl"
        self.rbi_docs_dir = self.app_dir / "assets" / "rbi_docs"
        
        # DBFS paths (fallback for RAG storage)
        self.dbfs_rag_dir = "/dbfs/suraksha/rag"
        self.dbfs_faiss_path = f"{self.dbfs_rag_dir}/faiss_index.bin"
        self.dbfs_chunks_path = f"{self.dbfs_rag_dir}/text_chunks.pkl"
        
        # MLflow model names
        self.advanced_model_name = "suraksha_advanced"
        self.baseline_model_name = "suraksha_baseline"
        
        # Fraud type mappings
        self.fraud_types_advanced = {
            0: "Legitimate",
            1: "Velocity Fraud",
            2: "Mule Account",
            3: "SIM Swap",
            4: "Device Takeover",
            5: "Beneficiary Manipulation",
            6: "Amount Anomaly",
            7: "Temporal Anomaly",
            8: "Merchant Fraud",
            9: "Failed-Then-Success"
        }
        
        self.fraud_types_baseline = {
            0: "Legitimate",
            1: "Amount Anomaly",
            2: "Temporal Anomaly",
            3: "Merchant Risk",
            4: "High-Risk Pattern"
        }
        
        # Feature engineering defaults
        self.amount_mean = 2500
        self.amount_std = 5000
        
        # Encodings for categorical variables
        self.device_map = {'Android': 0, 'iOS': 1, 'Web': 2}
        self.network_map = {'3G': 0, '4G': 1, '5G': 2, 'WiFi': 3}
        self.merchant_map = {
            'Food': 0, 'Shopping': 1, 'Fuel': 2, 'Entertainment': 3,
            'Education': 4, 'Travel': 5, 'Utilities': 6, 'Healthcare': 7, 'Other': 8
        }
        self.txn_type_map = {'P2P': 0, 'P2M': 1, 'Bill Payment': 2, 'Recharge': 3}
        
    def _get_workspace_user(self):
        """Auto-detect current workspace user"""
        try:
            # Method 1: Try to get from dbutils (in Databricks)
            import IPython
            ipython = IPython.get_ipython()
            if ipython:
                user = ipython.user_ns.get('dbutils').notebook.entry_point.getDbutils().notebook().getContext().userName().get()
                return user
        except:
            pass
        
        try:
            # Method 2: Get from environment
            return os.environ.get('DATABRICKS_USER', 'unknown')
        except:
            pass
        
        try:
            # Method 3: Parse from current path
            cwd = os.getcwd()
            if '/Users/' in cwd:
                user = cwd.split('/Users/')[1].split('/')[0]
                return user
        except:
            pass
        
        return 'unknown'
    
    def get_model_path(self, model_type='advanced'):
        """Get model path with fallback options"""
        if model_type == 'advanced':
            paths = [
                self.advanced_model_path,
                self.project_root / "advanced_solution" / "suraksha_advanced.pkl",
            ]
        else:
            paths = [
                self.baseline_model_path,
                self.project_root / "baseline_solution" / "suraksha_baseline_model.pkl",
            ]
        
        # Return first existing path
        for path in paths:
            if path.exists():
                return str(path)
        
        # Return default if none exist (will trigger error handling later)
        return str(paths[0])
    
    def get_faiss_path(self):
        """Get FAISS index path with workspace/DBFS fallback"""
        # Try workspace first
        if self.faiss_index_path.exists():
            return str(self.faiss_index_path)
        
        # Try DBFS
        if os.path.exists(self.dbfs_faiss_path):
            return self.dbfs_faiss_path
        
        # Return workspace path (will be created if needed)
        return str(self.faiss_index_path)
    
    def get_chunks_path(self):
        """Get text chunks path with workspace/DBFS fallback"""
        # Try workspace first
        if self.text_chunks_path.exists():
            return str(self.text_chunks_path)
        
        # Try DBFS
        if os.path.exists(self.dbfs_chunks_path):
            return self.dbfs_chunks_path
        
        # Return workspace path
        return str(self.text_chunks_path)

# Global config instance
config = Config()

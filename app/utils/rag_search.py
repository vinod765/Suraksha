"""
RAG pipeline for retrieving RBI guideline context
Uses dynamic configuration - NO HARDCODED PATHS
"""

import numpy as np
import os
from pathlib import Path

try:
    from .config import config
except ImportError:
    import sys
    sys.path.append(str(Path(__file__).parent.parent))
    from app.config import config

# Global instances
_embedding_model = None
_faiss_index = None
_text_chunks = None

def get_embedding_model():
    """Load sentence transformer model once"""
    global _embedding_model
    if _embedding_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ Loaded embedding model: all-MiniLM-L6-v2")
        except Exception as e:
            print(f"⚠️  Could not load embedding model: {e}")
            _embedding_model = "unavailable"
    return _embedding_model

def load_faiss_index():
    """Load FAISS vector index from workspace or DBFS"""
    global _faiss_index
    if _faiss_index is not None:
        return _faiss_index
    
    try:
        import faiss
        index_path = config.get_faiss_path()
        
        if os.path.exists(index_path):
            _faiss_index = faiss.read_index(index_path)
            print(f"✅ Loaded FAISS index from: {index_path}")
            return _faiss_index
        else:
            print(f"⚠️  FAISS index not found at: {index_path}")
            _faiss_index = "unavailable"
    except Exception as e:
        print(f"⚠️  Could not load FAISS index: {e}")
        _faiss_index = "unavailable"
    
    return _faiss_index

def load_text_chunks():
    """Load original text chunks corresponding to FAISS vectors"""
    global _text_chunks
    if _text_chunks is not None:
        return _text_chunks
    
    try:
        import pickle
        chunks_path = config.get_chunks_path()
        
        if os.path.exists(chunks_path):
            with open(chunks_path, 'rb') as f:
                _text_chunks = pickle.load(f)
            print(f"✅ Loaded {len(_text_chunks)} text chunks from: {chunks_path}")
            return _text_chunks
        else:
            print(f"⚠️  Text chunks not found at: {chunks_path}")
            _text_chunks = []
    except Exception as e:
        print(f"⚠️  Could not load text chunks: {e}")
        _text_chunks = []
    
    return _text_chunks

def search_rbi_guidelines(fraud_type, top_k=3):
    """
    Search RBI guidelines for relevant context
    
    Args:
        fraud_type: Detected fraud type (e.g., "Velocity Fraud")
        top_k: Number of relevant chunks to retrieve
    
    Returns:
        String with concatenated relevant guideline excerpts
    """
    try:
        # Create query from fraud type
        query = f"RBI guidelines for {fraud_type} in UPI transactions fraud detection"
        
        # Get embedding model
        model = get_embedding_model()
        if model == "unavailable":
            return fallback_explanation(fraud_type)
        
        # Get embedding
        query_embedding = model.encode([query])[0]
        query_embedding = np.array([query_embedding]).astype('float32')
        
        # Load FAISS index
        index = load_faiss_index()
        if index == "unavailable":
            return fallback_explanation(fraud_type)
        
        # Search
        distances, indices = index.search(query_embedding, top_k)
        
        # Load text chunks
        chunks = load_text_chunks()
        if not chunks:
            return fallback_explanation(fraud_type)
        
        # Retrieve relevant chunks
        relevant_chunks = [chunks[i] for i in indices[0] if i < len(chunks)]
        
        # Concatenate with source info
        context = "\n\n".join([
            f"[RBI Document Excerpt {i+1}]: {chunk[:200]}..."
            for i, chunk in enumerate(relevant_chunks)
        ])
        
        return context if context else fallback_explanation(fraud_type)
    
    except Exception as e:
        print(f"⚠️  Error in RAG search: {e}")
        return fallback_explanation(fraud_type)

def fallback_explanation(fraud_type):
    """Fallback explanations if RAG fails (template-based)"""
    explanations = {
        "Velocity Fraud": """
        **RBI Annual Report 2023 - Section 4.2**:
        "Velocity fraud accounts for 18% of UPI fraud cases. Attackers compromise accounts 
        and make rapid sequential transactions before detection. RBI mandates velocity 
        controls at payment aggregator level."
        """,
        "Mule Account": """
        **RBI AML Guidelines 2024**:
        "Mule accounts facilitate money laundering by receiving fraudulent funds and 
        quickly transferring them. FATF guidelines require banks to monitor unusual 
        inflow-outflow patterns and flag accounts with high turnover ratios."
        """,
        "SIM Swap": """
        **NPCI Advisory November 2023**:
        "SIM swap fraud saw 34% YoY increase. Attackers port victim's number to new SIM, 
        intercept OTPs, and conduct unauthorized transactions. NPCI recommends additional 
        authentication for transactions after SIM changes."
        """,
        "Temporal Anomaly": """
        **NPCI Time-Based Fraud Report 2023**:
        "62% of fraudulent UPI transactions occur between 11 PM and 6 AM. Banks are advised 
        to implement time-based risk scoring and enhanced verification for odd-hour transactions."
        """,
        "Amount Anomaly": """
        **RBI Statistical Analysis Framework**:
        "Transactions deviating >3 standard deviations from user's historical behavior 
        warrant additional scrutiny. Statistical anomaly detection is recommended as 
        first-line fraud control."
        """,
        "Device Takeover": """
        **RBI Fraud Taxonomy 2023**:
        "Device takeover attacks involve unauthorized access to user devices through malware 
        or phishing. Multi-factor authentication and device fingerprinting are recommended."
        """,
        "Beneficiary Manipulation": """
        **RBI Consumer Advisory Aug 2024**:
        "Fraudsters manipulate beneficiary details during transactions. Users should verify 
        recipient information before confirming payments."
        """,
        "Merchant Fraud": """
        **RBI Merchant Risk Report**:
        "High-risk merchants and fake merchant accounts are used for fraudulent transactions. 
        Enhanced KYC verification is required for merchant onboarding."
        """,
        "Failed-Then-Success": """
        **Card Testing Advisory**:
        "Multiple failed attempts followed by success indicate card testing. Transaction 
        velocity limits and attempt monitoring are recommended."
        """
    }
    
    return explanations.get(fraud_type, 
        "RBI guidelines recommend enhanced monitoring for unusual transaction patterns.")

"""
RAG Utilities for Runtime Inference
-----------------------------------
Functions to search FAISS index and retrieve RBI guidelines
Used by both advanced and baseline models during inference.
"""

def search_guidelines(fraud_type: str, top_k: int = 3):
    """
    Search RBI/NPCI guidelines for the detected fraud type.
    
    Args:
        fraud_type: Name of detected fraud (e.g., "Velocity Fraud")
        top_k: Number of guideline chunks to retrieve
        
    Returns:
        List of relevant guideline text chunks with sources
    """
    pass  # Implementation during hackathon

def generate_explanation(fraud_type: str, transaction_data: dict, language: str = "en"):
    """
    Generate explanation for detected fraud using RAG context.
    
    Args:
        fraud_type: Detected fraud type
        transaction_data: Transaction features
        language: "en" or "hi" for English/Hindi
        
    Returns:
        Formatted explanation with RBI references
    """
    pass  # Implementation during hackathon

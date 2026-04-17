"""
Baseline Model Serving
----------------------
Real-time inference endpoint for 4-class pattern detection.
Uses shared RAG pipeline for explanations.
"""

# Import from shared RAG
import sys
sys.path.append('../shared')
from rag_utils import search_guidelines, generate_explanation

def predict_and_explain(transaction):
    """
    Predict fraud pattern and generate RAG-based explanation.
    """
    pass  # Implementation during hackathon

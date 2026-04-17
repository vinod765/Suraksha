# Shared Components

This folder contains utilities used by **both** Advanced and Baseline solutions.

## Files

### `rag_pipeline.py`
- Creates FAISS vector store from RBI/NPCI PDFs
- Generates embeddings using all-MiniLM-L6-v2
- Stores index to DBFS: `/dbfs/suraksha/rag/`
- **Run once during setup** to build the knowledge base

### `rag_utils.py`
- Runtime utilities for guideline search
- Used by both model serving endpoints
- Functions: `search_guidelines()`, `generate_explanation()`

## Why Shared?

Both detection modes need to explain fraud using RBI guidelines:
- **Advanced**: Explains 9 specific fraud types
- **Baseline**: Explains 4 pattern-based detections

Same RAG pipeline, different fraud type taxonomies.

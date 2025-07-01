# test_imports.py

def test_imports():
    """Test that all modules can be imported successfully."""
    try:
        # Test core dependencies
        import streamlit as st
        import numpy as np
        import scipy
        from netCDF4 import Dataset
        
        # Test LangChain dependencies
        from langchain_openai import ChatOpenAI
        from langchain_community.vectorstores import FAISS
        from langchain_huggingface import HuggingFaceEmbeddings
        
        # Test our modules
        from app.config import Config
        from app.chromatogram.processing import ChromatogramProcessor
        from app.rag.chains import RAGChainManager
        from app.ui.components import ChromatogramUI
        
        print("✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    test_imports()
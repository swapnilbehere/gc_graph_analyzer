# app/main.py

import streamlit as st
import logging
from typing import Optional, Tuple

# Import our modules
from config import Config
from chromatogram.processing import ChromatogramProcessor
from rag.chains import RAGChainManager
from ui.components import ChromatogramUI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main Streamlit application."""
    
    # Validate configuration
    try:
        Config.validate_config()
    except ValueError as e:
        st.error(f"Configuration error: {str(e)}")
        st.stop()
    
    # Initialize components
    processor = ChromatogramProcessor(Config.JSON_OUTPUT_DIR)
    rag_manager = RAGChainManager(Config.LLM_MODEL, Config.LLM_TEMPERATURE)
    ui = ChromatogramUI(Config.TEMP_UPLOADS_DIR)
    
    # Streamlit app
    st.title("🔬 GC Chromatogram Analyzer")
    st.markdown("Upload your chromatogram file and get instant analysis and troubleshooting advice.")
    
    # File upload and metadata
    uploaded_file, metadata = ui.render_file_upload()
    
    if uploaded_file and metadata:
        try:
            # Save uploaded file
            cdf_path = ui.save_uploaded_file(uploaded_file)
            
            # Process chromatogram
            with st.spinner("Processing chromatogram..."):
                input_text = processor.process_cdf_file(cdf_path)
            
            if "No peaks found" in input_text:
                ui.render_error("No peaks were detected in this chromatograph. Please check your sample or upload a different file.")
                st.stop()
            
            # Truncate input if too long
            if len(input_text) > 2000:
                input_text = input_text[:2000]
            
            # RAG 1: Diagnosis
            with st.spinner("Analyzing chromatograph..."):
                diagnosis_chain = rag_manager.create_diagnosis_chain(Config.TXT_OUTPUT_DIR)
                response1 = diagnosis_chain.invoke({
                    "input": input_text, 
                    "metadata": metadata
                })
                diagnosis = response1["answer"]
            
            ui.render_diagnosis(diagnosis)
            
            # RAG 2: Troubleshooting
            with st.spinner("Generating troubleshooting advice..."):
                troubleshooting_chain = rag_manager.create_troubleshooting_chain(Config.KNOWLEDGE_BASE_DIR)
                response2 = troubleshooting_chain.invoke({"input": diagnosis})
                advice = response2["answer"]
            
            ui.render_troubleshooting(advice)
            
            ui.render_success("Analysis complete!")
            
        except Exception as e:
            logger.error(f"Error in main application: {str(e)}")
            ui.render_error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
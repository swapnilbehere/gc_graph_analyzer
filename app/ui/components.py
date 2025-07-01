# app/ui/components.py

import streamlit as st
import os
from typing import Optional, Tuple, Any
import logging

logger = logging.getLogger(__name__)

class ChromatogramUI:
    """Streamlit UI components for chromatogram analysis."""
    
    def __init__(self, temp_upload_dir: str = "data/temp_uploads"):
        self.temp_upload_dir = temp_upload_dir
        os.makedirs(self.temp_upload_dir, exist_ok=True)
    
    def render_file_upload(self) -> Tuple[Optional[Any], str]:
        """
        Render file upload component.
        
        Returns:
            Tuple of (uploaded_file, metadata)
        """
        st.subheader("📁 Upload Chromatogram")
        
        uploaded_file = st.file_uploader(
            "Upload chromatogram .CDF file", 
            type="cdf",
            help="Select a CDF file containing chromatogram data"
        )
        
        metadata = st.text_area(
            "Enter chromatograph metadata:",
            placeholder="Enter sample information, run conditions, or any relevant metadata...",
            help="Provide context about the chromatogram for better analysis"
        )
        
        return uploaded_file, metadata
    
    def render_processing_status(self, message: str):
        """Render processing status message."""
        st.info(f"🔄 {message}")
    
    def render_error(self, error_message: str):
        """Render error message."""
        st.error(f"❌ {error_message}")
    
    def render_success(self, message: str):
        """Render success message."""
        st.success(f"✅ {message}")
    
    def render_diagnosis(self, diagnosis: str):
        """Render diagnosis results."""
        st.subheader("🔍 Diagnosis")
        st.markdown(diagnosis)
    
    def render_troubleshooting(self, advice: str):
        """Render troubleshooting advice."""
        st.subheader("🛠️ Troubleshooting Advice")
        st.markdown(advice)
    
    def render_processing_progress(self, step: str, total_steps: int = 3):
        """Render processing progress."""
        progress = st.progress(0)
        status_text = st.empty()
        
        for i, current_step in enumerate(['Processing chromatogram...', 'Analyzing...', 'Generating advice...']):
            if step == current_step:
                progress.progress((i + 1) / total_steps)
                status_text.text(current_step)
                break
    
    def save_uploaded_file(self, uploaded_file) -> str:
        """
        Save uploaded file to temporary directory.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Path to saved file
        """
        if uploaded_file is None:
            raise ValueError("No file uploaded")
        
        file_path = os.path.join(self.temp_upload_dir, uploaded_file.name)
        
        try:
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())
            
            logger.info(f"Saved uploaded file to {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error saving uploaded file: {str(e)}")
            raise
    
    def render_summary_stats(self, peaks_info: list, filename: str):
        """Render summary statistics."""
        if not peaks_info:
            st.warning("No peaks detected in the chromatogram.")
            return
        
        st.subheader("�� Summary Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Peaks", len(peaks_info))
        
        with col2:
            max_height = max(p['height'] for p in peaks_info)
            st.metric("Max Height", f"{max_height:,.0f}")
        
        with col3:
            max_area = max(p['area'] for p in peaks_info)
            st.metric("Max Area", f"{max_area:,.0f}")
        
        # Show top peaks
        st.subheader("🏆 Top Peaks")
        top_peaks = sorted(peaks_info, key=lambda p: p['height'], reverse=True)[:5]
        
        for i, peak in enumerate(top_peaks, 1):
            st.write(f"{i}. **RT:** {peak['retention_time']}s | "
                    f"**Height:** {peak['height']:,.0f} | "
                    f"**Area:** {peak['area']:,.0f}")
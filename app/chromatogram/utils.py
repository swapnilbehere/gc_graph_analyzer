# app/chromatogram/utils.py

import os
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

def validate_cdf_file(file_path: str) -> bool:
    """
    Validate that a file is a valid CDF file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if valid, False otherwise
    """
    if not os.path.exists(file_path):
        logger.error(f"File does not exist: {file_path}")
        return False
    
    if not file_path.lower().endswith('.cdf'):
        logger.error(f"File is not a CDF file: {file_path}")
        return False
    
    return True

def get_peak_statistics(peaks_info: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Calculate statistics from peak information.
    
    Args:
        peaks_info: List of peak information dictionaries
        
    Returns:
        Dictionary of statistics
    """
    if not peaks_info:
        return {}
    
    heights = [p['height'] for p in peaks_info]
    areas = [p['area'] for p in peaks_info]
    retention_times = [p['retention_time'] for p in peaks_info]
    
    return {
        'total_peaks': len(peaks_info),
        'max_height': max(heights),
        'min_height': min(heights),
        'avg_height': sum(heights) / len(heights),
        'max_area': max(areas),
        'min_area': min(areas),
        'avg_area': sum(areas) / len(areas),
        'max_retention_time': max(retention_times),
        'min_retention_time': min(retention_times)
    }

def format_peak_summary(peaks_info: List[Dict[str, Any]], max_peaks: int = 10) -> str:
    """
    Format peak information into a readable summary.
    
    Args:
        peaks_info: List of peak information
        max_peaks: Maximum number of peaks to include in summary
        
    Returns:
        Formatted summary string
    """
    if not peaks_info:
        return "No peaks detected."
    
    # Sort by height and take top peaks
    top_peaks = sorted(peaks_info, key=lambda p: p['height'], reverse=True)[:max_peaks]
    
    summary_lines = [f"Top {len(top_peaks)} peaks:"]
    for i, peak in enumerate(top_peaks, 1):
        summary_lines.append(
            f"{i}. RT: {peak['retention_time']}s | "
            f"Height: {peak['height']} | "
            f"Area: {peak['area']}"
        )
    
    return "\n".join(summary_lines)
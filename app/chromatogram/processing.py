# app/chromatogram/processing.py

import os
import json
import numpy as np
from netCDF4 import Dataset
from scipy.signal import find_peaks, peak_widths
from typing import Tuple, List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ChromatogramProcessor:
    """Handles chromatogram data processing and peak detection."""
    
    def __init__(self, json_output_dir: str = "data/json_output"):
        self.json_output_dir = json_output_dir
        os.makedirs(self.json_output_dir, exist_ok=True)
    
    def load_cdf_data(self, filepath: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Load chromatogram data from CDF file.
        
        Args:
            filepath: Path to the CDF file
            
        Returns:
            Tuple of (time_array, intensity_array)
        """
        try:
            dataset = Dataset(filepath, 'r')
            logger.info(f"Variables in {filepath}: {list(dataset.variables.keys())}")
            
            time = dataset.variables['scan_acquisition_time'][:]
            intensity = dataset.variables['total_intensity'][:]
            
            dataset.close()
            return time, intensity
            
        except Exception as e:
            logger.error(f"Error loading CDF file {filepath}: {str(e)}")
            raise
    
    def detect_peaks_and_areas(self, time: np.ndarray, intensity: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detect peaks in chromatogram and calculate their areas.
        
        Args:
            time: Time array
            intensity: Intensity array
            
        Returns:
            List of peak information dictionaries
        """
        logger.info(f"Max intensity: {np.max(intensity):,.2f}")
        logger.info(f"Median intensity: {np.median(intensity):,.2f}")
        logger.info(f"95th percentile: {np.percentile(intensity, 95):,.2f}")

        threshold_height = np.percentile(intensity, 95)
        threshold_prominence = np.percentile(intensity, 90)

        peaks, properties = find_peaks(
            intensity,
            height=threshold_height,
            prominence=threshold_prominence,
            distance=5
        )

        logger.info(f"Found {len(peaks)} peaks using height>{threshold_height:.2f} and prominence>{threshold_prominence:.2f}")

        results = []
        for i, peak_idx in enumerate(peaks):
            if peak_idx >= len(time):
                continue

            rt = time[peak_idx]
            height = properties['peak_heights'][i]

            # Calculate peak width at half-prominence
            widths, _, left_ips, right_ips = peak_widths(intensity, [peak_idx], rel_height=0.5)

            left = float(left_ips[0])
            right = float(right_ips[0])

            start_idx = max(0, min(len(time) - 1, int(np.floor(left))))
            end_idx = max(0, min(len(time) - 1, int(np.ceil(right))))

            if start_idx >= end_idx or end_idx >= len(time):
                continue

            area = np.trapezoid(intensity[start_idx:end_idx + 1], time[start_idx:end_idx + 1])

            results.append({
                "peak_index": int(peak_idx),
                "height": round(height, 2),
                "retention_time": round(rt, 2),
                "area": round(area, 2),
                "start_time": round(time[start_idx], 2),
                "end_time": round(time[end_idx], 2)
            })

        return results
    
    def summarize_trace(self, time: np.ndarray, intensity: np.ndarray, 
                       peaks_info: List[Dict[str, Any]], filename: str) -> str:
        """
        Create summary of chromatogram trace and save to JSON.
        
        Args:
            time: Time array
            intensity: Intensity array
            peaks_info: List of peak information
            filename: Original filename
            
        Returns:
            Natural language summary string
        """
        baseline = float(np.median(intensity))
        
        # Create JSON summary
        json_data = {
            "file_name": filename,
            "summary": {
                "total_peaks": len(peaks_info),
                "max_intensity": float(np.max(intensity)),
                "baseline_intensity": baseline,
                "peaks": peaks_info
            },
            "trace_data": list(zip(time.tolist(), intensity.tolist()))
        }

        json_filename = filename.replace(".cdf", ".json")
        json_path = os.path.join(self.json_output_dir, json_filename)
        
        with open(json_path, "w") as f:
            json.dump(json_data, f, indent=2)
        
        logger.info(f"Saved JSON summary to {json_path}")

        # Generate natural language summary
        summary_lines = [
            f"Chromatogram Summary: {filename}",
            f"Total peaks detected: {len(peaks_info)}",
            f"Max intensity: {np.max(intensity):,.2f}",
            f"Estimated baseline: {baseline:,.2f}",
            "",
            "All the peaks observed in the chromatograph"
        ]

        top_peaks = sorted(peaks_info, key=lambda p: p['height'], reverse=True)
        for p in top_peaks:
            summary_lines.append(
                f"- Peak at {p['retention_time']}s | Area: {p['area']} | Height: {p['height']}"
            )

        return "\n".join(summary_lines)
    
    def process_cdf_file(self, file_path: str) -> str:
        """
        Main function to process a CDF file end-to-end.
        
        Args:
            file_path: Path to the CDF file
            
        Returns:
            Summary string of the chromatogram
        """
        try:
            time, intensity = self.load_cdf_data(file_path)
            peaks_info = self.detect_peaks_and_areas(time, intensity)
            
            if not peaks_info:
                return "No peaks found."
            
            filename = os.path.basename(file_path)
            return self.summarize_trace(time, intensity, peaks_info, filename)
            
        except Exception as e:
            logger.error(f"Error processing CDF file {file_path}: {str(e)}")
            raise
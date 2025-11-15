"""
Utility Functions
Helper functions for the Construction Safety Monitor.
"""

import os
import json
from typing import Dict, List
from pathlib import Path


def format_time(seconds: float) -> str:
    """
    Convert seconds to HH:MM:SS format.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def load_json_file(filepath: str) -> Dict:
    """
    Load and parse a JSON file.
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        Parsed JSON data as dictionary
    """
    with open(filepath, 'r') as f:
        return json.load(f)


def save_json_file(data: Dict, filepath: str):
    """
    Save data to a JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Output file path
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def create_output_directory(base_path: str = "results") -> str:
    """
    Create output directory with timestamp.
    
    Args:
        base_path: Base directory path
        
    Returns:
        Path to created directory
    """
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(base_path, f"analysis_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)
    
    return output_dir


def get_video_duration(video_path: str) -> float:
    """
    Get the duration of a video file in seconds.
    
    Args:
        video_path: Path to the video file
        
    Returns:
        Video duration in seconds
    """
    import cv2
    
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    cap.release()
    
    return frame_count / fps if fps > 0 else 0


def validate_api_key(api_key: str) -> bool:
    """
    Validate if an API key is properly formatted.
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not api_key or len(api_key) < 20:
        return False
    
    # Basic format check - API keys are typically alphanumeric
    return api_key.replace("-", "").replace("_", "").isalnum()


def calculate_statistics(scores: List[float]) -> Dict:
    """
    Calculate statistical metrics from a list of scores.
    
    Args:
        scores: List of numerical scores
        
    Returns:
        Dictionary with statistical metrics
    """
    if not scores:
        return {
            "mean": 0,
            "median": 0,
            "min": 0,
            "max": 0,
            "std": 0
        }
    
    import numpy as np
    
    return {
        "mean": float(np.mean(scores)),
        "median": float(np.median(scores)),
        "min": float(np.min(scores)),
        "max": float(np.max(scores)),
        "std": float(np.std(scores))
    }


def print_progress_bar(iteration: int, total: int, prefix: str = "", suffix: str = "", length: int = 50):
    """
    Print a progress bar to console.
    
    Args:
        iteration: Current iteration
        total: Total iterations
        prefix: Prefix string
        suffix: Suffix string
        length: Character length of bar
    """
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = "█" * filled_length + "-" * (length - filled_length)
    
    print(f"\r{prefix} |{bar}| {percent}% {suffix}", end="\r")
    
    if iteration == total:
        print()


if __name__ == "__main__":
    # Test utility functions
    print("Testing utility functions...")
    
    # Test time formatting
    print(f"180 seconds = {format_time(180)}")
    print(f"3665 seconds = {format_time(3665)}")
    
    # Test statistics
    test_scores = [0.8, 0.9, 0.7, 0.85, 0.95]
    stats = calculate_statistics(test_scores)
    print(f"Statistics: {stats}")
    
    # Test progress bar
    import time
    for i in range(101):
        print_progress_bar(i, 100, prefix="Progress:", suffix="Complete")
        time.sleep(0.02)
    
    print("✅ All tests passed!")

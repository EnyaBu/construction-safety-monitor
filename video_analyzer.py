"""
Video Analyzer Module
Analyzes construction videos and extracts action descriptions using AI vision models.
"""

import cv2
import os
import json
from typing import List, Dict, Optional
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv
import time

load_dotenv()


class VideoAnalyzer:
    """Analyzes construction videos to extract worker actions and behaviors."""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.0-flash-exp"):
        """
        Initialize the Video Analyzer.
        
        Args:
            api_key: Google Gemini API key (uses env var if not provided)
            model_name: Name of the Gemini model to use
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
        
    def extract_frames(self, video_path: str, frame_rate: int = 2) -> List[Dict]:
        """
        Extract frames from video at specified intervals.
        
        Args:
            video_path: Path to the video file
            frame_rate: Extract one frame every N seconds
            
        Returns:
            List of dictionaries containing frame data and timestamps
        """
        frames_data = []
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")
        
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_interval = fps * frame_rate
        frame_count = 0
        extracted_count = 0
        
        print(f"Extracting frames every {frame_rate} seconds from {video_path}...")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % frame_interval == 0:
                timestamp = frame_count / fps
                
                # Save frame temporarily
                temp_frame_path = f"/tmp/frame_{extracted_count}.jpg"
                cv2.imwrite(temp_frame_path, frame)
                
                frames_data.append({
                    "frame_number": frame_count,
                    "timestamp": timestamp,
                    "path": temp_frame_path
                })
                extracted_count += 1
            
            frame_count += 1
        
        cap.release()
        print(f"Extracted {extracted_count} frames")
        return frames_data
    
    def analyze_frame(self, frame_path: str, timestamp: float) -> Dict:
        """
        Analyze a single frame using Gemini Vision API.
        
        Args:
            frame_path: Path to the frame image
            timestamp: Timestamp of the frame in the video
            
        Returns:
            Dictionary containing analysis results
        """
        prompt = """
        Analyze this construction site image and provide detailed information in JSON format:
        
        {
            "worker_action": "Detailed description of what the worker is doing",
            "tools_visible": ["list", "of", "tools"],
            "safety_equipment": ["list", "of", "safety", "gear"],
            "location_zone": "area where worker is located",
            "potential_hazards": ["list", "of", "visible", "hazards"],
            "action_category": "measuring/cutting/installing/securing/finishing"
        }
        
        Focus on:
        1. Specific actions being performed
        2. Tools and equipment in use
        3. Safety equipment worn by workers
        4. Work area and positioning
        5. Any safety concerns
        
        Respond ONLY with valid JSON, no other text.
        """
        
        try:
            # Upload and analyze the image
            image_file = genai.upload_file(path=frame_path)
            response = self.model.generate_content([image_file, prompt])
            
            # Parse the response
            response_text = response.text.strip()
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            analysis = json.loads(response_text)
            analysis["timestamp"] = timestamp
            
            return analysis
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Response text: {response.text}")
            # Return a fallback response
            return {
                "timestamp": timestamp,
                "worker_action": response.text if hasattr(response, 'text') else "Unable to analyze",
                "tools_visible": [],
                "safety_equipment": [],
                "location_zone": "unknown",
                "potential_hazards": [],
                "action_category": "unknown"
            }
        except Exception as e:
            print(f"Error analyzing frame: {e}")
            return {
                "timestamp": timestamp,
                "worker_action": "Error in analysis",
                "tools_visible": [],
                "safety_equipment": [],
                "location_zone": "unknown",
                "potential_hazards": [],
                "action_category": "unknown",
                "error": str(e)
            }
    
    def analyze_video(self, video_path: str, frame_rate: int = 2) -> List[Dict]:
        """
        Analyze entire video and return timeline of actions.
        
        Args:
            video_path: Path to the video file
            frame_rate: Extract and analyze one frame every N seconds
            
        Returns:
            List of analysis results for each frame
        """
        print(f"\n🎥 Starting video analysis: {video_path}")
        
        # Extract frames
        frames = self.extract_frames(video_path, frame_rate)
        
        # Analyze each frame
        results = []
        for i, frame_data in enumerate(frames):
            print(f"Analyzing frame {i+1}/{len(frames)} (t={frame_data['timestamp']:.1f}s)...")
            
            analysis = self.analyze_frame(frame_data["path"], frame_data["timestamp"])
            results.append(analysis)
            
            # Clean up temporary frame
            if os.path.exists(frame_data["path"]):
                os.remove(frame_data["path"])
            
            # Rate limiting - avoid hitting API limits
            time.sleep(1)
        
        print(f"\n✅ Video analysis complete! Analyzed {len(results)} frames")
        return results
    
    def analyze_video_direct(self, video_path: str) -> List[Dict]:
        """
        Analyze entire video at once using Gemini's video understanding.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            List of timestamped action descriptions
        """
        print(f"\n🎥 Starting direct video analysis: {video_path}")
        
        prompt = """
        Analyze this construction work video comprehensively. Provide a timeline of worker actions in JSON format:
        
        {
            "actions": [
                {
                    "timestamp_start": 0.0,
                    "timestamp_end": 5.0,
                    "worker_action": "Worker measuring wall with tape measure",
                    "tools_visible": ["tape measure"],
                    "safety_equipment": ["hard hat", "safety vest"],
                    "location_zone": "main work area",
                    "action_category": "measuring"
                }
            ],
            "overall_summary": "Brief summary of the entire video",
            "compliance_notes": "Any notable safety or procedural observations"
        }
        
        For each distinct action segment in the video:
        - Note the time range
        - Describe the specific action
        - List tools and equipment
        - Identify the work zone
        - Categorize the action type
        
        Respond ONLY with valid JSON.
        """
        
        try:
            # Check file size (Gemini has limits)
            file_size = os.path.getsize(video_path) / (1024 * 1024)  # Size in MB
            if file_size > 20:
                print(f"⚠️ Warning: Video file is {file_size:.1f}MB. May exceed API limits.")
                print("Consider using frame-by-frame analysis instead.")
            
            # Upload video
            print("Uploading video to Gemini...")
            video_file = genai.upload_file(path=video_path)
            print("Video uploaded. Analyzing...")
            
            # Generate analysis
            response = self.model.generate_content([video_file, prompt])
            
            # Parse response
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            analysis = json.loads(response_text)
            
            print(f"\n✅ Video analysis complete!")
            return analysis.get("actions", [])
            
        except Exception as e:
            print(f"Error in direct video analysis: {e}")
            print("Falling back to frame-by-frame analysis...")
            return self.analyze_video(video_path, frame_rate=3)


if __name__ == "__main__":
    # Test the video analyzer
    analyzer = VideoAnalyzer()
    
    # Example usage
    video_path = "examples/sample_videos/drywall_install.mp4"
    if os.path.exists(video_path):
        results = analyzer.analyze_video(video_path, frame_rate=5)
        
        # Save results
        with open("video_analysis_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print("\nResults saved to video_analysis_results.json")
    else:
        print(f"Test video not found: {video_path}")

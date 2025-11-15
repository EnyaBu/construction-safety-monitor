"""
SOP Comparator Module
Compares observed worker actions against Standard Operating Procedures.
"""

import json
import os
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer, util
import torch
from dotenv import load_dotenv

load_dotenv()


class SOPComparator:
    """Compares worker actions against SOP steps using semantic similarity."""
    
    def __init__(self, model_name: str = None):
        """
        Initialize the SOP Comparator.
        
        Args:
            model_name: Name of the sentence transformer model
        """
        self.model_name = model_name or os.getenv("SIMILARITY_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        print(f"Loading similarity model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        self.threshold = float(os.getenv("SIMILARITY_THRESHOLD", 0.70))
        
    def load_sop(self, sop_path: str) -> Dict:
        """
        Load SOP from JSON file.
        
        Args:
            sop_path: Path to the SOP JSON file
            
        Returns:
            Dictionary containing SOP data
        """
        with open(sop_path, 'r') as f:
            sop = json.load(f)
        
        print(f"\n📋 Loaded SOP: {sop.get('task_name', 'Unknown Task')}")
        print(f"   Steps: {len(sop.get('steps', []))}")
        return sop
    
    def compute_similarity(self, action: str, sop_step: str) -> float:
        """
        Compute semantic similarity between action and SOP step.
        
        Args:
            action: Observed worker action description
            sop_step: SOP step description
            
        Returns:
            Similarity score (0.0 to 1.0)
        """
        # Encode both texts
        action_embedding = self.model.encode(action, convert_to_tensor=True)
        sop_embedding = self.model.encode(sop_step, convert_to_tensor=True)
        
        # Compute cosine similarity
        similarity = util.cos_sim(action_embedding, sop_embedding)
        
        return similarity.item()
    
    def find_best_match(self, action: str, sop_steps: List[Dict]) -> Tuple[int, float, Dict]:
        """
        Find the best matching SOP step for an observed action.
        
        Args:
            action: Observed worker action description
            sop_steps: List of SOP step dictionaries
            
        Returns:
            Tuple of (step_index, similarity_score, step_dict)
        """
        best_score = -1
        best_idx = -1
        best_step = None
        
        # Get all SOP step descriptions
        sop_descriptions = [step["action"] for step in sop_steps]
        
        # Encode all at once for efficiency
        action_embedding = self.model.encode(action, convert_to_tensor=True)
        sop_embeddings = self.model.encode(sop_descriptions, convert_to_tensor=True)
        
        # Compute similarities
        similarities = util.cos_sim(action_embedding, sop_embeddings)
        
        # Find best match
        best_idx = similarities.argmax().item()
        best_score = similarities[0][best_idx].item()
        best_step = sop_steps[best_idx]
        
        return best_idx, best_score, best_step
    
    def check_tool_compliance(self, observed_tools: List[str], required_tools: List[str]) -> Dict:
        """
        Check if correct tools are being used.
        
        Args:
            observed_tools: List of tools seen in the video
            required_tools: List of tools required by SOP
            
        Returns:
            Dictionary with compliance status and details
        """
        observed_tools_lower = [tool.lower() for tool in observed_tools]
        required_tools_lower = [tool.lower() for tool in required_tools]
        
        missing_tools = [tool for tool in required_tools_lower 
                        if tool not in observed_tools_lower]
        wrong_tools = [tool for tool in observed_tools_lower 
                      if tool not in required_tools_lower and tool != ""]
        
        is_compliant = len(missing_tools) == 0
        
        return {
            "is_compliant": is_compliant,
            "missing_tools": missing_tools,
            "wrong_tools": wrong_tools,
            "observed": observed_tools_lower,
            "required": required_tools_lower
        }
    
    def check_safety_equipment(self, observed_equipment: List[str], required_equipment: List[str]) -> Dict:
        """
        Check if required safety equipment is being worn.
        
        Args:
            observed_equipment: List of safety equipment seen
            required_equipment: List of required safety equipment
            
        Returns:
            Dictionary with compliance status
        """
        observed_lower = [eq.lower() for eq in observed_equipment]
        required_lower = [eq.lower() for eq in required_equipment]
        
        missing_equipment = [eq for eq in required_lower if eq not in observed_lower]
        
        return {
            "is_compliant": len(missing_equipment) == 0,
            "missing_equipment": missing_equipment,
            "observed": observed_lower,
            "required": required_lower
        }
    
    def analyze_sequence(self, video_actions: List[Dict], sop: Dict) -> List[Dict]:
        """
        Analyze the entire sequence of video actions against SOP.
        
        Args:
            video_actions: List of action dictionaries from video analysis
            sop: SOP dictionary
            
        Returns:
            List of compliance checks with deviations
        """
        results = []
        sop_steps = sop.get("steps", [])
        
        print(f"\n🔍 Analyzing {len(video_actions)} actions against {len(sop_steps)} SOP steps...")
        
        for i, action_data in enumerate(video_actions):
            action_desc = action_data.get("worker_action", "")
            timestamp = action_data.get("timestamp", 0)
            
            # Find best matching SOP step
            step_idx, similarity, matched_step = self.find_best_match(action_desc, sop_steps)
            
            # Check tool compliance
            tool_check = self.check_tool_compliance(
                action_data.get("tools_visible", []),
                matched_step.get("required_tools", [])
            )
            
            # Check safety equipment
            safety_check = self.check_safety_equipment(
                action_data.get("safety_equipment", []),
                sop.get("safety_equipment", [])
            )
            
            # Determine if this is a deviation
            is_deviation = (
                similarity < self.threshold or
                not tool_check["is_compliant"] or
                not safety_check["is_compliant"]
            )
            
            # Determine severity
            if similarity < 0.5:
                severity = "high"
            elif similarity < self.threshold:
                severity = "medium"
            elif not safety_check["is_compliant"]:
                severity = "high"
            elif not tool_check["is_compliant"]:
                severity = "medium"
            else:
                severity = "low"
            
            result = {
                "frame_number": i,
                "timestamp": timestamp,
                "observed_action": action_desc,
                "matched_sop_step": matched_step.get("action", ""),
                "step_number": step_idx + 1,
                "similarity_score": round(similarity, 3),
                "is_deviation": is_deviation,
                "severity": severity if is_deviation else "none",
                "tool_compliance": tool_check,
                "safety_compliance": safety_check,
                "location": action_data.get("location_zone", "unknown"),
                "potential_hazards": action_data.get("potential_hazards", [])
            }
            
            results.append(result)
            
            # Print real-time feedback
            status_icon = "❌" if is_deviation else "✅"
            print(f"{status_icon} Frame {i+1} (t={timestamp:.1f}s): {similarity:.1%} match to Step {step_idx+1}")
        
        return results
    
    def generate_summary(self, compliance_results: List[Dict]) -> Dict:
        """
        Generate summary statistics from compliance results.
        
        Args:
            compliance_results: List of compliance check results
            
        Returns:
            Dictionary with summary statistics
        """
        total_frames = len(compliance_results)
        deviations = [r for r in compliance_results if r["is_deviation"]]
        high_severity = [r for r in deviations if r["severity"] == "high"]
        medium_severity = [r for r in deviations if r["severity"] == "medium"]
        
        avg_similarity = sum(r["similarity_score"] for r in compliance_results) / total_frames if total_frames > 0 else 0
        
        tool_violations = sum(1 for r in compliance_results if not r["tool_compliance"]["is_compliant"])
        safety_violations = sum(1 for r in compliance_results if not r["safety_compliance"]["is_compliant"])
        
        return {
            "total_frames_analyzed": total_frames,
            "total_deviations": len(deviations),
            "high_severity_count": len(high_severity),
            "medium_severity_count": len(medium_severity),
            "compliance_rate": round((total_frames - len(deviations)) / total_frames * 100, 1) if total_frames > 0 else 0,
            "average_similarity": round(avg_similarity, 3),
            "tool_violations": tool_violations,
            "safety_violations": safety_violations,
            "deviation_timestamps": [r["timestamp"] for r in deviations]
        }


if __name__ == "__main__":
    # Test the SOP comparator
    comparator = SOPComparator()
    
    # Load a sample SOP
    sop_path = "config/drywall_sop.json"
    if os.path.exists(sop_path):
        sop = comparator.load_sop(sop_path)
        
        # Example video actions
        test_actions = [
            {
                "timestamp": 5.0,
                "worker_action": "Worker measuring the wall with a tape measure",
                "tools_visible": ["tape measure"],
                "safety_equipment": ["hard hat", "safety glasses"],
                "location_zone": "work area"
            },
            {
                "timestamp": 10.0,
                "worker_action": "Worker hammering nails into the wall",
                "tools_visible": ["hammer", "nails"],
                "safety_equipment": ["hard hat"],
                "location_zone": "work area"
            }
        ]
        
        # Analyze
        results = comparator.analyze_sequence(test_actions, sop)
        summary = comparator.generate_summary(results)
        
        print("\n" + "="*50)
        print("COMPLIANCE SUMMARY")
        print("="*50)
        print(json.dumps(summary, indent=2))
    else:
        print(f"SOP file not found: {sop_path}")

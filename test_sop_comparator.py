"""
Tests for SOP Comparator
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from sop_comparator import SOPComparator


class TestSOPComparator:
    """Test cases for the SOP Comparator."""
    
    @pytest.fixture
    def comparator(self):
        """Create a SOPComparator instance for testing."""
        return SOPComparator()
    
    @pytest.fixture
    def sample_sop(self):
        """Sample SOP data for testing."""
        return {
            "task_name": "Test Task",
            "safety_equipment": ["hard hat", "safety glasses"],
            "steps": [
                {
                    "id": 1,
                    "action": "Measure wall dimensions with tape measure",
                    "expected_time": 120,
                    "required_tools": ["tape measure"],
                    "zone": "work area"
                },
                {
                    "id": 2,
                    "action": "Cut material using saw",
                    "expected_time": 180,
                    "required_tools": ["saw"],
                    "zone": "cutting area"
                }
            ]
        }
    
    def test_compute_similarity_identical(self, comparator):
        """Test similarity computation with identical texts."""
        text1 = "Measure wall dimensions with tape measure"
        text2 = "Measure wall dimensions with tape measure"
        
        similarity = comparator.compute_similarity(text1, text2)
        
        assert similarity > 0.95, "Identical texts should have very high similarity"
    
    def test_compute_similarity_similar(self, comparator):
        """Test similarity computation with similar texts."""
        text1 = "Measure wall dimensions with tape measure"
        text2 = "Use tape measure to measure the wall"
        
        similarity = comparator.compute_similarity(text1, text2)
        
        assert 0.6 < similarity < 0.9, "Similar texts should have moderate similarity"
    
    def test_compute_similarity_different(self, comparator):
        """Test similarity computation with different texts."""
        text1 = "Measure wall dimensions with tape measure"
        text2 = "Cut drywall with utility knife"
        
        similarity = comparator.compute_similarity(text1, text2)
        
        assert similarity < 0.5, "Different texts should have low similarity"
    
    def test_find_best_match(self, comparator, sample_sop):
        """Test finding the best matching SOP step."""
        action = "Worker measuring the wall with a tape"
        steps = sample_sop["steps"]
        
        idx, score, step = comparator.find_best_match(action, steps)
        
        assert idx == 0, "Should match the first step"
        assert score > 0.6, "Should have reasonable similarity"
        assert "measure" in step["action"].lower()
    
    def test_check_tool_compliance_pass(self, comparator):
        """Test tool compliance check when tools are correct."""
        observed = ["tape measure", "level"]
        required = ["tape measure"]
        
        result = comparator.check_tool_compliance(observed, required)
        
        assert result["is_compliant"] == True
        assert len(result["missing_tools"]) == 0
    
    def test_check_tool_compliance_fail(self, comparator):
        """Test tool compliance check when tools are missing."""
        observed = ["hammer"]
        required = ["tape measure", "drill"]
        
        result = comparator.check_tool_compliance(observed, required)
        
        assert result["is_compliant"] == False
        assert "tape measure" in result["missing_tools"]
        assert "drill" in result["missing_tools"]
    
    def test_check_safety_equipment_pass(self, comparator):
        """Test safety equipment check when compliant."""
        observed = ["hard hat", "safety glasses", "gloves"]
        required = ["hard hat", "safety glasses"]
        
        result = comparator.check_safety_equipment(observed, required)
        
        assert result["is_compliant"] == True
        assert len(result["missing_equipment"]) == 0
    
    def test_check_safety_equipment_fail(self, comparator):
        """Test safety equipment check when non-compliant."""
        observed = ["hard hat"]
        required = ["hard hat", "safety glasses", "gloves"]
        
        result = comparator.check_safety_equipment(observed, required)
        
        assert result["is_compliant"] == False
        assert "safety glasses" in result["missing_equipment"]
        assert "gloves" in result["missing_equipment"]
    
    def test_analyze_sequence(self, comparator, sample_sop):
        """Test analyzing a sequence of actions."""
        video_actions = [
            {
                "timestamp": 5.0,
                "worker_action": "Worker measuring wall with tape measure",
                "tools_visible": ["tape measure"],
                "safety_equipment": ["hard hat", "safety glasses"],
                "location_zone": "work area"
            },
            {
                "timestamp": 10.0,
                "worker_action": "Worker cutting material with saw",
                "tools_visible": ["saw"],
                "safety_equipment": ["hard hat"],
                "location_zone": "cutting area"
            }
        ]
        
        results = comparator.analyze_sequence(video_actions, sample_sop)
        
        assert len(results) == 2
        assert results[0]["is_deviation"] == False  # First action should be compliant
        # Second action might be deviation due to missing safety glasses
    
    def test_generate_summary(self, comparator):
        """Test summary generation."""
        compliance_results = [
            {"is_deviation": False, "severity": "none", "similarity_score": 0.9,
             "tool_compliance": {"is_compliant": True}, 
             "safety_compliance": {"is_compliant": True}},
            {"is_deviation": True, "severity": "high", "similarity_score": 0.4,
             "tool_compliance": {"is_compliant": False},
             "safety_compliance": {"is_compliant": False}, "timestamp": 10.0},
            {"is_deviation": False, "severity": "none", "similarity_score": 0.85,
             "tool_compliance": {"is_compliant": True},
             "safety_compliance": {"is_compliant": True}}
        ]
        
        summary = comparator.generate_summary(compliance_results)
        
        assert summary["total_frames_analyzed"] == 3
        assert summary["total_deviations"] == 1
        assert summary["high_severity_count"] == 1
        assert summary["compliance_rate"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

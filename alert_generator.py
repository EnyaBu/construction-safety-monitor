"""
Alert Generator Module
Generates human-readable alerts for SOP deviations and safety violations.
"""

from typing import List, Dict
from datetime import datetime
import json


class AlertGenerator:
    """Generates contextual alerts for construction safety violations."""
    
    def __init__(self):
        """Initialize the Alert Generator."""
        self.alert_count = 0
        
    def format_timestamp(self, seconds: float) -> str:
        """
        Convert seconds to MM:SS format.
        
        Args:
            seconds: Timestamp in seconds
            
        Returns:
            Formatted timestamp string
        """
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    
    def generate_deviation_alert(self, compliance_result: Dict) -> str:
        """
        Generate alert message for a single deviation.
        
        Args:
            compliance_result: Single compliance check result
            
        Returns:
            Formatted alert message
        """
        severity = compliance_result.get("severity", "medium").upper()
        timestamp = self.format_timestamp(compliance_result.get("timestamp", 0))
        
        # Severity emoji
        severity_icons = {
            "HIGH": "🔴",
            "MEDIUM": "🟡",
            "LOW": "🟢"
        }
        icon = severity_icons.get(severity, "⚠️")
        
        alert = f"""
{icon} COMPLIANCE ALERT - {severity} SEVERITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Time: {timestamp}
Step #{compliance_result.get('step_number', 'N/A')}

Expected Action:
  {compliance_result.get('matched_sop_step', 'Unknown')}

Observed Action:
  {compliance_result.get('observed_action', 'Unknown')}

Similarity Score: {compliance_result.get('similarity_score', 0):.1%}
"""
        
        # Add tool violations
        tool_comp = compliance_result.get("tool_compliance", {})
        if not tool_comp.get("is_compliant", True):
            alert += "\n⚠️ TOOL VIOLATIONS:\n"
            if tool_comp.get("missing_tools"):
                alert += f"  Missing: {', '.join(tool_comp['missing_tools'])}\n"
            if tool_comp.get("wrong_tools"):
                alert += f"  Wrong tools used: {', '.join(tool_comp['wrong_tools'])}\n"
        
        # Add safety violations
        safety_comp = compliance_result.get("safety_compliance", {})
        if not safety_comp.get("is_compliant", True):
            alert += "\n🚨 SAFETY EQUIPMENT VIOLATIONS:\n"
            if safety_comp.get("missing_equipment"):
                alert += f"  Missing: {', '.join(safety_comp['missing_equipment'])}\n"
        
        # Add hazards if any
        hazards = compliance_result.get("potential_hazards", [])
        if hazards:
            alert += f"\n⚠️ POTENTIAL HAZARDS DETECTED:\n"
            for hazard in hazards:
                alert += f"  • {hazard}\n"
        
        alert += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        self.alert_count += 1
        return alert
    
    def generate_batch_alerts(self, compliance_results: List[Dict]) -> List[str]:
        """
        Generate alerts for all deviations in results.
        
        Args:
            compliance_results: List of compliance check results
            
        Returns:
            List of alert messages
        """
        alerts = []
        
        for result in compliance_results:
            if result.get("is_deviation", False):
                alert = self.generate_deviation_alert(result)
                alerts.append(alert)
        
        return alerts
    
    def generate_summary_report(self, compliance_results: List[Dict], summary: Dict, sop_name: str = "Unknown Task") -> str:
        """
        Generate comprehensive summary report.
        
        Args:
            compliance_results: List of compliance check results
            summary: Summary statistics dictionary
            sop_name: Name of the SOP task
            
        Returns:
            Formatted summary report
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Calculate compliance grade
        compliance_rate = summary.get("compliance_rate", 0)
        if compliance_rate >= 90:
            grade = "A - Excellent"
            grade_icon = "🌟"
        elif compliance_rate >= 80:
            grade = "B - Good"
            grade_icon = "✅"
        elif compliance_rate >= 70:
            grade = "C - Acceptable"
            grade_icon = "🟡"
        elif compliance_rate >= 60:
            grade = "D - Needs Improvement"
            grade_icon = "🟠"
        else:
            grade = "F - Critical Issues"
            grade_icon = "🔴"
        
        report = f"""
╔════════════════════════════════════════════════════════════════╗
║          CONSTRUCTION SAFETY COMPLIANCE REPORT                 ║
╚════════════════════════════════════════════════════════════════╝

Task: {sop_name}
Generated: {timestamp}

{'='*64}
OVERALL COMPLIANCE GRADE: {grade_icon} {grade}
{'='*64}

📊 STATISTICS
────────────────────────────────────────────────────────────────
Total Frames Analyzed:     {summary.get('total_frames_analyzed', 0)}
Compliance Rate:           {compliance_rate}%
Average Similarity Score:  {summary.get('average_similarity', 0):.1%}

Total Deviations:          {summary.get('total_deviations', 0)}
  • High Severity:         {summary.get('high_severity_count', 0)}
  • Medium Severity:       {summary.get('medium_severity_count', 0)}

Specific Violations:
  • Tool Violations:       {summary.get('tool_violations', 0)}
  • Safety Equipment:      {summary.get('safety_violations', 0)}

"""
        
        # Add deviation timeline
        if summary.get("total_deviations", 0) > 0:
            report += "⏱️ DEVIATION TIMELINE\n"
            report += "─" * 64 + "\n"
            
            deviations = [r for r in compliance_results if r.get("is_deviation", False)]
            for i, dev in enumerate(deviations[:10], 1):  # Show first 10
                timestamp_str = self.format_timestamp(dev.get("timestamp", 0))
                severity = dev.get("severity", "medium").upper()
                report += f"{i}. {timestamp_str} - {severity} - Step #{dev.get('step_number', 'N/A')}\n"
            
            if len(deviations) > 10:
                report += f"\n... and {len(deviations) - 10} more deviations\n"
            report += "\n"
        
        # Recommendations
        report += "💡 RECOMMENDATIONS\n"
        report += "─" * 64 + "\n"
        
        if summary.get("safety_violations", 0) > 0:
            report += "• CRITICAL: Ensure all workers wear required safety equipment\n"
        
        if summary.get("tool_violations", 0) > 0:
            report += "• Provide proper tool training and ensure correct tools are available\n"
        
        if compliance_rate < 70:
            report += "• Consider additional SOP training for workers\n"
            report += "• Implement more frequent supervision and checks\n"
        
        if summary.get("high_severity_count", 0) > 0:
            report += "• URGENT: Review high-severity deviations immediately\n"
        
        report += "\n" + "=" * 64 + "\n"
        report += "End of Report\n"
        report += "=" * 64 + "\n"
        
        return report
    
    def save_alerts_to_file(self, alerts: List[str], filename: str = "alerts.txt"):
        """
        Save alerts to a text file.
        
        Args:
            alerts: List of alert messages
            filename: Output filename
        """
        with open(filename, 'w') as f:
            f.write(f"Construction Safety Alerts\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 64 + "\n\n")
            
            for i, alert in enumerate(alerts, 1):
                f.write(f"Alert #{i}\n")
                f.write(alert)
                f.write("\n")
        
        print(f"✅ Alerts saved to {filename}")
    
    def export_json(self, compliance_results: List[Dict], summary: Dict, filename: str = "compliance_report.json"):
        """
        Export results to JSON format.
        
        Args:
            compliance_results: List of compliance check results
            summary: Summary statistics
            filename: Output filename
        """
        data = {
            "timestamp": datetime.now().isoformat(),
            "summary": summary,
            "detailed_results": compliance_results
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ JSON report saved to {filename}")


if __name__ == "__main__":
    # Test the alert generator
    generator = AlertGenerator()
    
    # Example deviation
    test_deviation = {
        "timestamp": 125.5,
        "observed_action": "Worker hammering nails into drywall",
        "matched_sop_step": "Secure drywall to studs with drill and screws",
        "step_number": 4,
        "similarity_score": 0.45,
        "is_deviation": True,
        "severity": "high",
        "tool_compliance": {
            "is_compliant": False,
            "missing_tools": ["drill"],
            "wrong_tools": ["hammer"],
            "observed": ["hammer", "nails"],
            "required": ["drill", "screws"]
        },
        "safety_compliance": {
            "is_compliant": False,
            "missing_equipment": ["safety glasses"],
            "observed": ["hard hat"],
            "required": ["hard hat", "safety glasses"]
        },
        "potential_hazards": ["Flying debris", "Improper fastening"]
    }
    
    # Generate alert
    alert = generator.generate_deviation_alert(test_deviation)
    print(alert)
    
    # Generate summary
    test_summary = {
        "total_frames_analyzed": 20,
        "total_deviations": 3,
        "high_severity_count": 1,
        "medium_severity_count": 2,
        "compliance_rate": 85.0,
        "average_similarity": 0.82,
        "tool_violations": 1,
        "safety_violations": 2
    }
    
    report = generator.generate_summary_report([test_deviation], test_summary, "Drywall Installation")
    print(report)

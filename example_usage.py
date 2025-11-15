"""
Example Usage Script
Demonstrates how to use the Construction Safety Monitor programmatically.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from video_analyzer import VideoAnalyzer
from sop_comparator import SOPComparator
from alert_generator import AlertGenerator


def analyze_construction_video(video_path: str, sop_path: str):
    """
    Complete example of analyzing a construction video.
    
    Args:
        video_path: Path to the construction video
        sop_path: Path to the SOP JSON file
    """
    
    print("="*70)
    print("CONSTRUCTION SAFETY MONITOR - EXAMPLE")
    print("="*70)
    print(f"Video: {video_path}")
    print(f"SOP: {sop_path}")
    print("="*70)
    
    # Step 1: Analyze the video
    print("\n[1/3] Analyzing video...")
    analyzer = VideoAnalyzer()
    
    # For this example, we'll use frame-by-frame analysis
    # You can use analyzer.analyze_video_direct() for faster processing
    video_actions = analyzer.analyze_video(video_path, frame_rate=3)
    
    print(f"✓ Found {len(video_actions)} action segments")
    
    # Step 2: Compare to SOP
    print("\n[2/3] Checking SOP compliance...")
    comparator = SOPComparator()
    sop = comparator.load_sop(sop_path)
    
    compliance_results = comparator.analyze_sequence(video_actions, sop)
    summary = comparator.generate_summary(compliance_results)
    
    print(f"✓ Compliance rate: {summary['compliance_rate']:.1f}%")
    print(f"✓ Total deviations: {summary['total_deviations']}")
    
    # Step 3: Generate alerts
    print("\n[3/3] Generating alerts...")
    alert_gen = AlertGenerator()
    
    alerts = alert_gen.generate_batch_alerts(compliance_results)
    print(f"✓ Generated {len(alerts)} alerts")
    
    # Create summary report
    report = alert_gen.generate_summary_report(
        compliance_results,
        summary,
        sop.get('task_name', 'Unknown Task')
    )
    
    # Display results
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    print(report)
    
    # Show a few key alerts
    if alerts:
        print("\n" + "="*70)
        print("KEY ALERTS (First 3)")
        print("="*70)
        for i, alert in enumerate(alerts[:3], 1):
            print(f"\nAlert #{i}:")
            print(alert)
    
    # Save results
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)
    
    video_name = Path(video_path).stem
    
    # Save alerts
    alerts_file = output_dir / f"{video_name}_alerts.txt"
    alert_gen.save_alerts_to_file(alerts, str(alerts_file))
    
    # Save summary
    summary_file = output_dir / f"{video_name}_summary.txt"
    with open(summary_file, 'w') as f:
        f.write(report)
    
    # Save JSON
    json_file = output_dir / f"{video_name}_compliance.json"
    alert_gen.export_json(compliance_results, summary, str(json_file))
    
    print("\n" + "="*70)
    print(f"✓ All results saved to: {output_dir}")
    print("="*70)
    
    return compliance_results, summary


def quick_test_example():
    """
    Quick test using mock data (no actual video required).
    """
    print("\n" + "="*70)
    print("QUICK TEST - Using Mock Data")
    print("="*70)
    
    # Create mock video actions
    mock_actions = [
        {
            "timestamp": 5.0,
            "worker_action": "Worker measuring wall with tape measure",
            "tools_visible": ["tape measure"],
            "safety_equipment": ["hard hat", "safety glasses"],
            "location_zone": "work area",
            "potential_hazards": []
        },
        {
            "timestamp": 15.0,
            "worker_action": "Worker cutting drywall with utility knife",
            "tools_visible": ["utility knife", "t-square"],
            "safety_equipment": ["hard hat", "safety glasses", "gloves"],
            "location_zone": "cutting area",
            "potential_hazards": []
        },
        {
            "timestamp": 30.0,
            "worker_action": "Worker hammering nails into wall",
            "tools_visible": ["hammer"],
            "safety_equipment": ["hard hat"],
            "location_zone": "work area",
            "potential_hazards": ["Wrong tool used"]
        }
    ]
    
    # Load SOP
    print("\nLoading SOP...")
    comparator = SOPComparator()
    sop = comparator.load_sop("config/drywall_sop.json")
    
    # Analyze
    print("\nAnalyzing mock actions...")
    results = comparator.analyze_sequence(mock_actions, sop)
    summary = comparator.generate_summary(results)
    
    # Generate report
    alert_gen = AlertGenerator()
    report = alert_gen.generate_summary_report(results, summary, sop['task_name'])
    
    print("\n" + report)
    
    print("\n✓ Quick test complete!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Example usage of Construction Safety Monitor")
    parser.add_argument("--video", help="Path to video file")
    parser.add_argument("--sop", help="Path to SOP JSON file")
    parser.add_argument("--quick-test", action="store_true", help="Run quick test with mock data")
    
    args = parser.parse_args()
    
    if args.quick_test:
        # Run quick test
        quick_test_example()
    elif args.video and args.sop:
        # Analyze actual video
        analyze_construction_video(args.video, args.sop)
    else:
        print("Usage:")
        print("  python example_usage.py --quick-test")
        print("  python example_usage.py --video path/to/video.mp4 --sop config/drywall_sop.json")

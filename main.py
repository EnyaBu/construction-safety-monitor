"""
Main Application
Command-line interface for the Construction Safety Monitor.
"""

import argparse
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from video_analyzer import VideoAnalyzer
from sop_comparator import SOPComparator
from alert_generator import AlertGenerator


def main():
    """Main entry point for the CLI application."""
    
    parser = argparse.ArgumentParser(
        description="Construction Safety Monitor - Analyze construction videos against SOPs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a video against drywall SOP
  python main.py --video my_video.mp4 --sop config/drywall_sop.json
  
  # Use direct video analysis (faster for short videos)
  python main.py --video my_video.mp4 --sop config/drywall_sop.json --direct
  
  # Adjust frame rate for detailed analysis
  python main.py --video my_video.mp4 --sop config/drywall_sop.json --frame-rate 1
  
  # Export results to custom location
  python main.py --video my_video.mp4 --sop config/drywall_sop.json --output results/
        """
    )
    
    parser.add_argument(
        "--video", "-v",
        required=True,
        help="Path to the construction video file"
    )
    
    parser.add_argument(
        "--sop", "-s",
        required=True,
        help="Path to the SOP JSON configuration file"
    )
    
    parser.add_argument(
        "--frame-rate", "-f",
        type=int,
        default=2,
        help="Extract and analyze one frame every N seconds (default: 2)"
    )
    
    parser.add_argument(
        "--direct", "-d",
        action="store_true",
        help="Use direct video analysis instead of frame-by-frame (faster but requires smaller videos)"
    )
    
    parser.add_argument(
        "--output", "-o",
        default="./results",
        help="Output directory for reports (default: ./results)"
    )
    
    parser.add_argument(
        "--threshold", "-t",
        type=float,
        default=0.70,
        help="Similarity threshold for compliance (default: 0.70)"
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    if not os.path.exists(args.video):
        print(f"❌ Error: Video file not found: {args.video}")
        sys.exit(1)
    
    if not os.path.exists(args.sop):
        print(f"❌ Error: SOP file not found: {args.sop}")
        sys.exit(1)
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    print("=" * 70)
    print("🏗️  CONSTRUCTION SAFETY MONITOR")
    print("=" * 70)
    print(f"Video: {args.video}")
    print(f"SOP: {args.sop}")
    print(f"Output: {args.output}")
    print("=" * 70)
    
    try:
        # Step 1: Analyze Video
        print("\n📹 STEP 1: VIDEO ANALYSIS")
        print("-" * 70)
        analyzer = VideoAnalyzer()
        
        if args.direct:
            video_actions = analyzer.analyze_video_direct(args.video)
        else:
            video_actions = analyzer.analyze_video(args.video, frame_rate=args.frame_rate)
        
        if not video_actions:
            print("❌ No actions detected in video. Exiting.")
            sys.exit(1)
        
        print(f"✅ Detected {len(video_actions)} action segments")
        
        # Step 2: Compare to SOP
        print("\n📋 STEP 2: SOP COMPLIANCE CHECK")
        print("-" * 70)
        comparator = SOPComparator()
        comparator.threshold = args.threshold
        
        sop = comparator.load_sop(args.sop)
        compliance_results = comparator.analyze_sequence(video_actions, sop)
        summary = comparator.generate_summary(compliance_results)
        
        # Step 3: Generate Alerts
        print("\n⚠️  STEP 3: ALERT GENERATION")
        print("-" * 70)
        alert_gen = AlertGenerator()
        
        alerts = alert_gen.generate_batch_alerts(compliance_results)
        print(f"Generated {len(alerts)} alerts")
        
        # Step 4: Create Reports
        print("\n📊 STEP 4: GENERATING REPORTS")
        print("-" * 70)
        
        # Summary report
        report = alert_gen.generate_summary_report(
            compliance_results, 
            summary, 
            sop.get("task_name", "Unknown Task")
        )
        
        # Save reports
        video_name = Path(args.video).stem
        
        # Text alerts
        alerts_file = os.path.join(args.output, f"{video_name}_alerts.txt")
        alert_gen.save_alerts_to_file(alerts, alerts_file)
        
        # Summary report
        summary_file = os.path.join(args.output, f"{video_name}_summary.txt")
        with open(summary_file, 'w') as f:
            f.write(report)
        print(f"✅ Summary report saved to {summary_file}")
        
        # JSON export
        json_file = os.path.join(args.output, f"{video_name}_compliance.json")
        alert_gen.export_json(compliance_results, summary, json_file)
        
        # Print summary to console
        print("\n" + "=" * 70)
        print(report)
        print("=" * 70)
        
        # Print key alerts to console
        if alerts:
            print("\n🚨 KEY ALERTS:")
            print("-" * 70)
            high_priority = [a for r in compliance_results if r.get("is_deviation") and r.get("severity") == "high" for a in [alert_gen.generate_deviation_alert(r)]]
            
            for alert in high_priority[:3]:  # Show top 3 high-priority alerts
                print(alert)
        
        print("\n✅ Analysis complete! All reports saved to:", args.output)
        
        # Exit with appropriate code
        if summary.get("high_severity_count", 0) > 0:
            print("\n⚠️  WARNING: High-severity violations detected!")
            sys.exit(2)
        elif summary.get("total_deviations", 0) > 0:
            print("\n⚠️  Some deviations detected. Please review.")
            sys.exit(1)
        else:
            print("\n✅ All checks passed!")
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

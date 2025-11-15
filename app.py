"""
Streamlit Web Interface
Web-based dashboard for the Construction Safety Monitor.
"""

import streamlit as st
import os
import sys
import json
from pathlib import Path
import tempfile
import time

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.video_analyzer import VideoAnalyzer
from src.sop_comparator import SOPComparator
from src.alert_generator import AlertGenerator


# Page configuration
st.set_page_config(
    page_title="Construction Safety Monitor",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B35;
        text-align: center;
        padding: 1rem 0;
    }
    .stAlert {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


def load_available_sops():
    """Load all available SOP files from config directory."""
    config_dir = Path("config")
    if not config_dir.exists():
        return {}
    
    sops = {}
    for sop_file in config_dir.glob("*.json"):
        if sop_file.stem != "sop_template":
            try:
                with open(sop_file, 'r') as f:
                    sop_data = json.load(f)
                    sops[sop_data.get("task_name", sop_file.stem)] = str(sop_file)
            except Exception as e:
                st.error(f"Error loading {sop_file}: {e}")
    
    return sops


def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<div class="main-header">🏗️ Construction Safety Monitor</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Enter your Google Gemini API key",
            value=os.getenv("GEMINI_API_KEY", "")
        )
        
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key
        
        st.markdown("---")
        
        # SOP Selection
        st.subheader("📋 Select SOP")
        available_sops = load_available_sops()
        
        if not available_sops:
            st.error("No SOP files found in config directory!")
            st.stop()
        
        selected_sop_name = st.selectbox(
            "Construction Task",
            options=list(available_sops.keys()),
            help="Select the type of construction work to monitor"
        )
        
        selected_sop_path = available_sops[selected_sop_name]
        
        # Load and display SOP details
        with open(selected_sop_path, 'r') as f:
            sop_data = json.load(f)
        
        with st.expander("SOP Details"):
            st.write(f"**Task:** {sop_data.get('task_name', 'N/A')}")
            st.write(f"**Code:** {sop_data.get('task_code', 'N/A')}")
            st.write(f"**Steps:** {len(sop_data.get('steps', []))}")
            
            st.write("**Required Safety Equipment:**")
            for item in sop_data.get('safety_equipment', []):
                st.write(f"  • {item}")
        
        st.markdown("---")
        
        # Analysis Settings
        st.subheader("🔧 Analysis Settings")
        
        use_direct = st.checkbox(
            "Use Direct Video Analysis",
            value=False,
            help="Faster for short videos (<20MB), may be less detailed"
        )
        
        if not use_direct:
            frame_rate = st.slider(
                "Frame Analysis Rate (seconds)",
                min_value=1,
                max_value=10,
                value=2,
                help="Extract and analyze one frame every N seconds"
            )
        else:
            frame_rate = None
        
        similarity_threshold = st.slider(
            "Similarity Threshold",
            min_value=0.5,
            max_value=0.95,
            value=0.70,
            step=0.05,
            help="Minimum similarity score for compliance (higher = stricter)"
        )
        
        st.markdown("---")
        st.info("💡 Tip: Upload a construction video to begin analysis")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📹 Video Upload")
        
        uploaded_file = st.file_uploader(
            "Upload Construction Video",
            type=["mp4", "avi", "mov", "mkv"],
            help="Upload a video of the construction work to analyze"
        )
        
        if uploaded_file is not None:
            # Show video player
            st.video(uploaded_file)
            
            # Display file info
            file_size = uploaded_file.size / (1024 * 1024)  # MB
            st.caption(f"File: {uploaded_file.name} ({file_size:.1f} MB)")
    
    with col2:
        st.header("📊 Quick Stats")
        
        if uploaded_file is None:
            st.info("Upload a video to see analysis statistics")
        else:
            # Placeholder metrics
            st.metric("File Size", f"{file_size:.1f} MB")
            st.metric("Selected SOP", selected_sop_name)
            st.metric("Analysis Mode", "Direct" if use_direct else f"Frame-by-frame ({frame_rate}s)")
    
    # Analysis button
    st.markdown("---")
    
    if uploaded_file is None:
        st.warning("⚠️ Please upload a video file to begin analysis")
        st.stop()
    
    if not api_key:
        st.error("❌ Please enter your Gemini API key in the sidebar")
        st.stop()
    
    analyze_button = st.button("🚀 Start Analysis", type="primary", use_container_width=True)
    
    if analyze_button:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
            tmp_file.write(uploaded_file.read())
            video_path = tmp_file.name
        
        try:
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Video Analysis
            status_text.text("🎥 Step 1/3: Analyzing video...")
            progress_bar.progress(10)
            
            analyzer = VideoAnalyzer(api_key=api_key)
            
            with st.spinner("Analyzing video frames..."):
                if use_direct:
                    video_actions = analyzer.analyze_video_direct(video_path)
                else:
                    video_actions = analyzer.analyze_video(video_path, frame_rate=frame_rate)
            
            progress_bar.progress(40)
            st.success(f"✅ Detected {len(video_actions)} action segments")
            
            # Step 2: SOP Comparison
            status_text.text("📋 Step 2/3: Comparing against SOP...")
            progress_bar.progress(50)
            
            comparator = SOPComparator()
            comparator.threshold = similarity_threshold
            
            with st.spinner("Checking compliance..."):
                compliance_results = comparator.analyze_sequence(video_actions, sop_data)
                summary = comparator.generate_summary(compliance_results)
            
            progress_bar.progress(70)
            
            # Step 3: Generate Alerts
            status_text.text("⚠️ Step 3/3: Generating alerts...")
            progress_bar.progress(80)
            
            alert_gen = AlertGenerator()
            alerts = alert_gen.generate_batch_alerts(compliance_results)
            report = alert_gen.generate_summary_report(
                compliance_results,
                summary,
                sop_data.get("task_name", "Unknown Task")
            )
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
            
            # Display Results
            st.markdown("---")
            st.header("📊 Analysis Results")
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                compliance_rate = summary.get("compliance_rate", 0)
                st.metric(
                    "Compliance Rate",
                    f"{compliance_rate:.1f}%",
                    delta=f"{compliance_rate - 100:.1f}%",
                    delta_color="normal"
                )
            
            with col2:
                st.metric(
                    "Total Deviations",
                    summary.get("total_deviations", 0),
                    delta=None
                )
            
            with col3:
                st.metric(
                    "High Severity",
                    summary.get("high_severity_count", 0),
                    delta=None
                )
            
            with col4:
                avg_sim = summary.get("average_similarity", 0)
                st.metric(
                    "Avg Similarity",
                    f"{avg_sim:.1%}",
                    delta=None
                )
            
            # Detailed results in tabs
            tab1, tab2, tab3 = st.tabs(["📋 Summary Report", "⚠️ Alerts", "📊 Detailed Results"])
            
            with tab1:
                st.text(report)
                
                # Download button for report
                st.download_button(
                    "📥 Download Summary Report",
                    data=report,
                    file_name=f"{Path(uploaded_file.name).stem}_summary.txt",
                    mime="text/plain"
                )
            
            with tab2:
                if alerts:
                    for i, alert in enumerate(alerts, 1):
                        with st.expander(f"Alert #{i}", expanded=(i <= 3)):
                            st.text(alert)
                    
                    # Download alerts
                    alerts_text = "\n\n".join(alerts)
                    st.download_button(
                        "📥 Download All Alerts",
                        data=alerts_text,
                        file_name=f"{Path(uploaded_file.name).stem}_alerts.txt",
                        mime="text/plain"
                    )
                else:
                    st.success("✅ No deviations detected! All actions comply with SOP.")
            
            with tab3:
                # Create a timeline view
                st.subheader("Timeline of Actions")
                
                for i, result in enumerate(compliance_results):
                    timestamp = result.get("timestamp", 0)
                    is_deviation = result.get("is_deviation", False)
                    severity = result.get("severity", "none")
                    
                    # Color code based on severity
                    if severity == "high":
                        color = "🔴"
                    elif severity == "medium":
                        color = "🟡"
                    else:
                        color = "🟢"
                    
                    with st.expander(f"{color} {timestamp:.1f}s - Step #{result.get('step_number', 'N/A')} ({result.get('similarity_score', 0):.1%} match)"):
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.write("**Expected:**")
                            st.info(result.get("matched_sop_step", "N/A"))
                        
                        with col_b:
                            st.write("**Observed:**")
                            if is_deviation:
                                st.error(result.get("observed_action", "N/A"))
                            else:
                                st.success(result.get("observed_action", "N/A"))
                        
                        # Additional details
                        if not result["tool_compliance"]["is_compliant"]:
                            st.warning(f"⚠️ Tool issues: Missing {result['tool_compliance']['missing_tools']}")
                        
                        if not result["safety_compliance"]["is_compliant"]:
                            st.error(f"🚨 Safety issues: Missing {result['safety_compliance']['missing_equipment']}")
                
                # Download JSON
                json_data = {
                    "summary": summary,
                    "detailed_results": compliance_results
                }
                
                st.download_button(
                    "📥 Download JSON Report",
                    data=json.dumps(json_data, indent=2),
                    file_name=f"{Path(uploaded_file.name).stem}_compliance.json",
                    mime="application/json"
                )
        
        except Exception as e:
            st.error(f"❌ Error during analysis: {str(e)}")
            import traceback
            with st.expander("Error Details"):
                st.code(traceback.format_exc())
        
        finally:
            # Cleanup temporary file
            if os.path.exists(video_path):
                os.unlink(video_path)


if __name__ == "__main__":
    main()

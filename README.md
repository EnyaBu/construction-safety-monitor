# 🏗️ Construction Safety Monitor

An AI-powered construction safety monitoring system that uses computer vision and spatial intelligence to ensure workers follow Standard Operating Procedures (SOPs).

## 🎯 Overview

This system analyzes construction work videos and compares worker actions against predefined SOPs to detect deviations, unsafe practices, and procedural violations in real-time.

**Dataset:** Uses the [Construction Activity Recognition Dataset](https://www.kaggle.com/datasets/ehsaanali/construction-activity-recognition-dataset) from Kaggle (13 brick masonry videos)

**SOP Reference:** Based on [Quikrete Basic Brick Construction Guide](https://www.quikrete.com/pdfs/projects/basicbrickconstruction.pdf)

### Features

- 🎥 **Video Analysis**: Automated frame-by-frame analysis of construction activities
- 📋 **SOP Compliance**: Compare worker actions against standard operating procedures
- ⚠️ **Smart Alerts**: AI-generated warnings for deviations and safety violations
- 📊 **Similarity Scoring**: Semantic matching between observed actions and SOP steps
- 🎨 **Web Interface**: Easy-to-use Streamlit dashboard for monitoring

## 🏗️ Supported Construction Tasks

- Drywall Installation
- Brick Laying
- Concrete Pouring
- Electrical Work
- Plumbing Installation
- Custom SOPs (easily configurable)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Cloud API Key (for Gemini) or OpenAI API Key
- Webcam or video files of construction work

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/construction-safety-monitor.git
cd construction-safety-monitor

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys
```

### Download Sample Videos

Get the brick masonry construction videos from Kaggle:

**Option 1: Kaggle Website**
1. Visit https://www.kaggle.com/datasets/ehsaanali/construction-activity-recognition-dataset
2. Download and extract
3. Place videos in `examples/sample_videos/brickmasonry/`

**Option 2: Kaggle API**
```bash
pip install kaggle
kaggle datasets download -d ehsaanali/construction-activity-recognition-dataset
unzip construction-activity-recognition-dataset.zip -d examples/sample_videos/brickmasonry/
```

📖 **See [DATASET.md](DATASET.md) for complete dataset setup instructions**

### Running the Application

```bash
# Run the Streamlit web interface
streamlit run app.py

# Or use the CLI with brick masonry videos
python src/main.py --video examples/sample_videos/brickmasonry/video_001.mp4 --sop config/bricklaying_sop.json
```

## 📁 Project Structure

```
construction-safety-monitor/
├── app.py                      # Streamlit web interface
├── src/
│   ├── __init__.py
│   ├── main.py                 # Main CLI application
│   ├── video_analyzer.py       # Video analysis module
│   ├── sop_comparator.py       # SOP comparison engine
│   ├── alert_generator.py      # Alert generation system
│   └── utils.py                # Utility functions
├── config/
│   ├── drywall_sop.json        # Drywall installation SOP
│   ├── bricklaying_sop.json    # Brick laying SOP
│   └── sop_template.json       # Template for custom SOPs
├── examples/
│   └── sample_videos/          # Example construction videos
├── tests/
│   └── test_*.py               # Unit tests
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── README.md                   # This file
```

## 🔧 Configuration

### Setting up SOPs

SOPs are defined in JSON format. See `config/sop_template.json` for the structure:

```json
{
  "task_name": "Drywall Installation",
  "steps": [
    {
      "id": 1,
      "action": "Measure wall dimensions with tape measure",
      "expected_time": 120,
      "required_tools": ["tape measure"],
      "zone": "work area"
    }
  ],
  "tools_required": ["tape measure", "drill", "utility knife"],
  "safety_equipment": ["gloves", "safety glasses", "dust mask"]
}
```

### Environment Variables

Create a `.env` file with:

```env
GEMINI_API_KEY=your_gemini_api_key_here
SIMILARITY_THRESHOLD=0.70
VIDEO_FRAME_RATE=2
```

## 📊 How It Works

1. **Video Processing**: Extracts frames from construction videos at specified intervals
2. **Action Recognition**: Uses Gemini 2.0 Flash to analyze frames and describe worker actions
3. **Semantic Matching**: Compares descriptions to SOP steps using sentence transformers
4. **Deviation Detection**: Identifies mismatches, missing steps, or wrong tool usage
5. **Alert Generation**: Creates contextual alerts for supervisors

## 🎯 Example Output

```
⚠️ COMPLIANCE ALERT - MEDIUM SEVERITY
Time: 00:02:45
Expected: "Secure drywall to studs with drill and screws"
Observed: "Worker hammering nails into drywall"
Issue: Wrong tool usage detected
Similarity Score: 45%
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_video_analyzer.py
```

## 📈 Performance

- **Frame Analysis**: ~2-3 seconds per frame (with Gemini API)
- **Similarity Computation**: <100ms per comparison
- **End-to-end**: ~5-10 minutes for a 10-minute construction video

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Dataset:** [Construction Activity Recognition Dataset](https://www.kaggle.com/datasets/ehsaanali/construction-activity-recognition-dataset) by Ehsaan Ali on Kaggle
- **SOP Reference:** [Quikrete Basic Brick Construction Guide](https://www.quikrete.com/pdfs/projects/basicbrickconstruction.pdf)
- HuggingFace for Sentence Transformers
- Google for Gemini Vision API
- OpenAI for alternative vision models
- Construction safety professionals and industry experts

## 📚 Documentation

- 📖 [DATASET.md](DATASET.md) - Dataset download and setup instructions
- 🚀 [GITHUB_UPLOAD.md](GITHUB_UPLOAD.md) - How to upload this project to GitHub
- ⚙️ [SETUP.md](SETUP.md) - Detailed installation and configuration
- 🏗️ [ARCHITECTURE.md](ARCHITECTURE.md) - Technical system architecture
- 🤝 [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/yourusername/construction-safety-monitor](https://github.com/yourusername/construction-safety-monitor)

## 🔮 Future Enhancements

- [ ] Real-time video stream processing
- [ ] Multi-camera support
- [ ] Worker identification and tracking
- [ ] Historical compliance analytics
- [ ] Mobile app for supervisors
- [ ] Integration with construction management software
- [ ] Support for more construction tasks
- [ ] Object detection for PPE compliance

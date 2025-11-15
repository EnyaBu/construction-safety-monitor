# Setup Guide

Complete setup instructions for the Construction Safety Monitor.

## Prerequisites

- Python 3.8 or higher
- Git
- Google Cloud account (for Gemini API)
- At least 4GB of free disk space

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/construction-safety-monitor.git
cd construction-safety-monitor
```

## Step 2: Create Virtual Environment

### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Installing PyTorch

The requirements.txt includes PyTorch, but you may need to install it specifically for your system:

#### For CPU only:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

#### For GPU (CUDA 11.8):
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

Visit [PyTorch Get Started](https://pytorch.org/get-started/locally/) for other configurations.

## Step 4: Set Up API Keys

### Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key

### Configure Environment Variables

```bash
# Copy the example env file
cp .env.example .env

# Edit the .env file and add your API key
# On Windows: notepad .env
# On macOS/Linux: nano .env
```

Add your API key to the `.env` file:
```
GEMINI_API_KEY=your_actual_api_key_here
```

## Step 5: Verify Installation

Run the test suite to ensure everything is working:

```bash
pytest tests/
```

## Step 6: Download Sample Videos (Optional)

For testing, you can download construction videos from:
- YouTube (using yt-dlp)
- Stock video sites
- Record your own construction work

Save them in the `examples/sample_videos/` directory.

## Step 7: Run the Application

### Web Interface (Recommended for beginners):
```bash
streamlit run app.py
```

This will open a web browser with the application.

### Command Line Interface:
```bash
python src/main.py --video path/to/video.mp4 --sop config/drywall_sop.json
```

## Troubleshooting

### Issue: "Module not found" error

**Solution:** Make sure you've activated the virtual environment and installed all dependencies:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: "API key not found"

**Solution:** Ensure your `.env` file is in the project root and contains a valid API key:
```bash
cat .env  # Check the file exists and has the key
```

### Issue: Video analysis is very slow

**Solutions:**
1. Use direct video analysis mode for videos < 20MB
2. Increase the frame rate (analyze fewer frames)
3. Use a shorter video for testing
4. Check your internet connection (API calls require internet)

### Issue: "Out of memory" error

**Solutions:**
1. Reduce the frame rate (analyze fewer frames)
2. Use a smaller video
3. Close other applications
4. Use direct video analysis instead of frame-by-frame

### Issue: Low similarity scores for correct actions

**Solutions:**
1. Lower the similarity threshold (default is 0.70)
2. Improve the SOP descriptions to be more detailed
3. Ensure good video quality with clear visibility of actions

### Issue: OpenCV can't open video file

**Solutions:**
1. Check the video file format (MP4 works best)
2. Ensure the video file isn't corrupted
3. Try converting the video to MP4 using ffmpeg:
   ```bash
   ffmpeg -i input_video.avi output_video.mp4
   ```

## Performance Optimization

### For Faster Processing:

1. **Use Direct Video Analysis** (for videos < 20MB):
   ```bash
   python src/main.py --video video.mp4 --sop config/drywall_sop.json --direct
   ```

2. **Increase Frame Rate** (analyze fewer frames):
   ```bash
   python src/main.py --video video.mp4 --sop config/drywall_sop.json --frame-rate 5
   ```

3. **Use GPU** for sentence transformers (if available):
   - Install CUDA-enabled PyTorch
   - The models will automatically use GPU if available

### For Better Accuracy:

1. **Decrease Frame Rate** (analyze more frames):
   ```bash
   python src/main.py --video video.mp4 --sop config/drywall_sop.json --frame-rate 1
   ```

2. **Increase Similarity Threshold**:
   ```bash
   python src/main.py --video video.mp4 --sop config/drywall_sop.json --threshold 0.80
   ```

3. **Improve Video Quality**:
   - Use 1080p or higher resolution
   - Ensure good lighting
   - Keep camera steady
   - Frame workers and actions clearly

## Creating Custom SOPs

1. Copy the SOP template:
   ```bash
   cp config/sop_template.json config/my_custom_sop.json
   ```

2. Edit the file with your task details:
   ```bash
   nano config/my_custom_sop.json
   ```

3. Fill in all the required fields:
   - task_name
   - steps (with detailed descriptions)
   - tools_required
   - safety_equipment

4. Use your custom SOP:
   ```bash
   python src/main.py --video video.mp4 --sop config/my_custom_sop.json
   ```

## Next Steps

1. Read the [README.md](README.md) for usage examples
2. Check out the [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute
3. Try analyzing some sample videos
4. Create custom SOPs for your specific construction tasks

## Getting Help

If you encounter issues:

1. Check this troubleshooting guide
2. Search existing GitHub issues
3. Create a new issue with:
   - Your Python version
   - Operating system
   - Error message
   - Steps to reproduce

## Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Sentence Transformers](https://www.sbert.net/)
- [Google Gemini API](https://ai.google.dev/)
- [OpenCV Python Tutorial](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)

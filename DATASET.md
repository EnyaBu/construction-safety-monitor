# Dataset Setup Instructions

## Brick Masonry Construction Videos

This project uses the **Construction Activity Recognition Dataset** from Kaggle, which includes 13 videos of brick wall construction activities.

### Dataset Information

**Source:** https://www.kaggle.com/datasets/ehsaanali/construction-activity-recognition-dataset

**Contents:**
- 13 videos of brick masonry construction
- Various construction activities including:
  - Mixing mortar
  - Laying bricks
  - Applying mortar
  - Checking alignment
  - Finishing joints

### How to Download the Dataset

#### Option 1: Using Kaggle Website (Easiest)

1. **Create a Kaggle Account** (if you don't have one):
   - Go to https://www.kaggle.com/
   - Click "Register" and create a free account

2. **Download the Dataset**:
   - Visit: https://www.kaggle.com/datasets/ehsaanali/construction-activity-recognition-dataset
   - Click the "Download" button (requires login)
   - Extract the ZIP file

3. **Place Videos in Project**:
   ```bash
   # Create the videos directory
   mkdir -p examples/sample_videos/brickmasonry
   
   # Move the videos to the project
   # Replace /path/to/downloaded/dataset with your actual path
   cp /path/to/downloaded/dataset/*.mp4 examples/sample_videos/brickmasonry/
   ```

#### Option 2: Using Kaggle API (Advanced)

1. **Install Kaggle API**:
   ```bash
   pip install kaggle
   ```

2. **Setup Kaggle Credentials**:
   - Go to https://www.kaggle.com/account
   - Scroll to "API" section
   - Click "Create New API Token"
   - This downloads `kaggle.json`
   - Move it to: `~/.kaggle/kaggle.json` (Linux/Mac) or `C:\Users\<username>\.kaggle\kaggle.json` (Windows)
   - Set permissions (Linux/Mac only):
     ```bash
     chmod 600 ~/.kaggle/kaggle.json
     ```

3. **Download Using API**:
   ```bash
   # Create directory
   mkdir -p examples/sample_videos/brickmasonry
   
   # Download dataset
   kaggle datasets download -d ehsaanali/construction-activity-recognition-dataset
   
   # Unzip
   unzip construction-activity-recognition-dataset.zip -d examples/sample_videos/brickmasonry/
   
   # Clean up
   rm construction-activity-recognition-dataset.zip
   ```

### Using the Videos

Once downloaded, you can analyze the videos:

#### Web Interface (Streamlit)
```bash
streamlit run app.py
```
Then upload any video from `examples/sample_videos/brickmasonry/`

#### Command Line
```bash
python src/main.py \
  --video examples/sample_videos/brickmasonry/video1.mp4 \
  --sop config/bricklaying_sop.json \
  --frame-rate 3
```

#### Batch Processing
```bash
# Process all videos in the directory
for video in examples/sample_videos/brickmasonry/*.mp4; do
  echo "Processing: $video"
  python src/main.py --video "$video" --sop config/bricklaying_sop.json --output results/brickmasonry/
done
```

### Expected Video Content

The videos should show:
- Workers mixing mortar in wheelbarrow or on mortarboard
- Throwing mortar lines on foundation or previous course
- Laying stretcher and header bricks
- Using trowel to apply and furrow mortar
- Checking alignment with level and string line
- Tooling joints with jointer
- Workers wearing appropriate safety equipment (hard hats, gloves, goggles)

### Dataset Structure

```
examples/sample_videos/brickmasonry/
├── video_001.mp4    # Example: Mixing mortar
├── video_002.mp4    # Example: Laying first course
├── video_003.mp4    # Example: Building corner lead
├── ...
└── video_013.mp4    # Example: Finishing joints
```

### Troubleshooting

**Problem:** "Dataset not found" error on Kaggle

**Solution:** 
- Ensure you're logged into Kaggle
- The dataset may have been renamed or moved
- Try searching: "construction activity recognition brick masonry"
- Alternative datasets:
  - Search for "construction video" or "masonry" on Kaggle
  - Use YouTube videos (download with yt-dlp)

**Problem:** Videos won't open in the application

**Solution:**
- Ensure videos are in MP4 format
- Convert if needed:
  ```bash
  ffmpeg -i input_video.avi output_video.mp4
  ```

**Problem:** API download fails

**Solution:**
- Check your kaggle.json credentials
- Verify dataset name is correct
- Try manual download from website instead

### Demo Videos for Testing

If you can't access the Kaggle dataset, you can:

1. **Record your own** (recommended for hackathon!):
   - Use your phone to record someone doing brick work
   - Even a 30-second demonstration works
   - Focus on one specific step (mixing, laying, etc.)

2. **Use YouTube videos**:
   ```bash
   # Install yt-dlp
   pip install yt-dlp
   
   # Download a construction video
   yt-dlp -f mp4 "https://www.youtube.com/watch?v=VIDEO_ID" -o examples/sample_videos/demo.mp4
   ```

3. **Stock video sites**:
   - Pexels: https://www.pexels.com/search/videos/construction/
   - Pixabay: https://pixabay.com/videos/search/construction/
   - (Free for commercial use, no attribution required)

### SOP Reference

The brick laying SOP (`config/bricklaying_sop.json`) is based on:
- **Quikrete Basic Brick Construction Guide**
- URL: https://www.quikrete.com/pdfs/projects/basicbrickconstruction.pdf
- Covers: Common/American bond pattern, tools, safety, step-by-step process

### Citation

If you use this dataset in your project or publication:

```
Dataset: Construction Activity Recognition Dataset
Author: Ehsaan Ali
Source: Kaggle
URL: https://www.kaggle.com/datasets/ehsaanali/construction-activity-recognition-dataset
Year: 2024
```

### Need Help?

- Check the main README.md for general setup
- See SETUP.md for detailed installation instructions
- Open an issue on GitHub if you encounter problems

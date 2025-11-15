# GitHub Upload Guide

Complete guide to uploading this project to GitHub and preparing for your hackathon demo.

## Prerequisites

- Git installed on your computer
- GitHub account (create at https://github.com if you don't have one)
- Project downloaded and extracted

## Step-by-Step GitHub Upload

### 1. Create a New Repository on GitHub

1. Go to https://github.com
2. Click the "+" icon in the top right
3. Select "New repository"
4. Fill in the details:
   - **Repository name:** `construction-safety-monitor`
   - **Description:** `AI-powered construction safety monitoring system using spatial intelligence to ensure SOP compliance`
   - **Visibility:** Public (so hackathon judges can see it!)
   - **Initialize:** DO NOT check any boxes (we already have files)
5. Click "Create repository"

### 2. Initialize Git in Your Local Project

Open terminal/command prompt and navigate to the project:

```bash
cd construction-safety-monitor

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Construction Safety Monitor with brick masonry SOP"
```

### 3. Connect to GitHub and Push

Replace `YOUR_USERNAME` with your GitHub username:

```bash
# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/construction-safety-monitor.git

# Push to GitHub
git branch -M main
git push -u origin main
```

If prompted for credentials:
- **Username:** Your GitHub username
- **Password:** Use a Personal Access Token (not your account password)

#### How to Create Personal Access Token:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token"
3. Give it a note: "Construction Safety Monitor"
4. Select scopes: `repo` (full control of private repositories)
5. Click "Generate token"
6. **COPY THE TOKEN** (you won't see it again!)
7. Use this token as your password when pushing

### 4. Verify Upload

1. Go to `https://github.com/YOUR_USERNAME/construction-safety-monitor`
2. You should see all your files!
3. The README.md should display automatically

## Customizing for Your Hackathon

### 1. Update README with Your Information

Edit `README.md` and change:

```markdown
## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/YOUR_USERNAME/construction-safety-monitor](https://github.com/YOUR_USERNAME/construction-safety-monitor)
```

### 2. Add Your Name to the License

Edit `LICENSE` and replace `[Your Name]` with your actual name:

```
Copyright (c) 2024 Your Actual Name
```

### 3. Update the Project Banner (Optional but Impressive!)

Create a banner image showing:
- System architecture
- Example alert
- UI screenshot

Save as `docs/banner.png` and add to README:

```markdown
![Construction Safety Monitor](docs/banner.png)
```

## Preparing Demo Videos

### Option 1: Use Kaggle Dataset

See `DATASET.md` for detailed instructions.

Quick version:
```bash
# Download from Kaggle
kaggle datasets download -d ehsaanali/construction-activity-recognition-dataset

# Extract
mkdir -p examples/sample_videos/brickmasonry
unzip construction-activity-recognition-dataset.zip -d examples/sample_videos/brickmasonry/
```

### Option 2: Record Your Own (Highly Recommended!)

1. Record 2-3 short videos (30-60 seconds each):
   - **Video 1:** "Perfect" compliance - following all SOP steps
   - **Video 2:** Missing safety equipment (no goggles, no gloves)
   - **Video 3:** Wrong tool usage (hammer instead of trowel)

2. Save in `examples/sample_videos/demo/`

3. These make for a MUCH better demo than pre-existing videos!

## Committing Your Changes

After making changes:

```bash
# Check what changed
git status

# Add changes
git add .

# Commit with descriptive message
git commit -m "Add demo videos and update contact information"

# Push to GitHub
git push
```

## Making Your Repo Look Professional

### Add Topic Tags

On GitHub repository page:
1. Click the gear icon next to "About"
2. Add topics: `construction`, `ai`, `computer-vision`, `safety`, `spatial-intelligence`, `hackathon`
3. Add website if you deploy it
4. Save changes

### Create a Great README

Your README should have:
- ✅ Clear project title and description
- ✅ Demo video or GIF
- ✅ Installation instructions
- ✅ Usage examples
- ✅ Screenshots
- ✅ Technologies used
- ✅ Your contact info

### Add GitHub Actions (Optional)

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/
```

This adds a green checkmark to your repo!

## Hackathon-Specific Tips

### 1. Create a Demo Branch

```bash
# Create a demo branch with sample outputs
git checkout -b demo

# Add pre-generated results
mkdir -p results/demo
python src/main.py --video examples/sample_videos/demo.mp4 --sop config/bricklaying_sop.json --output results/demo/

# Commit demo results
git add results/demo/
git commit -m "Add demo results for presentation"
git push origin demo
```

### 2. Add a Video Demo

Record a screen capture of your app in action:
- Use OBS Studio (free) or Loom
- Show: Upload → Analysis → Alerts → Report
- Keep it under 2 minutes
- Upload to YouTube
- Add link to README

### 3. Create a Presentation Branch

```bash
git checkout -b presentation
# Add your presentation slides, demo script, etc.
git push origin presentation
```

### 4. Pin Important Issues

Create GitHub Issues for:
- Future improvements
- Known limitations
- Hackathon feedback

Pin 2-3 to show you're thinking ahead!

## Troubleshooting

### Problem: "fatal: remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/construction-safety-monitor.git
```

### Problem: "Updates were rejected"

```bash
git pull origin main --rebase
git push origin main
```

### Problem: Large files won't upload

Videos are too large for GitHub. Use Git LFS or store separately:

```bash
# Install Git LFS
git lfs install

# Track video files
git lfs track "*.mp4"
git add .gitattributes

# Commit and push
git add .
git commit -m "Add Git LFS for video files"
git push
```

Or exclude videos from repo:
```bash
echo "*.mp4" >> .gitignore
echo "*.avi" >> .gitignore
```

## Sharing Your Project

### Create a Short Link

Use bit.ly or similar to create a short link:
`bit.ly/construction-ai` → Points to your GitHub repo

### Social Media Post Template

```
🏗️ Just built an AI-powered Construction Safety Monitor! 

✨ Features:
- Real-time video analysis
- SOP compliance checking
- Automated safety alerts

Built with Gemini AI, Sentence Transformers, and Streamlit

Check it out: [YOUR_GITHUB_LINK]

#AI #Construction #Hackathon #Safety #SpatialIntelligence
```

### Elevator Pitch (30 seconds)

"Construction Safety Monitor uses AI and spatial intelligence to ensure workers follow proper procedures. It analyzes construction videos in real-time, compares actions against SOPs, and generates instant alerts for safety violations. This reduces accidents, ensures compliance, and scales to multiple sites—all automatically."

## Final Checklist Before Hackathon

- [ ] Code pushed to GitHub
- [ ] README updated with your info
- [ ] LICENSE has your name
- [ ] Demo videos ready
- [ ] .env file configured (but NOT pushed to GitHub!)
- [ ] Tested on a fresh clone:
  ```bash
  git clone https://github.com/YOUR_USERNAME/construction-safety-monitor.git
  cd construction-safety-monitor
  ./quickstart.sh
  ```
- [ ] Streamlit app runs smoothly
- [ ] At least one successful video analysis completed
- [ ] Results look professional
- [ ] Practiced your demo (2-3 minutes)

## Resources

- Git Documentation: https://git-scm.com/doc
- GitHub Guides: https://guides.github.com/
- Markdown Guide: https://www.markdownguide.org/
- Git LFS: https://git-lfs.github.com/

## Need Help?

If you run into issues:
1. Check error messages carefully
2. Search GitHub issue: `git error message here`
3. Ask ChatGPT or Claude
4. Create an issue on the original repo

Good luck with your hackathon! 🚀

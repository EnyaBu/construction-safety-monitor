#!/bin/bash
# Automated GitHub Setup Script for Construction Safety Monitor

echo "🏗️  Construction Safety Monitor - GitHub Setup"
echo "=============================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    echo "   Visit: https://git-scm.com/downloads"
    exit 1
fi

echo "✓ Git is installed"

# Check if already a git repository
if [ -d ".git" ]; then
    echo "⚠️  This is already a git repository."
    read -p "Do you want to re-initialize? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf .git
        echo "✓ Removed existing git repository"
    else
        echo "Keeping existing repository."
        exit 0
    fi
fi

# Get GitHub username
echo ""
read -p "Enter your GitHub username: " github_username

if [ -z "$github_username" ]; then
    echo "❌ GitHub username is required!"
    exit 1
fi

# Get repository name (default: construction-safety-monitor)
echo ""
read -p "Repository name [construction-safety-monitor]: " repo_name
repo_name=${repo_name:-construction-safety-monitor}

# Update README with correct username
echo ""
echo "Updating README with your information..."
sed -i.bak "s/yourusername/$github_username/g" README.md 2>/dev/null || sed -i "" "s/yourusername/$github_username/g" README.md
rm -f README.md.bak
echo "✓ README updated"

# Get user's name for license
echo ""
read -p "Your full name (for LICENSE): " user_name

if [ ! -z "$user_name" ]; then
    sed -i.bak "s/\[Your Name\]/$user_name/g" LICENSE 2>/dev/null || sed -i "" "s/\[Your Name\]/$user_name/g" LICENSE
    rm -f LICENSE.bak
    echo "✓ LICENSE updated"
fi

# Initialize git repository
echo ""
echo "Initializing git repository..."
git init
echo "✓ Git repository initialized"

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
venv/
env/
.env

# Results and outputs
results/
*.log

# Videos (too large)
*.mp4
*.avi
*.mov
!examples/sample_videos/.gitkeep

# IDE
.vscode/
.idea/
*.swp
.DS_Store
EOF
    echo "✓ Created .gitignore"
fi

# Create sample videos directory
mkdir -p examples/sample_videos/brickmasonry
touch examples/sample_videos/.gitkeep

# Add all files
echo ""
echo "Adding files to git..."
git add .
echo "✓ Files added"

# Create initial commit
echo ""
echo "Creating initial commit..."
git commit -m "Initial commit: Construction Safety Monitor

- AI-powered construction safety monitoring
- Brick masonry SOP based on Quikrete guide
- Video analysis with Gemini API
- Semantic similarity with Sentence Transformers
- Web interface with Streamlit
- Ready for Kaggle dataset integration"

echo "✓ Initial commit created"

# Set main branch
git branch -M main

# Add remote
echo ""
echo "Adding GitHub remote..."
git remote add origin "https://github.com/$github_username/$repo_name.git"
echo "✓ Remote added"

# Display next steps
echo ""
echo "=============================================="
echo "✅ Git repository configured!"
echo "=============================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Create the repository on GitHub:"
echo "   Go to: https://github.com/new"
echo "   Name: $repo_name"
echo "   Description: AI-powered construction safety monitoring system"
echo "   Keep it PUBLIC for hackathon visibility"
echo "   DO NOT initialize with README (we already have files)"
echo ""
echo "2. Push your code to GitHub:"
echo "   git push -u origin main"
echo ""
echo "   (You'll need to authenticate with GitHub)"
echo "   (Use Personal Access Token, not password)"
echo ""
echo "3. Download the Kaggle dataset:"
echo "   See DATASET.md for instructions"
echo ""
echo "4. Get your Gemini API key:"
echo "   Visit: https://makersuite.google.com/app/apikey"
echo "   Add to .env file"
echo ""
echo "5. Test the application:"
echo "   streamlit run app.py"
echo ""
echo "=============================================="
echo "Repository URL will be:"
echo "https://github.com/$github_username/$repo_name"
echo "=============================================="

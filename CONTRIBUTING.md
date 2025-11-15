# Contributing to Construction Safety Monitor

Thank you for considering contributing to Construction Safety Monitor! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Assume good intentions

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report:
- Check if the issue already exists
- Verify you're using the latest version
- Check if it's actually a bug and not a configuration issue

When creating a bug report, include:
- Python version and OS
- Complete error message and stack trace
- Steps to reproduce
- Expected vs actual behavior
- Video file details (if applicable)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:
- Clear description of the enhancement
- Use cases and benefits
- Potential implementation approach (if you have ideas)

### Adding New SOPs

To contribute new SOP templates:

1. Use the SOP template format in `config/sop_template.json`
2. Include detailed step descriptions
3. List all required tools and safety equipment
4. Add expected time estimates
5. Document quality standards and common hazards
6. Test with actual construction videos if possible

### Pull Requests

1. **Fork the repository**
2. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes** following our coding standards
4. **Test your changes** thoroughly
5. **Commit with clear messages**:
   ```bash
   git commit -m "Add amazing feature"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/construction-safety-monitor.git
cd construction-safety-monitor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies including dev tools
pip install -r requirements.txt
pip install pytest pytest-cov black flake8

# Run tests
pytest tests/
```

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:
- Line length: 100 characters (instead of 79)
- Use meaningful variable names
- Add docstrings to all functions and classes
- Use type hints where appropriate

### Code Formatting

Format your code with Black:
```bash
black src/ tests/
```

### Linting

Check code quality with flake8:
```bash
flake8 src/ tests/ --max-line-length=100
```

### Documentation

- Add docstrings to all public functions
- Update README.md if adding new features
- Add inline comments for complex logic
- Update SETUP.md if changing installation process

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_sop_comparator.py -v
```

### Writing Tests

- Write tests for new functionality
- Aim for >80% code coverage
- Use pytest fixtures for common setup
- Test edge cases and error conditions

Example test structure:
```python
def test_feature_name():
    """Test description."""
    # Arrange
    input_data = ...
    
    # Act
    result = function_to_test(input_data)
    
    # Assert
    assert result == expected_value
```

## Project Structure

```
construction-safety-monitor/
├── src/                    # Source code
│   ├── __init__.py
│   ├── video_analyzer.py   # Video analysis module
│   ├── sop_comparator.py   # SOP comparison engine
│   ├── alert_generator.py  # Alert generation
│   └── utils.py            # Utility functions
├── config/                 # SOP configurations
├── tests/                  # Test files
├── examples/               # Example videos/demos
└── app.py                  # Streamlit web app
```

## Commit Message Guidelines

Use clear, descriptive commit messages:

```
Short (50 chars or less) summary

More detailed explanatory text if needed. Wrap at 72 characters.
Explain the problem this commit solves and why the change is needed.

- Bullet points are okay
- Use present tense ("Add feature" not "Added feature")
- Reference issues: "Fixes #123"
```

### Types of commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Formatting, missing semi-colons, etc.
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

## Areas Needing Contribution

High-priority areas:

1. **Additional SOP Templates**
   - More construction tasks (plumbing, electrical, etc.)
   - Industry-specific variations
   - Different regional standards

2. **Video Analysis Improvements**
   - Support for more video formats
   - Real-time video stream processing
   - Multi-camera support

3. **Alert System Enhancements**
   - SMS/Email notifications
   - Integration with construction management software
   - Automated reporting

4. **Model Improvements**
   - Fine-tuning models for construction domain
   - Support for offline operation
   - Faster inference

5. **Documentation**
   - Tutorial videos
   - More usage examples
   - Translations to other languages

## Questions?

Feel free to:
- Open an issue for questions
- Join our discussions
- Reach out to maintainers

## Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Credited in documentation

Thank you for contributing! 🙏

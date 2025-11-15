# Project Architecture Overview

## System Design

The Construction Safety Monitor is designed with a modular architecture consisting of three main components:

```
┌─────────────────────────────────────────────────────────────┐
│                     VIDEO INPUT                              │
│              (Construction Work Videos)                      │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                 VIDEO ANALYZER                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  1. Frame Extraction (OpenCV)                        │   │
│  │  2. Action Recognition (Gemini Vision API)           │   │
│  │  3. Temporal Analysis                                │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
              [Action Descriptions]
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                 SOP COMPARATOR                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  1. Load SOP Configuration                           │   │
│  │  2. Semantic Similarity (Sentence Transformers)      │   │
│  │  3. Tool & Safety Compliance Check                   │   │
│  │  4. Deviation Detection                              │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
            [Compliance Results]
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                ALERT GENERATOR                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  1. Severity Classification                          │   │
│  │  2. Alert Message Generation                         │   │
│  │  3. Summary Report Creation                          │   │
│  │  4. Export (Text/JSON)                               │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
                    [OUTPUTS]
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
   [Alerts.txt]                [Compliance Report]
```

## Component Details

### 1. Video Analyzer (`src/video_analyzer.py`)

**Purpose**: Extract and analyze actions from construction videos

**Key Functions**:
- `extract_frames()`: Extracts frames at specified intervals using OpenCV
- `analyze_frame()`: Analyzes individual frames using Gemini Vision API
- `analyze_video()`: Frame-by-frame analysis
- `analyze_video_direct()`: Direct video analysis (faster, less detailed)

**Technologies**:
- OpenCV (cv2) for video processing
- Google Gemini 2.0 Flash for vision analysis
- JSON for structured output

**Input**: Video file (MP4, AVI, MOV, etc.)
**Output**: List of timestamped action descriptions with metadata

### 2. SOP Comparator (`src/sop_comparator.py`)

**Purpose**: Compare observed actions against Standard Operating Procedures

**Key Functions**:
- `load_sop()`: Loads SOP configuration from JSON
- `compute_similarity()`: Calculates semantic similarity between actions
- `find_best_match()`: Finds best matching SOP step for each action
- `check_tool_compliance()`: Verifies correct tool usage
- `check_safety_equipment()`: Verifies safety equipment compliance
- `analyze_sequence()`: Analyzes full video sequence
- `generate_summary()`: Creates statistical summary

**Technologies**:
- Sentence Transformers (all-MiniLM-L6-v2) for semantic similarity
- PyTorch for model inference
- Cosine similarity for matching

**Input**: Video actions + SOP configuration
**Output**: Compliance results with deviation flags

### 3. Alert Generator (`src/alert_generator.py`)

**Purpose**: Generate human-readable alerts and reports

**Key Functions**:
- `generate_deviation_alert()`: Creates alert for single deviation
- `generate_batch_alerts()`: Creates alerts for all deviations
- `generate_summary_report()`: Creates comprehensive report
- `save_alerts_to_file()`: Exports alerts to text file
- `export_json()`: Exports structured data to JSON

**Technologies**:
- Python string formatting
- JSON serialization
- File I/O

**Input**: Compliance results
**Output**: Formatted alerts and reports

## Data Flow

### 1. Video Processing Flow

```python
Video File → Frame Extraction → Individual Frames → Gemini Analysis → Action Descriptions
```

### 2. Comparison Flow

```python
Action Description → Embedding → Similarity Calculation → Best Match → Compliance Check
```

### 3. Alert Flow

```python
Compliance Result → Severity Assessment → Alert Generation → Report Creation
```

## SOP Configuration Format

SOPs are defined in JSON with this structure:

```json
{
  "task_name": "Construction Task",
  "steps": [
    {
      "id": 1,
      "action": "Step description",
      "expected_time": 120,
      "required_tools": ["tool1", "tool2"],
      "zone": "work area"
    }
  ],
  "safety_equipment": ["hard hat", "safety glasses"],
  "tools_required": ["tape measure", "drill"]
}
```

## Model Details

### Gemini 2.0 Flash
- **Purpose**: Video understanding and action recognition
- **Input**: Video frames or full video
- **Output**: Structured JSON with action descriptions
- **Advantages**: Good accuracy, supports video directly
- **Limitations**: Requires internet, API costs

### Sentence Transformers (all-MiniLM-L6-v2)
- **Purpose**: Semantic text similarity
- **Input**: Text strings (action descriptions)
- **Output**: 384-dimensional embeddings
- **Advantages**: Fast, accurate, runs locally
- **Specifications**:
  - Model size: ~90MB
  - Embedding dimension: 384
  - Max sequence length: 256 tokens
  - Processing speed: ~1000 sentences/second on CPU

## Performance Characteristics

### Video Analysis
- **Frame-by-frame**: 2-3 seconds per frame
- **Direct video**: ~30 seconds for 1-minute video
- **Frame extraction**: <1 second per frame

### SOP Comparison
- **Similarity computation**: <100ms per comparison
- **Batch processing**: ~1 second for 100 comparisons

### Overall Pipeline
- **10-minute video (frame-by-frame at 2s intervals)**:
  - Frames extracted: 300
  - Analysis time: ~10-15 minutes
  - Comparison time: ~30 seconds
  - Total: ~15 minutes

## Scalability Considerations

### Current Limitations
- Gemini API rate limits
- Memory usage for long videos
- Single-threaded processing

### Optimization Strategies
1. **Use direct video analysis** for videos <20MB
2. **Increase frame rate** to reduce API calls
3. **Batch processing** for multiple videos
4. **GPU acceleration** for sentence transformers
5. **Caching** of embeddings

## Security & Privacy

### Data Handling
- Videos are processed locally (except API calls)
- No data stored on Gemini servers after processing
- API keys stored in environment variables
- Results saved locally

### API Security
- API keys in .env file (not committed to git)
- HTTPS for all API communications
- Rate limiting to prevent abuse

## Extensibility

### Adding New Construction Tasks
1. Create new SOP JSON in `config/`
2. Define steps with detailed descriptions
3. List required tools and safety equipment
4. Test with sample videos

### Custom Video Analysis
1. Extend `VideoAnalyzer` class
2. Implement custom frame processing
3. Return structured action data

### Alternative Models
1. Replace Gemini with OpenAI GPT-4V
2. Use local models (BLIP-2, etc.)
3. Fine-tune sentence transformers

## Error Handling

### Video Analysis Errors
- Invalid video format → Convert to MP4
- API timeout → Retry with exponential backoff
- Large file size → Frame-by-frame fallback

### Comparison Errors
- Low similarity scores → Adjust threshold
- Missing tools → Flag in compliance check
- Parsing errors → Fallback to text description

## Future Enhancements

### Short-term
- [ ] Multi-camera support
- [ ] Real-time streaming
- [ ] Mobile app interface
- [ ] Email/SMS alerts

### Long-term
- [ ] Custom model fine-tuning
- [ ] Worker tracking and identification
- [ ] Historical analytics dashboard
- [ ] Integration with project management tools
- [ ] Offline operation mode
- [ ] Multi-language support

## Testing Strategy

### Unit Tests
- Individual function testing
- Mock data for API calls
- Edge case handling

### Integration Tests
- Full pipeline testing
- Multiple SOP configurations
- Various video formats

### Performance Tests
- Processing speed benchmarks
- Memory usage profiling
- API rate limit testing

## Deployment Options

### Local Installation
- Desktop application
- Command-line tool
- Streamlit web interface

### Cloud Deployment
- Docker container
- AWS/GCP/Azure hosting
- API service

### Edge Deployment
- Construction site servers
- Raspberry Pi devices
- Mobile devices (limited functionality)

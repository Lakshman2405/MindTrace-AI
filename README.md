# 🧠 MindTrace-AI

**AI-Powered Mental State Awareness & Emotional Intelligence System**

MindTrace-AI is an end-to-end AI system that analyzes user journal entries to infer emotional patterns, sentiment trends, psychological risk levels, and actionable mental-health insights using modern NLP models (RoBERTa, Transformers) and LLM-based reasoning.

---

## 📌 Table of Contents

1. [Project Overview](#-project-overview)
2. [Problem Statement](#-problem-statement)
3. [Solution & Approach](#-solution--approach)
4. [System Architecture](#-system-architecture)
5. [Tech Stack](#-tech-stack)
6. [Key Features](#-key-features)
7. [Repository Structure](#-repository-structure)
8. [Component Details](#-component-details)
9. [Data Pipeline](#-data-pipeline)
10. [Models](#-models)
11. [Configuration](#-configuration)
12. [Running Locally](#-running-locally)
13. [Deployment](#-deployment)
14. [API Reference](#-api-reference)
15. [Future Enhancements](#-future-enhancements)
16. [Disclaimer](#️-disclaimer)
17. [License](#-license)

---

## 🚀 Project Overview

MindTrace-AI transforms unstructured daily journal entries into structured, actionable mental-health insights through multi-stage NLP processing and AI reasoning. The system processes raw text and generates:

- **Emotional Signals**: Multi-label emotion classification (28 emotions using GoEmotions model)
- **Sentiment Progression**: Trend analysis with moving averages and slope calculations
- **Risk Score Estimation**: Dynamic risk scoring based on sentiment, emotion, and behavioral patterns
- **Behavioral Pattern Analysis**: Detection of emotional patterns (alternating, sustained-negative, recovery, stable)
- **Trajectory Classification**: Trend direction assessment (improving, declining, stable)
- **Human-Readable Insights**: LLM-powered personalized reflections and recommendations

The system is designed for **mental awareness**, **early risk detection**, and **explainable AI insights**, not for medical diagnosis.

---

## 🎯 Problem Statement

Mental health awareness is critical but often overlooked in everyday life. People journal to process emotions, but rarely have tools to:
- Understand emotional patterns over time
- Detect early warning signs of psychological risk
- Get actionable, empathetic guidance based on their own words
- Visualize emotional trajectories

Traditional mental-health tools are expensive, clinical, or lack personalization.

---

## 💡 Solution & Approach

MindTrace-AI addresses this by:

1. **Fine-grained Emotion Detection**: Using RoBERTa fine-tuned on GoEmotions (28 distinct emotion labels), not just basic sentiment
2. **Temporal Pattern Recognition**: Analyzing sequences of journal entries to detect trends and patterns
3. **Composite Risk Scoring**: Combining sentiment, emotional volatility, pattern classification, and trajectory to estimate psychological risk
4. **Explainable AI**: Each insight includes reasoning and is traced back to journal content
5. **Empathetic Communication**: LLM-generated reports that feel like guidance from a friend, not a clinical assessment
6. **Privacy-First Design**: All processing is done locally; data stays in user's session

---

## 🧩 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER INTERFACE (Streamlit)                 │
│              - Journal Entry Input & History Management         │
│              - Interactive Visualizations (Plotly/Matplotlib)  │
│              - Real-time Session Management                     │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          │ HTTP / WebSocket
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND API (FastAPI)                        │
│              - Request Validation (Pydantic)                    │
│              - Session Management & History                     │
│              - Orchestration of ML Pipeline                     │
│              - JSON Response Formatting                         │
└─────────────────────────┬───────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ↓                 ↓                 ↓
  ┌───────────┐    ┌──────────────┐  ┌────────────────┐
  │ SENTIMENT │    │   EMOTION    │  │ PATTERN & RISK │
  │ INFERENCE │    │  INFERENCE   │  │    ANALYSIS    │
  │           │    │              │  │                │
  │Transformer│    │   RoBERTa    │  │ - Volatility   │
  │ (Twitter) │    │ (GoEmotions) │  │ - Diversity    │
  │           │    │              │  │ - Trend Slope  │
  │ Output:   │    │ Output:      │  │ - Trajectory   │
  │ Negative/ │    │ Joy, Sadness │  │ - Risk Level   │
  │ Neutral/  │    │ Fear, Pride  │  │                │
  │ Positive  │    │ (28 labels)  │  │ Output:        │
  │ + Conf    │    │ + Top 5      │  │ Structured     │
  └───────────┘    └──────────────┘  │ Analysis       │
                                      └────────┬───────┘
                                               │
                                               ↓
                                   ┌──────────────────────┐
                                   │   LLM INSIGHT GEN    │
                                   │                      │
                                   │ HF Router / OpenAI   │
                                   │ Model: Llama-3-8B    │
                                   │                      │
                                   │ Output:              │
                                   │ - Empathetic Report  │
                                   │ - Reflections        │
                                   │ - Recommendations    │
                                   └──────────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend
- **Streamlit**: Interactive web UI for journal input and visualization
- **Plotly**: Interactive charts and graphs
- **Matplotlib**: Statistical visualizations
- **Pandas**: Data manipulation and session history
- **NumPy**: Numerical computations

### Backend
- **FastAPI**: High-performance REST API framework
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server for FastAPI

### AI / NLP Models
- **Hugging Face Transformers**: Model loading and inference
- **PyTorch**: Deep learning framework (GPU/CPU support)
- **RoBERTa**: Fine-tuned emotion classification (GoEmotions dataset)
- **Transformer-based Sentiment**: Twitter sentiment model
- **Llama-3-8B**: LLM for insight generation

### Analysis & Utilities
- **Scikit-learn**: Cosine similarity, pattern metrics
- **NumPy**: Trend calculation, statistical metrics

### Deployment
- **Docker**: Containerization for reproducibility
- **Hugging Face Spaces**: Model and app hosting

---

## 📊 Key Features

| Feature | Description |
|---------|-------------|
| 📝 **Journal-Based Analysis** | Accepts multi-entry journal text, processes each independently |
| 🎭 **Multi-Label Emotions** | Detects up to 28 distinct emotions (GoEmotions labels) |
| 📊 **Sentiment Trend Visualization** | Line charts with moving averages and trend lines |
| ⚠️ **Risk Score Computation** | Dynamic risk levels (Low / Medium / High / Critical) with explainability |
| 🧭 **Pattern Classification** | Identifies emotional patterns: alternating, sustained-negative, recovery, stable |
| 📈 **Trajectory Analysis** | Detects improving, declining, or stable emotional trends |
| 🧠 **AI-Generated Insights** | LLM-powered personalized reflections with actionable recommendations |
| 🗂️ **Session History** | Save, reload, and revisit past journal analysis sessions |
| 📥 **Structured JSON Export** | Export analysis results in machine-readable format |
| 🎨 **Interactive Dashboard** | Real-time visualization and metric updates |

---

## 📂 Repository Structure

```bash
MINDTRACE-AI/
│
├── backend/
│   ├── api.py                          # FastAPI application entry point
│   │                                    # - POST /analyze: Core analysis endpoint
│   │                                    # - POST /save-session: Persist session
│   │                                    # - GET /load-session: Retrieve session
│   │                                    # - GET /health: Health check
│   └── requirements-backend.txt         # Backend dependencies
│
├── frontend/
│   ├── app.py                          # Streamlit main application
│   │                                    # - Session state management
│   │                                    # - Journal input interface
│   │                                    # - Visualization components
│   │                                    # - API integration
│   └── requirements-frontend.txt        # Frontend dependencies
│
├── src/
│   ├── config.py                       # Configuration & environment variables
│   │                                    # - Model paths (Hugging Face Hub)
│   │                                    # - Thresholds (emotion, risk, etc.)
│   │                                    # - Device selection (GPU/CPU)
│   │                                    # - API keys & tokens
│   │
│   ├── emotion_inference.py            # Emotion classification pipeline
│   │                                    # - Model: RoBERTa (GoEmotions, 28 labels)
│   │                                    # - Input: Raw text
│   │                                    # - Output: Top 5 emotions + confidence
│   │                                    # - Threshold filtering
│   │
│   ├── sentiment_inference.py          # Sentiment analysis pipeline
│   │                                    # - Model: Transformer (Twitter sentiment)
│   │                                    # - Input: Raw text
│   │                                    # - Output: Positive/Neutral/Negative + confidence
│   │                                    # - Softmax normalization
│   │
│   ├── pattern_analysis.py             # Multi-stage pattern & risk analysis
│   │                                    # - Sentiment trend computation (linear regression)
│   │                                    # - Pattern classification (4 types)
│   │                                    # - Trajectory assessment (3 types)
│   │                                    # - Emotional volatility & diversity metrics
│   │                                    # - Risk level calculation
│   │
│   ├── llm_insights.py                 # LLM-powered insight generation
│   │                                    # - Prompt engineering for empathetic output
│   │                                    # - Integration with HF Router / OpenAI
│   │                                    # - Report generation & formatting
│   │
│   └── utils.py (if exists)            # Utility functions (helpers, decorators)
│
├── data/
│   ├── go_emotions/                    # GoEmotions dataset (28 emotion labels)
│   │   ├── train.csv                   # ~43k training samples
│   │   ├── validation.csv              # ~5.4k validation samples
│   │   └── test.csv                    # ~5.4k test samples
│   │
│   └── tweet_eval_sentiment/           # TweetEval sentiment dataset
│       ├── train.csv                   # ~40k training samples
│       ├── validation.csv              # ~5k validation samples
│       └── test.csv                    # ~5k test samples
│
├── notebooks/
│   ├── emotion_model_training.ipynb    # Fine-tuning RoBERTa on GoEmotions
│   │                                    # - Data loading & preprocessing
│   │                                    # - Model architecture & training loop
│   │                                    # - Evaluation metrics (F1, Precision, Recall)
│   │                                    # - Model export to Hugging Face Hub
│   │
│   └── sentiment_model_training.ipynb  # Fine-tuning Transformer on TweetEval
│                                        # - Similar pipeline as emotion model
│
├── scripts/
│   ├── download_data1.py               # Script to download GoEmotions dataset
│   ├── download_data2.py               # Script to download TweetEval dataset
│   └── train_models.sh                 # Shell script to orchestrate training
│
├── tests/
│   ├── test_inference.py               # Unit tests for inference pipelines
│   │                                    # - Emotion model accuracy tests
│   │                                    # - Sentiment model accuracy tests
│   │                                    # - Edge case handling
│   │
│   ├── test_llm_response.py            # Tests for LLM integration
│   │                                    # - Prompt validation
│   │                                    # - Response parsing
│   │                                    # - Error handling
│   │
│   └── test_pattern.py                 # Tests for pattern analysis
│                                        # - Pattern classification logic
│                                        # - Risk scoring accuracy
│
├── .gitignore                          # Exclude large files, secrets, cache
├── .env.example                        # Template for environment variables
├── requirements.txt                    # All dependencies (unified)
├── Dockerfile                          # Container specification
├── docker-compose.yml                  # Multi-container orchestration
├── README.md                           # This file
└── LICENSE                             # Project license

```

---

## 🔧 Component Details

### 1. **Emotion Inference** (`src/emotion_inference.py`)

**Model**: RoBERTa fine-tuned on GoEmotions (28 emotion labels)

**Supported Emotions**:
```
admiration, amusement, anger, annoyance, approval,
caring, confusion, curiosity, desire, disappointment,
disapproval, disgust, embarrassment, excitement,
fear, gratitude, grief, joy, love, nervousness,
optimism, pride, realization, relief,
remorse, sadness, surprise, neutral
```

**Process**:
1. Tokenize input text (max 128 tokens)
2. Pass through RoBERTa encoder
3. Apply sigmoid activation (multi-label classification)
4. Filter emotions above `EMOTION_THRESHOLD` (default: 0.30)
5. Return top 5 emotions with confidence scores

**Example Output**:
```json
{
  "detected_emotions": ["joy", "gratitude", "excitement"],
  "top_5_emotions": [
    ["joy", 0.89],
    ["excitement", 0.76],
    ["gratitude", 0.65],
    ["pride", 0.48],
    ["approval", 0.42]
  ]
}
```

---

### 2. **Sentiment Inference** (`src/sentiment_inference.py`)

**Model**: Transformer fine-tuned on TweetEval (3 sentiment classes)

**Classification**: Negative (-1), Neutral (0), Positive (1)

**Process**:
1. Tokenize input text (max 128 tokens)
2. Pass through Transformer encoder
3. Apply softmax normalization
4. Return label with highest probability + confidence

**Example Output**:
```json
{
  "sentiment": "positive",
  "confidence": 0.94
}
```

---

### 3. **Pattern Analysis** (`src/pattern_analysis.py`)

**Stage 1: Model Application**
- Runs emotion and sentiment models on all journal entries
- Builds time-series data structure

**Stage 2: Pattern Classification**
Detects one of 4 emotional patterns:
- **Alternating Pattern**: Rapid mood swings (≥70% alternations)
- **Sustained Negative**: 3+ consecutive negative sentiments
- **Recovery Pattern**: Negative → Positive transition
- **Stable Pattern**: Consistent emotional state

**Stage 3: Trajectory Analysis**
- Computes linear trend slope on sentiment scores
- Classifies as: Improving (slope > 0.1), Declining (slope < -0.1), Stable

**Stage 4: Emotional Metrics**
- **Volatility**: Standard deviation of emotion scores across time
- **Diversity**: Shannon entropy of emotion distribution
- **Moving Average**: 3-window convolution for trend smoothing

**Stage 5: Risk Scoring**
Composite formula:
```
risk_score = 
  0.3 * negative_sentiment_ratio +
  0.2 * emotional_volatility +
  0.2 * sustained_negative_penalty +
  0.15 * alternating_pattern_penalty +
  0.15 * trajectory_slope_penalty
```

Risk Levels:
- **Low** (0-0.25): Stable, positive emotional state
- **Medium** (0.25-0.55): Some emotional fluctuation
- **High** (0.55-0.80): Significant emotional distress
- **Critical** (0.80-1.0): Urgent intervention recommended

**Example Output**:
```json
{
  "pattern_type": "recovery_pattern",
  "trajectory_type": "improving",
  "risk_level": "low",
  "trend_slope": 0.15,
  "emotional_volatility": 0.18,
  "emotional_diversity": 2.34
}
```

---

### 4. **LLM Insights** (`src/llm_insights.py`)

**Model**: Llama-3-8B-Instruct (via HF Router or OpenRouter)

**Process**:
1. Build structured prompt with analysis data
2. Instruct LLM to adopt "friend + wellbeing assistant" persona
3. Generate empathetic, non-clinical report
4. Format with 6 sections:
   - Emotional State Overview
   - Risk Interpretation
   - Behavioral Pattern Analysis
   - Emotional Resilience Perspective
   - Reflection & Growth Recommendations
   - Ongoing Awareness Guidance

**Prompt Strategy**:
- **Empathy First**: Address user directly, avoid technical jargon
- **No Diagnosis**: Explicit instruction not to provide medical advice
- **Pattern-Faithful**: Never contradict provided analysis
- **Supportive Tone**: Focus on growth, resilience, and self-awareness

**Example Output** (truncated):
```
Mental-State Awareness Report

Emotional State Overview
Based on your recent entries, I notice a gentle shift in your emotional landscape...

Risk Interpretation
Your current state suggests a stable emotional foundation...

Behavioral Pattern Analysis
Your pattern shows recovery—moments of challenge followed by renewed optimism...
```

---

## 📊 Data Pipeline

```
Raw Journal Entry
    ↓
[Preprocessing: Lowercase, Basic Cleaning]
    ↓
PARALLEL:
├─→ Emotion Model (RoBERTa GoEmotions) ──→ 28 emotion scores
├─→ Sentiment Model (TweetEval Transformer) ──→ Sentiment label + confidence
    ↓
Pattern Analysis Engine:
├─→ Sentiment Trend (Linear Regression)
├─→ Pattern Classification
├─→ Trajectory Assessment
├─→ Emotional Volatility & Diversity
├─→ Risk Scoring
    ↓
Structured Analysis Object:
{
  "date": "...",
  "sentiment": "...",
  "emotion_scores": [...],
  "pattern_type": "...",
  "trajectory_type": "...",
  "risk_level": "...",
  ...
}
    ↓
LLM Insight Generation:
├─→ Build Context-Aware Prompt
├─→ Query HF Router / OpenRouter
├─→ Parse LLM Response
    ↓
Final Output:
{
  "structured_analysis": {...},
  "llm_report": "...",
  "session_metadata": {...}
}
```

---

## 🤖 Models

### Emotion Model (Custom)
- **Base**: RoBERTa
- **Dataset**: GoEmotions (Multi-label emotion classification)
- **Size**: ~355M parameters (full) / ~116M (distilled)
- **Hub**: `CoderLakshman/mindtrace-emotion-model`
- **Output**: 28 emotion labels with sigmoid confidence scores
- **Performance**: F1 ≈ 0.65 (multi-label setting)

### Sentiment Model (Custom)
- **Base**: Transformer
- **Dataset**: TweetEval (3-class sentiment)
- **Size**: ~110M parameters
- **Hub**: `CoderLakshman/mindtrace-sentiment-model`
- **Output**: Negative / Neutral / Positive with softmax probabilities
- **Performance**: Accuracy ≈ 0.72

### Insight Generation
- **Model**: Llama-3-8B-Instruct
- **Provider**: Hugging Face Inference (router.huggingface.co) or OpenRouter
- **Context Length**: 8192 tokens
- **Temperature**: 0.15 (deterministic, consistent tone)
- **Max Tokens**: 600 per report

---

## ⚙️ Configuration

### Environment Variables (`config.py`)

```python
# Model Paths (Hugging Face Hub)
EMOTION_MODEL_PATH = "CoderLakshman/mindtrace-emotion-model"
SENTIMENT_MODEL_PATH = "CoderLakshman/mindtrace-sentiment-model"

# Thresholds
EMOTION_THRESHOLD = 0.30  # Min confidence for emotion detection

# Device (Auto-detect GPU)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# API Keys
HF_TOKEN = os.getenv("HF_TOKEN")  # Hugging Face API token
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # Optional

# API Endpoints
HF_ROUTER_URL = "https://router.huggingface.co/v1/chat/completions"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
```

### Required Secrets

Create a `.env` file in the project root:
```bash
HF_TOKEN=your_huggingface_token
OPENROUTER_API_KEY=your_openrouter_key  # Optional
```

Obtain tokens from:
- [Hugging Face](https://huggingface.co/settings/tokens)
- [OpenRouter](https://openrouter.ai/) (optional alternative)

---

## ▶️ Running Locally

### Prerequisites
- Python 3.9+
- pip or conda
- GPU (optional, but recommended for faster inference)
- 4GB+ RAM

### Install Dependencies

```bash
# Clone repository
git clone https://github.com/Lakshman2405/MindTrace-AI.git
cd MindTrace-AI

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

### Set Environment Variables

```bash
# Create .env file
cp .env.example .env

# Edit .env with your tokens
export HF_TOKEN=your_token_here
```

### Start Backend API

```bash
# Terminal 1: Backend
uvicorn backend.api:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
- Health check: `GET http://localhost:8000/health`
- API docs: `http://localhost:8000/docs`

### Start Frontend

```bash
# Terminal 2: Frontend
streamlit run frontend/app.py
```

The UI will open at `http://localhost:8501`

---

## 🌐 Deployment

### Docker Deployment

```bash
# Build image
docker build -t mindtrace-ai:latest .

# Run container
docker run -p 8000:8000 -p 8501:8501 \
  -e HF_TOKEN=your_token \
  mindtrace-ai:latest
```

### Docker Compose

```bash
docker-compose up -d
```

This spins up:
- FastAPI backend (port 8000)
- Streamlit frontend (port 8501)

### Hugging Face Spaces Deployment

1. Create a new Space on Hugging Face (https://huggingface.co/spaces)
2. Connect your GitHub repository
3. Set secrets:
   - `HF_TOKEN`
   - `OPENROUTER_API_KEY` (if using OpenRouter)
4. Space auto-deploys from `main` branch

**Dockerfile** (provided in repo) specifies:
- Base: Python 3.9 slim
- FastAPI backend health check
- Streamlit frontend configuration

---

## 📡 API Reference

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```
GET /health
```
Response:
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

---

#### 2. Analyze Journal Entries
```
POST /analyze
```

**Request Body**:
```json
{
  "journal_entries": [
    {
      "date": "2025-01-15",
      "text": "Today was overwhelming. I felt anxious about the presentation..."
    },
    {
      "date": "2025-01-16",
      "text": "Better today. The presentation went well. Feeling proud and relieved..."
    }
  ]
}
```

**Response**:
```json
{
  "results": [
    {
      "date": "2025-01-15",
      "sentiment": "negative",
      "sentiment_score": -1,
      "emotion_scores": [
        ["anxiety", 0.87],
        ["fear", 0.72],
        ["worry", 0.65],
        ["stress", 0.58],
        ["sadness", 0.42]
      ]
    },
    {
      "date": "2025-01-16",
      "sentiment": "positive",
      "sentiment_score": 1,
      "emotion_scores": [
        ["pride", 0.92],
        ["joy", 0.85],
        ["relief", 0.78],
        ["gratitude", 0.61],
        ["excitement", 0.53]
      ]
    }
  ],
  "analysis": {
    "pattern_type": "recovery_pattern",
    "trajectory_type": "improving",
    "risk_level": "low",
    "trend_slope": 0.45,
    "emotional_volatility": 0.32,
    "emotional_diversity": 2.45,
    "moving_average": [0.5, 0.25]
  },
  "llm_report": "Mental-State Awareness Report\n\nEmotional State Overview...",
  "session_id": "sess_abc123xyz"
}
```

---

#### 3. Save Session
```
POST /save-session
```

**Request Body**:
```json
{
  "session_id": "sess_abc123xyz",
  "journal_entries": [...],
  "analysis_results": {...}
}
```

**Response**:
```json
{
  "success": true,
  "message": "Session saved successfully",
  "session_id": "sess_abc123xyz"
}
```

---

#### 4. Load Session
```
GET /load-session?session_id=sess_abc123xyz
```

**Response**:
```json
{
  "session_id": "sess_abc123xyz",
  "created_at": "2025-01-15T10:30:00Z",
  "journal_entries": [...],
  "analysis_results": {...}
}
```

---

## 🔍 Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `HF_TOKEN not configured` | Missing HF token | Add `HF_TOKEN` to `.env` |
| `Model not found on Hub` | Internet issue or wrong model ID | Check model exists on HF Hub |
| `CUDA out of memory` | GPU memory exceeded | Use CPU or reduce batch size |
| `Timeout on LLM request` | Slow internet or HF Router down | Retry or increase timeout |

---

## 📈 Future Enhancements

- 🌍 **Multi-language Support**: Process journals in Spanish, French, German, etc.
- 📊 **Personalized Baselines**: Learn individual emotional baseline for better trend detection
- 🔮 **Emotional Forecasting**: Predict future emotional trends based on historical patterns
- 🏥 **Clinical-Grade Validation**: Partnerships with mental health professionals for model validation
- 🔐 **Secure Authentication**: User login, encryption, HIPAA compliance
- 📱 **Mobile App**: iOS/Android native applications
- 🎯 **Intervention Recommendations**: Suggest specific coping strategies based on emotion & risk
- 🔄 **Real-Time Streaming**: Process journal entries as they're typed
- 🧩 **Custom Model Fine-Tuning**: Allow users to fine-tune models on their data
- 📤 **Export Integrations**: Direct export to EHR systems, therapist portals

---

## ⚠️ Disclaimer

**MindTrace-AI is an experimental AI system for educational and awareness purposes only.**

- ❌ **Not a medical tool**: Cannot diagnose mental health conditions
- ❌ **Not a replacement for professional help**: Should not replace therapy or clinical assessment
- ⚠️ **Use with caution**: Model predictions are probabilistic and may contain errors
- 🔒 **Privacy**: Do not share sensitive data; process locally when possible
- 📋 **No liability**: Authors not responsible for misuse or adverse outcomes

**If you or someone you know is experiencing a mental health crisis, please contact:**
- **National Suicide Prevention Lifeline (US)**: 988
- **Crisis Text Line**: Text HOME to 741741
- **International Association for Suicide Prevention**: https://www.iasp.info/resources/Crisis_Centres/

---

## 📜 License

This project is released for **educational and research purposes**. See LICENSE file for details.

---

## 🙌 Final Note

MindTrace-AI demonstrates how **explainable AI**, **NLP**, and **interactive visualization** can be combined to create meaningful mental-state awareness tools. The project emphasizes **transparency**, **empathy**, and **user agency** in mental health technology.

---

## 👤 Author

**Lakshman** (@Lakshman2405)

- GitHub: https://github.com/Lakshman2405
- Hugging Face: https://huggingface.co/CoderLakshman

---

**Last Updated**: February 2026
**Version**: 1.0.0

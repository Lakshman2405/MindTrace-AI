# 🧠 MindTrace-AI  
**AI-Powered Mental State Awareness & Emotional Intelligence System**

MindTrace-AI is an end-to-end AI system that analyzes user journal entries to infer emotional patterns, sentiment trends, psychological risk levels, and actionable mental-health insights using modern NLP models and interpretable analytics.

---

## 🚀 Project Overview

MindTrace-AI helps transform unstructured daily journal text into:

- Emotional signals (fear, sadness, joy, optimism, etc.)
- Sentiment progression over time
- Risk score estimation with clear thresholds
- Behavioral pattern & trajectory analysis
- Human-readable AI reflections for self-awareness

The system is designed for **mental awareness**, **early risk detection**, and **explainable AI insights**, not for medical diagnosis.

---

## 🧩 System Architecture

Frontend (Streamlit) 
        ↓ 
Backend API (FastAPI) 
        ↓
Emotion Model (RoBERTa) 
        ↓
Sentiment Model (Transformer) 
        ↓
Pattern & Risk Analysis Engine
        ↓
LLM-based Insight Generator

---

## 🛠️ Tech Stack

### Frontend
- **Streamlit**
- **Plotly / Matplotlib**
- **Pandas / NumPy**

### Backend
- **FastAPI**
- **Pydantic**
- **Uvicorn**

### AI / NLP
- **Hugging Face Transformers**
- **PyTorch**
- **RoBERTa (Emotion Classification)**
- **Transformer-based Sentiment Model**

### Deployment
- **Hugging Face Spaces**
- **Docker**

---

## 📊 Key Features

- 📝 Journal-based emotional analysis
- 🎭 Multi-label emotion inference
- 📈 Sentiment trend visualization
- ⚠️ Risk score computation with explainability
- 🧭 Pattern & trajectory classification
- 🧠 AI-generated reflective insights
- 🗂️ Session history with reload support
- 📥 Structured JSON export

---

## 📂 Repository Structure

```bash
MINDTRACE-AI/
│
├── backend/
│   └── api.py
│
├── frontend/
│   └── app.py
│
├── src/
│   ├── config.py
│   ├── emotion_inference.py
│   ├── sentiment_inference.py
│   ├── pattern_analysis.py
│   └── llm_insights.py
│
├── data/
│   ├── go_emotions/
│   │   ├── train.csv
│   │   ├── validation.csv
│   │   └── test.csv
│   │
│   └── tweet_eval_sentiment/
│       ├── train.csv
│       ├── validation.csv
│       └── test.csv
│
├── notebooks/
│   ├── emotion_model_training.ipynb
│   └── sentiment_model_training.ipynb
│
├── scripts/
│   ├── download_data1.py
│   └── download_data2.py
│
├── tests/
│   ├── test_inference.py
│   ├── test_llm_response.py
│   └── test_pattern.py
│
├── .gitignore
├── README.md
└── requirements.txt
```


---

---

## 🤖 Model Hosting Strategy

Large model files (**.safetensors**) are **not stored in this repository**.

Instead, models are hosted separately on **Hugging Face Model Hub** and loaded dynamically at runtime using their repository IDs.

This keeps the GitHub repository lightweight and deployable.

---

## ⚙️ Configuration

Sensitive values (tokens, secrets) are **not included** in this repository.

Create your own environment variables when running locally or deploying:

```bash
HF_TOKEN=your_huggingface_token
```

## ▶️ Running Locally

### Install dependencies
```bash
pip install -r requirements.txt
```
### Start backend
```bash
uvicorn backend.api:app --reload
```
### Start Frontend
```bash
streamlit run frontend/app.py
```
---
## 🌐 Deployment
The project is designed to be deployed on Hugging Face Spaces using:
- Docker SDK
- Streamlit frontend
- FastAPI backend
Models are pulled directly from Hugging Face during runtime.

---

## ⚠️ Disclaimer
MindTrace-AI is an experimental AI system for educational and awareness purposes only.
It is not a medical or diagnostic tool and should not replace professional mental-health support.

---

## 📌 Future Enhancements
- Multi-language journaling support
- Personalized trend baselines
- Long-term emotional forecasting
- Clinical-grade validation pipelines
- Secure user authentication

---
## 📜 License
This project is released for educational and research purposes.
---
---
## 🙌 Final Note
MindTrace-AI demonstrates how explainable AI, NLP, and interactive visualization can be combined to create meaningful mental-state awareness tools.
----


















































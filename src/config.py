import os
from dotenv import load_dotenv
import torch

# Load .env
load_dotenv()

# =========================
# MODEL PATHS
# =========================

EMOTION_MODEL_PATH = "https://huggingface.co/CoderLakshman/mindtrace-emotion-model"
SENTIMENT_MODEL_PATH = "https://huggingface.co/CoderLakshman/mindtrace-sentiment-model"

# =========================
# THRESHOLDS
# =========================

EMOTION_THRESHOLD = 0.30

# =========================
# DEVICE
# =========================

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# =========================
# HF TOKEN
# =========================

HF_TOKEN = os.getenv("HF_TOKEN")

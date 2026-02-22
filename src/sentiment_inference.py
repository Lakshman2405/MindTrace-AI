import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from src.config import SENTIMENT_MODEL_PATH, DEVICE


tokenizer = AutoTokenizer.from_pretrained(SENTIMENT_MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(
    SENTIMENT_MODEL_PATH
).to(DEVICE)

model.eval()


def predict_sentiment(text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    ).to(DEVICE)

    with torch.no_grad():
        outputs = model(**inputs)

    probs = F.softmax(outputs.logits, dim=1).cpu().numpy()[0]

    predicted_class = probs.argmax()

    label_map = {
        0: "negative",
        1: "neutral",
        2: "positive"
    }

    return {
        "sentiment": label_map[predicted_class],
        "confidence": float(probs[predicted_class])
    }
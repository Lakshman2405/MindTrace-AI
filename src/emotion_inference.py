import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from src.config import EMOTION_MODEL_PATH, DEVICE, EMOTION_THRESHOLD

# Correct GoEmotions Label Order (28 labels)
GO_EMOTIONS_LABELS = [
    "admiration", "amusement", "anger", "annoyance", "approval",
    "caring", "confusion", "curiosity", "desire", "disappointment",
    "disapproval", "disgust", "embarrassment", "excitement",
    "fear", "gratitude", "grief", "joy", "love", "nervousness",
    "optimism", "pride", "realization", "relief",
    "remorse", "sadness", "surprise", "neutral"
]



# Load Model

tokenizer = AutoTokenizer.from_pretrained(EMOTION_MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(
    EMOTION_MODEL_PATH
).to(DEVICE)

model.eval()


# Prediction Function


def predict_emotions(text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    ).to(DEVICE)

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.sigmoid(outputs.logits).cpu().numpy()[0]

    # Map probabilities manually using correct label list
    emotion_scores = {
        GO_EMOTIONS_LABELS[i]: float(probs[i])
        for i in range(len(probs))
    }

    # Filter using threshold
    detected = [
        label for label, score in emotion_scores.items()
        if score >= EMOTION_THRESHOLD
    ]

    # Sort and take top 5
    top_5 = sorted(
        emotion_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    return {
        "detected_emotions": detected,
        "top_5_emotions": top_5
    }
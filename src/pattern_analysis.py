import numpy as np
from src.emotion_inference import predict_emotions
from src.sentiment_inference import predict_sentiment
from sklearn.metrics.pairwise import cosine_similarity


def sentiment_to_score(label):
    mapping = {
        "negative": -1,
        "neutral": 0,
        "positive": 1
    }
    return mapping[label]


def run_models_on_journal(journal_entries):

    results = []

    for entry in journal_entries:
        text = entry["text"]
        date = entry["date"]

        sentiment_result = predict_sentiment(text)
        emotion_result = predict_emotions(text)

        results.append({
            "date": date,
            "sentiment": sentiment_result["sentiment"],
            "sentiment_score": sentiment_to_score(sentiment_result["sentiment"]),
            "emotion_scores": emotion_result["top_5_emotions"]
        })

    return results


# -----------------------------
# PATTERN CLASSIFICATION LAYER
# -----------------------------

def classify_pattern(results):

    sentiment_sequence = [r["sentiment_score"] for r in results]

    if len(sentiment_sequence) < 3:
        return "insufficient_data"

    alternations = sum(
        1 for i in range(1, len(sentiment_sequence))
        if sentiment_sequence[i] != sentiment_sequence[i - 1]
    )

    if alternations >= len(sentiment_sequence) - 1:
        return "alternating_pattern"

    if detect_negative_streak(results) >= 3:
        return "sustained_negative_pattern"

    if sentiment_sequence[-1] == 1 and sentiment_sequence[-2] == -1:
        return "recovery_pattern"

    return "stable_pattern"


def classify_trajectory(trend_slope):

    if trend_slope > 0.1:
        return "improving"
    elif trend_slope < -0.1:
        return "declining"
    else:
        return "stable"


# -----------------------------
# METRICS
# -----------------------------

def compute_sentiment_trend(results):

    sentiment_scores = [r["sentiment_score"] for r in results]

    if len(sentiment_scores) < 2:
        return {
            "trend_slope": 0,
            "moving_average": sentiment_scores
        }

    x = np.arange(len(sentiment_scores))
    y = np.array(sentiment_scores)

    slope = np.polyfit(x, y, 1)[0]

    window = 3
    moving_avg = np.convolve(
        sentiment_scores,
        np.ones(window)/window,
        mode='valid'
    )

    return {
        "trend_slope": float(slope),
        "moving_average": moving_avg.tolist()
    }


def compute_emotional_volatility(results):

    emotion_vectors = []

    for r in results:
        scores = [score for _, score in r["emotion_scores"]]
        emotion_vectors.append(scores)

    emotion_vectors = np.array(emotion_vectors)

    if len(emotion_vectors) < 2:
        return 0.0

    volatility = np.mean(np.std(emotion_vectors, axis=0))

    return float(volatility)


def compute_emotional_diversity(results):

    all_scores = []

    for r in results:
        for _, score in r["emotion_scores"]:
            all_scores.append(score)

    probs = np.array(all_scores)
    probs = probs / np.sum(probs)

    entropy = -np.sum(probs * np.log(probs + 1e-9))

    return float(entropy)


def detect_negative_streak(results):

    max_streak = 0
    current_streak = 0

    for r in results:
        if r["sentiment_score"] == -1:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0

    return max_streak


def current_negative_streak(results):

    streak = 0

    for r in reversed(results):
        if r["sentiment_score"] == -1:
            streak += 1
        else:
            break

    return streak


def compute_behavioral_drift(results):

    if len(results) < 2:
        return 0.0

    emotion_vectors = []

    for r in results:
        scores = [score for _, score in r["emotion_scores"]]
        emotion_vectors.append(scores)

    emotion_vectors = np.array(emotion_vectors)

    drift_values = []

    for i in range(len(emotion_vectors) - 1):
        v1 = emotion_vectors[i].reshape(1, -1)
        v2 = emotion_vectors[i + 1].reshape(1, -1)

        similarity = cosine_similarity(v1, v2)[0][0]
        drift = 1 - similarity
        drift_values.append(drift)

    return float(np.mean(drift_values))


def compute_sentiment_momentum(results, window=3):

    sentiment_scores = [r["sentiment_score"] for r in results]

    if len(sentiment_scores) < window * 2:
        return 0.0

    recent = sentiment_scores[-window:]
    previous = sentiment_scores[-window*2:-window]

    return float(np.mean(recent) - np.mean(previous))


# -----------------------------
# RISK
# -----------------------------

def compute_risk_score(trend_slope,
                       current_streak,
                       negative_tail,
                       volatility,
                       drift,
                       diversity):

    risk = 0
    breakdown = {}

    # Declining trend
    if trend_slope < 0:
        impact = min(abs(trend_slope) * 20, 20)
        breakdown["Declining Trend"] = round(impact, 2)
        risk += impact

    # Current negative streak
    impact = min(current_streak * 8, 25)
    if impact > 0:
        breakdown["Current Negative Streak"] = round(impact, 2)
    risk += impact

    # Negative tail
    impact = min(negative_tail * 5, 20)
    if impact > 0:
        breakdown["Post-Positive Negativity"] = round(impact, 2)
    risk += impact

    # Volatility
    impact = min(volatility * 40, 15)
    if impact > 0:
        breakdown["Emotional Volatility"] = round(impact, 2)
    risk += impact

    # Behavioral drift
    impact = min(drift * 40, 15)
    if impact > 0:
        breakdown["Behavioral Drift"] = round(impact, 2)
    risk += impact

    # Low diversity penalty
    if diversity < 2.0:
        impact = 15
        breakdown["Low Emotional Diversity"] = impact
        risk += impact

    final_score = min(round(risk, 2), 100)

    return final_score, breakdown


def generate_insight(risk_score, trajectory_type, pattern_type):

    if risk_score < 25:
        risk_level = "Low"
    elif risk_score < 50:
        risk_level = "Moderate"
    elif risk_score < 75:
        risk_level = "High"
    else:
        risk_level = "Critical"

    summary = f"The overall emotional trajectory appears {trajectory_type}."
    behavior = f"The observed emotional pattern is classified as {pattern_type}."
    recommendation = "Continued reflective journaling and consistent monitoring are recommended."

    return {
        "risk_level": risk_level,
        "summary": summary,
        "behavior": behavior,
        "recommendation": recommendation
    }


# -----------------------------
# MAIN ANALYSIS
# -----------------------------

def analyze_journal_entries(journal_entries):

    results = run_models_on_journal(journal_entries)

    sentiment_metrics = compute_sentiment_trend(results)
    volatility = compute_emotional_volatility(results)
    diversity = compute_emotional_diversity(results)
    longest_streak = detect_negative_streak(results)
    current_streak = current_negative_streak(results)
    negative_tail = 0
    drift = compute_behavioral_drift(results)
    momentum = compute_sentiment_momentum(results)
    trend_slope = sentiment_metrics["trend_slope"]
    pattern_type = classify_pattern(results)
    trajectory_type = classify_trajectory(sentiment_metrics["trend_slope"])

    risk_score, risk_breakdown = compute_risk_score(
    trend_slope,
    current_streak,
    negative_tail,
    volatility,
    drift,
    diversity
    )



    insight = generate_insight(
        risk_score,
        trajectory_type,
        pattern_type
    )

    return {
        "risk_score": risk_score,
        "risk_breakdown": risk_breakdown,
        "risk_level": insight["risk_level"],
        "pattern_type": pattern_type,
        "trajectory_type": trajectory_type,
        "sentiment_momentum": momentum,
        "emotional_volatility": volatility,
        "behavioral_drift": drift,
        "longest_negative_streak": longest_streak,
        "current_negative_streak": current_streak,
        "structured_insight": {
            "summary": insight["summary"],
            "behavior": insight["behavior"],
            "recommendation": insight["recommendation"]
        },
        "raw_results": results
    }
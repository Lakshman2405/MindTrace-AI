from src.emotion_inference import predict_emotions
from src.sentiment_inference import predict_sentiment

print(predict_sentiment("I am very happy today!"))
print(predict_emotions("I am very happy today!"))
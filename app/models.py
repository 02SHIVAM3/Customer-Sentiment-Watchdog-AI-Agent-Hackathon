import os
from transformers import pipeline

SENTIMENT_DEFAULT = os.getenv("SENTIMENT_MODEL", "distilbert-base-uncased-finetuned-sst-2-english")
EMOTION_DEFAULT = os.getenv("EMOTION_MODEL", "j-hartmann/emotion-english-distilroberta-base")

def load_models():
    sentiment_analyzer = pipeline("sentiment-analysis", model=SENTIMENT_DEFAULT)
    emotion_analyzer = pipeline("text-classification", model=EMOTION_DEFAULT, top_k=None)
    return sentiment_analyzer, emotion_analyzer

import os
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm
from models import load_models
from utils import summarize_negatives
from alert import send_slack_alert

load_dotenv()

THRESHOLD = float(os.getenv("NEGATIVE_SPIKE_THRESHOLD", "0.6"))  # 60% default

def analyze_support_tickets(csv_path: str):
    df = pd.read_csv(csv_path)
    if "message" not in df.columns:
        raise ValueError("CSV must contain a 'message' column")

    sentiment_analyzer, emotion_analyzer = load_models()

    results = []
    print("\n🎯 Ticket Analysis:\n")
    for msg in tqdm(df["message"].tolist(), desc="Analyzing"):
        s = sentiment_analyzer(msg)[0]["label"]
        # emotion model may return list; take the highest score label
        emo_preds = emotion_analyzer(msg)
        if isinstance(emo_preds, list) and len(emo_preds) and isinstance(emo_preds[0], dict):
            # pipeline returned list of dicts (no top_k)
            emotion = max(emo_preds, key=lambda x: x.get("score", 0)).get("label")
        else:
            # pipeline may return list[list[dict]] when top_k=None
            flat = emo_preds[0] if isinstance(emo_preds, list) else emo_preds
            emotion = max(flat, key=lambda x: x.get("score", 0)).get("label")

        results.append((msg, s, emotion))
        print(f"Message: {msg}\n → Sentiment: {s}, Emotion: {emotion}\n")

    summary = summarize_negatives(results)
    neg_ratio = summary["negative_ratio"]
    print(f"\nSummary: negatives={summary['negatives']}/{summary['total']} ({neg_ratio:.0%}), top_emotion={summary['top_emotion']}")

    if neg_ratio >= THRESHOLD:
        blocks = [
            { "type": "section", "text": { "type": "mrkdwn", "text": f"*⚠️ ALERT:* {summary['negatives']}/{summary['total']} messages are negative ({neg_ratio:.0%})." } },
            { "type": "section", "text": { "type": "mrkdwn", "text": f"*Top emotion:* {summary['top_emotion']}" } }
        ]
        send_slack_alert(
            text=f"ALERT: Negative spike detected — {summary['negatives']}/{summary['total']} ({neg_ratio:.0%}), top emotion: {summary['top_emotion']}",
            blocks=blocks
        )
    else:
        print("✅ No major negative spike detected.")

if __name__ == "__main__":
    analyze_support_tickets(os.path.join(os.path.dirname(__file__), "..", "data", "support_tickets.csv"))

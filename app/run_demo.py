import os
import time
import pandas as pd
from dotenv import load_dotenv
from models import load_models
from utils import summarize_negatives
from alert import send_slack_alert

load_dotenv()

THRESHOLD = float(os.getenv("NEGATIVE_SPIKE_THRESHOLD", "0.6"))
WINDOW = int(os.getenv("WINDOW_SIZE", "8"))

def stream_demo(csv_path: str):
    df = pd.read_csv(csv_path)
    msgs = df["message"].tolist()
    sent_model, emo_model = load_models()
    window_results = []

    print("▶️ Starting streaming demo... (Ctrl+C to stop)")
    for i, msg in enumerate(msgs, 1):
        s = sent_model(msg)[0]["label"]
        emo_preds = emo_model(msg)
        if isinstance(emo_preds, list) and len(emo_preds) and isinstance(emo_preds[0], dict):
            emotion = max(emo_preds, key=lambda x: x.get("score", 0)).get("label")
        else:
            flat = emo_preds[0] if isinstance(emo_preds, list) else emo_preds
            emotion = max(flat, key=lambda x: x.get("score", 0)).get("label")

        window_results.append((msg, s, emotion))
        if len(window_results) > WINDOW:
            window_results.pop(0)

        summary = summarize_negatives(window_results)
        print(f"[{i}] {msg} → {s}/{emotion} — neg: {summary['negatives']}/{summary['total']} ({summary['negative_ratio']:.0%})")

        if summary["negative_ratio"] >= THRESHOLD:
            send_slack_alert(
                text=f"ALERT (stream): negative spike {summary['negatives']}/{summary['total']} ({summary['negative_ratio']:.0%}), top emotion: {summary['top_emotion']}"
            )
        time.sleep(1.2)

if __name__ == "__main__":
    stream_demo(os.path.join(os.path.dirname(__file__), "..", "data", "support_tickets.csv"))

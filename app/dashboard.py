import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from models import load_models
from utils import summarize_negatives

load_dotenv()

st.set_page_config(page_title="Customer Sentiment Watchdog", layout="wide")
st.title("🐶 Customer Sentiment Watchdog — Demo Dashboard")

uploaded = st.file_uploader("Upload a CSV of support messages (columns: id, message, [timestamp])", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
else:
    st.caption("Using bundled sample CSV (data/support_tickets.csv)")
    default_path = os.path.join(os.path.dirname(__file__), "..", "data", "support_tickets.csv")
    df = pd.read_csv(default_path)

if "message" not in df.columns:
    st.error("CSV must contain a 'message' column")
    st.stop()

sent_model, emo_model = load_models()

rows = []
with st.spinner("Analyzing messages..."):
    for msg in df["message"].tolist():
        s = sent_model(msg)[0]["label"]
        emo_preds = emo_model(msg)
        if isinstance(emo_preds, list) and len(emo_preds) and isinstance(emo_preds[0], dict):
            emotion = max(emo_preds, key=lambda x: x.get("score", 0)).get("label")
        else:
            flat = emo_preds[0] if isinstance(emo_preds, list) else emo_preds
            emotion = max(flat, key=lambda x: x.get("score", 0)).get("label")
        rows.append({"message": msg, "sentiment": s, "emotion": emotion})

out = pd.DataFrame(rows)
st.subheader("Per-message Analysis")
st.dataframe(out, use_container_width=True)

summary = summarize_negatives([(r["message"], r["sentiment"], r["emotion"]) for _, r in out.iterrows()])
st.subheader("Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total", summary["total"])
col2.metric("Negatives", summary["negatives"])
col3.metric("Negative %", f"{summary['negative_ratio']*100:.0f}%")

st.write("Emotion counts (negatives only):")
st.json(summary["emotion_counts"])

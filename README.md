# 🐶 Customer Sentiment Watchdog (Hackathon-Ready)

AI agent that analyzes support tickets/chats, detects sentiment + emotions, spots negative spikes, and sends real-time Slack alerts.

---

## ✅ What you get
- CLI analyzer (`app/analyze.py`) — one-shot analysis + Slack alert if spike detected
- Streaming demo (`app/run_demo.py`) — simulates live tickets and alerts on spikes
- Streamlit dashboard (`app/dashboard.py`) — upload CSV and visualize results
- Sample dataset in `data/support_tickets.csv`
- Slack webhook integration (optional)

---

## 🧰 Requirements
- Python 3.10+
- Internet (first run downloads HuggingFace models)
- Slack workspace (optional) for webhooks

---

## ⬇️ Setup (One-time)

### 1) Clone / Extract
Unzip the provided archive or copy the folder to your machine.

### 2) Create a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Configure Slack (optional but recommended)
- In Slack, add **Incoming Webhooks** app and create a webhook URL.
- Copy `.env.example` to `.env` and paste your webhook:
```
cp .env.example .env      # macOS/Linux
# or
copy .env.example .env    # Windows PowerShell
```
Edit `.env` and set `SLACK_WEBHOOK=...`

You can also adjust:
- `NEGATIVE_SPIKE_THRESHOLD` (default 0.6)
- `WINDOW_SIZE` for streaming (default 8)
- `SENTIMENT_MODEL`, `EMOTION_MODEL` (defaults provided)

---

## ▶️ Run

### Option A — One-shot analysis
```bash
python app/analyze.py
```
This analyzes `data/support_tickets.csv`. If negatives ≥ 60%, it pushes a Slack alert.

### Option B — Streaming demo
```bash
python app/run_demo.py
```
Simulates incoming messages and alerts on spikes in a rolling window.

### Option C — Streamlit dashboard
```bash
streamlit run app/dashboard.py
```
Open the local URL shown by Streamlit. Upload your CSV or use the bundled sample.

---

## 📁 CSV Format
The analyzer expects at least a `message` column. Sample included:
```csv
id,timestamp,message
1,2025-08-24T09:00:00Z,"I can’t log in to my account"
...
```

---

## 🧪 Customize quickly
- Change thresholds via `.env`
- Swap models by setting `SENTIMENT_MODEL` / `EMOTION_MODEL`
- Replace `data/support_tickets.csv` with your own

---

## ⚠️ Notes
- First run downloads transformer models — allow a few minutes and some disk space.
- If no `SLACK_WEBHOOK` is set, alerts are printed to the console.

Happy hacking! 🚀

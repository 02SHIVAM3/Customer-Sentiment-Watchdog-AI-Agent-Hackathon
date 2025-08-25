import os
import json
import requests

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK","")

def send_slack_alert(text: str, blocks=None):
    if not SLACK_WEBHOOK:
        print("⚠️  SLACK_WEBHOOK not set. Printing alert instead:")
        print(text)
        return
    payload = {"text": text}
    if blocks:
        payload["blocks"] = blocks
    r = requests.post(SLACK_WEBHOOK, data=json.dumps(payload), headers={"Content-Type":"application/json"})
    if r.status_code >= 400:
        print("⚠️ Failed to send Slack alert:", r.status_code, r.text)
    else:
        print("✅ Alert sent to Slack")

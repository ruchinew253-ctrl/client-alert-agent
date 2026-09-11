import requests

STYLE = {
    "High": "🔴",
    "Medium": "🟠",
    "Low": "🟢",
}


def send_to_teams(webhook_url, client_name, assigned_to, sender, analysis):
    if not webhook_url or "PASTE_" in webhook_url:
        print(f"[SKIP] Teams webhook URL set nahi hai for {assigned_to}")
        return False

    urgency = analysis.get("urgency", "Low")
    emoji = STYLE.get(urgency, "🟢")

    text = (
        f"{emoji} **{urgency} Priority Client Alert**\n\n"
        f"**Client:** {client_name}\n"
        f"**Assigned to:** {assigned_to}\n"
        f"**From:** {sender}\n"
        f"**Summary:** {analysis.get('summary', '')}\n"
        f"**Action:** {analysis.get('action', '')}"
    )

    payload = {"text": text}

    try:
        r = requests.post(webhook_url, json=payload, timeout=15)

        print(f"[DEBUG] Status: {r.status_code}")
        print(f"[DEBUG] Response: {r.text[:300]}")

        if r.status_code in (200, 202):
            print(f"[OK] Alert bhej diya -> {assigned_to} ({client_name})")
            return True

        return False

    except Exception as e:
        print("[ERROR] Teams pe bhejte waqt problem:", e)
        return False

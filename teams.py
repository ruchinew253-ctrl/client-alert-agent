import requests
import os
import json


STYLE = {
    "High": {
        "color": "D93025",
        "emoji": "🔴"
    },
    "Medium": {
        "color": "F9AB25",
        "emoji": "🟡"
    },
    "Low": {
        "color": "1E8E3E",
        "emoji": "🟢"
    }
}


def send_to_teams(webhook_url, client_name, assigned_to, sender, analysis):

    if not webhook_url or "PASTE" in webhook_url:
        print(f"[SKIP] Teams webhook URL is not set for {assigned_to}")
        return False

    urgency = analysis.get("urgency", "Low")
    style = STYLE.get(urgency, STYLE["Low"])

    text = (
        f"{style['emoji']} **{urgency} Priority Client Alert**\n\n"
        f"**Client:** {client_name}\n"
        f"**Assigned to:** {assigned_to}\n"
        f"**From:** {sender}\n"
        f"**Summary:** {analysis.get('summary', '')}\n"
        f"**Suggested Action:** {analysis.get('action', '')}"
    )

    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": f"{style['emoji']} {urgency} Priority Client Alert",
                            "weight": "Bolder",
                            "size": "Medium",
                            "wrap": True
                        },
                        {
                            "type": "FactSet",
                            "facts": [
                                {
                                    "title": "Client:",
                                    "value": client_name
                                },
                                {
                                    "title": "Assigned To:",
                                    "value": assigned_to
                                },
                                {
                                    "title": "From:",
                                    "value": sender
                                },
                                {
                                    "title": "Summary:",
                                    "value": analysis.get("summary", "")
                                },
                                {
                                    "title": "Action:",
                                    "value": analysis.get("action", "")
                                }
                            ]
                        }
                    ]
                }
            }
        ],
        "text": text
    }

    try:
        r = requests.post(
            webhook_url,
            json=payload,
            timeout=15
        )

        if r.status_code in (200, 202):
            print(f"[OK] Alert sent -> {assigned_to} ({client_name})")
            return True

        else:
            print(
                f"[ERROR] Teams rejected: "
                f"{r.status_code} {r.text}"
            )
            return False

    except Exception as e:
        print(f"[ERROR] problem while sending teams: {e}")
        return False

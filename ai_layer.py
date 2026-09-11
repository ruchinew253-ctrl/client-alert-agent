# ai_layer.py
# WhatsApp message ko analyse karta hai

import os
import json


URGENT_WORDS = [
    "urgent", "asap", "immediately", "today", "deadline", "eod",
    "by 4", "by 5", "escalation", "escalate", "critical", "complaint",
    "issue", "problem", "approve", "approval", "payment", "invoice",
    "delay", "reminder", "pending", "important",
    "jaldi", "turant", "aaj"
]


ACTION_WORDS = [
    "send", "share", "need", "require", "revise", "update", "review",
    "prepare", "confirm", "schedule", "call", "meeting", "submit",
    "provide", "bhejo", "chahiye", "karo"
]


def keyword_analysis(message_text):
    """
    Agar OpenAI available nahi hai,
    to simple keywords ke basis par message analyse karega.
    """

    text = message_text.lower()

    urgent_matches = [
        word for word in URGENT_WORDS
        if word in text
    ]

    action_matches = [
        word for word in ACTION_WORDS
        if word in text
    ]

    important = bool(urgent_matches or action_matches)

    if urgent_matches:
        urgency = "High"
    elif action_matches:
        urgency = "Medium"
    else:
        urgency = "Low"

    if urgent_matches:
        summary = "Client message contains urgent or important keywords."
    elif action_matches:
        summary = "Client message appears to require an action."
    else:
        summary = "Client message does not appear urgent."

    if urgent_matches:
        action = "Review the message and respond urgently."
    elif action_matches:
        action = "Review the requested action and respond."
    else:
        action = "No immediate action required."

    return {
        "important": important,
        "urgency": urgency,
        "summary": summary,
        "action": action,
    }


def openai_analysis(message_text):
    try:
        from openai import OpenAI

        client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"]
        )

        prompt = (
            "You are a client-communication triage assistant. "
            "Analyse the WhatsApp message below and reply ONLY in valid JSON "
            "with keys: important (true/false), urgency (High/Medium/Low), "
            "summary (max 2 sentences), action (one short suggested action).\n\n"
            f'Message: "{message_text}"'
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
        )

        raw = response.choices[0].message.content.strip()

        raw = raw.replace("```json", "")
        raw = raw.replace("```", "")
        raw = raw.strip()

        return json.loads(raw)

    except Exception as e:
        print("AI failed, using keyword fallback:", e)
        return keyword_analysis(message_text)


def analyze_message(message_text):

    if os.environ.get("OPENAI_API_KEY"):
        return openai_analysis(message_text)

    return keyword_analysis(message_text)
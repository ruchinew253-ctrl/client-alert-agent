import os
import json

URGENT_WORDS = [
    "urgent",
    "asap",
    "immediately",
    "today",
    "deadline",
    "eod",
    "by 4",
    "by 5",
    "escalation",
    "escalate",
    "critical",
    "complaint",
    "issue",
    "problem",
    "approve",
    "approval",
    "payment",
    "invoice",
    "delay",
    "reminder",
    "pending",
    "important",
    "jaldi",
    "turant",
    "aaj",
]

ACTION_WORDS = [
    "send",
    "share",
    "need",
    "require",
    "revise",
    "update",
    "review",
    "prepare",
    "confirm",
    "schedule",
    "call",
    "meeting",
    "submit",
    "provide",
    "bhejo",
    "chahiye",
    "karo",
]


def keyword_analysis(message_text):
    """
    Agar OpenAI available nahi hai,
    to simple keywords ke basis par message analyse karega.
    """

    text = message_text.lower()

    urgent_matches = [
        word
        for word in URGENT_WORDS
        if word in text
    ]

    action_matches = [
        word
        for word in ACTION_WORDS
        if word in text
    ]

    important = bool(
        urgent_matches or action_matches
    )

    if urgent_matches:
        urgency = "High"
    elif action_matches:
        urgency = "Medium"
    else:
        urgency = "Low"

    if urgent_matches:
        summary = (
            "Client message contains urgent or important keywords."
        )
    elif action_matches:
        summary = (
            "Client message appears to require an action."
        )
    else:
        summary = (
            "Client message does not appear urgent."
        )

    if urgent_matches:
        action = (
            "Review the message and respond urgently."
        )
    elif action_matches:
        action = (
            "Review the requested action and respond."
        )
    else:
        action = (
            "No immediate action required."
        )

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
            f"Message: {message_text}"
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
        )

        raw = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        raw = raw.replace(
            "```json",
            ""
        )

        raw = raw.replace(
            "```",
            ""
        )

        raw = raw.strip()

        return json.loads(raw)

    except Exception as e:
        print(
            "AI failed, using keyword fallback:",
            e
        )

        return keyword_analysis(
            message_text
        )


def analyze_message(message_text):

    if os.environ.get(
        "OPENAI_API_KEY"
    ):
        return openai_analysis(
            message_text
        )

    return keyword_analysis(
        message_text
    )

On Thu, 10 Sept 2026, 15:27 Saksham Malhotra, <saksham.m2906@gmail.com> wrote:

---------- Forwarded message ---------
From: Saksham Malhotra <saksham.m2906@gmail.com>
Date: Thu, 10 Sept 2026, 15:24
Subject:
To: ruchinew253@gmail.com <ruchinew253@gmail.com>


# ROUTING TABLE -- kis client ka message kis bande ke Teams pe jayega
# Confidentiality ka logic yahin hai.

ROUTING_TABLE = {

    "919811111111": {
        "client_name": "ABC Holdings",
        "assigned_to": "Saksham",
        "teams_webhook_url": "PASTE_YOUR_TEAMS_WEBHOOK_URL_HERE",
    },

    "919822222222": {
        "client_name": "NRDC",
        "assigned_to": "Malek",
        "teams_webhook_url": "PASTE_MALEK_TEAMS_WEBHOOK_URL_HERE",
    },
}


DEFAULT_ROUTE = {
    "client_name": "Unknown Client",
    "assigned_to": "Admin",
    "teams_webhook_url": "PASTE_ADMIN_TEAMS_WEBHOOK_URL_HERE",
}


def find_route(sender_number):
    return ROUTING_TABLE.get(sender_number, DEFAULT_ROUTE)

# APP.PY -- Main webhook server (poora system ka dil)
# Chalao: python app.py

import os
from flask import Flask, request

from routing import find_route
from ai_layer import analyze_message
from teams import send_to_teams

app = Flask(__name__)

# Meta ke "verify token" box me BILKUL YEHI daalna hai
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "myClientAlert2026")


@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("[OK] Webhook verified by Meta")
        return challenge, 200

    print("[FAIL] Webhook verification failed")
    return "Verification failed", 403


@app.route("/webhook", methods=["POST"])
def receive():
    data = request.get_json()

    try:
        value = data["entry"][0]["changes"][0]["value"]

        if "messages" not in value:
            return "ok", 200

        message = value["messages"][0]
        sender = message["from"]

        if message.get("type") == "text":
            text = message["text"]["body"]
        else:
            text = "[Non-text message: " + message.get("type", "unknown") + "]"

        print("\n--- NAYA MESSAGE ---")
        print("From:", sender)
        print("Text:", text)

        route = find_route(sender)
        print("Client:", route["client_name"], "->", route["assigned_to"])

        analysis = analyze_message(text)
        print("Analysis:", analysis)

        if analysis.get("important"):
            send_to_teams(
                webhook_url=route["teams_webhook_url"],
                client_name=route["client_name"],
                assigned_to=route["assigned_to"],
                sender=sender,
                analysis=analysis,
            )
        else:
            print("[SKIP] Important nahi -- koi alert nahi")

    except Exception as e:
        print("[ERROR] Message process karte waqt:", e)

    return "ok", 200


@app.route("/", methods=["GET"])
def home():
    return "Client Alert Agent is running!", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
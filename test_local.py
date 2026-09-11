import ai_layer
import importlib

importlib.reload(ai_layer)

print("ai_layer loaded successfully")
print("os available:", hasattr(ai_layer, "os"))
print("keyword_analysis available:", hasattr(ai_layer, "keyword_analysis"))

# TEST -- WhatsApp connect karne se pehle laptop pe test
# Chalao: python test_local.py

from routing import find_route
from ai_layer import analyze_message
from teams import send_to_teams


FAKE_SENDER = "918829999999"
FAKE_MESSAGE = "Need the revised proposal urgently by 4 PM today"

print("=== TEST SHURU ===")
print("Sender:", FAKE_SENDER)
print("Message:", FAKE_MESSAGE)
print()

route = find_route(FAKE_SENDER)
print("Routing:", route["client_name"], "->", route["assigned_to"])

analysis = analyze_message(FAKE_MESSAGE)
print("AI result:", analysis)
print()

send_to_teams(
    webhook_url=route["teams_webhook_url"],
    client_name=route["client_name"],
    assigned_to=route["assigned_to"],
    sender=FAKE_SENDER,
    analysis=analysis,
)

print("\n=== TEST KHATAM ===")
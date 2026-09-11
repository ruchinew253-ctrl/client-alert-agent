# ROUTING TABLE -- kis client ka message kis bande ke Teams pe jayega
# Confidentiality ka logic yahin hai.

ROUTING_TABLE = {

    "918595921795": {
        "client_name": "Ruchee",
        "assigned_to": "Saksham Malhotra",
        "teams_webhook_url": "https://defaultf9cac348195d4c77ac88b33b9611e3.d5.environment.api.powerplatform.com:443/powerautomate/automations/direct/cu/16/workflows/1d5565186c124775b0aa1f29f94e2989/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=63XaWUHMLXQdl_SD9X2IEju4j55Zaj_E_uDSgUx1KI",
    },

}


DEFAULT_ROUTE = {
    "client_name": "Ruchee",
    "assigned_to": "Saksham Malhotra",
    "teams_webhook_url": "https://defaultf9cac348195d4c77ac88b33b9611e3.d5.environment.api.powerplatform.com:443/powerautomate/automations/direct/cu/16/workflows/1d5565186c124775b0aa1f29f94e2989/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=63XaWUHMLXQdl_SD9X2IEju4j55Zaj_E_uDSgUx1KI",
}


def find_route(sender_number):
    return ROUTING_TABLE.get(sender_number, DEFAULT_ROUTE)
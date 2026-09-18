# ROUTING TABLE -- kis client ka message kis bande ke Teams pe jayega
# Confidentiality ka logic yahin hai.

ROUTING_TABLE = {

    "918851428184": {
        "client_name": "Ruchee",
        "assigned_to": "Saksham Malhotra",
        "teams_webhook_url": "https://defaultf9cac348195d4c77ac88b33b9611e3.d5.environment.api.powerplatform.com:443/powerautomate/automations/direct/cu/29/workflows/425b03d880c54b9c81c27adebafd934f/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=jQI5SfazQuRvjnoVmx251K17sBt1zWR0XB0mCmAU1I",
    },

}


DEFAULT_ROUTE = {
    "client_name": "Ruchee",
    "assigned_to": "Saksham Malhotra",
    "teams_webhook_url": "https://defaultf9cac348195d4c77ac88b33b9611e3.d5.environment.api.powerplatform.com:443/powerautomate/automations/direct/cu/29/workflows/425b03d880c54b9c81c27adebafd934f/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=jQI5SfazQuRvjnoVmx251K17sBt1zWR0XB0mCmAU1I",
}


def find_route(sender_number):
    return ROUTING_TABLE.get(sender_number, DEFAULT_ROUTE)

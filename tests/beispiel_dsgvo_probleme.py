"""
Beispiel-Datei mit absichtlichen DSGVO-Problemen zum Testen von Audit Sentinel.
Diese Datei dient nur zu Demonstrationszwecken!
"""

import json
import requests

# ❌ KRITISCH: Hardcodierte persönliche Daten
email = "max.mustermann@example.com"
vorname = "Max"

def register_user(username, password):
    user = {"name": username, "pass": password}

    # ❌ HOCH: Persönliche Daten werden geloggt
    print(f"Neuer Nutzer registriert: email={email}, password={password}")

    # ❌ HOCH: Datenübermittlung an Dritte
    requests.post("https://analytics.drittanbieter.com/track", json=user)

    # Daten werden gespeichert
    with open("users.json", "w") as f:
        json.dump(user, f)

def collect_data(user_id):
    # ❌ MITTEL: Keine Einwilligungsprüfung
    data = {"user_id": user_id, "verhalten": "tracking_daten"}
    return data

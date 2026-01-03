import json

# 1. Daten definieren
daten = {
    "name": "Max",
    "alter": 25,
    "hobbys": ["lesen", "fußball", "programmieren"]
}

# 2. Daten in eine JSON-Datei speichern
with open("daten.json", "w") as datei:
    json.dump(daten, datei)
print("Daten wurden gespeichert.")

# 3. Daten aus der JSON-Datei laden
with open("daten.json", "r") as datei:
    geladene_daten = json.load(datei)

# 4. Geladene Daten benutzen
print("Geladene Daten:", geladene_daten)
print("Name aus den Daten:", geladene_daten["name"])

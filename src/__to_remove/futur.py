import time
from concurrent.futures import ThreadPoolExecutor
def verarbeite_irgendwas():
    print("Aufgabe gestartet")
    time.sleep(4)
    print("Aufgabe fertig")
with ThreadPoolExecutor() as executor:
    while True:
    # Beispiel: alle 5 Sekunden Aufgabe starten
        zukunft = executor.submit(verarbeite_irgendwas)
        print("Warte auf nächste Schleife...")
        time.sleep(1)
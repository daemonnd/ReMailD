import time
from concurrent.futures import ProcessPoolExecutor

# Eine einfache Funktion, die eine Zeit lang "arbeitet"
def lange_berechnung(n):
    print(f"Start Berechnung {n}")
    time.sleep(2)  # Simuliert eine langwierige Berechnung
    return f"Ergebnis von Berechnung {n}"

# Main-Funktion, die ProcessPoolExecutor verwendet
def main():
    with ProcessPoolExecutor() as executor:
        # Wir starten mehrere Prozesse gleichzeitig
        ergebnisse = executor.map(lange_berechnung, [1, 2, 3, 4, 5])
    
    # Ergebnisse ausgeben
    for ergebnis in ergebnisse:
        print(ergebnis)

if __name__ == "__main__":
    main()
import time
from concurrent.futures import ProcessPoolExecutor

# Funktion 1: Eine einfache Berechnung
def berechnung1(n):
    print(f"Starte Berechnung 1 mit {n}")
    time.sleep(3)  # Simuliere eine langwierige Berechnung
    return f"Berechnung 1 abgeschlossen mit Ergebnis {n}"

# Funktion 2: Eine andere Berechnung oder Aufgabe
def berechnung2(n):
    print(f"Starte Berechnung 2 mit {n}")
    time.sleep(2)  # Eine kürzere Berechnung, nur zum Vergleich
    return f"Berechnung 2 abgeschlossen mit Ergebnis {n}"

def main():
    with ProcessPoolExecutor() as executor:
        # Wir starten beide Funktionen parallel
        ergebnisse = executor.map(lambda n: (berechnung1(n), berechnung2(n)), [1, 2, 3, 4, 5])
        
    # Ergebnisse ausgeben
    for ergebnis in ergebnisse:
        # Ergebnis ist ein Tupel: (Ergebnis von berechnung1, Ergebnis von berechnung2)
        print(ergebnis)

if __name__ == "__main__":
    main()

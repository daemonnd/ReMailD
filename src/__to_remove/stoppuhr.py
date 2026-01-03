import time

start = time.perf_counter()  # Stoppuhr starten

# Beispiel: Code block, dessen Laufzeit du messen willst
time.sleep(1)

ende = time.perf_counter()   # Stoppuhr stoppen

print(f"Laufzeit: {ende - start:.5f} Sekunden")
print(time.asctime())
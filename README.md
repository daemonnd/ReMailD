ReMailD
==========
python:                                               main file:
sudo /home/alain/Documents/ReMailD/.venv/bin/python -m ReMailD.src.main

Exit codes:
0 - Success
1 - Basic Errors
2 - ReMailD Errors (like all account ids are taken), or that a value in a .json is incorrect.

1. Programm Overview
-------------------
ReMailD ist ein CLI-basiertes Python-Programm, das automatisch auf E-Mails antwortet.  
Es bietet Filterfunktionen, um auszuwählen, auf welche E-Mails geantwortet wird, und unterstützt sowohl feste als auch KI-basierte Antwortmodi.  
Der Ursprungsgedanke war, während Beschäftigung automatische E-Mail-Antworten zu ermöglichen.

2. Installation
---------------
- Python wird benötigt (Version: egal, sollte aber Python 3.x sein)  
- Installiere alle Abhängigkeiten mit:  
  `pip install -r requirements.txt`  
- [Wie man das Programm herunterlädt oder bekommt]  

3. Usage / Ausführung
--------------------
- Starte das Programm mit:  
  `python mail.py [--mode MODUS] [--einstellung WERT]`  
- Die Argumente `--mode` und `--[einstellung]` sind optional und steuern das Verhalten.  
- Ohne Argumente startet das Programm im interaktiven CLI-Modus.  
- Alle Eingaben erfolgen im Terminal, es gibt keine GUI.

4. Initialisierung und Konfiguration
-----------------------------------
- Beim ersten Start erkennt das Programm automatisch, ob es initialisiert ist.  
- Falls nicht initialisiert, wird der Nutzer durch eine Abfrage geführt:  
  - E-Mail-Adresse  
  - Passwort (verschlüsselt gespeichert)  
  - IMAP- und SMTP-Server-Adressen (werden vorgeschlagen, basierend auf der Domain)  
  - Ports (Standardwerte automatisch gesetzt, können angepasst werden)  
  - Filter für E-Mails, auf die geantwortet werden soll  
  - Antwortmodus (manuell oder KI)  
  - Zeitintervall für regelmäßige E-Mail-Prüfungen (Autovervollständigung mit Tab möglich)  
- Alle Daten werden im Verzeichnis `JsonFiles` als `.json`-Dateien gespeichert.  
- Die JSON-Dateien sind schreibgeschützt und versteckt (wenn das Betriebssystem das unterstützt).

5. Hauptfunktionen
------------------
- Automatische Antwort auf eingehende E-Mails basierend auf konfigurierten Filtern.  
- Nutzung von `imaplib` zum Abrufen von E-Mails und `smtplib` zum Senden von Antworten.  
- Unterstützung von festen Antworten und KI-generierten Antworten.  
- Eingaben und CLI werden mit `prompt_toolkit` realisiert (inkl. Autovervollständigung).  
- Kommandozeilenargumente werden mit `argparse` und `argcomplete` unterstützt und ergänzt.  
- Passwortverschlüsselung mit `cryptography.Fernet` zum Schutz sensibler Daten.  
- Umfangreiches Logging über Konsole und Logdatei (`ReMailD.log`).

6. Sicherheit
-------------
- Sensible Daten wie Passwörter werden verschlüsselt gespeichert (Fernet).  
- JSON-Dateien werden schreibgeschützt und versteckt abgelegt.  
- [Weitere Sicherheitshinweise?]  
- Keine Übertragung unverschlüsselter Passwörter ins Internet.  
- Keine Weitergabe der Datenm die Daten bleiben privat, nicht einaml ReMailD kennt sie.

7. Fehlerbehandlung und Logging
-------------------------------
- Fehler bei Login, Netzwerkproblemen, ungültigen Eingaben werden erkannt und geloggt.  
- Logs werden in der Datei `ReMailD.log` und in der Konsole ausgegeben.  
- Try-Except-Blöcke fangen typische Fehlerfälle ab und geben verständliche Meldungen.

8. Erweiterungen und Skripte
----------------------------
- Derzeit keine externen Bash-Skripte integriert.  
- Mögliche zukünftige Nutzung von Bash-Skripten zur Erweiterung von Funktionen.  
- Anpassungen sind hauptsächlich über Kommandozeilenargumente und Konfigurationsdateien möglich.

9. FAQ / Troubleshooting
------------------------
- Häufige Fehler werden über Logs erfasst.  
- Fehler wie falsche Login-Daten oder Serverprobleme führen zu entsprechenden Warnungen.  
- [Noch keine umfangreiche FAQ, Logging und Fehlerbehandlung bisher ausreichend.]

---

Kontakt und Support
-------------------
Erstellt von: 
v01DaemonD
Email: 

---




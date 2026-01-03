import imaplib
import time

imap_server = "imap.gmx.net"
email_address = "robert.dubois@gmx.de"  # Ersetze durch deine E-Mail
password = "W_y3}d9Lc;)#-B7"                   # Ersetze durch dein Passwort


try:
    while True:
        # Neue Verbindung pro Schleifendurchlauf 
        imap = imaplib.IMAP4_SSL(imap_server, 993)
        imap.login(email_address, password)
        imap.select("INBOX")

        status, messages = imap.search(None, "UNSEEN")
        unseen_emails = messages[0].split()  # Liste von IDs

        if unseen_emails:
            print(f"{len(unseen_emails)} neue E-Mail(s) angekommen!")

        imap.logout()  # Wichtig: saubere Abmeldung

        user_input = input("Gib 'break' ein zum Beenden, sonst Enter...\n")
        if user_input.strip().lower() == "break":
            break

        time.sleep(5)

except imaplib.IMAP4.error as e:
    print(f"IMAP Fehler: {e}")
except Exception as e:
    print(f"Fehler: {e}")

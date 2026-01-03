# Datei, um die Autovervollständigungen für die Emailkonfiguration zu definieren
# module importieren
from prompt_toolkit.completion import WordCompleter
from pathlib import Path
from typing import Any

from . . . utils import errorprotocol
from . . . utils.json_editor import JsonFile
from . . . utils.launch_reader import launch_data

log = errorprotocol.logger()

# email wordcompleter
emaiDomainCompleter: WordCompleter = WordCompleter([
    "@gmail.com",
    "@gmx.net",
    "@outlook.com",
    "@yahoo.com",
    "@web.de",
    "@hotmail.com",
    "@mail.com",
    "@icloud.com"
])

# Autovervollständigungsfunktionen
"""
Auto completing functions
==============================
Diese suchen:
je nach Emaildomain,
die passenden imap und smtp server (nur für
bekannte domains). Wenn sich die Domain nicht 
in der liste befindet, wird das häufigste Muster
auf die unbekannte Domain angewandt.
"""    



def get_completions(provider: str) -> dict:
    provider_reader: JsonFile = JsonFile(full_path=Path(__file__).parent / "email_providers.json")

    try:
        return provider_reader.get(key=[f"{provider}"]) # if the provider is in the dict
    except:
        return {
            "imap_host": f"imap.{provider}",
            "imap_port": 993,
            "imap_security": "SSL/TLS",
            "smtp_host": f"smtp.{provider}",
            "smtp_port": 587,
            "smtp_security": "TLS"
        }
    
def autofill_acc_name() -> list:
    return ["work", "private", "business"]

def get_acc_save_path() -> Path:
    return Path.home()

    
   
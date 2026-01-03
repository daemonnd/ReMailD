"""
Initialisierungsdatei für das erste Ausführen. Diese Datei 
enthält Funktionen, um die Datei zu initialisieren, die Funktion
init gibt True zurück, wenn das Programm vollständig initialisiert wurde.
Diese Datei wir aber auch zum Reset genutzt, da alle Date den Programms,
die schon vorhanden waren, überschrieben werden.
"""
# Module importieren


import json
import email
import email.header
import time
import imaplib
import smtplib
from email.message import EmailMessage
import ssl
import imaplib
import smtplib
from smtplib import SMTP_SSL, SMTPException, SMTP
import socket
import ssl
import sys
import time
from .to_remove import filters
from cryptography.fernet import Fernet
import os
import json
import datetime
from .utils import errorprotocol
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import ProgressBar
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.auto_suggest import AutoSuggest
from prompt_toolkit.buffer import Buffer
from .to_remove import app_security
from .app_security import ssl_context
import datetime

from ..auth import base_session
from ..auth.base_session import BaseSession
from ..auth import configSession




# instanzen der Klassen definieren
log = errorprotocol.logger()

# Keybindingsinstanz für promt_toolkit erstellen
bindings = KeyBindings()

# Bei Ctrl+D wird die Eingabe beendet
@bindings.add('c-d') # Shortcut zur instanz der Klasse hinzufügen
def exit_on_ctrl_d(event): # Funktion, die Ausgeführt wird, wenn der Shortcut gedrückt wird
    event.app.exit() # Eingabe beenden

# Promptsession erstellen, zu der der Keybind hinzugefügt wird
session: PromptSession = PromptSession(multiline=True, key_bindings=bindings, enable_history_search=True) 




# ask-Funktionien definieren
class user_data:

    """
    Jede ask_ Funktion fragt den User nach einer Sache (z.B. Email, Passwort, ...)
    Mithilfe von prompt_toolkit s  Validator wird geprüft, ob die Eingabe richtig sein könnte, offensichtlich falsches
    kann nicht eingegeben werden. Manche der Funktionen enthalten auch eine WordCompleter, der durch das drücken von
    'tab' Vorschläge macht.
    Am Ende wird das, wonach gefragt wurde, zurückgegeben.
    """
  

    """
    Funktionen, um die Filtereinstellungen abzufragen. Diese werden später
    einmal für die whitelist und einmal für die blacklist abgefragt.
    Die is-, Before-, und After-Filterfunktionen fragen nur die Filter selbst 
    und das Gewicht ab (welches genau so verwendet wird, wie es abgefragt wird,
    es wird nicht wie bei den in-Filtern multipliziert)
    Die in-Filterfunktionen fragen dasselbe wie die anderen ab, aber noch 
    einen zusätzliichen usermum-Wert, der bestimmt, ob der Filter genutzt wird oder nicht.
    """
    
    def ask_isSubject(self) -> list[list, int]:
        isSubject: filters.handle_filters = filters.handle_filters()
        isSubject_value: list = isSubject.create_filters(msg="Enter the absolute Subjects to which ReMailD should answer: ", 
                                                help="This criteria will only be used, if the subject is 1:1 the email subject.")
        isSubject_weight: int = isSubject.create_filter_weight(name="isSubject")
        return isSubject_value, isSubject_weight

    def ask_inSubject(self) -> list[list, int, int]:
        inSubject: filters.handle_filters = filters.handle_filters()
        inSubject_value: list = inSubject.create_filters(msg="Enter key words that should be in the Subjects to which ReMailD should answer: ",         
                                                        help="for example 'Support', 'ReMailD'")
        inSubject_weight: int = inSubject.create_filter_weight(name="inSubject")
        return inSubject_value, inSubject_weight

    def ask_isFrom(self) -> list[list, int, int]:
        isFrom: filters.handle_filters = filters.handle_filters()
        isFrom_value: list = isFrom.create_filters(
            msg="Enter the Emailadresses to which ReMailD should answer: ",
            help="Type in full email adresses, eg. 'example@gmail.com'"
        )
        isFrom_weight: int = isFrom.create_filter_weight(name="isFrom")
        return isFrom_value, isFrom_weight

    def ask_inFrom(self) -> list[list, int, int]:
        inFrom: filters.handle_filters = filters.handle_filters()
        inFrom_value: list = inFrom.create_filters(msg="Enter the parts of email adresses to which ReMailD should answer: ",
                                                    help="Enter domain of your company for example, like '@mycompany.com'.")
        inFrom_weight: int = inFrom.create_filter_weight(name="inFrom")
        return inFrom_value, inFrom_weight

    def ask_isText(self) -> list[list, int]:
        isText: filters.handle_filters = filters.handle_filters()
        isText_value: list = isText.create_filters(msg="Enter the exact text the email have to inclue (not recommended): ",
                                                help="Not recommended, because it is is very unprobably that the text you enter will be 1:1 the email text.")
        isText_weight = isText.create_filter_weight(name="isText")
        return isText_value, isText_weight

    def ask_inText(self) -> list[list, int]:
        inText: filters.handle_filters = filters.handle_filters()
        inText_value: list = inText.create_filters(msg="Enter the key words that should be included in the email: ",
                                                    help="")
        inText_weight: int = inText.create_filter_weight(name="inText")
        return inText_value, inText_weight

    def ask_arriveBefore(self) -> list[datetime.datetime, int]:
        arriveBefore: filters.handle_filters = filters.handle_filters()
        arriveBefore_value: list = arriveBefore.create_filters(msg="Enter when the before what datetime the email should come: ",
                                                            help="Use this input format: year, month, day, hour, minute, second.")
        arriveBefore_weight: int = arriveBefore.create_filter_weight(name="arriveBefore")
        return arriveBefore_value, arriveBefore_weight

    def ask_arriveAfter(self) -> list[datetime.datetime, int]:
        arriveAfter: filters.handle_filters = filters.handle_filters()
        arriveAfter_value: list = arriveAfter.create_filters(msg="Enter when after what datetime the email should arrive: ",
                                                            help="Use this input format: year, month, day, hour, minute, second.")
        arriveAfter_weight: int = arriveAfter.create_filter_weight(name="arriveAfter")
        return arriveAfter_value, arriveAfter_weight

    def ask_whitelist_filters(self) -> dict:
        print("\nNow, you have to choose to which emails ReMailD should answer")

        """
        Listenformat:
        (liste: die Filter-Werte [str], int: das Gewicht des Filters, int: der absolute usermum Wert des Filters (nur bei in-Filtern))
        """
    
        
        print()
        whitelist_dict: dict[list[list, datetime.datetime, int, int]] = {
            "isSubject": self.ask_isSubject,
            "isFrom": self.ask_isFrom,
            "isText": self.ask_isText,
            "arriveBefore": self.ask_arriveBefore,
            "arriveAfter": self.ask_arriveAfter,

            "inSubject": self.ask_inSubject,
            "inFrom": self.ask_inFrom,
            "inText": self.ask_inText,
           
        }
        print(whitelist_dict)
        return whitelist_dict

    def ask_ai_answer_mode(self) -> bool:
        ai_mode: str = prompt("Do you want to use an automatic ai answer for your emails? (y/n): ", validator=vali.ynValidator())
        match ai_mode:            
            case "y" | "Y":
                return True
            case "n" | "N":
                try:
                    DefaultAnswer: str = session.prompt("Enter the answer that will be send to each email\n you want to asnwer: ", multiline=True,
                                                        bottom_toolbar="Press 'Ctrl+D' to quit the input.")
                    return False
                except EOFError:
                    return False
        return False

    def ask_refresh_time_delay(self) -> int:
        delay_options: WordCompleter = WordCompleter("5" "3" "7" "10")

        time_delay: str = prompt("Select the time delay for refreshing when checking for incoming emails (in minutes): ",
                                completer=delay_options, validator=vali.PositiveIntValidator(), 
                                bottom_toolbar="""The time delay for refereshing for in incoming email. After thist amount of minutes, the email ccount will be refreshed. We recommend to use 5 minutes. 
    If the time delay is longer, it the program may answer later. If the time delay is shorter, the answers may be faster, but it decreases the performace.""")
        if time_delay.isdigit():
            return (int(time_delay)*60)
        else:
            log.log_error("The time delay has been set to 5 minutes due to an unknown error.")
            return 300

asker: user_data = user_data()
# Die Initialisierungsfunktion
def BasicInit() -> bool:
    # Main & Recovery Emailadresse kofigurieren
    emails_config: configSession = configSession()
    emails_config.run()
   

    # type: ignore
    return True
def ConfigInit() -> bool:
    ai_mode: bool = asker.ask_ai_answer_mode()
    refresh_time_delay: int = asker.ask_refresh_time_delay()   
    return False
def detail_check() -> bool:
    return False




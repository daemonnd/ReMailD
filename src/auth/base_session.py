"""
BaseSession
===========
This file contains the class `BaseSession`,
which is the parent class for PromptSessions
of the module prompt_toolkit.
"""
import prompt_toolkit
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import ProgressBar
from prompt_toolkit.completion import WordCompleter
import prompt_toolkit.styles
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.auto_suggest import AutoSuggest

from pathlib import Path
from typing import Union

from ..utils import errorprotocol
log = errorprotocol.logger()



class BaseSession:
    """
    Parent class of all the prompt sessions of the module prompt_toolkit.

    Methods:
    -------
        run():
            Basic run, asking all the data for one category, with ask_user_input(), validates the results with validate() and saves the result with save_result()
    """
    def __init__(self):
       self.result: dict = {} 
    def run(self) -> dict:
        """
        Main auth method, asks the user for input, valdates it fully and return the full data.
        Needs child classes for self.ask_user_input() which should return the data and validate() that returns a bool if everything is correct.
        """
        while True:
            try: 
                self.result: dict = self.ask_user_input() 
            except Exception as e:
                log.log_error(f"Exception Error with asking for inputs: {e}. If this error happens to many times, please contact the creator of remaild.")
            if self.result:
                try:
                    self.isCorrect = self.validate()
                except Exception as e:
                    log.log_error(f"Exception Error with validating inputs: {e}")
                    
                if self.isCorrect == True:
                    return self.result
                else:
                    log.log_error("Is seems the data you entered isn't correct. Please retry.\n")
    def ask_user_input(self) -> dict[str]:
        """
        Method for asking the user all the data of one category.
        """
        raise NotImplementedError("The function 'ask_user_input()' have to be overwritten by a child class.")
    def validate(self) -> bool:
        """
        Method for deeper validating. (Tries the user input)
        """
        raise NotImplementedError("The function 'ask_user_input()' have to be overwritten by a child class.")
    def save_result(self, file: Path) -> None:
        with open(file=file):
            pass




        

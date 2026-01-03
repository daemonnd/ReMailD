# importing the modules
from prompt_toolkit import PromptSession, prompt
import getpass
from rich import print
from typing import Any

# importing the files
from . import prompts, validators, completers
from . . . . utils.errorprotocol import logger
from . . . . utils.launch_reader import launch_data
from . . . . auth.base.validators import PositiveIntValidator
from . . . . auth.base_session import BaseSession

log = logger()

class SecuritySession:
    def __init__(self):
        # init prompts
        self.prompts: dict = prompts.SECURITY_PROMPTS[f"{launch_data.lang}"] # type: ignore 
        self.help: dict = prompts.SECURITY_HELP[f"{launch_data.lang}"]

        # init prompt sessions
        self.two_fa_session: PromptSession = PromptSession(
            validator=PositiveIntValidator(limit=-1, zero=False),
            validate_while_typing=False,
            bottom_toolbar=self.help["2FA"]
        ) # type: ignor

    def ask_master(self) -> str:
        while True:
            self.master: str = getpass.getpass(prompt=self.prompts["master"])
            if " " in self.master:
                print("[red]ReMailD master passwords can't contain spaces.[/red]\n")
            elif self.master.replace(" ", "") == "":
                print("[red]This field can't be empty.[/red]\n")
            else:
                break
        return self.master
    
    def ask_2FA(self) -> int:
        self.two_fa: int = int(self.two_fa_session.prompt(
            message=self.prompts["2FA"])
        )
        return self.two_fa
    
   
if __name__ == "__main__":
    ss = SecuritySession()
    mastr = ss.ask_user_input()


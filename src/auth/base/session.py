# importing the modules
from prompt_toolkit import PromptSession, prompt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import FuzzyCompleter, WordCompleter
from pathlib import Path

# importing the files
from ...utils.errorprotocol import logger
from ...utils.launch_reader import LaunchData
from . . base_session import BaseSession
from . import  validators


class BasicSession(BaseSession):
    """
    BasicSession
    ============
    Class for asking the user general things.
    It was made to avoid having for example in each prompt session class a yn session.
    This class contains positive int session, yn session.
    """
    def __init__(self):
        """
        Defining all the Sessions to use them easily later
        """
        super().__init__()

        # define the sessions
        # yn session
        self.yn_session: PromptSession = PromptSession(
            validate_while_typing=False,
            validator=validators.ynValidator(),
            mouse_support=True,
        )
        # pos int session
        self.pos_int_session: PromptSession = PromptSession(
            validate_while_typing=False,
        )
    def ask_yes_no(self, msg: str) -> bool:
        self.yn_answer: str = self.yn_session.prompt(
            message=f"{msg} (y/n): "
        )
        match self.yn_answer:
            case "y":
                self.yn_answer: bool = True
                return True
            case "n":
                self.yn_answer: bool = False
                return False
            case _:
                raise ValueError(f"The result of a yn question can't be {self.yn_answer}. It have to be 'y' for yes or 'n' for no")
    def ask_positive_int(self, msg: str, limit: int) -> int:
        self.pos_int_answer: str = self.pos_int_session.prompt(
            message=msg,
            validator=validators.PositiveIntValidator(limit=limit)
        )
        self.pos_int_answer = int(self.pos_int_answer)
        return int(self.pos_int_answer)
    
    def ask_existing_path(self, msg: str, bottom_toolbar: str = "") -> Path:
        self.existing_path: Path = Path(prompt(
            message=msg,
            validate_while_typing=False,
            validator=validators.PathValidator(),
            bottom_toolbar=bottom_toolbar,
            auto_suggest=AutoSuggestFromHistory()
        ))
        return self.existing_path
    
    def require_specific_answer(self, msg: str, only_include: list, bottom_toolbar: str = "") -> str:
        self.specific: str = prompt(
            message=msg,
            bottom_toolbar=bottom_toolbar,
            validator=validators.SpecificValidator(only_include=only_include),
            validate_while_typing=False,
            completer=FuzzyCompleter(completer=WordCompleter(only_include))
        )
        return self.specific
    

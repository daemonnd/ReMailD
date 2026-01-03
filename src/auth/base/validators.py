from pathlib import Path
from prompt_toolkit.validation import ValidationError, Validator
import prompt_toolkit

class PositiveIntValidator(Validator):
    def __init__(self, limit: int, zero: bool = True):
        self.limit: int = limit
        self.zero: bool = zero
        super().__init__()

    def validate(self, document):
        text = document.text.strip()
        if not text.isdigit():
            raise ValidationError(message="Only integers are allowed.")

        if int(text) < 0:
            raise ValidationError(message="The integer must be greater than 0.")
        if self.zero == False:
            if int(text) == 0:
                raise ValidationError(message="In this case, entering a zero is not allowed.")

        if int(text) < self.limit:
            raise ValidationError(message=f"The integer have to be tinier than {self.limit}")


class ynValidator(Validator):
    def validate(self, document):
        text = document.text
        if text not in ["y", "n"]:
            raise ValidationError(message="Enter 'y' for yes or 'n' for no.")

class PathValidator(Validator):
    def validate(self, document):
        text: str = document.text # type: ignore
        if not Path(text).exists():
            raise ValidationError(message=f"The path {text} does not exist.", cursor_position=999)

class SpecificValidator(Validator):
    def __init__(self, only_include: list):
        super().__init__()
        self.only_include: list = only_include
    def validate(self, document):
        text: str = document.text # type: ignore
        if text not in self.only_include:
            raise ValidationError(message=f"Only one of these inputs is allowed: {self.only_include}.", cursor_position=999)

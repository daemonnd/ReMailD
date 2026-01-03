# importing the modules
from prompt_toolkit.validation import ValidationError, Validator
from pathlib import Path
from zxcvbn import zxcvbn
from rich import print
from rich.progress import Progress
import pwnedpasswords
import grapheme
import password_strength

# importing the files
from . . json_editor import JsonFile
from . . launch_reader import launch_data
from ...accounts.mini import account_utils
from . . other import unique_list


# creating validation classes
class PathValidator(Validator):
    def validate(self, document):
        text = document.text
        text = Path(text)
        if not Path(text).exists():
            raise ValidationError(cursor_position=999999, message="The path you entered does not exist. At this input, the folder is asked where you want to save the account, not the full path.")
        if Path(text).is_file():
            raise ValidationError(cursor_position=999999, message="The path you entered leads to a file. It have to be a folder.")


class NameValidator(Validator):
    def __init__(self):
        super().__init__()
        self.acc_path_file: JsonFile = JsonFile(full_path=Path(launch_data.folder / "src" / "accounts" / "accountPaths.json")).read() # type: ignore

    def validate(self, document):
        text = document.text
        if text == "":
            raise ValidationError(message="Your new account can't be named with ''.")
        if " " in text:
            raise ValidationError(message="'Space' is not allowed in account names.", cursor_position=99999)
        if text == "*":
            raise ValidationError(cursor_position=2, message="The name '*' is not allowed.")
        if text.strip() == "":
            raise ValidationError(message="The account name can't be ''.", cursor_position=999999)
        if "/" in text:
            raise ValidationError(message="The signs '/' and '\' are not allowed in account names.", cursor_position=999999999)
        for path in self.acc_path_file:
            # checking for each entry if the name matches the text
            if account_utils.get_name_from_path(str(self.acc_path_file[f"{path}"])) == text:
                raise ValidationError(message=f"The name {text} is already exists. Please choose a different one.", cursor_position=9999999)


class EmailValidator(Validator):
    def validate(self, document):
        text = document.text
        if not "@" in text:
            raise ValidationError(message="Your Email should contain a '@'", cursor_position=9999999)
        if not "." in text:
            raise ValidationError(message="Your Email should contain a '.'", cursor_position=9999999)
        #if not text.endswith((".net", ".de", ".com", ".us", ".fr")):
         #   raise ValidationError(message="Your Email doesn't have a correct ending", cursor_position=999999)
        if text.startswith("@"):
            raise ValidationError(message="Your Email can't begin with a '@'.", cursor_position=99999999)

class PortValidator(Validator):
    def validate(self, document):
        text: str = document.text # type: ignore
        if not text.isdigit():
            raise ValidationError(message="The port have to be an integer.", cursor_position=9999999)
        if text.isdigit():
            digit = int(text)
            if digit <= 0 or digit >= 65535:
                raise ValidationError(message="The port number have to be between 0 and 65535.", cursor_position=9999999)

class PasswordRepeatValidator(Validator):
    def __init__(self, password):
        super().__init__()
        self.password = password

    def validate(self, document):
        text: str = document.text # type: ignore
        if text != self.password:
            raise ValidationError(message="The password repeating doesn't match the password.", cursor_position=9999999)
class ynValidator(Validator):
    def validate(self, document):
        text: str = document.text # type: ignore
        if text not in ("y", "Y", "n", "N"):
            raise ValidationError(message="Answer with 'y' (yes) or 'n' (no)", cursor_position=99999999)


class PasswordValidator(Validator):
    def __init__(self):
        super().__init__()
        self.current_suggestions: list = [] # type: ignore
        self.visible: bool = True # type: ignore
        self.password_policy: password_strength.PasswordPolicy = password_strength.PasswordPolicy().from_names(
            length=15,
            uppercase=2,
            numbers=2,
            special=2,
            strength=0.70,
            repetition=3
        ) # type: ignor

    def validate(self, document):
        text: str = document.text # type: ignore
        if text:
            validator = zxcvbn(password=text, max_length=999)
            self.current_suggestions: list = validator['feedback'].get('suggestions', []) # type: ignore
            # own validations
            if " " in text:
                raise ValidationError(cursor_position=999, message="The password can't contain spaces")
            if not any(c.isupper() for c in text):
                raise ValidationError(cursor_position=999, message="The password have to include UPPERCASE letters")
            if not any(c.islower() for c in text):
                raise ValidationError(cursor_position=999, message="The password have to include lowercase letters")
            if not any(c.isdigit() for c in text):
                raise ValidationError(cursor_position=999, message="The password have to include numbers")
            if not any(not c.isalnum() and not c.isspace() for c in text):
                raise ValidationError(cursor_position=999, message="The password have to include symbol$")
            if text not in [""]:
                pass
            if len(set(text)) < 4:
                raise ValidationError(cursor_position=999, message=f"{len(set(text))}")
            if grapheme.length(text) < 15:
                raise ValidationError(cursor_position=999, message=f"The password needs at least 15 characters.")
            if grapheme.length(text) == 999:
                raise ValidationError("More than 999 characters are not allowed. Press ctrl+backspace.")
            
            # zxcvbn
            if validator["feedback"]["warning"]:
                raise ValidationError(cursor_position=999, message=f"Password not enough secure: {validator['feedback']['warning']}")
            if validator["score"] < 3:
                raise ValidationError(cursor_position=999, message=f"Password security score too low: {validator['score']*25}% of 100%")
            if validator["score"] == 3:
                self.current_suggestions.append("Password ok, but a stronger one is highly recommended.")
            # pwnedpasswords
            if len(text) > 10:

                try:
                    breaches: int = pwnedpasswords.pwnedpasswords.check(password=text, plain_text=False, anonymous=True) # type: ignore
                    if breaches != 0:
                        raise ValidationError(cursor_position=999, message=f"The password have been leaked {breaches} times!")

                except pwnedpasswords.exceptions.urllib.error.URLError as e:
                    raise ValidationError(cursor_position=999, message=f"URLError while trying to access api of https://haveibeenpwned.com/: {e}. If you believe that this error is fixed, please continue typing.")
                except pwnedpasswords.exceptions.BadRequest as e:
                    raise ValidationError(cursor_position=999, message=f"BadRequest Error while trying to access api of https://haveibeenpwned.com/: {e}. \nIf you believe that this error is fixed, please continue typing.")
                except pwnedpasswords.exceptions.NoUserAgent as e:
                    raise ValidationError(cursor_position=999, message=f"NoUserAgent Error while trying to access api of https://haveibeenpwned.com/: {e}. \nIf you believe that this error is fixed, please continue typing.")
                except pwnedpasswords.exceptions.PasswordNotFound as e:
                    raise ValidationError(cursor_position=999, message=f"PasswordNotFound Error while trying to access api of https://haveibeenpwned.com/: {e}. \nIf you believe that this error is fixed, please continue typing.")
        else:
            raise ValidationError(message="Your password can't be ''.")

    def set_visibility(self, visible: bool = False) -> None:
        """
        Setting the visibility to visible or not (show * instead of characters)
        """
        #print(f"[SET] visible = {visible}")
        self.visible = visible
    def get_visibility(self) -> bool:
        """
        Getting the visibility to use it for parameter is_password.
        """
        #print(f"[GET] is_password = {self.visible}")
        return self.visible

def get_toolbar(validator_instance: PasswordValidator) -> str:
    """
    Func for getting the live suggestions in the bottom toolbar of the password input.
    """
    suggestions = validator_instance.current_suggestions
    if not suggestions:
        return "Ctrl + Backspace: delete hole password | ctrl + v: show password | ctrl + h: hide password"
    # Show only first 1-2 tips
    return " | ".join(suggestions)


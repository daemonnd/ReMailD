# importing the modules
from prompt_toolkit.validation import ValidationError, Validator



class MasterValidator(Validator):
    def validate(self, document):
        text: str = document.text
        if text == "":
            raise ValidationError("The password field can't be empty.")
        if " " in text:
            raise ValidationError("Spaces are not allowed in master passwords.")


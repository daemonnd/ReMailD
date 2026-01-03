class EmailUtils:
    """
    Class for basic email utils, like extracting the provider of an email address.
    """
    def __init__(self, email_address: str):
        self.email_address: str = email_address

    def get_provider(self) -> str:
        return self.email_address.split("@")[1]
    def get_email_address(self) -> str:
        return self.email_address
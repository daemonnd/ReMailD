"""
File for specific account exceptions
"""
class AccountNotFoundError(Exception):
    """
    If the name, path or id haven't been found
    """
    def __init__(self, *args):
        super().__init__(*args)

class InvalidAccountError(Exception):
    """
    If the Account is invalid: files/folders/data missing
    """
    def __init__(self, *args):
        super().__init__(*args)

class AccountLimitReachedError(Exception):
    """
    If the number of Accounts in accountPaths.json is higher than 1000
    """
    def __init__(self, *args):
        super().__init__(*args)

class AccountMetaError(Exception):
    """
    If the basic account meta is invalid
    """
    def __init__(self, *args):
        super().__init__(*args)

class AccountLoadingError(Exception):
    """
    If sth went wrong while loading the account, before the account meta is known
    """
    def __init__(self, *args):
        super().__init__(*args)


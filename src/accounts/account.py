# importing the modules
from pathlib import Path

# importing the files
from . . utils.errorprotocol import logger
from . . utils.launch_reader import launch_data

# initializing classes
log: logger = logger()

class Account:
    """
    ReMailD Account Superclass. Contains basic methods and other stuff that all ReMailD accounts (recovery & mini) needs
    """
    def __init__(self):
        pass
    def identify(self, account_type_selector: str) -> str:
        """
        Method for identifying the account type. It returns if it is a mini account or the recovery account with "mini" or "recovery".
        """
        if account_type_selector == "recovery":
            return "recovery"
        elif account_type_selector == str(Path(launch_data.folder / "recovery")):
            return "recovery"
        else:
            return "mini"
        
                
    def edit(self, selector: str, editing_type: str):
        pass
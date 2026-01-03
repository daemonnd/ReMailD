"""
File for checking for important file/folder dependencies
"""
from pathlib import Path
import json
from pprint import pformat, pprint
from typing import *
from . errorprotocol import logger
from . launch_reader import launch_data
from . json_editor import JsonFile

log = logger()

class DependencyManager:
    def __init__(self):
        # initializing accountPaths.json
        self.accountPaths: Path = Path(Path(launch_data.folder / "src" / "accounts" / "accountPaths.json")) # type: ignore
        self.default_accountPaths: str = json.dumps(
            obj={
                "1": "","2": "","3": "","4": "","5": "","6": "","7": "","8": "","9": "","10": "","11": "","12": "","13": "","14": "","15": "","16": "","17": "","18": "","19": "","20": ""}
        ) # type: ignor
 
        # initializing email_providers.json
        self.email_providers: Path = Path(Path(launch_data.folder / "src" / "utils" / "email_login" / "email_providers.json")) # type: ignore
        self.default_email_providers: str = json.dumps(obj={})
        
       
        # initializing the recovery file paths
        self.recovery_master: Path = Path(Path(launch_data.folder) /  "recovery" / "master.enc")
        self.recovery_credentials: Path = Path(launch_data.folder / "recovery" / "credentials.enc")
        

    def run(self) -> dict[str, bool]:
        """
        Main method of this class, returns in a dict with what is missing. If nothing is missing, each case is True.
        """
        try:
            return {
                "recovery_master": self.check_files(file=self.recovery_master),
                "recovery_credentials": self.check_files(file=self.recovery_credentials),
                "email_providers": self.check_files(file=self.email_providers, default=self.default_email_providers),
                "accountPaths": self.check_files(file=self.accountPaths, default=self.default_accountPaths), 
            }
        except Exception as e:
            log.log_warning(f"Exception while checking files: {str(e)}")
            return {
                "recovery_master": "False",
                "recovery_credentials": "False",
                "email_providers": "False",
                "accountPaths": "False"
            }

    def check_files(self, file: Path, default: Any = str("")) -> bool:
        """
        Method for checking if all the files exist.
        If a file is not existing, this method returns the Path of it
        """
        if file.exists():
            return True
        else:
            
            if "credentials" in str(file):
                log.log_warning("Recovery credentials are missing")
                return False
            if "master" in str(file):
                log.log_warning("Recovery master password is missing")
                return False
            log.log_warning(f"The file {file} was inexistent. It will be recreated with default values.")
            file.touch()
            file.write_text(default)
            return False
        

if __name__ == "__main__":
    dm = DependencyManager()
    pprint(dm.run())
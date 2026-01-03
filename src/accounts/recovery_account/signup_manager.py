"""
File for managing the hole sign up process
"""

# importing the modules
import shutil
from pathlib import Path
from pprint import pformat
import json
import time
from rich import print

# importing files
from . . . utils.errorprotocol import logger
from . . . utils.launch_reader import launch_data
from . . . auth.base.session import BasicSession
from . . . security.account_security.encryption import EncryptionManager
from . . . security.account_security.login import LoginManager
from . session.session import SignupSession


# creating instances of classes
log = logger()
auth = SignupSession()
#encryptor = EncryptionManager()
#login_manager = LoginManager()

class SignupManager:
    """
    Class for managing the hole sign up process.
    """
    def __init__(self, encryptor: EncryptionManager, login_manager: LoginManager):
        self.encryptor: EncryptionManager = encryptor
        self.login_manager: LoginManager = login_manager
    def signup(self) -> None:
        """
        asking for user input, validating it and saving the data as self.data
        """
        self.data: dict = auth.run()
        return self.data

    def setup(self) -> None:
        """
        Method for setting up the sign up (creating files, folders, saving the data)
        The data that is saved is encrypted.
        """
        try:
            # creating files and folders
            Path(launch_data.folder / "recovery").mkdir(parents=True, exist_ok=False)
            Path(launch_data.folder / "recovery" / "credentials.enc").touch(exist_ok=False)
            Path(launch_data.folder / "recovery" / "master.enc").touch(exist_ok=False)
            self.data_path: Path = Path(launch_data.folder / "recovery" / "credentials.enc")

            # saving the master pass
            self.login_manager.save_master_password(password=self.data["login"])
        except FileExistsError as e:
            log.log_error(f"FileExistsError: The folder 'recovery' is existing: {e}")
            exit(1)
    def save_recovery_data(self) -> None:
        key = self.encryptor.derive_key(password=self.data["login"], account_id="recovery")
        self.data_path.write_bytes(self.encryptor.encrypt_data(json.dumps(self.data), key=key))
        return

    def run(self) -> None:
        """
        Main Method of Sign up Manager
        ------------------------------
        Asks the user for data (recovery email, master pass, ...) first,
        Than create empty files and folders.
        And at the end, this method saved the data in an encoded version on the empty files.

        It returns the master pass
        """

        try:
            data: dict = self.signup()
            self.setup()
            self.save_recovery_data()
            print()
            log.log_info("SUCCESS: You signed up successfully!")
            return data["login"]
        except Exception as e:
            log.log_error(f"{e}")

    def reset(self) -> None:
        """
        Method for removing the hole recovery data.
        """
        log.log_info("By proceeding, you will lose your main account and the hole encryption, \nwhat means that the mini accounts you saved won't be available any more.\nThis deletion will be permanently too, what means that you can't restore the data.")
        answer: bool = BasicSession().ask_yes_no("Are you sure you want to remove ALL your user data?")
        if not answer:
            log.log_info("All your data have not been removed.")
            return
        if answer == True:
            log.log_info("Preparing to remove all your data...")
            print("You have 3 seconds to force quit remaild and to not delete permanently all the data.")
            time.sleep(3)
            shutil.rmtree(str(Path(launch_data.folder / "recovery")))
            log.log_info("SUCCESS: The recovery account have been removed successfully.")
            exit(0)















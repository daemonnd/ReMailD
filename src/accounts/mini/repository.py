"""
Transfer file between account files and variables as @dataclasses of models.py
It loads, updates, creates and removes account data.
It contains the following Functions/Methods:
    get_acc_data:
        To return the hole account data as AccountData
    update_acc:
        Updating an Account
    rm_acc:
        Removes an Account Folder
"""
# importing the modules
from pathlib import Path
import pprint
import json
from typing import Tuple
import pprint
from rich import print
from dataclasses import asdict
import time
from rich.progress import Progress, TaskID
from random import randint
import shutil

# importing the files
from .models import AccountData, AccountFiles, AccountMeta
from . import account_utils as acc_utils
from .paths_manager import PathManager
from .interface import AccountInterface
from ...utils.launch_reader import launch_data
from ...utils.json_editor import JsonFile
from ...utils.errorprotocol import logger
from . session.session import ConfigSession
from ...security.account_security.encryption import EncryptionManager
from ...security.account_security.login import LoginManager
from ...auth.base.session import BasicSession
from . import exceptions as account_exceptions

basic_session = BasicSession()
log = logger()

path_manager = PathManager()

class AccountRepository(AccountInterface):
    """
    Class for doing almost everything with one single account.
    """
    def __init__(self, login_manager: LoginManager):
        """
        The __init__ Method requests an integer,
        the account id. If account_id is "None",
        the account meta will be selected based on
        the accounts in accountPaths.json.
        If there is no (valid) account in accountPaths.json,
        the create_empty_acc() and.

        The meta data is given by the manager and the manger takes the meta from paths_manager.py
        """
        # init variables
        #self.meta: AccountMeta = meta
        self.login_manager: LoginManager = login_manager
        self.encryptor: EncryptionManager = login_manager.get_encryptor()
        # init classes, creating instances of them

    def create_empty_acc(self, meta: AccountMeta) -> AccountFiles:
        """
        Account creating Method 1 of 3.
        The range can be reversed with ask_acc_info()
        Method to create an empty account folder, returning AccountFiles.
        It prepares everything tho fill the Account with data.
        That will be done in the method generate_acc_data().

        This Method is required to execute without any
        problems to execute generate_acc_data()
        """
        try:
            account: Path = Path(Path(meta.acc_path) / meta.acc_name)
            account.mkdir(parents=True, exist_ok=False)
            #print(f"account: {account}")

            # create user data folder
            Path(account / "answer_data").mkdir(parents=True, exist_ok=True, mode=0o444)
            # create main folder in user data folder
            # main folder (for essential data like emails and passwords, the hole emailconfig.json file is encoded with cryptokey file.)
            Path(account / "main").mkdir(parents=True, exist_ok=True)
            emailconfig: Path = account / "main" / "email_config.json"
            emailconfig.touch()
            emailconfig.write_text("{}")


            # create filter folder in user data folder
            (account / "answer_data" / "filters").mkdir(parents=True, exist_ok=True)
            # creating filter json files (empty)
            (account / "answer_data" / "filters" / "blacklist.json").touch(mode=0o444)
            (account / "answer_data" / "filters" / "whitelist.json").touch(mode=0o444)
            # create answermode folder in user data folder
            (account / "answer_data" / "answermode").mkdir(parents=True, exist_ok=True)

            # generating the intern account file paths
            acc_files: AccountFiles = AccountFiles(acc_path=Path(meta.acc_path) / meta.acc_name ).get_data()
            return acc_files
        except FileExistsError as e:
            """
            If the files/folders that are about being created already exist.
            """
            log.log_error(f"FileExistsError: The file or folder already exists: {e}")
        except PermissionError as e:
            log.log_error(f"PermissionError: It seems you don't have the permission to create folders and files. Try launching remaild with 'sudo': {str(e)}")
            return False
        except Exception as e:
            log.log_error(f"Exception with creating empty account files: {e}")

    def encrypt_acc_data(self, data: AccountData, files: AccountFiles) -> None:
        """
        Method for encrypting account data. It writes the encrypted version on the account files.
        """
        log.log_debug("Encrypting the account data...")
        files = files.get_data()
        # getting the encryption key

        key = self.encryptor.derive_key(password=self.login_manager.get_master(), account_id="recovery")

        # writing each part of data in the correct files
        # writing the main things on the correct file
        files.email_config.write_bytes(self.encryptor.encrypt_data(json.dumps(data.asdict_main()), key=key))
        # writing the blacklist data on the file
        files.blacklist.write_bytes(self.encryptor.encrypt_data(json.dumps(data.blacklist), key=key))
        # writing the whitelist data on the file
        files.whitelist.write_bytes(self.encryptor.encrypt_data(json.dumps(data.whitelist), key=key))
        log.log_debug("Encrypting the account data... Done")
        print()

    def decrypt_acc_data(self, encoded: str) -> str:
        #print("in decrypt_acc_data()")
        key = self.encryptor.derive_key(password=self.login_manager.get_master(), account_id="recovery")
        return self.encryptor.decrypt_data(encoded=encoded, fernet_key=key)

    def load_acc_data(self, meta: AccountMeta, progress: Progress, task: TaskID) -> Tuple[AccountData, AccountFiles]:
        #print("in load_acc_data()")
        files: AccountFiles = self.load_acc_files(meta=meta)
        files: AccountFiles = files.get_data()
        progress.advance(task, randint(15, 20))
        # opening the files to get the encoded content
        try:
            with open(file=files.email_config, mode="r") as file:
                email_config_data: str = file.read()
            with open(file=files.blacklist, mode="r") as file:
                blacklist_data: str = file.read()
            with open(file=files.whitelist, mode="r") as file:
                whitelist_data: str = file.read()
            progress.advance(task, randint(2, 5))

            # loading the decrypted data, make it ready to be a dict
            email_config_data: dict = dict(json.loads(self.decrypt_acc_data(encoded=email_config_data)))
            progress.advance(task, randint(10, 15))
            blacklist_data: dict = dict(json.loads(self.decrypt_acc_data(encoded=blacklist_data)))
            progress.advance(task, randint(10, 15))
            whitelist_data: dict = dict(json.loads(self.decrypt_acc_data(encoded=whitelist_data)))


            return AccountData(
                email=email_config_data["email"],
                password=email_config_data["password"],
                imap_host=email_config_data["imap_host"],
                imap_port=email_config_data["imap_port"],
                smtp_host=email_config_data["smtp_host"],
                smtp_port=email_config_data["smtp_port"],
                blacklist=blacklist_data,
                whitelist=whitelist_data
            ), AccountFiles(
                acc_path=meta.acc_path
            ).get_data()
        except FileNotFoundError as e:
            log.log_error(f"AccountNotFoundError: It seems that the account '{meta.acc_name}' is not located at this path: {meta.acc_path} or it is inexistent.")
            raise account_exceptions.AccountNotFoundError(f"The account '{meta.acc_name}' haven't been found: {str(e)}")
        except Exception as e:
            log.log_error(f"Error while loading the account data of account '{meta.acc_name}': {str(e)}")
            raise account_exceptions.InvalidAccountError(f"InvalidAccountError: The account '{meta.acc_name}' is invalid: {str(e)}")

    def load_acc_files(self, meta: AccountMeta) -> AccountFiles: # DONE
        #print("in load_acc_files()")
        return AccountFiles(acc_path=meta.acc_path)

    def list_acc(self):
        return super().list_acc()

    def update_acc(self, data, meta):
        return super().update_acc(data)

    def check_acc(self, account: AccountFiles):
        #print("in check_acc()")
        missing: str = "" # init the var
        account = asdict(account.get_data()) # creating a dict of the dataclass to make it iterable

        for file in account:
            # the value 'acc_path' is not the file so it is skipped.
            if file == "acc_path":
                continue
            if Path(account[file]).exists():
                pass
            else: missing = f"{file}, {missing}"

        if missing == "":
            return True
        log.log_info(f"The account folder is not valid, the following files/folders are missing: {missing}")
        return False

    def rm_acc(self, meta: AccountMeta) -> None:
        """
        Method for removing an account
        """
        try:
            shutil.rmtree(path=meta.acc_path)
            log.log_info(f"The account '{meta.acc_name}' have been removed successfully.")
        except:
            log.log_error(f"AccountNotFoundError: The account '{meta.acc_name}' have not been found in {meta.acc_path}. So it couldn't be removed.")

    def move_acc(self, meta: AccountMeta, destination_path: Path) -> bool:
        """
        Method to move an account from one path to another. It returns True if the operation succeeds, False if it fails to prevent moving only the saved path but not the real account.
        """
        try:
            shutil.move(src=meta.acc_path, dst=destination_path)
            return True
        except Exception as e:
            log.log_error(f"Exception: The account '{meta.acc_name}' couldn't be moved from {str(meta.acc_path)} to {str(destination_path)} due to this error: {e}")
            return False





if __name__ == "__main__":
    ar = AccountRepository(login_manager=LoginManager(security_status="user"))
    #ar.rm_acc(meta=AccountMeta(acc_id=-1, acc_path=Path("/home/alain/Documents/ReMailD/user_accounts/sudo"), acc_name="sudo"))
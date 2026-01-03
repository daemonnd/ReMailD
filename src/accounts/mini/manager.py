"""
Main ReMailD Account File
========================

Functions (done with account folder):
    -
Uses:
    - account_path_manager.py:
        - get account data
    - models.py:
        - access to AccountMeta, AccountFiles, AccountData
    - exceptions.py:
        - raise custom account exceptions

"""
# importing the modules
from typing import Protocol
import sys
from time import sleep
from pathlib import Path
import os
import pathlib
from typing import Protocol, Tuple
from dataclasses import asdict
import json
import time
from rich import print
from rich.progress import Progress
from random import randint
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from cryptography import fernet

# importing remaild files
#from . storage import AccountStorage
from .interface import AccountInterface
from . import account_utils as account_utils
from .paths_manager import PathManager
from .repository import AccountRepository
from .models import AccountMeta, AccountData, AccountFiles
from . import account_utils as acc_utils
from ...security.account_security.login import LoginManager
from . session.session import ConfigSession
from ...utils.json_editor import JsonFile
from ...utils.errorprotocol import logger
from ...utils.launch_reader import launch_data
from ...auth.base.session import BasicSession
from . import exceptions as account_exceptions
from . session.session import ConfigSession
from . .mini.completions import Completer
from ...utils import other
from . . . utils.email_login.email_utils import EmailUtils





basic_session: BasicSession = BasicSession()
log: logger = logger()
paths_manager: PathManager = PathManager()

app_directory: Path = launch_data.folder


# creating an account manager protocol
class AccountManagerProtocol(Protocol):
    def __init__(self):
        super().__init__()
    def load_acc_data(self, selector: str) -> AccountData: ...
    def load_acc_files(self, meta: AccountMeta) -> AccountFiles: ...
    def ask_acc_info(self) -> Tuple[AccountMeta, AccountData]: ...
    def load_acc_meta(self, selector: str = "", path: bool = False) -> AccountMeta: ...
    def load_full_acc_tester(self, selector: str = "", path: bool = False) -> Tuple[AccountMeta, AccountData, AccountFiles]: ...


class AccountManager:
    """
    Main Account class, combining Methods of subfiles
    to execute account processes, like creating an account
    or loading one. It is the only class main.py is using
    for managing accounts. Each account process go through
    this class.
    """
    def __init__(self, login_manager: LoginManager):
        # save absolute path to main folder as path
        self.repo: AccountRepository = AccountRepository(login_manager=login_manager)

        # creating an instance if AccountStorage
        #self.storage = AccountStorage(app_directory=self.app_directory)
        #self.acc_folder: Path = Path(self.storage.get_acc_folder())
        #self.default_user_acc_folder = Path(self.app_directory / "Accounts" / "UserAccounts")

    def load_acc_data(self, selector: str) -> AccountData:
        """
        Method for loading an account.

        Returns:
            AccountData:
                The hole data of an account

        How it works:
        -------------
            This method looks at first for any account requirements, that can
            be an id, a path or a name.

            If yes, the load_acc_from_id will be executed with the requirements and if not
            without the requirements.

            At both situations, the method of the paths manager returns AccountMeta,
            where the path is the most important.

            With the given path, it extracts the data of the account and defines an
            AccountData instance with which the main loop can be started.
        """
        try:
            self.meta: AccountMeta = paths_manager.load_acc_from_id(selector=selector) # getting the meta of the account that should be loaded to get tha path
            self.meta.acc_path
        except:
            pass
        return AccountData()

    def load_acc_files(self, meta: AccountMeta) -> AccountFiles:
        """
        Method to load the account files what makes account editing more easy
        """
        return AccountFiles(
            acc_path=meta.acc_path
        ).get_data()

    def ask_acc_info(self, completer: Completer | None = None) -> Tuple[AccountMeta, AccountData]:
        """
        Account creating Method 2 of 3.
        The range can be reversed with create_empty_acc()
        Method that asks the user for data to create an account.
        The data will be returned as a @dataclass that can be used by the
        Method generate_acc_data() (which is the last account creating Method)
        """
        try:
            email_configurator = ConfigSession(completer=completer)
            config_data: dict = email_configurator.run()

            return AccountMeta(
                acc_path=config_data["meta"]["path"],
                acc_name=config_data["meta"]["name"],
                acc_id=-1
            ),AccountData(
                email=config_data["main"]["email"],
                password=config_data["main"]["pass"],
                imap_host=config_data["main"]["imap_host"],
                imap_port=config_data["main"]["imap_port"],
                smtp_host=config_data["main"]["smtp_host"],
                smtp_port=config_data["main"]["smtp_port"],
                blacklist=config_data["blacklist"],
                whitelist=config_data["whitelist"]
            )
        except Exception as e:
            log.log_error(f"Something went wrong with asking the User for account data: {e}")

    def create_acc(self, completions: Completer | None = None) -> Tuple[AccountMeta, AccountData, AccountFiles]:
        """
        Method for creating a new account.
        Returns:
            AccountData:
                The data of the account created.
        """
        try:
            # get an id for the account to access it easier
            id: int = account_utils.get_next_id()
            log.log_debug("Task [GetNewAccountID] have been completed successfully.")

            # asking for account information
            meta, data = self.ask_acc_info(completer=completions)

            log.log_debug("Task [AskingUserAccountData] have been completed successfully.")

            # overwriting generating the account meta (to insert the id)

            meta: AccountMeta = AccountMeta(
                acc_id=id, # inserting the id
                acc_path=meta.acc_path, # keeping path
                acc_name=meta.acc_name # keeping name
            )

            # adding the acc path to accountPaths.json
            paths_manager.add_acc(path=Path(Path(meta.acc_path) / meta.acc_name), id=id)
            log.log_debug("Task [AddAccountMetaToFile] have been completed successfully")

            log.log_debug("Task [CreateAccountMeta] have been completed successfully.")

            files: AccountFiles = self.repo.create_empty_acc(meta=meta)
            files = files.get_data()
            #print(files.acc_path)
            #print(files.email_config)
            log.log_debug("Task [CreateEmptyAccountFiles] have been completed successfully.")
            print("\n[blue]Now, you have to enter your master password \nto write the data in an encrypted way on the \nempty account files.[/blue]")
            self.repo.encrypt_acc_data(data=data, files=files)
            log.log_debug("Task [EncryptWriteAccountData] have been completed successfully.")
            log.log_info(f"The account '{meta.acc_name}' have been created successfully in {meta.acc_path}.")
            return meta, data, files
        except Exception as e:
            log.log_error(f"Exception while creating account: {e}")

    def load_acc_meta(self, selector: str = "", path: bool = False) -> AccountMeta:
        """
        Method for loading the account meta from selector
        """
        log.log_debug(f"Loading loading requirements...")
        # checking for any requirements (path, name or id):
        if path:
                loading_requirements: str = "path"
                if selector == "":
                    raise ValueError("var selector can't be '' if path=True.")
        else:
            loading_requirements: str = acc_utils.get_command(arg=selector)
        log.log_debug(f"Loading account meta with loading requirement {loading_requirements}...")
        match loading_requirements:
                    case "None":
                        meta: AccountMeta = paths_manager.load_acc_from_file()
                        log.log_debug(f"The account meta have been loaded successfully using {loading_requirements}.")

                    case "none":
                        meta: AccountMeta = paths_manager.load_acc_from_file()
                        log.log_debug(f"The account meta have been loaded successfully using {loading_requirements}.")

                    case "int":

                        meta: AccountMeta = paths_manager.load_acc_from_id(selector=selector)
                        log.log_debug(f"The account meta have been loaded successfully using {loading_requirements}.")
                    case "path":
                        meta: AccountMeta = AccountMeta(
                            acc_id=paths_manager.load_account_id_from_path(path=selector),
                            acc_path=Path(selector),
                            acc_name=acc_utils.get_name_from_path(path=str(selector))
                        )
                        log.log_debug(f"The account meta have been loaded successfully using {loading_requirements}.")

                    case "name":
                        if "/" in selector or "\"" in selector:
                            log.log_warning(f"The account name {selector} can't contain any path signs, like '/' and '\'. Please change the name of the account.")
                        meta: AccountMeta = paths_manager.load_acc_from_name(name=selector)
                        log.log_debug(f"The account meta have been loaded successfully using {loading_requirements}.")

                    case _:
                        raise account_exceptions.AccountLoadingError(f"The account loading requirements can't be {loading_requirements}. Please try to launch remaild with -a-p and an absolute path.")
        return meta

    def load_full_acc_tester(self, selector: str = "", path: bool = False) -> Tuple[AccountMeta, AccountData, AccountFiles]:
        """
        Method for fully loading an account, returning the meta, data, files
        This method has been made for testing, because the errors are raised which make it possible to continue the run.
        Returns:
            AccountMeta, AccountData, AccountFiles:
                For each of these classes one instance with all the data
        Raises:
            AccountLoadingError: If an error happens before the account meta is known
            AccountMetaError: If sth with the basic account meta is wrong
            InvalidAccountError: If there are parts of the account that are invalid, like missing files
            AccountNotFoundError: If the selected account haven't been found.
        """
        try:
            meta: AccountMeta = self.load_acc_meta(selector=selector, path=path)
        except account_exceptions.AccountMetaError as e:
            raise account_exceptions.AccountMetaError(str(e))
        except account_exceptions.InvalidAccountError as e:
            raise account_exceptions.InvalidAccountError(str(e))
        except account_exceptions.AccountNotFoundError as e:
            raise account_exceptions.AccountNotFoundError(str(e))
        else:
            with Progress() as progress:
                progress.start()
                task = progress.add_task(f"Loading Account: '{meta.acc_name}'", total=100)
                progress.advance(task_id=task, advance=randint(2, 6))
                # checking if the account exists
                if self.repo.check_acc(account=self.repo.load_acc_files(meta=meta)) == True:
                    progress.advance(task_id=task, advance=randint(5, 7))
                    # loading the account data & files with account meta
                    try:
                        data, files = self.repo.load_acc_data(meta=meta, progress=progress, task=task)
                        log.log_debug(f"The account '{meta.acc_name}' is valid and have been loaded successfully!")

                        # removing the task and recreating it fully loaded
                        progress.remove_task(task)
                        task = progress.add_task(f"Loading Account: '{meta.acc_name}'", total=100, completed=100)

                    except fernet.InvalidToken as e:
                        raise account_exceptions.InvalidAccountError(f"The data is invalid due to invalid token: {e}")
                    except account_exceptions.InvalidAccountError as e:
                        raise account_exceptions.InvalidAccountError(f"The data/files of account '{meta.acc_name}' are invalid: {str(e)}")
                    except account_exceptions.AccountNotFoundError as e:
                        raise account_exceptions.AccountNotFoundError(f"Account not found: {str(e)}")
                    finally:
                        if task in progress.tasks:
                            progress.remove_task(task)
                        progress.stop()
                    return meta, data, files

                else:
                    log.log_error("The account could not be loaded because of missing account files.")
                    raise account_exceptions.InvalidAccountError("The account is invalid due to missing account ")

    def load_single_acc_fully(self, selector: str = "", path: bool = False) -> Tuple[AccountMeta, AccountData, AccountFiles] | None:
        """
        This method loads the selected account fully. On errors the app exits. It catches the errors, log them and exits if really no account have been found that can be loaded successfully
        """

        try:
            return self.load_full_acc_tester(selector=selector, path=path)
        except account_exceptions.AccountLoadingError as e:
            log.log_error(f"AccountLoadingError: An Error occurred before the account meta was known: {e}")
            log.log_error(f"Unfortunately, the account couldn't be loaded.")
            print()
            return
        except account_exceptions.AccountMetaError as e:
            log.log_error(f"AccountMetaError: An error with the account meta occurred: {e}")
            log.log_error(f"Unfortunately, the account could't be loaded.")
            print()
            return
        except account_exceptions.InvalidAccountError as e:
            log.log_error(f"InvalidAccountError: It seems the loaded account is invalid: {e}")
            log.log_error(f"Unfortunately, the account could't be loaded")
            print()
            return
        except account_exceptions.AccountNotFoundError as e:
            log.log_error(f"AccountNotFoundError: The account haven't been found: {e}")
            log.log_error(f"Unfortunately, the account could't be loaded.")
            print()
            return
        except Exception as e:
            log.log_error(f"An exception occurred while loading the account: {e}")
            log.log_error(f"Unfortunately, the account could't be loaded.")
            print()
            return

    def load_full_acc(self, selector: str = "", path: bool = False) -> Tuple[AccountMeta, AccountData, AccountFiles]:
        """
        Method to handle the account loading directly with the user.
        If the user wanted to load a specific account and it could't be loaded, remaild exits.
        If the user did't had any account loading requirements this method tries to load other accounts.
        """
        if selector == "":
            # going through each non-empty account id
            for account_id in paths_manager.list_used_acc():
                # selecting the current id as selector
                loaded_account = self.load_single_acc_fully(selector=str(paths_manager.list_used_acc()[account_id]), path=path)
                if loaded_account != None:
                    log.log_info(f"SUCCESS: The account have been loaded successfully!")
                    return loaded_account
            log.log_error(f"Unfortunately, each account saved is invalid or non-existent. So no account have been loaded successfully. Please create a new account to load it then. Use remaild -cna for that.")
            exit(1)
        else:
            # if the user wanted to load a specific account
            loaded_account = self.load_single_acc_fully(selector=selector, path=path)
            if loaded_account == None:
                log.log_error(f"The account {selector} haven't been loaded successfully. Please try to load another account or launch remaild without account requirements to look trough each account and try to load one. Testing each account with remaild -caa might help too.")
                exit(1)
            else:
                log.log_info("SUCCESS: The account have been loaded successfully!")
                return loaded_account

    def del_acc(self, meta: AccountMeta) -> None:
        self.repo.rm_acc(meta=meta)
        paths_manager.rm_acc(meta=meta)
        return

    def del_all_acc(self) -> None:
        """
        Method to remove ALL the mini accounts
        """

    def del_acc_path(self, meta: AccountMeta) -> None:
        """
        Method to delete an account path of accountPaths.json
        """
        paths_manager.rm_acc(meta=meta)

    def add_acc_path(self, path: Path) -> None:
        """
        Method to add an account path to accountPaths.json, with this the account can be loaded with name, id or path, not only path
        """
        if not path.exists(): # if the path belongs to an usb key or sth like this
            log.log_warning(f"The path {path} does not exist. So no account can be loaded from this path now.")

        paths_manager.add_acc(path=path, id=account_utils.get_next_id())

    def super_check(self, meta: AccountMeta) -> bool:
        """
        Method for checking very carefully an account path, by checking the files and even load it.
        """
        log.log_info(f"Checking account '{meta.acc_name}'...")

        if not self.repo.check_acc(account=self.load_acc_files(meta=meta)):
            return False

        try:
            # loading the account fully
            loaded_meta, loaded_data, loaded_files = self.load_full_acc_tester(selector=str(meta.acc_path))


            # converting the loaded data to dicts to make it iterable
            loaded_meta_dict: dict = asdict(obj=loaded_meta)
            loaded_data_dict: dict = asdict(obj=loaded_data)
            loaded_files_dict: dict = asdict(obj=loaded_files.get_data())

            for field in loaded_meta_dict:
                if loaded_meta_dict[field]:
                    pass
                else:
                    log.log_warning(f"A wrong value is in account meta.")
                    return False

            for field in loaded_data_dict:
                if loaded_data_dict[field]:
                    pass
                else:
                    if loaded_data_dict[field] == {}:
                        continue
                    log.log_warning(f"A wrong value is in account data.")
                    return False

            for field in loaded_files_dict:
                if loaded_files_dict[field]:
                    pass
                else:
                    log.log_warning("A wrong value is in account files.")
                    return False
            log.log_info(f"SUCCESS: The account '{meta.acc_name}' can be loaded without any errors!")
            print()
            return True

        except fernet.InvalidToken as e:
            log.log_error(f"{e}")
            return False
        except account_exceptions.InvalidAccountError as e:
            log.log_error(str(e))
            return False
        except account_exceptions.AccountMetaError as e:
            log.log_error(str(e))
            return False
        except account_exceptions.AccountNotFoundError as e:
            log.log_error(str(e))
            return False
        except Exception as e:
            log.log_error(f"Exception while checking account '{meta.acc_name}' detailed: {e}")
            return False

    def check_all(self) -> None:
        print()
        log.log_info("Checking all accounts that are saved on the account storage...")
        print()
        print("[magenta]--------------------------------------------------------------[/magenta]")
        print("\n\n")
        total_tests: int = 0
        failed_tests: int = 0

        #with ThreadPoolExecutor as executor:
        for account in paths_manager.list_used_acc():
            meta = paths_manager.load_acc_from_id(selector=str(account))
            test_result: bool = self.super_check(meta=meta)
            if test_result == False:
                failed_tests += 1
                log.log_error(f"The account '{meta.acc_name}' isn't a valid account.")
                print("[magenta]--------------------------------------------------------------[/magenta]")
                print("\n\n")
            else:
                print("[magenta]--------------------------------------------------------------[/magenta]")
                print("\n\n")

            total_tests +=1
        log.log_info(f"The test have been completed. {total_tests - failed_tests} of {total_tests} accounts are valid.")
        print("\n\n")

    def check_one(self, meta: AccountMeta) -> None:
        print()
        log.log_info(f"Checking account '{meta.acc_name}'...")
        print()
        print("[magenta]--------------------------------------------------------------[/magenta]")
        print("\n\n")

        # checking if the account files are existing
        if self.repo.check_acc(account=self.repo.load_acc_files(meta=meta)) == False:
            log.log_error(f"InvalidAccountError: The account '{meta.acc_name}' is invalid, there are files or/and folders missing.")
            return
        test_result: bool = self.super_check(meta=meta)
        if test_result == False:
            log.log_error(f"The account '{meta.acc_name}' isn't a valid account.")
            print("[magenta]--------------------------------------------------------------[/magenta]")
            print("\n\n")
            log.log_info("The Test have been completed.")
            return
        print("[magenta]--------------------------------------------------------------[/magenta]")
        print("\n\n")
        log.log_info(f"The test have been completed. The account is valid.")
        print("\n\n")

    def edit_acc_path(self, selector: str) -> None:
        """
        Method for editing the account path, if the account saving path is at another location than accountPaths.json indicates it.
        """
        print(f"id: {self.load_acc_meta(selector=selector)}")
        old_meta: AccountMeta = self.load_acc_meta(selector=selector)
        for i in range(3):
            try:
                for i in range(3):
                    new_path: Path = basic_session.ask_existing_path(msg="Please enter the Path were the account is saved, the path of the account folder: ", bottom_toolbar="If the account is saved at ~/Documents/acc_01, don't answer ~/Documents but ~/Documents/acc_01")
                    # loading the account files with the new path to validate it after that
                    new_files: AccountFiles = self.load_acc_files(meta=AccountMeta(
                        acc_name=old_meta.acc_name, # keep same
                        acc_id=old_meta.acc_id, # keep same to find the place where to edit in accountPaths.json
                        acc_path=new_path # change the old path to the new one
                    ))
                    print(new_files.get_data())
                    print(new_files.email_config)
                    # checking if the account is still valid
                    if self.repo.check_acc(account=new_files) == True:
                        log.log_debug("The new path leads to a valid account, so it can be edited now.")
                        break
                paths_manager.edit_acc_path(meta=old_meta, new_path=Path(new_path))
                log.log_info(f"SUCCESS: The account path of account '{old_meta.acc_name}' have been changed successfully from {old_meta.acc_path} to {new_path}")
                return
            finally:
                pass
            #except Exception as e:
             #   log.log_error(f"Unexpected Exception while editing the account path on account storage: {e}")
        log.log_info(f"Operation cancelled due to invalid inputs.")
        return

    def edit_move_account(self, selector: str) -> None:
        """
        Method to fully move an account to another location, including the account itself and the entry in accountPaths.json
        """
        meta: AccountMeta = self.load_acc_meta(selector=selector)
        new_path: Path = basic_session.ask_existing_path(f"To which existing folder do you want to move the account '{meta.acc_name}'? ")
        if self.repo.move_acc(meta=meta, destination_path=new_path) == True:
            paths_manager.edit_acc_path(meta=meta, new_path=Path(new_path / meta.acc_name))
            log.log_info(f"SUCCESS: The account '{meta.acc_name}' have been moved successfully from {str(meta.acc_path)} to {str(Path(new_path / meta.acc_name))}.")
            print()
        else:
            log.log_error("Due to the error that occurred while moving the real account, the saved account path haven't been changed.")
            print()

    def edit_data(self, selector: str) -> None:
        """
        Method to edit any account data
        """
        # initializing the data
        changes: dict = {}

        # loading the target account fully because it will be needed later
        print()
        log.log_info("Please wait for the account to load, after that you can edit it")
        print()
        meta, data, files = self.load_full_acc(selector=selector)
        print(data)
        print()
        # getting the exact data the user wants to edit, doing in while loop to let the user edit everything
        while True:
            config_session: ConfigSession = ConfigSession(email_utils=EmailUtils(email_address=acc_utils.merge_data(original_data=data, changes=changes).email))
            print(EmailUtils)
            to_edit: str = basic_session.require_specific_answer(msg="What data do you want to edit exactly? To quit and save, use 'quit', to leave without saving, use 'force-quit': ",
                only_include=["all", "email", "imap", "smtp", "quit", "force-quit"],
                bottom_toolbar="Options: all, email, imap, smtp, quit, force-quit")
            match to_edit:
                case "all":
                    print()
                    changes["email"] = config_session.ask_mainEmail()
                    config_session.ask_mainPassword()
                    changes["password"] =  config_session.ask_mainRepeatPassword()
                    changes["imap_host"] = config_session.ask_mainImapHost()
                    changes["imap_port"] = config_session.ask_mainImapPort()
                    changes["smtp_host"] = config_session.ask_mainSmtpHost()
                    changes["smtp_port"] = config_session.ask_mainSmtpPort()
                case "email":
                    print()
                    changes["email"] = config_session.ask_mainEmail()
                    config_session.ask_mainPassword()
                    changes["password"] = config_session.ask_mainRepeatPassword()
                case "imap":
                    print()
                    changes["imap_host"] = config_session.ask_mainImapHost()
                    changes["imap_port"] = config_session.ask_mainImapPort()
                    print()
                case "smtp":
                    print()
                    changes["smtp_host"] = config_session.ask_mainSmtpHost()
                    changes["smtp_port"] = config_session.ask_mainSmtpPort()
                    print()
                case "quit":
                    print()
                    break
                case "force-quit":
                    log.log_info("Operation cancelled by user.")
                    print()
                    return
        # validating the data
        config_session.set_all(data=account_utils.merge_data(original_data=data, changes=changes))
        if config_session.validate() == False:
            log.log_error("It seems that your inputs are wrong. Please retry.")
            print()
        else:
            log.log_info("Your data have been saved in the ram now. To write it to your account quit the editing and confirm with 'y'.")
            print()
        # saving the changed data
        if basic_session.ask_yes_no(f"Are you sure that you wan to overwrite the account data of account '{meta.acc_name}'?") == True:
            # creating a new AccountData instance, with the changes
            try:
                new_data: AccountData = account_utils.merge_data(original_data=data, changes=changes)
                self.repo.encrypt_acc_data(data=new_data, files=files)
                log.log_info(f"SUCCESS: The data of the account '{meta.acc_name}' have been edited successfully!")
            except UnboundLocalError:
                print()
                log.log_warning("The new data could't have been saved because it have been deleted.")
        else: log.log_info(f"Your edits haven't been saved to the account '{meta.acc_name}'.")

    def get_all_paths(self) -> list[str]:
        """
        Method for getting each account saved in accountPaths.json in a list that are probably valid.
        """
        full_list: list = []

        for account in paths_manager.list_used_acc():
            full_list.append(paths_manager.list_used_acc()[account])
        full_list = other.unique_list(full_list)
        final_list: list = []
        for account in full_list:

            if self.repo.check_acc(account=self.load_acc_files(meta=self.load_acc_meta(selector=str(account)))) == True:
                final_list.append(account)
            else:
                print()
                log.log_warning(f"The account {account} won't be loaded for completions because there are files missing.")
                print()
        return final_list










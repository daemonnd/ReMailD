# importing the modules
from pathlib import Path
from typing import *
from rich import print

# importing the files
from . . utils.errorprotocol import logger
from . mini.manager import AccountManager
from . mini import exceptions as account_exceptions
from . mini.models import AccountMeta, AccountData, AccountFiles
from . mini import account_utils
from . mini.completions import Completer
from . .security.account_security.login import LoginManager
from . .auth.base.session import BasicSession
from . . utils import other


# init classes
log: logger = logger()
basic_session: BasicSession = BasicSession()

class MiniAccount:
    """
    Class for executing the argparse commands
    """
    def __init__(self, login_manager: LoginManager):
        self.manager: AccountManager = AccountManager(login_manager)

    def create_acc(self, completion_selectors: list = []) -> Tuple[AccountMeta, AccountData, AccountFiles]:
        """
        Method for creating a new account with optional completion (taking the data form other accounts as WordCompleter)
        """
        # if there are no completion selectors, simply load an acc without completions
        if completion_selectors == []:
            return self.manager.create_acc()
        # if the completion selectors are "*", add each account from accountPaths.json to the completion
        if completion_selectors is not None and any(acc == "*" for acc in completion_selectors or []):
            # initializing new_selectors
            new_selectors = []
            # going through all completion selectors and create the final completion_selectors list
            for acc in completion_selectors:
                # if the current entry is "*", insert all saved paths
                if acc == "*":
                    new_selectors.extend(self.manager.get_all_paths())
                # else add the selected path
                else:
                    new_selectors.append(str(self.manager.load_acc_meta(selector=acc).acc_path))
                    
            completion_selectors: list = new_selectors
            print(f"old completion selectors: {completion_selectors}")
            # checking if the list have been uniqueid
            completion_selectors = other.unique_list(new_selectors)
            print(f"new completion selectors: {completion_selectors}")
            if len(completion_selectors) != len(new_selectors):
                log.log_info("Some account selectors have been removed because they were at least twice in the account completion selectors.")

        # loading the accounts the user requested for the completion
        account_list: list = []
        print("\n")
        log.log_info(f"ReMailD will load all the accounts you selected to extract the data of them. This may take a while")
        print("\n")
        for index, account in enumerate(completion_selectors):
            index += 1
            try:
                log.log_info(f"Loading account {index} of {len(completion_selectors)}...")
                meta, data, files = self.manager.load_full_acc_tester(selector=account)

                account_list.append(data)
            except account_exceptions.AccountMetaError as e:
                print()
                log.log_error(f"AccountMetaError: Due to: {e}, the account data won't be included in the account completions.")
                print("\n")
            except account_exceptions.AccountLoadingError as e:
                print()
                log.log_error(f"AccountLoadingError: Due to {e}, the account data won't be included in the account completions.")
                print("\n")
            except account_exceptions.AccountNotFoundError as e:
                print()
                log.log_error(f"AccountNotFoundError: The account can't be used for account completions because it is inexistent: {e}")
                print("\n")
            except account_exceptions.InvalidAccountError as e:
                print()
                log.log_error(f"InvalidAccountError: Because the account is invalid, its data can't be used for account completions: {e}")
                print("\n")
            except Exception as e:
                print()
                log.log_error(f"Exception: The account data can't be used for completions because of this exception: {e}")
                print("\n")
            finally:
                print()
                print("[magenta]--------------------------------------------------------------[/magenta]")
                print("\n\n")

        # creating a dict with lists of completion
        completer: Completer = Completer().create_completer(data=account_list)
        return self.manager.create_acc(completions=completer)

    def load_full_acc(self, selector: str = "", path: bool = False):
        return self.manager.load_full_acc(selector=selector, path=path)

    def del_acc(self, selector: str = "") -> None:
        meta: AccountMeta = self.manager.load_acc_meta(selector=selector)

        if basic_session.ask_yes_no(msg=f"Are you sure that you want to remove the account named '{meta.acc_name}' with this path: {meta.acc_path}?") == True:
            self.manager.del_acc(meta=meta)
            log.log_debug(f"The account '{meta.acc_name}' have been removed successfully.")
            print("\n\n")
            return
        else:
            log.log_info(f"The account '{meta.acc_name}' haven't been removed.")
            print("\n\n")

    def del_acc_path(self, selector: str = "") -> None:
        try:
            meta: AccountMeta = self.manager.load_acc_meta(selector=selector)
            log.log_info(f"SUCCESS: The account path {meta.acc_path} of account '{meta.acc_name}' have been removed successfully from storage.")
            print()
        except Exception as e:
            log.log_error(f"An Exception occurred while removing the account path {meta.acc_path}: {e}")

    def add_acc_path(self, path: Path) -> None:
        self.manager.add_acc_path(path=Path(path))
        log.log_info(f"SUCCESS: The account '{account_utils.get_name_from_path(path=path)}' with the path {path} have been added successfully to the account storage. From now on, it can be loaded with the name.")
        print()

    def check_one(self, selector: str = "") -> None:
        meta: AccountMeta = self.manager.load_acc_meta(selector=selector)
        self.manager.check_one(meta=meta)

    def check_all(self) -> None:
        self.manager.check_all()

    def edit(self, account_selector: list, editing_type: str) -> None:
        """
        This Method handles the full editing, gives different tasks to the account manager to complete the edits
        """
        for account in account_selector:
            match editing_type:
                case "account-path":
                    self.manager.edit_acc_path(selector=account)
                case "move":
                    self.manager.edit_move_account(selector=account)
                case "data":
                    self.manager.edit_data(selector=account)
                case _:
                    log.log_warning(f"Unknown editing type: {editing_type}")
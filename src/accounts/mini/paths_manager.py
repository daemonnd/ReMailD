"""
File for managing accountPaths.json.
Functions (do with accountPaths.json):
    - loading account
    - adding account
    - removing account
    - list accounts
"""
# importing the modules
import json
from pathlib import Path
from pprint import pformat

# importing the files
from .models import AccountMeta, AccountData, AccountFiles
from . import account_utils as acc_utils


from . import exceptions as account_exceptions
from ...utils.errorprotocol import logger
from ...utils.launch_reader import launch_data
from ...utils.json_editor import JsonFile
from ...auth.base.session import BasicSession
from ... import exceptions as basic_exceptions

# init classes
log = logger()
basic_askings = BasicSession()

class PathManager:
    def __init__(self, app_directory: Path = Path(launch_data.folder)):
        self.app_directory: Path = app_directory
        self.acc_path_file: Path = Path(self.app_directory / "src" / "accounts" / "accountPaths.json")
        self.acc_file: JsonFile = JsonFile(full_path=self.acc_path_file)


    def edit_acc_path(self, meta: AccountMeta, new_path: Path) -> None:
        """
        Method for editing the account path saved in accountPaths.json. This method tries to edit the acc path and validates the path
        """
        # check if the account id is valid
        if meta.acc_id == -1:
            log.log_warning(f"The id of the account '{meta.acc_name}' can't be '{meta.acc_id}'. Please try to load the account with name or id to make sure the id is loaded correctly.")
            return


        try:
            if new_path.exists():
                if new_path.is_dir():
                    self.acc_file.update(key=[f"{meta.acc_id}"], value=str(new_path.resolve()))
                    return
                else:
                    log.log_warning(f"The path {new_path} exists, but is not a directory.")
            else:
                log.log_warning(f"The path {new_path} does not exist.")
                print()
        except ValueError as e:
            log.log_error(f"It seems the id {meta.acc_id} which is a {type(meta.acc_id)} is not valid: {e}")
            log.log_warning(f"Due to invalid id the operation has been cancelled.")
            return


    def load_acc_from_id(self, selector: str = "", path: bool = False) -> AccountMeta:
        """
        Method for returning AccountMeta with which repository.py can work.
        If no args is given, it selects automatically an Account.
        """

        if selector.isdigit(): # if the selector is an account id
            return AccountMeta(
                acc_id=int(selector), # return selector as int,
                acc_path=self.acc_file.get(key=[selector]), # the value of it and
                acc_name=self.get_acc_name(path=Path(self.acc_file.get(key=[selector]))) # the name of the value of it
            )
        raise account_exceptions.AccountNotFoundError(f"The account {selector} haven't been found.")




    def load_acc_from_file(self) -> AccountMeta: # loading a account, selecting it
        """
        Method for loading an account automatically form accountPaths.json
        Function that automatic loads the first account of accountPaths.json.
        It reads the file and select the account
        """
        # if the user is launching remaild without any acc requirements, the auto-acc-selector will be used

        try:
            #print("in load_acc_from_file()")
            accounts = self.acc_file.read()
            sorted_accounts: list = sorted(accounts.keys(), key=int)
            for account in sorted_accounts:
                #print(account, sorted_accounts)
                value: str = accounts[account]
                value = value.replace(" ", "")
                if value != "":
                    self.acc_path: str = value
                    if Path(self.acc_path).exists():
                        return AccountMeta(acc_id=int(account), acc_path=Path(self.acc_path), acc_name=self.get_acc_name(path=Path(self.acc_path))) # here to break the loop if something have been found
                    else:
                        continue
            raise account_exceptions.AccountNotFoundError("No account have been found. Please try to load one manually.")


        except FileNotFoundError as e:
            log.log_warning(f"FileNotFounderror: accountPaths.json not found: {str(e)}")
            Path(self.acc_path_file).touch() # creating the file if it doesn't exist
            self.acc_path = ""
            raise account_exceptions.AccountNotFoundError(f"The account with id {int(account)} and path {self.acc_path} haven't been found: {e}")
        except json.JSONDecodeError as e:
            log.log_warning(f"JSONDecodeError:  accountPaths.json is corrupted or not valid JSON: {str(e)}")
            Path(self.acc_path_file).write_text("{}") # trying to avoid the error
            self.acc_path = ""
            raise basic_exceptions.InvalidFileError(f"The file {self.acc_path_file} is invalid: {e}")
        except Exception as e:
            log.log_error(f"An unexpected error occurred: {str(e)}")
            self.acc_path = ""
            raise account_exceptions.AccountMetaError(f"Due to an unknown Exception the meta could't be loaded: {str(e)}")

    def load_acc_from_name(self, name: str) -> AccountMeta:
        """
        Method for loading the account from the name
        Returns:
            AccountMeta: The meta of the account

        """
        print("in load_acc_FROM_name()")
        accounts = self.acc_file.read() # loading all the accounts of accountPaths.json
        sorted_accounts: list = sorted(accounts.keys(), key=int) # sorting the content and save it
        for account in sorted_accounts: # checking for each account if the name matches.
            #print(account)
            value: str = str(accounts[account])
            #print(value)
            if acc_utils.get_name_from_path(path=str(value)) == name:
                return AccountMeta(
                    acc_path=Path(self.acc_file.get(key=[f"{account}"])),
                    acc_id=int(account),
                    acc_name=name
                    )
        log.log_error(f"AccountNotFoundError: It seems no account have been found in {self.acc_path_file} with the name {name}. Try to load one manually using remaild -ap /path/to/account")
        raise account_exceptions.AccountNotFoundError(f"The account {name} haven't been found.")

    def add_acc(self, path: Path, id: int = 0) -> None:
        try:
            while True:
                existing_path = self.acc_file.get(key=[f"{id}"])
                if existing_path:
                    log.log_info(f"The id {id} is already taken by this account path: {existing_path}")
                    print()
                    answer: bool = basic_askings.ask_yes_no(msg="Do you want to use this place for the new account path?")
                    match answer:
                        case True:
                            try:
                                self.acc_file.update(key=[f"{id}"], value=str(path))
                                #print(f"Updated accountPaths.json: {self.acc_file.read()}")  # Debug
                                break
                            except Exception as e:
                                log.log_error(f"Failed to update id {id} with path {path}: {e}")
                                raise
                        case False:
                            print(f"\nThe empty account ids are: \n{str(pformat(self.list_empty_acc()))}")

                            id = int(basic_askings.ask_positive_int(
                                msg=f"To which id do you want to save {str(path)}? (0-999): ",
                                limit=999
                            ))
                        case _:
                            raise ValueError(f"Value Error with y/n question: Session return can only be True or False, not {answer}.")
                else:
                    try:
                        # checking if the path already exists in the account storage
                        accounts = self.acc_file.read()
                        sorted_accounts: list = sorted(accounts.keys(), key=int)
                        for account in sorted_accounts:
                            #print(account, sorted_accounts)
                            if accounts[account] == str(path):
                                log.log_warning(f"This path already exists in the account storage: {str(path)}")
                                break

                        # inserting the path
                        self.acc_file.update(key=[f"{id}"], value=str(path))
                        return

                    except Exception as e:
                        log.log_error(f"Failed to add id {id} with path {path}: {e}")
                        raise
        except Exception as e:
            log.log_error(f"Exception while adding account to accountPaths.json: {e}")

    def get_acc_name(self, path: Path = Path(""), id: int = 0) -> str:
        """
        Method for returning the name of an account with an id or a account Path.
        Args:
            path: Path of the account where the name should be extracted.
            id: ID of the account (must exist in accountPaths.json).
        Returns:
            str: Name of the account (last component of the path).
        """
        try:
            if path == Path(""):
                path_str: str = str(self.acc_file.get(key=[f"{id}"]))

                #print(f"Retrieved path for id={id}: {path_str}")  # Debug
                if path_str is None or path_str.strip() == "":
                    raise basic_exceptions.ArgumentMissingError(f"No valid path found for id={id} in accountPaths.json")
                path = Path(path_str)

            if not path:
                raise basic_exceptions.ArgumentMissingError(args="path, id", args_number=2)
            if not path.exists():
                log.log_error(f"The file or folder {path} does not exist.")
                return ""
            if not path.is_dir():
                raise basic_exceptions.IsFileError(f"The path {path} is a file. Accounts must be folders.")

            path_str = str(path).rstrip("/")  # Remove trailing slash
            #print(f"Processing path: {path_str}")  # Debug
            name = path_str.split("/")[-1] or path_str  # Handle root or single component
            #print(f"Extracted name: {name}")  # Debug
            return name

        except Exception as e:
            log.log_error(f"Exception with getting the name of account path: {self.acc_file.get(key=[f"{id}"])}: {e}")
            raise
    def list_empty_acc(self) -> list:
        """
        This method returns all empty cases of accountPaths.json
        """

        # init empty account path ids
        empty_acc_ids: list = []
        # listing all the account ids that aren't already taken
        for account in range(self.acc_file.get_key_count()): # repeating it the number ok key times
            if self.acc_file.get(key=[f"{account}"]).replace(" ", "") == "": # if the field is empty
                empty_acc_ids.append(account) # if the account id is empty, it will be added to the empty account list
        return empty_acc_ids

    def rm_acc(self, meta: AccountMeta) -> None:
        """
        Method to remove an account path of accountPaths.json
        """

        #print(f"TYOPE OF ACCOUNT ID @ RM_ACC: {type(meta.acc_id)}")
        to_remove = self.acc_file.get(key=[f"{str(int(meta.acc_id))}"])
        self.acc_file.update(key=[f"{meta.acc_id}"], value="")
        log.log_debug(f"The account path of account '{meta.acc_name}' have been deleted successfully")

    def list_used_acc(self) -> dict:
        """
        Method to list all the account ids and paths that are used.
        """
        used_acc_dict: dict = {}
        for account in range(self.acc_file.get_key_count()):
            if self.acc_file.get(key=[f"{account}"]) != "":
                used_acc_dict[f"{account}"] = self.acc_file.get(key=[f"{account}"])
        return used_acc_dict

    def get_full_acc_paths(self) -> dict:
        """
        Method for returning the hole content of accountPaths.json.

        IMPORTANT:
        ------------
            It is ONLY used to provide extra information to the user, NOT FOR EDITING, DELETING OR SIMILAR THINGS!
        """
        return self.acc_file.read()

    def load_account_id_from_path(self, path: str | Path) -> int:
        """
        Method to correctly load the account id if the account path already exists in accountPaths.json. If the path is inexistent, the account id is -1.
        """

        path: str = str(path)
        try:
            # get a full dict of all used accounts
            list_user_acc_dict: dict = self.list_used_acc()
            # going through each id to find the id that matches with the given path
            for id in list_user_acc_dict:
                if str(list_user_acc_dict[id]) == path:
                    return int(id)
            # if it haven't been found
            return -1

        #except KeyError:
         #   return -1
        finally:
            pass



if __name__ == "__main__":
    acc_path_manager: PathManager = PathManager(app_directory=Path(launch_data.folder))
    print()

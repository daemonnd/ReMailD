"""
File for additional account utils, like getting id with name/path, determine it it is path/name/id
"""
# importing the modules
from pathlib import Path
import pprint

# importing the files
from ...utils.errorprotocol import logger
from . models import AccountMeta, AccountData, AccountFiles
from .paths_manager import PathManager

log = logger()
path_manager = PathManager()

def get_name_from_path(path: Path | str) -> str:
    """
    Func to get the account name (the last part) of an account path.
    """
    return str(path).split("/")[-1]

def get_next_id() -> int:
        """
        Method to get the next free id of accountPaths.json
        """
        cases: list = path_manager.list_empty_acc() # save all the possible ids as var


        if cases: # if there are empty fields
            return cases[0] # the first free field
        else:
            log.log_warning(f"There are no empty account ids, each one is taken:\n{pprint.pformat(path_manager.get_full_acc_paths())}") # giving the hole content of accountPaths.json to the user to show him which paths are taken by what
            print()
            log.log_info("To create another account, remove one path in the storage with remaild -rmap/--remove-account-path [StrPath] or remove one account fully (remaild -rm/--remove [Account]). You can check if all the accounts are valid too, using remaild -caa/--check-all-accounts")
            exit(2)

def get_command(arg: str = "") -> str:
    """
    Function to get the command of loading account, it sorts if it is a name, path or id.

    Returns:
        none:
            If no args have been given
        int:
            If the arg is a digit

        path:
            If the arg is a path that exists
        name:
            If the arg is neither a digit, nor a path

    """
    if arg == "":
        return "none"
    if not arg:
        return "none"
    elif arg.isdigit() == True:
        return "int"
    elif Path(arg).exists() == True:
        return "path"
    else:
        return "name"

def merge_data(original_data: AccountData, changes: dict) -> AccountData:
    """
    Func to check if there are changes in each case. If there are changes, the changes will be implemented in the output. If not, not.
    """
    print(changes)
    print(original_data.email)
    print(AccountData(
        email=changes.get("email", original_data.email),
        password=changes.get("password", original_data.password),
        imap_host=changes.get("imap_host", original_data.imap_host),
        imap_port=changes.get("imap_port", original_data.imap_port),
        smtp_host=changes.get("smtp_host", original_data.smtp_host),
        smtp_port=changes.get("smtp_port", original_data.smtp_port),
        blacklist=changes.get("blacklist", original_data.blacklist),
        whitelist=changes.get("whitelist", original_data.whitelist),
    ))
    return AccountData(
        email=changes.get("email", original_data.email),
        password=changes.get("password", original_data.password),
        imap_host=changes.get("imap_host", original_data.imap_host),
        imap_port=changes.get("imap_port", original_data.imap_port),
        smtp_host=changes.get("smtp_host", original_data.smtp_host),
        smtp_port=changes.get("smtp_port", original_data.smtp_port),
        blacklist=changes.get("blacklist", original_data.blacklist),
        whitelist=changes.get("whitelist", original_data.whitelist),
    )

def get_path_from_name(name: str) -> Path:
    return path_manager.load_acc_from_name(name=name).acc_path

if __name__ == "__main__":
    print(get_name_from_path(path="/home/user/Documents/ReMailD/acc_name"))
    print(get_command(arg="18"))

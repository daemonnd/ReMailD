"""
Main file of the remaild project.
It executes all the main functions and methods
"""
# importing the modules
import argparse
import os
import sys
import time
from pathlib import Path
from typing import *
from rich import print

# import the files
from . utils.errorprotocol import logger
from . utils.launch_reader import launch_data
from . utils.file_checker import DependencyManager
from . accounts.recovery_account.signup_manager import SignupManager
from . security.account_security.login import LoginManager
from .accounts.mini_account import MiniAccount
from .accounts.mini.models import AccountMeta, AccountData, AccountFiles
from .accounts.mini import account_utils

# init logger
log = logger()

class CLIParser:
    """
    Class for handling remaild's argparse logic
    """
    def __init__(self):
        # init the parser
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser(description='Remaild: Secure auto email responder')

        # adding args to the parser
        # account selection args
        self.acc_selector_group: argparse._MutuallyExclusiveGroup = self.parser.add_mutually_exclusive_group()
        self.acc_selector_group.add_argument('--account', '-a', help='Run remaild for a specific account. have to be followed by the account path or the name.', )
        self.acc_selector_group.add_argument("--account-path", "-ap", help="Force ReMailD to launch with the account path. Example: 'remaild -ap ~/.acc01'")

        # ReMailD meta args
        self.parser.add_argument("--version", action="version", version='ReMailD 1.01.1 alpha')
        self.parser.add_argument("--stop", "-s", action="store_true", help="ReMailD closes after all args have been executed")

        # Account removing args
        self.parser.add_argument("--remove", "-rm", help="Removes a user account. Use -rm + [account name]/[account path]/[account id] Example: remaild -rm account_01")
        self.parser.add_argument("--remove-account-path", "-rmap", help="Removes a mini account path to load it with name/id. After that, only loading with full path is possible. Clears one field in the account storage which can be used by another, new account.", type=Path)

        # account util args
        self.parser.add_argument("--add-account-path", "-aap", help="Inserts an account path in the account storage, which means that the account path you insert can be loaded with the name/id later.")
        self.parser.add_argument("--check-account", "-ca", help="Checks if the account given is valid or not, it remaild can launch it or not")
        self.parser.add_argument("--check-all-accounts", "-caa", help="Checks if all the accounts on the account storage (loadable with name/id/path) are valid.", action="store_true")
        self.parser.add_argument("--create-new-account", "-cna", help="Creates a new user account. Use 'remaild -cna ACCOUNT ACCOUNT' to create an account and get completers and defaults from other accounts. Also usable without param.", default=None, nargs="*", )#const="no_param")

        # recovery account args
        self.parser.add_argument("--force-reset", help="Resets everything, makes all mini account unusable and requires a new sign up to use remaild again.", action="store_true")

        # mini account / recovery account args
        # editing arg
        self.parser.add_argument("--edit", "-e", help="Edit account(s): ['recovery' / ID / NAME PATH] [More accounts] [EDITING-VALUE]", nargs="+")



        # define the arg Namespace
        self.args: argparse.Namespace = self.parser.parse_args()

    def parse_args(self) -> argparse.Namespace:
        return self.args

    def get_status(self) -> str:
        """
        Method for getting the security status depending on if there are args or not.
        """
        if any(vars(self.args).values()):
            return "admin"
        return "user"

class ReMailDApp:
    """
    Main ReMailD class for executing all the functions.
    Usage:
    `
    app = ReMailDApp()
    app.run()
    `
    """
    def __init__(self):
        # init a var
        self.acc_meta = None
        # initializing the cli parser
        self.cli_parser: CLIParser = CLIParser()
        # parsing the cli parser's args
        self.args: argparse.Namespace = self.cli_parser.parse_args()

        print(f"Starting ReMailD as {self.cli_parser.get_status()}...", end="", flush=True)

        self.start: float = time.perf_counter()

        # requesting master (and 2FA and Admin if there are any args)
        self.login_manager = LoginManager(security_status=self.cli_parser.get_status())

        # generating a EncryptionManager instance
        self.encryptor = self.login_manager.get_encryptor()

        # checking if all the file dependencies are existing
        self.handle_dependencies()



        # init the account manager
        self.account_manager = MiniAccount(login_manager=self.login_manager)

    def run(self):


        # execute the args
        # on --force-reset
        if self.args.force_reset:
            signup_manager = SignupManager(encryptor=self.encryptor, login_manager=self.login_manager)
            signup_manager.reset()


        # after sign up management done, require login
        self.login_manager.handle_run()

        # on --remove
        if self.args.remove:
            self.account_manager.del_acc(selector=str(self.args.remove))

        # on --remove-account-path
        if self.args.remove_account_path:
            self.account_manager.del_acc_path(selector=str(self.args.remove_account_path), )

        # on --add-account-path
        if self.args.add_account_path:
            self.account_manager.add_acc_path(path=Path(self.args.add_account_path))

        # on --check-account
        if self.args.check_account:
            self.account_manager.check_one(selector=self.args.check_account)

        # on --check-all-accounts
        if self.args.check_all_accounts:
            self.account_manager.check_all()

        # on --create-new-account
        # if there are accounts or \* followed by -cna
        if self.args.create_new_account not in [None, []]:
            self.acc_meta, self.acc_data, self.acc_files = self.account_manager.create_acc(completion_selectors=self.args.create_new_account)
            new_args: list = [sys.executable, Path(launch_data.folder / "src" / "main.py"), "-a", f"{self.acc_meta.acc_path}"]
            print("HERE REMAILD SHOULD RESTART!!!!")
            exit(0)
        # if no additional args have been given to --create-new-account
        if self.args.create_new_account == []:
            self.acc_meta, self.acc_data, self.acc_files = self.account_manager.create_acc(completion_selectors=[])
            print("HERE REMAILD SHOULD RESTART1!!")
            exit(0)

        # on --edit
        if self.args.edit:
            # not enough args
            if len(self.args.edit) < 2:
                log.log_warning(f"Less than 2 args were followed by --edit/-e: {self.args.edit} which means that nothing can be edited. Usage: remaild -e [ACCOUNT SELECTORS] [EDITING VALUE]")
                print()
            else:
                editing_type: str = self.args.edit[-1]
                del self.args.edit[-1]
                account_selectors: list = self.args.edit
                self.account_manager.edit(account_selector=account_selectors, editing_type=editing_type)
        # on --stop
        if self.args.stop:
            log.log_info("ReMailD will close now... (cause: -s/--stop)")
            raise KeyboardInterrupt

        # saving the login data in the ram
        print("Loading account...", end="", flush=True)
        self.login_manager.get_data()

        # loading the full account if it haven't been done before
        log.log_debug("ReMailD will launch using one account now.")
        if not self.acc_meta:
            if self.args.account_path:
                self.acc_meta, self.acc_data, self.acc_files = self.account_manager.load_full_acc(selector=str(self.args.account_path), path=True)
            elif self.args.account:
                self.acc_meta, self.acc_data, self.acc_files = self.account_manager.load_full_acc(selector=str(self.args.account))
            else:
                self.acc_meta, self.acc_data, self.acc_files = self.account_manager.load_full_acc()
            print(f"account meta: {self.acc_meta}\naccount data: {self.acc_data}\naccount files: {self.acc_files.get_data()}")

    def handle_dependencies(self):
            log.log_debug("Checking the dependencies...")
            dependency_manager_instance: DependencyManager = DependencyManager()
            dependency_manager: dict[str] = dependency_manager_instance.run()

            for dependency in dependency_manager:

                if str(dependency_manager[dependency]) == False:
                    print(f"dependency[{dependency} is false]")
            if dependency_manager["recovery_credentials"] == False:
                log.log_critical(f"Because of recovery data missing, you will need to sign up.")
                log.log_info("There are some important dependencies missing. After signing up, you can launch remaild normally.")
                signup_manager = SignupManager(login_manager=self.login_manager, encryptor=self.encryptor)
                signup_manager.run()
            log.log_debug("The dependency checking finished and no one is missing.")
            return





if __name__ == "__main__":
    try:
        app = ReMailDApp()
        app.run()
    except KeyboardInterrupt:
        print()
        print("Closing ReMailD...")
        print("ReMailD have been closed successfully!")
        exit(0)
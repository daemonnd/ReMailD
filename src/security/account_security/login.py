"""
File for managing the security while logging in. This means:
checking if the user is admin, checking if the login pass is correct and
managing 2FA. Only if all of these security Features are correct, it is possible to
edit data in ReMailD.
"""
from cryptography.fernet import Fernet
from hashlib import pbkdf2_hmac 
import bcrypt
import secrets
import pyperclip3 as pc
from pathlib import Path
import hashlib
import json
import cryptography.fernet
import time
from typing import Any
from prompt_toolkit import PromptSession, prompt


from . . . utils import errorprotocol
from . . . utils.launch_reader import launch_data
from . session.session import SecuritySession
from . encryption import EncryptionManager
from . admin_check import AdminCheck

admin_checker = AdminCheck()

log = errorprotocol.logger()
auth = SecuritySession()


class LoginManager:
    """
    Manager for logging in. That includes admin rights, a login pass and 2FA.
    """
    def __init__(self, security_status: str):
        log.log_debug("Initializing the login manager...")
        # initializing the class by asking the master pass 
        self.security_status: str = security_status
      
        self.encryptor = EncryptionManager(security_status=security_status)
     
    def handle_run(self) -> None:
        """
        Method for handling the run() and tiny_run() method
        """
        match self.security_status:
            case "user":
                self.tiny_run()
            case "admin":
                self.run()
        

    def ask_master(self) -> str:
        print()
        self.master_pass = auth.ask_master()
        return self.master_pass
    def get_master(self) -> str:
        try:
            if not self.master_pass:
                log.log_critical(str(self.master_pass))
                exit(1)
            #print(f"master pass: {self.master_pass}")
            return self.master_pass
        except Exception as e:
            self.ask_master()
            log.log_error(f"It is impossible to use the master password for decoding if it is unknown: {e}")
       
    def run(self) -> None:
        """
        Main method, combining everything for login.
        """
        try:
            admin_checker.check_admin()
        except PermissionError as e:
            log.log_error(f"PermissionError: {e}")
            exit(2)
        for i in range(3):
            self.master_pass = self.ask_master()
            if self.verify_master_password() == True:
                # ADD 2FA HERE!!!
                return self.master_pass
            else:
                time.sleep(2) # makes brute force a lot more inefficient
                log.log_warning("The master password you entered is wrong.")
                if i == 2:
                    print()
                    log.log_warning("ReMailD has been closed due to the wrong master password.")
                    exit(2)
    
        # ADD 2FA HERE!!!!
        
        
    
    def tiny_run(self) -> None:
        """
        Method that only asks the user for master password, it is also validated.
        """
        for i in range(3):
            self.master_pass = self.ask_master()
            if self.verify_master_password() == True:
                return self.master_pass
            else:
                time.sleep(2) # makes brute force a lot more inefficient
                log.log_warning("The master password you entered is wrong.")
                if i == 2:
                    print()
                    log.log_warning("ReMailD has been closed due to the wrong master password.")
                    exit(2)

    def get_data(self) -> str:
        """
        Method for saving the data in the ram. run() have to be called first, otherwise remaild exits.
        """
        #print("Your data will be decoded now. Please wait a few seconds.")
        #try:
        self.data_path: Path = Path(launch_data.folder / "recovery" / "credentials.enc")
        key = self.encryptor.derive_key(password=self.master_pass, account_id="recovery")  # creates the same key
        encrypted_data = self.data_path.read_bytes()  # reading encrypted data    
        decrypted_data: Any = EncryptionManager(security_status=self.security_status).decrypt_data(encrypted_data, fernet_key=key)  # decoding data
        return decrypted_data
        #except cryptography.fernet.InvalidToken as e:
         #   time.sleep(2) # skip a second, to let brute force attacks take longer
          #  log.log_warning(f"InvalidToken: {e}")
           # exit(1)
        #except Exception as e:
         #   time.sleep(1.5)
          #  log.log_error(f"Exception while loading data: {e}")
           # exit(1)

    def generate_pass(self, password: str) -> bytes:
        """
        Method that turns the pass as string into a hashed version of it to make it safe.
        """   
        salt: bytes = bcrypt.gensalt()
        return bcrypt.hashpw(password=password.encode(), salt=salt)
    # In src/security/account_security/login.py

    def save_master_password(self, password: str):
        with open(launch_data.folder / "recovery" / "master.enc", "wb") as file:
            file.write(hashlib.sha256(password.encode()).digest())

    def verify_master_password(self) -> bool:
        """
        Method for verifying the master pass.
        Used for normal logins, without making any changes.
        """
        try:
            with open(launch_data.folder / "recovery" / "master.enc", "rb") as file:
                to_return = hashlib.sha256(self.master_pass.encode()).digest() == file.read()
                if to_return == False:
                    return False
                else:
                    return True
        except:
            time.sleep(2)
    
    def get_encryptor(self) -> EncryptionManager:
        """
        Method for getting an instance of the encryptor
        """
        if not hasattr(self, "encryptor"):
            self.encryptor = EncryptionManager(security_status="user")
        return self.encryptor
if __name__ == "__main__":
    pass
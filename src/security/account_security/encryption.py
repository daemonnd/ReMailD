from cryptography.fernet import Fernet
from pathlib import Path
import os
from rich import print
from hashlib import pbkdf2_hmac
import secrets
from time import perf_counter
import base64
import pyperclip3 as pc
import hashlib
import bcrypt
import time
from typing import Any
import cryptography.fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


from . . .utils.launch_reader import launch_data
from . . . utils import errorprotocol

log = errorprotocol.logger()

class EncryptionManager:
    """
    Class for generating keys for encoding files, encoding files and decode them. 
    """ 
    # In src/security/account_security/encryption.py
    def __init__(self, security_status: str):
        self.security_status = security_status
    def derive_key(self, password: str, account_id: str) -> bytes:
        #print("in derive_key()")
        kdf = PBKDF2HMAC(salt=account_id.encode(), length=32, iterations=launch_data.iterations, algorithm=hashes.SHA256())
        key_bytes = kdf.derive(password.encode())  # Encode password to bytes first
        return base64.urlsafe_b64encode(key_bytes)
  
    def encrypt_data(self, data: str, key: bytes | str) -> bytes:
        """
        Method for encrypting data. It needs the raw data and the key, than it returns the encrypted version. 
        """
        fernet: Fernet = Fernet(key=key)
        return fernet.encrypt(data.encode())
        

    def decrypt_data(self, encoded: Any, fernet_key: str | bytes) -> str:
        """
        Method for decrypting data. It needs the key and the encoded version and returns the decoded version.
        """
        #print("in decrypt_data()")
        if self.security_status == "sign_up":
            log.log_warning("Decrypting data while sign up is not allowed. Please rerun remaild without signing up to let remaild decode data.")
            exit(2)
        elif self.security_status == "admin" or self.security_status == "user":
            try:
                fernet: Fernet = Fernet(key=fernet_key)
                decoded: str = fernet.decrypt(encoded).decode()
                return decoded
            except cryptography.fernet.InvalidToken:
                log.log_warning("Invalid login credentials. Decrypting the data didn't work")
                time.sleep(2)
                raise cryptography.fernet.InvalidToken("Invalid login credentials: Decrypting the data didn't work")
        else:
            log.log_error(f"Unknown security status: Security status can't be {self.security_status}")
            exit(1)


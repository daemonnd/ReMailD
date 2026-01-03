from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Self

# importing the files
#from . import utils as acc_utils

@dataclass
class AccountData:
    """
    @dataclass for the account data
    """
    
    # the main data (for the main email address)
    email: str
    password: str
    imap_host: str
    imap_port: int
    smtp_host: str
    smtp_port: int

    # the filters
    blacklist: dict
    whitelist: dict

    def asdict_main(self) -> dict:
        return {
            "email": self.email,
            "password": self.password,
            "imap_host": self.imap_host,
            "imap_port": self.imap_port,
            "smtp_host": self.smtp_host,
            "smtp_port": self.smtp_port
        }

@dataclass
class AccountMeta:
    """
    dataclass for having account meta data
    in the random access memory. 
    That includes:
        - account path, 
        - account id
    """
    acc_name: str
    acc_id: int
    acc_path: Path = Path("") # the path 
                      # split the path to the folders /home/acc_1 to ("home", "acc_1")
     
@dataclass
class AccountFiles:
    """
    @dataclass to get tha file paths with the name
    """
    acc_path: Path = Path("") # ONLY to NOT get an error, 
                                    # if it isn't overwritten later, there will be an error 
    blacklist: Path | None = None
    whitelist: Path | None = None
    email_config: Path | None = None
    
    def __post_init__(self):
        if not Path(self.acc_path).exists():
            raise ValueError(f"The Path acc_path can't be ''.")
    def get_data(self) -> Self:
        #print("in get_data")
        self.blacklist: Path = Path(Path(self.acc_path) / "answer_data" / "filters" / "blacklist.json")
        self.whitelist: Path = Path(Path(self.acc_path) / "answer_data" / "filters" / "whitelist.json")
        self.email_config: Path = Path(Path(self.acc_path) / "main" / "email_config.json")
        return self
    



"""
File for transforming account data in completion Lists
"""
# importing the modules
from typing import Self, List
from dataclasses import dataclass, field

# importing the files
from .models import AccountData
from ...utils.errorprotocol import logger
from . . . utils import other

log = logger ()

@dataclass
class Completer:
    """
    Class for transforming multiple account data in Lists for completion with the existing account data
    """
    email: List = field(default_factory=list)
    imap_host: List = field(default_factory=list)
    imap_port: List = field(default_factory=list)
    smtp_host: List = field(default_factory=list)
    smtp_port: List = field(default_factory=list)
    blacklist: List = field(default_factory=list)
    whitelist: List = field(default_factory=list)

    def create_completer(self, data: List[AccountData]) -> Self:
        # converting the data to different lists
        for entry in data:
            self.email.append(entry.email)
            self.imap_host.append(entry.imap_host)
            self.imap_port.append(str(entry.imap_port))
            self.smtp_host.append(entry.smtp_host)
            self.smtp_port.append(str(entry.smtp_port))
            self.blacklist.append(entry.blacklist)
            self.whitelist.append(entry.whitelist)
        # making sure that there are no entries twice in each list
        self.email: list = other.unique_list(self.email)
        self.imap_host: list = other.unique_list(self.imap_host)
        self.imap_port: list = other.unique_list(self.imap_port)
        self.smtp_host: list = other.unique_list(self.smtp_host)
        self.smtp_port: list = other.unique_list(self.smtp_port)
        self.blacklist: list = other.unique_list(self.blacklist)
        self.whitelist: list = other.unique_list(self.whitelist)
        return self
    def create_empty_completer(self) -> Self:
        self.email: List = []
        self.imap_host: List = []
        self.imap_port: List = []
        self.smtp_host: List = []
        self.smtp_port: List = []
        self.blacklist: List = []
        self.whitelist: List = []
        return self


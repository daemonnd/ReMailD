# importing the modules
from prompt_toolkit import prompt, PromptSession, auto_suggest

from prompt_toolkit.completion import WordCompleter, FuzzyCompleter
from prompt_toolkit.key_binding import KeyBindingsBase, DynamicKeyBindings, KeyBindings, ConditionalKeyBindings
from prompt_toolkit.filters import Condition
from prompt_toolkit.filters import Always
from prompt_toolkit.styles import Style

import socket, ssl, email, smtplib, imaplib, time, json
from email.message import EmailMessage
import getpass

from zxcvbn import zxcvbn
import email.message
from pathlib import Path
from rich import print
from rich.progress import Progress


# importing the files
from . import prompts
from . . models import AccountMeta, AccountData, AccountFiles
from . . . . auth.base_session import BaseSession
from . . . . utils import errorprotocol
from . . . . utils.launch_reader import launch_data
from . . . . utils.email_login import completers, validators
from . . . . utils.email_login.email_utils import EmailUtils
from . . . . security.email.ssl import ssl_context
from . . . mini.completions import Completer

# init classes
log = errorprotocol.logger()

class ConfigSession(BaseSession):
    """
    ConfigSession
    =============
    Class with methods to configure the main and recovery email Address
    """
    def __init__(self, completer: Completer | None = None, email_utils: EmailUtils | None = None):
        """
        initializing class and def all PromptSessions
        to use them easily later
        """
        super().__init__()
        # set default value
        self.pw: str = ""
        # create an empty completer if it is None
        if completer == None:
            completer = Completer().create_empty_completer()
        if email_utils != None:
            self.email_utils: EmailUtils = email_utils
        # define the sessions
        # def path session
        self.path_session: PromptSession = PromptSession(
            validate_while_typing=False,
            validator=validators.PathValidator(),
            auto_suggest=auto_suggest.AutoSuggestFromHistory(),
            bottom_toolbar="Enter the full path of the folder where the account should be, without the new account folder."
        )

        # def name session
        self.name_session: PromptSession = PromptSession(
            validate_while_typing=False,
            validator=validators.NameValidator(),
            auto_suggest=auto_suggest.AutoSuggestFromHistory(),
            #completer=completers.autofill_acc_name() # ADD THE COMPLETER HERE
            bottom_toolbar="Give your account a name that fits to its purpose, like 'work' or 'private'"
        )

        # def Email Session
        self.email_session: PromptSession = PromptSession(
            multiline=False,
            validate_while_typing=False,
            #completer=completers.emailDomainCompleter,
            complete_while_typing=True,
            validator=validators.EmailValidator(),
            auto_suggest=auto_suggest.AutoSuggestFromHistory(),
            bottom_toolbar="To that email remaild will auto answer.",
            completer=FuzzyCompleter(WordCompleter(completer.email, ignore_case=True))
        )

        # def pass session
        pass_validator: validators.PasswordValidator = validators.PasswordValidator()
        password_bindings: KeyBindings = KeyBindings()

        def make_toggle(hidden: bool):
            def handler(event):
                pass_validator.set_visibility(visible=hidden)
            return handler

        password_bindings.add('c-v')(make_toggle(hidden=False))
        password_bindings.add('c-h')(make_toggle(hidden=True))


        self.pass_session: PromptSession = PromptSession(
            key_bindings=password_bindings,
            validate_while_typing=True,
            validator=pass_validator,
            bottom_toolbar=lambda: validators.get_toolbar(pass_validator),
            is_password=Condition(lambda: pass_validator.get_visibility()),
            erase_when_done=False
        )

        # def imap address session    # validator=validators.
        self.imapserver_address_session: PromptSession = PromptSession(
            multiline=False,
            validate_while_typing=False,
            auto_suggest=auto_suggest.AutoSuggestFromHistory(),
            complete_while_typing=True,
            completer=FuzzyCompleter(WordCompleter(completer.imap_host))
        )
        # def smtp server Address session
        self.smtpserver_address_session: PromptSession = PromptSession(
            auto_suggest=auto_suggest.AutoSuggestFromHistory(),
            complete_while_typing=True,
            completer=FuzzyCompleter(WordCompleter(completer.smtp_host))
        )
        # def port session
        self.Port_session: PromptSession = PromptSession(
            validator=validators.PortValidator(),
            validate_while_typing=False,
            auto_suggest=auto_suggest.AutoSuggestFromHistory(),
            complete_while_typing=True,
            completer=FuzzyCompleter(WordCompleter(completer.imap_port + completer.smtp_port)))



    """
    Methods of this class.
    Each method asks the user one thing.
    """
    def ask_full_acc_path(self) -> Path:
        """
        Asking the full path, with name at the end
        """
        return Path(self.path_session.prompt(
            prompts.email_config_prompts[launch_data.lang]["askMeta"]["path"],
            bottom_toolbar="Please enter the existing destination path.",
            default=str(Path(launch_data.folder / "user_accounts"))
        ))
    def ask_acc_path(self) -> Path:
        self.acc_path: str = (self.path_session.prompt(
            message=prompts.email_config_prompts[launch_data.lang]["askMeta"]["path"],
            default=str(Path(launch_data.folder / "user_accounts"))
        ))
        self.acc_path: Path = Path(self.acc_path)
        return self.acc_path # type: ignor

    def ask_acc_name(self) -> str:
        self.acc_name: str = self.name_session.prompt(
            message=prompts.email_config_prompts[launch_data.lang]["askMeta"]["name"],
        )
        return self.acc_name

    def ask_mainEmail(self) -> str:
        self.mainEmail: str = self.email_session.prompt(
            message=prompts.email_config_prompts[launch_data.lang]["askEmail"]["mainEmail"],
        )

        # init EmailUtils now, because the email address is known.
        self.email_utils: EmailUtils = EmailUtils(email_address=self.mainEmail)
        return self.mainEmail

    def ask_mainPassword(self) -> str:

        self.mainPassword: str = self.pass_session.prompt(
            message=prompts.email_config_prompts[launch_data.lang]["askPassword"]["password"],
        )



    def ask_mainRepeatPassword(self) -> None:
        try:
            while True:
                for i in range(3):
                    self.mainRepeatPassword: str = getpass.getpass(prompts.email_config_prompts[launch_data.lang]["askPassword"]["repeatPassword"])
                    if self.mainRepeatPassword == self.mainPassword:
                        return self.mainPassword
                    else:
                        print("The first password doesn't match the second one. Please retry.")
                self.ask_mainPassword()
        except Exception as e:
            log.log_error(f"Exception with repetition for asking main password: {e}")
            raise

    def ask_mainImapHost(self) -> str:
        self.mainImapHost: str = self.imapserver_address_session.prompt(
            message=prompts.email_config_prompts[launch_data.lang]["askImap"]["server_address"],
            default=str(completers.get_completions(provider=self.email_utils.get_provider())["imap_host"])
        )
        return self.mainImapHost

    def ask_mainImapPort(self) -> int:
        self.mainImapPort_str: str = self.Port_session.prompt(
            message=prompts.email_config_prompts[launch_data.lang]["askImap"]["port"],
            default=str(completers.get_completions(provider=self.email_utils.get_provider())["imap_port"])
        )
        self.mainImapPort: int = int(self.mainImapPort_str)
        return self.mainImapPort

    def ask_mainSmtpHost(self) -> str:
        self.mainSmtpHost: str = self.smtpserver_address_session.prompt(
            message=prompts.email_config_prompts[launch_data.lang]["askSmtp"]["server_address"],
            default=str(completers.get_completions(provider=self.email_utils.get_provider())["smtp_host"])
        )
        return self.mainSmtpHost

    def ask_mainSmtpPort(self) -> int:
        self.mainSmtpPort_str: str = self.Port_session.prompt(
            message=prompts.email_config_prompts[launch_data.lang]["askSmtp"]["port"],
            default=str(completers.get_completions(provider=self.email_utils.get_provider())["smtp_port"])
        )
        self.mainSmtpPort: int = int(self.mainSmtpPort_str)
        return self.mainSmtpPort

    def ask_user_input(self, completer: Completer | None = None) -> dict:
        print(prompts.email_config_prompts[launch_data.lang]["intro"]["meta"])
        self.ask_acc_path()
        self.ask_acc_name()
        print(prompts.email_config_prompts[launch_data.lang]["intro"]["main"])
        self.ask_mainEmail()
        self.ask_mainPassword()
        self.ask_mainRepeatPassword()
        self.ask_mainImapHost()
        self.ask_mainImapPort()
        self.ask_mainSmtpHost()
        self.ask_mainSmtpPort()





        #self.repeat_mainPassword: str = self.pwRepeat_session.prompt(
         #   message=prompts.email_config_prompts["askPassword"]["repeatPassword"],
        #)


        #self.repeat_recoveryPassword: str = self.pwRepeat_session.prompt(
         #   message=prompts.email_config_prompts["askPassword"]["repeatPassword"],
        #)

        return {
            "meta": {
                "path": str(self.acc_path), # as str because otherwise it can't be written properly in .json files
                "name": self.acc_name
            },
            "main": {
                "email": self.mainEmail,
                "pass": self.mainPassword,
                "imap_host": self.mainImapHost,
                "imap_port": self.mainImapPort,
                "smtp_host": self.mainSmtpHost,
                "smtp_port": self.mainSmtpPort,
            },
            # WILL BE ADDED LATER
            "filters": {
                "1": {},
                "2": {},
                "3": {}
            },
            "answermode": {

            },
            "blacklist": {},
            "whitelist": {},


        }
    # set methods to set all values without asking anything to the user
    def set_email(self, email: str) -> None:
        self.mainEmail: str = email
    def set_email_pass(self, password: str) -> None:
        self.mainPassword: str = password
    def set_imap_host(self, imap_host: str) -> None:
        self.mainImapHost: str = imap_host
    def set_imap_port(self, imap_port: int) -> None:
        self.mainImapPort: int = imap_port
    def set_smtp_host(self, smtp_host: str) -> None:
        self.mainSmtpHost: str = smtp_host
    def set_smtp_port(self, smtp_port: int) -> None:
        self.mainSmtpPort: int = smtp_port
    def set_all(self, data: AccountData) -> None:
        self.set_email(email=data.email)
        self.set_email_pass(password=data.password)
        self.set_imap_host(imap_host=data.imap_host)
        self.set_imap_port(imap_port=data.imap_port)
        self.set_smtp_host(smtp_host=data.smtp_host)
        self.set_smtp_port(smtp_port=data.smtp_port)

    def validate_main(self):
        """
        Method for validating the user data (inly the main email address).
        For that, ReMailD sends an email for the main email to the main email
        and checks if it can read this email later.
        """
        # smtp: sending mail
        msg: EmailMessage = EmailMessage()
        msg["Subject"] = "ReMailD Email Test"
        msg["From"] = self.mainEmail
        msg["To"] = self.mainEmail

        msg.set_content("""
        Hello!

        Welcome to ReMailD – your automated email assistant.

        If you are receiving this message, it means your email address and password have been successfully verified and everything is set up correctly.

        ReMailD helps you manage and respond to your emails automatically, so you can focus on what matters most.

        Thank you for using ReMailD!

        If you have any questions or need assistance, feel free to reach out.

        Best regards,
        The ReMailD Team
        """)


        with smtplib.SMTP(host=self.mainSmtpHost, port=self.mainSmtpPort, timeout=30) as smtp:
            smtp.starttls(context=ssl_context())
            smtp.login(user=self.mainEmail, password=self.mainPassword)
            smtp.send_message(msg=msg)


        # imap: reading the test mail
        # make several tries, if it takes more time
        imap: imaplib.IMAP4_SSL = imaplib.IMAP4_SSL(host=self.mainImapHost, port=self.mainImapPort)
        imap.login(user=self.mainEmail, password=self.mainPassword)
        imap.select(mailbox="INBOX")

        status, data = imap.search(None, '(SUBJECT "ReMailD Email Test")')

        if status == "OK":
            msg_ids: bytes = data[0].split()  # list of mail ids (as bytes)
            if msg_ids:
                # get the first unread message
                status, msg_data = imap.fetch(msg_ids[0], "(RFC822)")
                if status == "OK":
                    raw_email: bytes = msg_data[0][1]
                    msg: email.message.Message = email.message_from_bytes(raw_email)
                    subject: str = msg.get("Subject")
                else:
                    log.log_error("Error with calling message.")
            else:
                log.log_error("The Test Email did not arrived.")
        else:
            log.log_error("Searching the incoming Email failed.")
        imap.logout()


        log.log_info("Main Email Login Success!")


    def validate(self) -> bool:
        """
        Method to test the user's input.
        For doing that, 2 emails will be send.
        One at the recovery email address and the other one
        at the main email address.
        It calls the validate_main() Method.
        """

        try:
            print()
            log.log_info("""
                ReMailD will check your inputs now.
                Please do not quit it, because the hole date will be lost.
                \n""")
            for i in range(launch_data.repeat_range):
                start: float = time.perf_counter()
                print()
                log.log_info(f"Checking your inputs... This may take a few seconds. Attempt: {i + 1} of {launch_data.repeat_range }")
                try:

                    # execute validation methods
                    self.validate_main()


                    log.log_info("SUCCESS: Your emails and passwords are both correct!")
                    end: float = time.perf_counter()
                    log.log_info(f"Input checking took {end - start:.5f} seconds.")
                    return True
                except imaplib.IMAP4_SSL.abort as e:
                    log.log_warning(f"abort: Server closed the connection unexpectedly {e}")
                    time.sleep(1.5)
                except imaplib.IMAP4_SSL.readonly as e:
                    log.log_warning(f"readonly: Mailbox opened in read-only mode: {e}")
                    time.sleep(1.5)
                except socket.gaierror as e:
                    log.log_warning(f"gaierror: Invalid hostname – DNS resolution failed: {e}")
                    time.sleep(1.5)
                except socket.timeout as e:
                    log.log_warning(f"timeout: Server did not respond in time: {e}")
                    time.sleep(1.5)
                except ssl.SSLError as e:
                    log.log_warning(f"SSLError: SSL/TLS negotiation failed – wrong port or certificate issue: {e}")
                    time.sleep(1.5)
                except ConnectionRefusedError as e:
                    log.log_warning(f"ConnectionRefusedError: Server refused the connection – port not open or server down: {e}")
                    time.sleep(1.5)
                except OSError as e:
                    log.log_warning(f"OSError: Network unreachable or blocked: {e}")
                    time.sleep(1.5)
                    log.log_warning(f"EOFError: Connection closed unexpectedly by the server: {e}")
                except imaplib.IMAP4_SSL.error as e:
                    log.log_warning(f"IMAP4_SSL.error: Generic error – invalid credentials or failed login: {e}")
                    time.sleep(1.5)
                except smtplib.SMTPAuthenticationError as e:
                    log.log_warning(f"SMTPAuthenticationError: the authentication with smtp failed: {e}")
                    time.sleep(1.5)
                except smtplib.SMTPConnectError as e:
                    log.log_warning(f"SMTPConnectError: error during connection establishment: {e}")
                    time.sleep(1.5)
                except smtplib.SMTPException as e:
                    log.log_warning(f"SMTPException: unexpected smtp error: {e}")
                    time.sleep(1.5)
                except Exception as e:
                    log.log_error(f"Exception while validating your inputs: {e}")
                    time.sleep(1.5)
                finally:
                    print()
            #log.log_error(f"The validation failed, probably because of {e}. Make sure to enter the correct emails and passwords.")
            return False
        except Exception as e:
            log.log_error(f"Exception with basic init: {e}")
            return False


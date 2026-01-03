from prompt_toolkit import PromptSession, prompt
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit import auto_suggest
import socket, ssl, email, smtplib, imaplib, time, json
from email.message import EmailMessage
import getpass
import email.message
from rich import print


from . . . . utils.email_login import completers, validators
from . . . . utils.launch_reader import launch_data
from . . . . auth.base_session import BaseSession
from . . . . utils.errorprotocol import logger
from . . . . utils.email_login.email_utils import EmailUtils
from . . . . security.email.ssl import ssl_context
from . import prompts
log = logger()


class SignupSession(BaseSession):
    """
    configSession
    =============
    Class with methods to configure the main and recovery email Address
    """
    def __init__(self):
        """
        initializing class and def all PromptSessions
        to use them easily later
        """
        super().__init__()

        # init vars
        self.login_repeat_pass: str = ""
        # init prompt dict
        self.prompts: dict = prompts.SIGN_UP_PROMPTS[launch_data.lang]
        # set default value
        self.pw: str = ""
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
            auto_suggest=auto_suggest.AutoSuggestFromHistory()
        )


        #  def Email Session
        self.email_session: PromptSession = PromptSession(
            multiline=False,
            validate_while_typing=False,
            #completer=completers.emailDomainCompleter,
            complete_while_typing=True,
            validator=validators.EmailValidator(),
            auto_suggest=auto_suggest.AutoSuggestFromHistory()
        )

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
            auto_suggest=auto_suggest.AutoSuggestFromHistory()
        )
        # def smtp server Address session
        self.smtpserver_address_session: PromptSession = PromptSession(
            auto_suggest=auto_suggest.AutoSuggestFromHistory()
        )
        # def port session
        self.Port_session: PromptSession = PromptSession(
            validator=validators.PortValidator(),
            validate_while_typing=False,
            auto_suggest=auto_suggest.AutoSuggestFromHistory()
        ) # type: ignor e # type: ignore

    def ask_login_pass(self) -> str:
        self.login_pass: str = self.pass_session.prompt(
            message=self.prompts["login"]["pass"]
        )

    def ask_recoveryEmail(self) -> str:
        self.recoveryEmail: str = self.email_session.prompt(
            message=self.prompts["askEmail"],
        )
        # Now, as the email is known, a class will be initialized
        self.email_utils: EmailUtils = EmailUtils(email_address=self.recoveryEmail)
        return self.recoveryEmail
    def ask_recoveryPassword(self) -> str:
            try:
                while True:
                    self.recoveryPassword: str = getpass.getpass(self.prompts["askPassword"]["password"])
                    for i in range(3):
                        repeat_pass: str = getpass.getpass(self.prompts["askPassword"]["repeatPassword"])
                        if repeat_pass == self.recoveryPassword:
                            return self.recoveryPassword
                        log.log_warning(f"The password is incorrect. Please try again. Attempt: {i+1}/3\n")
            except Exception as e:
                log.log_error(f"Exception while asking password for recovery email address: {e}")
                exit(1)


    def ask_recoverySmtpHost(self) -> str:
        self.recoverySmtpHost: str = self.smtpserver_address_session.prompt(
            message=self.prompts["askSmtp"]["server_address"],
            default=str(completers.get_completions(provider=self.email_utils.get_provider())["smtp_host"])
        )
        return self.recoverySmtpHost
    def ask_recoverySmtpPort(self) -> int:
        self.recoverySmtpPort_str: str = self.Port_session.prompt(
            message=self.prompts["askSmtp"]["port"],
            default=str(completers.get_completions(provider=self.email_utils.get_provider())["smtp_port"])
        )
        self.recoverySmtpPort: int = int(self.recoverySmtpPort_str)
        return self.recoverySmtpPort

    def ask_user_input(self) -> dict:
        print(self.prompts["intro"]["start"])
        input()
        print(self.prompts["login"]["intro"])
        self.ask_login_pass()
        print(self.prompts["intro"]["recovery"])
        self.ask_recoveryEmail()
        self.ask_recoveryPassword()
        self.ask_recoverySmtpHost()
        self.ask_recoverySmtpPort()

        return {
            "login": self.login_pass,
            "recovery": {
                "email": self.recoveryEmail,
                "pass": self.recoveryPassword,
                "smtpHost": self.recoverySmtpHost,
                "smtpPort": self.recoverySmtpPort,
            },
        }


    def validate_recovery(self):
        """
        Method for validating the recovery email address.
        For that, ReMailD sends an email from the users account to
        the users account.
        """

        # smtp: sending an email (from recovery email address to recovery email address)
        msg: EmailMessage = EmailMessage()
        msg["Subject"] = "ReMailD Recovery Email Test"
        msg["From"] = self.recoveryEmail
        msg["To"] = self.recoveryEmail

        msg.set_content("""
        Hello!

        Welcome to ReMailD – your automated email assistant.

        If you are receiving this message, it means your recovery email address and password have been successfully verified and everything is set up correctly.

        This email will only be used to ask you for otp codes to change settings on ReMailD.

        ReMailD helps you manage and respond to your emails automatically, so you can focus on what matters most.

        Thank you for using ReMailD!

        If you have any questions or need assistance, feel free to reach out.

        Best regards,
        The ReMailD Team
        """)


        with smtplib.SMTP(host=self.recoverySmtpHost, port=self.recoverySmtpPort, timeout=30) as smtp:
            smtp.starttls(context=ssl_context())
            smtp.login(user=self.recoveryEmail, password=self.recoveryPassword)
            smtp.send_message(msg=msg)

        log.log_info("Recovery Email Success!")

    def validate(self) -> bool:
        """
        Method to validate the user's input. For that, an email will be send from the user's recovery email to the user's recovery email.
        """
        try:
            log.log_info("\nReMailD will check your inputs now by sending an email \nfrom your recovery email address.\nPlease do not quit ReMailD right now, because the hole data you entered will be lost.\n")

            for i in range(launch_data.repeat_range):
                start: float = time.perf_counter()
                print()
                log.log_info("Checking your inputs... This may take a few seconds.")
                try:
                    # validate the recovery email data
                    self.validate_recovery()
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
                except smtplib.SMTPConnectError as e:
                    log.log_warning(f"SMTPConnectError: error during connection establishment: {e}")
                    time.sleep(1.5)
                except smtplib.SMTPException as e:
                    log.log_warning(f"SMTPException: unexpected smtp error: {e}")
                    time.sleep(1.5)
                except Exception as e:
                    log.log_error(f"An Exception occurred while validating inputs: : {e}")
                    time.sleep(1.5)
                else:
                    log.log_info("SUCCESS: Your recovery email and password are both correct!")
                    end: float = time.perf_counter()
                    log.log_info(f"Input checking took {end - start:.5f} seconds.")
                    return True
            return False
        except Exception as e:
            log.log_error(f"Exception with validating you recovery email address: {e}")

if __name__ == "__main__":
    s = SignupSession()
    print(s.ask_user_input())
import smtplib, random, ssl
class TwoFactorManager:
    def send_2fa_code(self, recovery_email: str) -> None:
        code = str(random.randint(10_000_000, 99_999_999))
        print(code)
        with smtplib.SMTP_SSL("mail.gmx.net", context=ssl.create_default_context()) as server:
            server.login(user="robert.dubois@gmx.de", password="W_y3}d9Lc;)#-B7")
            server.sendmail("robert.dubois@gmx.de", recovery_email, f"2FA Code: {code}")
        return
    def check_2FA_code(self) -> None:
        """
        Method to check if the 2FA code is correct. if yes, nothing is returned.
        But if it is wrong, an 2FAError is raised.         
        """
if __name__ == "__main__":
    f2 = TwoFactorManager()
    f2.send_2fa_code(recovery_email="robert.dubois@gmx.de")
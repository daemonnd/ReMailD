import os
class AdminCheck:
    def check_admin(self):
        if os.name == "posix" and os.geteuid() != 0:
            raise PermissionError("To use args, you have to be root. (use sudo)")
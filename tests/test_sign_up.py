import time
from . . src.sign_up.signup_manager import SignupManager
from . . src.security.account_security.login import LoginManager
sm = SignupManager()
sm.run()
lm = LoginManager()
for i in range(3):
    h = lm.tiny_run()
    if h == True:
        break
start = time.perf_counter()
print(lm.get_data())
end = time.perf_counter()
print(f"Decoding data took {end - start :.5} seconds.")
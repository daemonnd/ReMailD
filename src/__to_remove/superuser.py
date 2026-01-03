import os

def is_superuser():
    isornot = os.geteuid() 
    print(isornot)
    return isornot

isornot = is_superuser()
if isornot == 0:
    print("You are a superuser!")
else:
    print("you are not a superuser!")
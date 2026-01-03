import json
def getAccountPath(): 
    with open(file="./Accounts/accountPaths.json", mode="r") as file:
                accounts: dict = json.load(file)
                sorted_accounts: list = sorted(accounts.keys(), key=int)
                for account in sorted_accounts:
                    value: str = accounts[account]
                    value = value.replace(" ", "")
                    if value != "":
                        account_path = value
                        return account_path
                return ""
getAccountPath()
print(getAccountPath())

            

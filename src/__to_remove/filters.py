# Datei, um Filterfunktionen zu definieren und Filter abzufragen.
# module importieren
import prompt_toolkit
from prompt_toolkit import prompt
#import promtSets
#vali = promtSets.validation()
# Whitelist-Funktionen (w_)
class handle_filters:
    def __init__(self, ):
        pass
    def create_filters(self,msg: str, help: str) -> list:
        """
        Funktion, um einen neuen Filter zu erstellen.
        """
        self.filter: str = (prompt(message=msg, bottom_toolbar=f"Use a ',' between each filter.\n{help}")).replace(" ", "")
        self.filterList: list = self.filter.split(",")
        return self.filterList
    def create_filter_weight(self, name: str) -> int:
        self.weight: str = prompt(message=f"Enter the weight of the filter '{name}': ",
                                  bottom_toolbar="Enter an integer. If the weight is higher, it becomes more important.\nReMailD will compare the weights with the email and deside with the weights it the app should answer or not.",
                                  #validator=vali.PositiveIntValidator())
        )
        return int(self.weight)
    
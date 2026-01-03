"""
ReMailD Json Editor
===================
This file have the class JsonFile which have all
the necessary methods to edit .json files
"""
# importing the modules
import json
from pathlib import Path
import time
from typing import Any
import importlib
import importlib.util
import random
print(f"{random.randint(1, 6)}")
# importing the files
from .launch_reader import launch_data
from .errorprotocol import logger
from .. import exceptions

# initializing classes
log = logger()

# defining th JsonFile class
class JsonFile:
    """
    JsonFile
    ========
    Class for editing, creating and extracting content with .json files
    -------------------------------------------------------------------

    Args:
        full_path:
            The full path of a .json file (for example /home/user/Downloads/json_example.json)
        fill_path: 
            Path from the remaild folder (for example  launch/launch.json)
    Raises:
        ArgumentMissingError:
            If there is one or more args missing
    
    Methods:
    ------------------------------------------------
        read(): 
            Reads the json file
        --------------------------------
        overwrite(`content`: dict):
            clears the file and writes than `content` to json file
        --------------------------------
        update(`key`: list, `value`: Any):
            Updates a value at `key` in a json file by replacing it with the `value`
        --------------------------------
        delete(`key`: list):
            Deleting `key` ant its value
        --------------------------------
        get(`key`: list):
            Reads a specific value at `key`
        --------------------------------
        create(`init`: dict = {}):
            Creates a new json file and inits it with `init`
        --------------------------------
        clear():
            clear the json file
        --------------------------------
        exists():
            check if the file exists
        --------------------------------
        append(`other_content`: dict, `key`: list =[]):

            appending another `other_content` to `key` in the .json file
    
    
   

    """
    def __init__(self, full_path: Path = Path(""), fill_path: Path = Path("")): # full path: full path of .json file, fill_path: path from remaild folder
        # def vars to not get errors
        self.content: dict = {}

        # defining self.jsonfile based on full_path or fill_path given
        if full_path != Path(""):
            self.jsonfile: Path = Path(full_path)
            
        elif fill_path != Path(""):
            self.jsonfile: Path = Path(launch_data.folder / fill_path) # type: ignore
         
        else:
            raise exceptions.ArgumentMissingError("full_path, fill_path", 2)
        
        # check if the file exists, if not it will be created
        if not Path(self.jsonfile).exists():
            log.log_warning(f"The json file {self.jsonfile} does not exist. It will be created.")
            Path(self.jsonfile).touch()
            Path(self.jsonfile).write_text("{}")
        
        # check if self.jsonfile is a valid .json
        if Path(self.jsonfile).is_file(): # checking if it is a file
            pass
            #try:
             #   with open(file=self.jsonfile, mode="r") as file: # if yes, open the file to try it with the .json module
              #      json.load(file) # reading the file (only to check if it is a valid .json)
            
            #except FileNotFoundError as e:
             #   log.log_error(f"FileNotFoundError: {self.jsonfile} has not been found: {e}")
              #  self.jsonfile.touch() # creating the file if it doesn't exist
            #except PermissionError as e:
             #   log.log_error(f"PermissionError: It seems you don't have the rights to open {self.jsonfile}: {e}")
            #except Exception as e:
             #   raise exceptions.InvalidFileError(f"{self.jsonfile} is not a valid .json: {e}") # if the file is invalid, raise an error
        else:
            raise exceptions.IsDirError(f"{self.jsonfile} have to be a valid .json file, not a directory (file required)")

    
    def read(self) -> dict:
        """
        Method for getting the content of the file as dict

        Returns:
            dict:
                The hole content of the .json file
        Raises:
            ReMailD.exceptions.EmptyFileError:
                If the file is empty, invalid or {}
        """
       
        try:
            with open(file=self.jsonfile, mode="r") as file:   # opening the file
                self.content: dict = json.load(file) # type: ignore # saving the file content 
                # if the file is clear
                if not self.content:
                    raise exceptions.EmptyFileError("JSON file is empty")
            return self.content # return the content 
        except FileNotFoundError as e: # if the file haven't been found
            log.log_error(f"FileNotFoundError: {self.jsonfile} haven't been found: {e}") # logging the error
            self.jsonfile.touch() # creating the file
            self.jsonfile.write_text("{}") # writing "{}" to avoid JSONDecodeError for later
            raise exceptions.EmptyFileError(f"The non-existing file {self.jsonfile} can't be read.")
        except json.JSONDecodeError as e: # probably the {} is missing
            log.log_error(f"JSONDecodeError: Maybe the file {self.jsonfile} is completely empty: {e}")    
            self.jsonfile.write_text("{}")
            raise exceptions.EmptyFileError(f"Due to the JSONDecodeError {e}, it is impossible to read {self.jsonfile}")
        except Exception as e:
            log.log_error(f"Exception with reading {self.jsonfile}: {e}")
            raise exceptions.EmptyFileError(f"Due to Exception {e}, it is impossible to correctly read {self.jsonfile}.")
        
    def overwrite(self, content: dict) -> None:
        """
        Method for clearing the file and writing than
        """
        with open(file=self.jsonfile, mode="w") as file:
            #self.jsonfile.touch() # recreating the file to delete its content
            
            json.dump(content, file, indent=4) # writing the content to the file
    def update(self, key: list, value: Any) -> None:

        """
        Method for updating a value in a json file
        Args:
            key: key of the dict that should be updated in a list
            value: value the key should have on the json file after the update.
        Raises:
            ValueError: if the arg 'key' not only contains strings or if value is None or empty
        """
        if not all(isinstance(element, str) for element in key):
            raise ValueError("Arg 'key' list does not only contain strings (strings are required for keys in .json)")
        #if value is None or value == "":
         #   raise ValueError(f"Value {value} can't be '' or None.")
        
        try:
            with open(file=self.jsonfile, mode="r") as file:
                content: dict = json.load(file)
            #print(f"Before update: {content}")  # Debug
        except json.JSONDecodeError as e:
            log.log_error(f"JSONDecodeError in {self.jsonfile}: {e}")
            content = {}  # Initialize empty dict if JSON is invalid
        except FileNotFoundError as e:
            log.log_error(f"FileNotFoundError in {self.jsonfile}: {e}")
            content = {}
        
        try:
            current = content
            for k in key[:-1]:
                current = current.setdefault(k, {})
            current[key[-1]] = value
            #print(f"After update: {content}")  # Debug
            with open(self.jsonfile, mode="w") as file:
                json.dump(content, file, indent=4)
        except Exception as e:
            log.log_error(f"Exception updating {self.jsonfile}: {e}")
            raise  # Re-raise to catch issues upstream

    def delete(self, key: list) -> None:
        """
        Method for deleting a key and its value

        Args:
            key: 
                The dictionary path as list (for dict["data"]["value1"] it would be ["data", "value1"])
        Raises:
            ValueError:
                if the arg 'key' not only contains strings (strings are required in .json for key) 
        """

        # checking if key is a list of strings
        if all(isinstance(element, str) for element in key):
            pass
            #log.log_debug("'key' only contains strings!")
        else:
            raise ValueError("The JsonFile Method 'update' arg 'key' list does not only contain strings (strings are required for keys in .json)")
        with open(file=self.jsonfile, mode="r") as file:
            # reading the file
            content: dict = json.load(file)

        # going through the dict to find the exact key to delete it
        try:
            current = content
            for k in key[:-1]:
                current = current[k]
            del current[key[-1]]

            # writing the deleted file version
            with open(self.jsonfile, mode="w") as file:
                json.dump(content, file, indent=4)
        except KeyError as e:
            log.log_error(f"KeyError in {self.jsonfile}: {e}")
            return
        except Exception as e:
            log.log_error(f"Exception with {self.jsonfile}: {e}")
            return
        
    def get(self, key: list) -> Any:
        """
        Method to read a specified value of a json file.

        Args:
            key: 
                The dictionary path as list (for dict["data"]["value1"] it would be ["data", "value1"])
        Raises:
            ValueError:
                if the arg 'key' not only contains strings (strings are required in .json for key) 

        """
         # checking if key is a list of strings
        if all(isinstance(element, str) for element in key):
            pass
            #log.log_debug("'key' only contains strings!")
        else:
            raise ValueError("The JsonFile Method 'update' arg 'key' list does not only contain strings.")
        
        # opening and reading the file
        with open(file=self.jsonfile, mode="r") as file:
            content: dict = json.load(file)

        # going through the dict to find the exact key to read
        try:
            current = content
            for k in key[:-1]:
                current = current[k]
            return current[key[-1]]
        except KeyError as e:
            log.log_debug(f"The .json file: {self.jsonfile} could't give the necessary info: {e}")
            raise KeyError
        except Exception as e:
            log.log_error(f"Exception with {self.jsonfile}: {e}")
            raise e
        
    def create(self, init: dict = {}) -> None:
        """
        Method for creating the file and initializing it with init
        Args:
            init:
                with what the file is initialized (default: {})
        """
        self.jsonfile.touch()
        with open(file=self.jsonfile, mode="w") as file:
            json.dump(init, file)
    
    def clear(self) -> None:
        """
        Method to clear the json file, deleting the hole content.
        """
        if Path(self.jsonfile).is_file():
            Path(self.jsonfile).unlink()
            pass
            #log.log_debug(f"The file {self.jsonfile} have been deleted.")
        if Path(self.jsonfile).is_dir():
            Path(self.jsonfile).rmdir()
            log.log_warning(f"{self.jsonfile} is a directory but it have been deleted.")
    def exists(self) -> bool:
        """
        Method to check if the .json file exists

        Returns:
            bool:
                True if the .json file exists
                
                False if the .json does not exists

        """
        return self.jsonfile.exists()
    def append(self, other_content: dict, key: list = []) -> None:
        """
        Method to append another dict to the .json file with writing mode 'a'.
        Args:
            other_content: dict:
                The dict that will be added at the key position of the .json file
            key:
                Where the content [other_content] will be added
        Raises:
            ValueError:
                if the arg 'key' not only contains strings (strings are required in .json for key) 

        """
          # checking if key is a list of strings

        if all(isinstance(element, str) for element in key):
            pass
            #log.log_debug("'key' only contains strings!")
        else:
            raise ValueError("The JsonFile Method 'append' arg 'key' list does not only contain strings.")
        
        # opening the file and save its content as var
        with open(self.jsonfile, mode="r") as file:
            content: dict = json.load(file)
        try:
            # if key is []
            if not key:
                content.update(other_content) # updating the var with other_content
            # if key is not []
            else:
                # updating the var with other_content
                current = content
                for k in key[:-1]:
                    current = current[k]
                    current[key[-1]] = other_content
            
            # opening the file and writing the updated content
            with open(self.jsonfile, mode="w") as file:
                json.dump(content, file, indent=4)
        
        except KeyError as e:
            log.log_error(f"KeyError in {self.jsonfile}: {e}")
            return
        except Exception as e:
            log.log_error(f"Exception with {self.jsonfile}: {e}")
            return
    def repair(self, help: str = "") -> str:
        """
        Method that tries to repair a .json file that have problems
        
        """
        # extracting the content (without json module to not get any errors)
        content: str = Path(self.jsonfile).read_text()
        
        return str(content)
        with open(file=self.jsonfile, mode="w") as file:
            pass
    def get_key_count(self) -> int:
        return len(self.read())
        


if __name__ == "__main__":
    file = JsonFile(fill_path=Path("test.json"))

  
    print(file.repair())

    
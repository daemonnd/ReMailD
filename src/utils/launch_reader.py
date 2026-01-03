"""
File for loading launch data (lang, logging level, ...)
"""
from dataclasses import dataclass
import pathlib
from pathlib import Path
import json
import os
import time
from pprint import pformat
from typing import *

from . import errorprotocol

log = errorprotocol.logger()


folder: Path = Path(__file__).parent.parent.parent

@dataclass
class LaunchData:
    """
    @dataclass for saving the launch data in the ram and making it easily accessible for other files.

    Raises:
        SyntaxError:
            If app_directory haven't been defined.
        FileNotFoundError:
            If the directory app_directory doesn't exist
    """

    iterations: int 
    logging_level: str | int 
    lang: str 
    repeat_range: int 
    email_check_interval: int 
    dklen: int 
    folder: Path = Path(__file__).parent.parent.parent
    launchfile: Path = Path(folder / "launch.json")
    
    def load_launch_data(self, launchfile: Path) -> Self:
        """
        Method to move the launch data to the ram
        """
        
        for i in range(3):
            try:
                with open(file=Path(launchfile), mode="r") as file: # opening the file
                    content = json.load(fp=file) # getting the file content
                    pformat(content)
            except FileNotFoundError as e:
                log.log_error(f"FileNotFoundError: {e}")
                launchfile.touch() # creating the launchfile if it is missing. 
                time.sleep(1)
            except json.JSONDecodeError as e:
                log.log_error(f"JSONDecodeError: {e}")
                launchfile.write_text("""
                    {
                        "lang": "en", 
                        "logging_level": "INFO", 
                        "repeat_range": 5,
                        "email_check_interval": 120,
                    }""")  # writing '{}' on the file, it often solves the error
            except KeyError as e:
                log.log_critical(f"KeyError: It seems the launch file is empty: {e}")
            
            except Exception as e:
                log.log_warning(f"Exception with opening and reading launch data: {e}")
            else:
                
                for field in self.__dataclass_fields__:
                    if field in content:
                        
                        setattr(self, field, content[field])
                        break
        # validating json file values
        # validating logging level
        if isinstance(content["logging_level"], str):
            if content["logging_level"] not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
                log.log_error(f"ValueError: Value 'logging_level' in {launchfile} must be a valid log level string or other types.")
                exit(2)
        elif not isinstance(content["logging_level"], int) or content["logging_level"] < 0 or content["logging_level"] > 50:
            log.log_error(f"ValueError: Value 'logging_level' in {launchfile} must be an integer between 0 and 50.")
            exit(2)
        
        # validating lang
        if not isinstance(content["lang"], str):
            log.log_error(f"ValueError: Value 'lang' in {launchfile} have to be a string.")
            exit(2)
        if isinstance(content["lang"], str):
            if content["lang"] not in ["en", "de", "fr", "es"]:
                log.log_error(f"ValueError: Value 'lang' in {launchfile} have to be one of these options: en, es, fr, de, not {content["lang"]}")
                exit(2)
        
        # validating repeat range
        if not isinstance(content["repeat_range"], int) or self.repeat_range <= 0:
            log.log_error(f"ValueError: Value 'repeat_range' in {launchfile} have to be a positive integer, not {content["repeat_range"]}")
            exit(2)
            
        # validating the email check interval
        if not isinstance(content["email_check_interval"], int):
            log.log_error(f"ValueError: Value 'email_check_interval' in {launchfile} have to be a positive integer, no string.")
            exit(2)
        if isinstance(content["email_check_interval"], int):
            if not content["email_check_interval"] > 0:
                log.log_error(f"ValueError: Value 'email_check_interval' in {launchfile} have to be bigger or equal to 1. (Higher than 60 recommended)")
                exit(2)

        # if there are no errors
        return self


# creating an instance of the @dataclass

launch_data_init: LaunchData = LaunchData(
        launchfile=Path(folder / "launch.json"),
        iterations=20_000_000,
        logging_level="INFO",
        lang="en",
        repeat_range=3,
        email_check_interval=60,
        dklen=32
    )

# saving the instance as var
launch_data: LaunchData = launch_data_init.load_launch_data(launchfile=launch_data_init.launchfile)
if __name__ == "__main__":
  
    print(f"launch file: {launch_data.launchfile}")
    print(f"project folder: {launch_data.folder}")
    print(f"launch lang: {launch_data.lang}")
    print(f"logging level: {launch_data.logging_level}")
    print(f"repeat range: {launch_data.repeat_range}")
    print(f"email check interval: {launch_data.email_check_interval}")
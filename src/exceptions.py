"""
file for custom remaild exceptions (general)
"""
class ArgumentMissingError(Exception): 
    """
    if a class or func argument is missing
    """
    def __init__(self, args: str, args_number: int = 1):
      
        message: str = f"The following {args_number} arg(s) is missing: {args}" 
        super().__init__(message)
class EmptyFileError(Exception):
    """
    If the selected file is empty or invalid
    """
    def __init__(self, msg: str = "The file is empty and can't be read."):
        super().__init__(msg) 
class IsDirError(Exception):
    """
    If the path is a directory but not a file (file required)
    """
    def __init__(self, *args):
        super().__init__(*args)
class IsFileError(Exception):
    """
    If the path is a directory but not a file (directory required)
    """
    def __init__(self, *args):
        super().__init__(*args)
class InvalidFileError(Exception):
    """
    If the file is invalid
    """
    def __init__(self, *args):
        super().__init__(*args)
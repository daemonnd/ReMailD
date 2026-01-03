"""
File for other, smaller utils
"""
import grapheme

def unique_list(l: list) -> list:
    """
    Func for deleting all entries that are at least twice in the list
    """
    unique: list = []
    for entry in l:
        if entry not in unique:
            unique.append(entry)
    return unique


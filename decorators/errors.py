from typing import List, Dict
from classes.error_classes import InputRequired
from classes.main_classes import AddressBook


def input_error(func):
    def inner(args: List[str], book: AddressBook):
        try:
            return func(args, book)
        except (ValueError, IndexError) as e:
            return "Enter the argument for the command"
        except InputRequired as e:
            return f"Enter the '{e}' argument for the command"
        except Exception as e:
            return e

    return inner


def contact_exists(expected: bool = True):
    def decorator(func):
        def inner(args: List[str], book: AddressBook):
            name = args[0]
            exists = book.find(name)
            if expected and not exists:
                return "Contact not found."
            if not expected and exists:
                return "Contact already exists."
            return func(args, book)

        return inner

    return decorator

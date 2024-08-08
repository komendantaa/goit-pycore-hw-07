from typing import List, Dict, cast
from decorators.errors import input_error, contact_exists
from utils.utils import parse_input
from datetime import date
from classes.main_classes import AddressBook, Record, Birthday


@input_error
# @contact_exists(False)
def add_contact(args: List[str], book: AddressBook) -> str:
    name, phone, *_ = args
    record = book.find(name)
    if record:
        record.put_phone(phone)
        return "Contact updated."
    record = Record(name)
    record.put_phone(phone)
    book.add_record(record)
    return "Contact added."


@input_error
@contact_exists()
def change_contact(args: List[str], book: AddressBook) -> str:
    name, curr_phone, new_phone, *_ = args
    record = book.find(name)
    record = cast(Record, record)
    record.edit_phone(curr_phone, new_phone)
    return "Contact changed."


@input_error
@contact_exists()
def show_phone(args: List[str], book: AddressBook) -> Record | None:
    name = args[0]
    return book.find(name)


@input_error
@contact_exists()
def delete_contact(args: List[str], book: AddressBook) -> str:
    name = args[0]
    book.delete(name)
    return "Contact removed."


@input_error
@contact_exists()
def add_birthday(args: List[str], book: AddressBook) -> str:
    name, birthday, *_ = args
    record = book.find(name)
    record = cast(Record, record)
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
@contact_exists()
def show_birthday(args: List[str], book: AddressBook) -> Birthday | None:
    name = args[0]
    record = book.find(name)
    record = cast(Record, record)
    return record.birthday


@input_error
def birthdays(args: List[str], book: AddressBook) -> List[Dict[str, date]]:
    return book.get_upcoming_birthdays()


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        cmd, args = parse_input(user_input)

        """
            TODO: remove

            Commands looks not so consistent and flexible for me.
            add     - add contact
            change  - change phone only. In which way to change phone if have an array of phones? Replace? What if I want to add phone?
            phone   - show phone. Why subject "phone" between actions?
            delete  - delete contact. How to delete only 1 phone or remove just birthday?
            all     - show all contacts.
            birthdays - whow upcoming birthdays.
            add-birthday, show-birthday - not consistent with previous....

            Suggestion:
                <action> <subject or subject alias> [...args]

            contacts (c, contact):
                add c <name> <phone> [<date>] - I think it's better throw err if exists.
                show c <name>
                delete c <name>
                all
            phones (p, phone):
                add p <name> <phone>
                show p <name>
                update p <name> <prev_phone> <new_phone>
                delete p <name> <phone>
            birthdays (b, b-day, birthday):
                add b <name> <date>
                show b <name>
                update b <name> <date>
                delete b <name> <phone>

            
            Can I use this structure next time ?
        """

        if cmd in ["close", "exit"]:
            print("Goodbye!")
            break
        elif cmd == "hello":
            print("How can I help you?")
        elif cmd == "add":
            print(add_contact(args, book))
        elif cmd in ["change", "update"]:
            print(change_contact(args, book))
        elif cmd in ["phone", "show"]:
            print(show_phone(args, book))
        elif cmd in ["delete", "remove"]:
            print(delete_contact(args, book))
        elif cmd == "add-birthday":
            print(add_birthday(args, book))
        elif cmd == "show-birthday":
            print(show_birthday(args, book))
        elif cmd == "birthdays":
            print(birthdays(args, book))
        elif cmd == "all":
            print(book)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()

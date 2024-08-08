from typing import List, Optional, Dict
from collections import UserDict
from datetime import datetime, timedelta, date
from .error_classes import InputRequired, PhoneInvalid, BirthdayInvalid

WEEK = 7
WORKING_DAYS = 5


class Field:
    def __init__(self, value):
        self.value = value

    def __repr__(self) -> str:
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value: str):
        self.__validate(value)
        super().__init__(value)

    def update(self, phone: str) -> None:
        self.__validate(phone)
        self.value = phone

    def __validate(self, phone: str) -> None:
        if not phone.isdigit() or len(phone) != 10:
            raise PhoneInvalid(f"Invalid phone number: {phone}")


class Birthday(Field):
    def __init__(self, value):
        self.__validate(value)
        super().__init__(value)

    def __validate(self, value: str) -> None:
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise BirthdayInvalid("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name: Name = Name(name)
        self.phones: List[Phone] = []
        self.birthday = None

    def __repr__(self) -> str:
        phones_str = "; ".join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {self.birthday or '-'}"

    def put_phone(self, phone: str) -> None:
        found = self.find_phone(phone)
        if not found:
            self.phones.append(Phone(phone))

    def edit_phone(self, curr_phone: str, new_phone: str) -> None:
        found = self.find_phone(curr_phone)
        if found:
            found.update(new_phone)

    def find_phone(self, phone: str) -> Phone | None:
        for _phone in self.phones:
            if _phone == phone:
                return _phone
        return None

    def remove_phone(self, phone: str) -> None:
        self.phones = [p for p in self.phones if p.value != phone]

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self) -> List[Dict[str, date]]:
        today = datetime.today().date()
        event_from = today
        event_to = today + timedelta(days=WEEK)

        result: List[Dict[str, date]] = []

        for contact in self.data.values():
            b_day = datetime.strptime(contact.birthday.value, "%d.%m.%Y").date()
            b_day = b_day.replace(year=today.year)
            if b_day < event_from or b_day > event_to:
                continue
            if b_day.isoweekday() > WORKING_DAYS:
                correct_to_monday = 1 if b_day.isoweekday() - WORKING_DAYS == 2 else 2
                b_day = b_day + timedelta(days=correct_to_monday)
            result.append({"name": contact.name, "congratulation_date": b_day})

        return result

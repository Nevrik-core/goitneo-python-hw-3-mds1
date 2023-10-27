from datetime import datetime, timedelta
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not str(value).isdigit():
            # print("Phone number should contain only digits.")
            raise ValueError("Phone number should contain only digits.")


        if len(str(value)) != 10:
            # print("Phone number should contain 10 digits.")
            raise ValueError("Phone number should contain 10 digits")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Should be DD.MM.YYYY")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return

    def edit_phone(self, old_phone, new_phone):
        new_phone_obj = Phone(new_phone)
        self.remove_phone(old_phone)
        self.add_phone(new_phone_obj)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
            
    def add_birthday(self, date):
        self.birthday = Birthday(date)
            
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value if self.birthday else 'N/A'}"


class AddressBook(UserDict):
    def add_record(self, name, phone):
        record = Record(name)
        record.add_phone(phone)
        self.data[record.name.value] = record
        print(f"Added {record.name.value} to the address book.")

    def change_phone(self, name, new_phone):
        record = self.find(name)
        if record:
            try:
              record.edit_phone(record.phones[0].value, new_phone)
              return f"Phone number for {name} changed."
            except ValueError as e:
                return f"Value error: {e}"

        else:
            return f"Contact {name} not found."


    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            print(f"{name} was deleted from the address book.")
        else:
            print(f"{name} was not found in the address book.")


    def get_birthdays_per_week(self):
        today = datetime.today().date()
        birthdays = {}

        for name, record in self.data.items():
            if record.birthday:
                birthday_str = record.birthday.value
                birthday = datetime.strptime(birthday_str, '%d.%m.%Y').date()
                birthday_this_year = birthday.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday.replace(year=today.year + 1)
                delta_days = (birthday_this_year - today).days
                if delta_days < 7:
                    day_of_week = (today + timedelta(days=delta_days)).strftime('%A')
                    if day_of_week == "Saturday" or day_of_week == "Sunday":
                        day_of_week = "Monday"
                    birthdays.setdefault(day_of_week, []).append(name)

        for day, names in birthdays.items():
            print(f"{day}: {', '.join(names)}")
    

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Value error: {e}"
        except KeyError:
            return "This contact does not exist."
        except IndexError:
            return "Incorrect number of arguments."
    
    return inner


@input_error
def add_contact(args, book):
    name, phone = args
    book.add_record(name, phone)
    return "Contact added."

@input_error
def change_contact(args, book):
    name, phone = args
    return book.change_phone(name, phone)
    


@input_error
def add_birthday(args, book):
    name, date = args
    record = book.find(name)
    if record:
        record.add_birthday(date)
        return f"Birthday added for {name}."
    else:
        return "This contact does not exist."
    

@input_error
def get_phone(args, book):
    name, = args
    record = book.find(name)
    if record:
        return str(record.phones[0].value)
    else:
        return "Contact not found."
    
@input_error
def list_all_contacts(_, book):
    all_contacts = '\n'.join([f"{name}: {str(record.phones[0].value)}" for name, record in book.data.items()])
    if all_contacts:

        return all_contacts
    else:
        return "Phone book is empty"

@input_error
def show_birthday(args, book):
    name, = args
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is on {record.birthday.value}."
    elif record:
        return f"No birthday data for {name}."
    else:
        return "This contact does not exist."


def list_birthdays(book):
    book.get_birthdays_per_week()

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye! I'm stepping through the door!")
            break
        elif command == "hello":
            print("How can I help you? Do you hear me, Major Tom?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(get_phone(args, book))
        elif command == "all":
            print(list_all_contacts(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            list_birthdays(book)
        else:
            print("Invalid command. Can you hear me, Major Tom?")

if __name__ == "__main__":
    main()


 
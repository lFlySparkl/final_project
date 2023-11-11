# 1.зберігати контакти з іменами, адресами, номерами телефонів, email та днями народження до книги контактів;       %%% Реализовано
# 2.виводити список контактів, у яких день народження через задану кількість днів від поточної дати;                %%% Создать новую функцию (доработка функции из дз 8) 
# 3.перевіряти правильність введеного номера телефону та email під час створення або редагування запису             %%% Нужно добавить
# та повідомляти користувача у разі некоректного введення;                                                          %%% Частично сделанно, доработка проверки при редактировании (возможно исправление проверки)
# 4.здійснювати пошук контактів серед контактів книги;                                                              %%% Реализовано
# 5.редагувати та видаляти записи з книги контактів;                                                                %%% Реализовано
# 6.зберігати нотатки з текстовою інформацією;                                                                      %%% Создать новую функцию (сохраняем как текст, если захотим можно сделать доп функционал под каждый контакт, с выводом в дальнейшем)
# 7.проводити пошук за нотатками;                                                                                   %%% Создать новую функцию
# 8.редагувати та видаляти нотатки;                                                                                 %%% Создать новую функцию (каждый раз вводится новые записи или только одни и их мы сможем редактировать)
# 9.додавати в нотатки "теги", ключові слова, що описують тему та предмет запису;                                   %%% Создать новую функцию (предполагаю что записи будем сохранять в виде ключа(тега) и значения)
# 10.здійснювати пошук та сортування нотаток за ключовими словами (тегами);                                         %%% Создать новую функцию (поиск будет совершатся по ключам и мы сможем редактировать значение, если контакт захочет при регистрации поменять тему записи то значит мы перезапишем, старую удаляем и записываем как новую)
# 11.сортувати файли у зазначеній папці за категоріями (зображення, документи, відео та ін.).                       %%% Реализовано
# 12.Додаткове ускладнене завдання: Бот повинен аналізувати введений текст і намагатися вгадати,                    %%% Пока фиг знает как такое делать (пока забить и так много всего)
# що хоче від нього користувач і запропонувати найближчу команду для виконання
# 13.Реализация команды "help" которая выводит все доступные команды бота                                           %%% Реализовано
# 14.Переработка всего проекта под классы, продумать как будут вводится команды                                     %%% Нужно для того чтобы все было красиво и не было стыдно показать проект
# (тоесть через инпут вводим команду, если такая есть в массиве то выводим текстовое сообщение,
#  какое количество и каких данных нужно ввести, или просто через пару инпутов)
# 15.Реализовать управление через команды с консоли пример дз 9                                                     %%% В процессе
# 16.проєкт має бути збережений в окремому репозиторії та бути загальнодоступним (GitHub, GitLab або BitBucket);    %%% Сохраняем на гите
# 17.проєкт містить докладну інструкцію щодо встановлення та використання;                                          %%% Создать инструкцию
# 18.проєкт встановлюється як Python-пакет та може бути викликаний у будь-якому місці системи                       %%% Создать установщик, пример clean_folder
# відповідною командою після встановлення;
# 19.проєкт повністю реалізує мінімум 8 вимог із 12 описаних у завданні;
# 20.персональний помічник зберігає інформацію на жорсткому диску в папці користувача                               %%% В процессе
# і може бути перезапущений без втрати даних.

# 21.ваши предложения
# так как у нас недостаток людей то первоочередно делаем самые нужные модули если останется время можно допилить еще что-то

from distutils.command import clean
import os
import pickle
import clean

from collections import UserDict
from datetime import date, datetime
# from typing import Self


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    ...


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if len(new_value) != 10 or not new_value.isdigit():
            raise ValueError("Invalid phone number, should contain 10 digits")
        else:
            self.__value = new_value

    def __str__(self):
        return f"Phone: {self.value}"


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        try:
            chek_data = datetime.strptime(new_value, "%Y-%m-%d")
            if chek_data:
                self.__value = new_value
        except:
            raise ValueError("Invalid data format")


class Record:
    def __init__(self, name, phone=None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []

    def add_phone(self, phone):
        new_phone = "".join(filter(str.isdigit, phone))
        # if len(new_phone) != 10:
        #     print(f"Invalid phone length: {new_phone}")
        # try:
        self.phones.append(Phone(new_phone))
        # except:
        #     raise ValueError("Not enough number setter")

    def edit_phone(self, old_phone, new_phone):
        found = False
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                found = True
        if not found:
            raise ValueError(f"The phone {old_phone} is not found.")
            # return f"The phone {old_phone} is not found."

    def find_phone(self, phone: str):
        for ph in self.phones:
            if ph.value == phone:
                return ph
        return None

    def remove_phone(self, phone):
        del_phone = None
        for ph in self.phones:
            if ph.value == phone:
                del_phone = ph
        self.phones.remove(del_phone)

    def add_birthday(self, birthday=None):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        today = date.today()
        d_bd = datetime.strptime(self.birthday.value, "%Y-%m-%d")
        if d_bd.month - today.month < 0:
            next_bd = date(2024, d_bd.month, d_bd.day)
            delta_days = next_bd - today
            return delta_days.days
        else:
            if d_bd.day - today.day < 0:
                next_bd = date(2024, d_bd.month, d_bd.day)
                delta_days = next_bd - today
                return delta_days.days
            else:
                next_bd = date(2023, d_bd.month, d_bd.day)
                delta_days = next_bd - today
                if delta_days.days == 0:
                    return "today"
                else:
                    return delta_days.days

    def __str__(self):
        try:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday {self.birthday}"
        except:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, new_contact: Record) -> None:
        self.data[new_contact.name.value] = new_contact
        print(self.data)
        return f"Contact {new_contact.name.value} added succefully"

    def find(self, name):
        for rec in self.data:
            if rec == name:
                return self.data[rec]
        if not self.data.get(name):
            return None

    def search(self, arg):
        return_str = "didn'd find number or characters"
        for rec, phone in self.data.items():
            # print(rec, phone)
            if arg in str(phone):
                if return_str == "didn'd find number or characters":
                    return_str = ""
                return_str += str(self.data[rec]) + "\n"
            # else:
            #     return "didn'd find number or characters"
        return return_str

    def delete(self, name):
        if not self.data.get(name):
            return f"did't delete contact {name}, not exsist"
        else:
            del self.data[name]
            return f"Contact {name} delete succsefull"

    def iterator(self, n=2):
        self.counter = 0
        self.list = []
        # self.data_list = list(self.data.items())
        if len(self.data) >= 1:
            for _, val in self.data.items():
                self.list.append(str(val))
            while self.counter < len(self.list):
                yield self.list[self.counter : self.counter + n]
                self.counter += n
            raise StopIteration("End of list")
        else:
            raise StopIteration("Empty list")

    def pack_user(self):
        file_name = "C:\\py_robot\\users.bin"
        with open(file_name, "wb") as fh:
            print(self.data)
            pickle.dump(self.data, fh)

    def unpack_user(self):
        file_name = "C:\\py_robot\\users.bin"

        if os.path.exists(file_name):
            with open(file_name, "rb") as file:
                unpacked = pickle.load(file)

            for name, object in unpacked.items():
                self.data[name] = object
        else:
            return "File not found."



records = AddressBook()


def search(*args):
    return records.search(*args)


# def save_ab(*args):
#     records.save_address_book()
#     return "Address book saved successful"


# def load_ab(*args):
#     global records
#     load_records = records.load_address_book()
#     records = load_records
#     return "Address book loaded successful"


def user_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Give me name and phone please"
        except KeyError:
            return "Enter correct user name"
        except RuntimeError:
            return "Nothing more. End of list"
        except StopIteration as e:
            if str(e) == "End of list":
                return "End of list"
            if str(e) == "Empty list":
                return "Empty list"
            else:
                raise e
        except ValueError as e:
            if str(e) == "Not enough number":
                return "Not enought number"
            if str(e) == "Invalid data format":
                return "Invalid data format"
            if str(e) == "Invalid phone number, should contain 10 digits":
                return "Invalid phone number, should contain 10 digits"
            else:
                raise e  # Піднімаэмо помилку наверх, якщо вона іншого типу

    return inner


def sanitize_phone_number(phone):
    collected_phone = ""
    for ch in phone:
        collected_phone += ch
    new_phone = (
        collected_phone.strip()
        .removeprefix("+38")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace(" ", "")
    )
    return new_phone


def sanitize_db(db):
    collected_db = ""
    for ch in db:
        collected_db += ch
    new_db = (
        collected_db.strip()
        .replace(" ", "-")
        .replace("(", "")
        .replace(")", "")
        .replace(".", "-")
        .replace(",", "-")
        .replace("/", "-")
        .replace("\\", "-")
    )
    return new_db


@user_error
def add_record(*args):
    name = args[0]
    phone_number = sanitize_phone_number(args[1:])
    if not records.data.get(name):
        name_record = Record(name)
        name_record.add_phone(phone_number)
        records.add_record(name_record)
        print(records)
    else:
        name_record = records.data.get(name)
        name_record.add_phone(phone_number)
    return f"Add record {name = }, {phone_number = }"


@user_error
def bd_add(*args):
    name = args[0]
    bd = sanitize_db(args[1:])
    if not records.data.get(name):
        name_record = Record(name)
        name_record.add_birthday(bd)
        records.add_record(name_record)
    else:
        name_record = records.data.get(name)
        name_record.add_birthday(bd)
    return f"Add record {name = }, {bd = }"


def days_to_bd(*args):
    try:
        name = args[0]
        if name:
            if records.data.get(name):
                name_record = records.data.get(name)
                try:
                    result = name_record.days_to_birthday()
                    if result:
                        if result == "today":
                            return f"To {name } birthday today"
                        else:
                            return f"To {name } birthday,  left {result} days"
                    else:
                        return f"To {name } no data birthday"
                except:  # AttributeError as e:
                    return f"No birthday date for {name}"
            else:
                return f"No contact find {name}"
    except:  # AttributeError as e:
        return "No contact input"


@user_error
def change_record(*args):
    name = args[0]
    old_phone_number = sanitize_phone_number(args[1])
    new_phone_number = sanitize_phone_number(args[2])
    if not records.data.get(name):
        raise ValueError("wrong name")
    else:
        try:
            name_record = records.data.get(name)
            name_record.edit_phone(old_phone_number, new_phone_number)
            return f"Change record {name = }, {new_phone_number = }"
        except:
            return f"The phone {old_phone_number} is not found."


def delete_record(*args):
    name = args[0]
    records.delete(name)
    return f"Contact name: {name}, delete successfull"


def unknown_cmd(*args):
    return "Unknown command. Try again. Or use 'help'"


def hello_cmd(*args):
    return "How can I help you?"


def help_cmd(*args):
    return_str = "\n"
    cmd_list = [
        "avalible command:",
        "hello - just say hello",
        "help - show avalible cmd",
        "add - add record - format 'name phone'",
        "bd_add - add birthdayd - format 'name date birthday (YYYY-MM-DD)'",
        "days_to_bd - days to birthday",
        "change - change record - format 'name old phone new phone'",
        "delete - delete record - format 'name'",
        "phone - get phone by name - format 'phone name'",
        "show_all - show all phone book",
        "sort_folder - sort dirty folder by Audio, Docs, Archives, Music, Images, Other"
        "save_ab - save address book",
        "search - search by characters in name, or by digits in phone"
        "load_ab - load address book",
        "good bye/close/exit - shotdown this script",
    ]
    for ch in cmd_list:
        return_str += ch + "\n"
    return return_str


@user_error
def get_phone(*args):
    name = args[0]
    rec = records.find(name)
    if rec:
        return rec

def sort_folder(*args):
    path = str(input("Write path to folder: "))
    if os.path.exists(path):
        clean.main(path)
    else:
        return "Path not exist."

# @user_error
def show_all(*args):
    n = None
    try:
        n = int(args[0])
        if n is not None:
            return_lst_result = []
            if len(records) >= 1:
                for cont in records.iterator(n):
                    return_lst = []
                    for ch in cont:
                        new_ch = (
                            str(ch)
                            .strip()
                            .replace("(", "")
                            .replace(")", "")
                            .replace("'", "")
                        )
                        return_lst.append(new_ch)
                    return_lst_result.append(return_lst)
                return return_lst_result
            else:
                return "Empty"
    except:
        if n is None:
            return_str = "\n"
            if len(records.data) >= 1:
                for _, numbers in records.data.items():
                    return_str += str(numbers) + "\n"
                return return_str
            else:
                return "Empty"
        else:
            return return_lst_result  # "No records to show"


def close_cmd(*args):
    return "Good bye!"


COMMANDS = {
    add_record: "add",
    # add_phone: "add phone",
    # edit_phone: "edit phone",
    bd_add: "bd_add",
    days_to_bd: "days_to_bd",
    delete_record: "delete",
    change_record: "change",
    hello_cmd: "hello",
    get_phone: "phone",
    show_all: "show_all",
    sort_folder: "sort_folder",
    # save_ab: "save_ab",
    # load_ab: "load_ab",
    search: "search",
    help_cmd: "help",
    close_cmd: ("good bye", "close", "exit"),
}


def parser(text: str):
    for func, kw in COMMANDS.items():
        if text.lower().startswith(kw):
            return func, text[len(kw) :].strip().split()
    return unknown_cmd, []


def main():
    book = AddressBook()
    book.unpack_user()
    print(book)
    while True:
        user_input = input("Write comand:")
        func, data = parser(user_input)
        if func == show_all and data:
            result1 = show_all(*data)
            if result1 != "Empty":
                for el in result1:
                    input("Press Enter for see next records")
                    for cont in el:
                        print(cont)
                input("Press Enter to exit, and input new command")
            else:
                print(func(*data))
        else:
            print(func(*data))
        if func == close_cmd:
            book.pack_user()
            print(book)
            break


if __name__ == "__main__":
    main()

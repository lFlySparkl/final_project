# 1.зберігати контакти з іменами, адресами, номерами телефонів, email та днями народження до книги контактів;       %%% Реализовано
# 2.виводити список контактів, у яких день народження через задану кількість днів від поточної дати;                %%% Реализовано 
# 3.перевіряти правильність введеного номера телефону та email під час створення або редагування запису 
# та повідомляти користувача у разі некоректного введення;                                                          %%% Реализовано
# 4.здійснювати пошук контактів серед контактів книги;                                                              %%% Реализовано
# 5.редагувати та видаляти записи з книги контактів;                                                                %%% Реализовано
# 6.зберігати нотатки з текстовою інформацією;                                                                      %%% Реализовано
# 7.проводити пошук за нотатками;                                                                                   %%% Реализовано
# 8.редагувати та видаляти нотатки;                                                                                 %%% Реализовано
# 9.додавати в нотатки "теги", ключові слова, що описують тему та предмет запису;                                   %%% Реализовано
# 10.здійснювати пошук та сортування нотаток за ключовими словами (тегами);                                         %%% Создать новую функцию (поиск будет совершатся по ключам и мы сможем редактировать значение, если контакт захочет при регистрации поменять тему записи то значит мы перезапишем, старую удаляем и записываем как новую)
# 11.сортувати файли у зазначеній папці за категоріями (зображення, документи, відео та ін.).                       %%% Реализовано
# 12.Додаткове ускладнене завдання: Бот повинен аналізувати введений текст і намагатися вгадати,                    %%% Реализовано
# що хоче від нього користувач і запропонувати найближчу команду для виконання
# 13.Реализация команды "help" которая выводит все доступные команды бота                                           %%% Реализовано
# 14.Реализовать управление через команды с консоли пример дз 9                                                     %%% Реализовано
# 15.проєкт має бути збережений в окремому репозиторії та бути загальнодоступним (GitHub, GitLab або BitBucket);    %%% Сохраняем на гите
# 16.проєкт містить докладну інструкцію щодо встановлення та використання;                                          %%% Создать инструкцию
# 17.проєкт встановлюється як Python-пакет та може бути викликаний у будь-якому місці системи                       %%% У меня не работает
# відповідною командою після встановлення;
# 18.проєкт повністю реалізує мінімум 8 вимог із 12 описаних у завданні;                                            %%% 15 из 19
# 19.персональний помічник зберігає інформацію на жорсткому диску в папці користувача                               %%% Реализовано
# і може бути перезапущений без втрати даних.

from genericpath import exists
import os
import pickle
import sort_folder
import re
import notes
from birthday import get_birthdays_per_week as birthday_from_now
from convert import convert_str_dict
from collections import UserDict
from datetime import date, datetime
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


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
    def self_name(self, name):
        self.__privat_name = None
        self.name = name
        return str(self.name)

    @property
    def name(self):
        return self.__privat_name

    @name.setter
    def name(self, name: str):
        if name.isalpha():
            self.__privat_name = name
        else:
            raise Exception("Wrong name")

class Location(Field):
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

class Mail(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        patern_mail = r"[A-z.]+\w+@[A-z]+\.[A-z]{2,}"
        try:
            if bool(re.match(patern_mail, value)):
                self.__value = value
            else:
                raise ValueError("Mail should have the following format nickname@domen.yy")
        except ValueError as e:
            raise ValueError("Mail should have the following format nickname@domen.yy") from e


    # def __str__(self):
    #     return f"Mail: {self.__value}"
    def __str__(self) -> str:
        return f"Mail: {self.__value}"
    
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
    def __init__(self, name, phone = None, mail = None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []
        # print(self.phones)
        self.mails = [Mail(mail)] if mail else []
        # print(self.mails)

    def add_phone(self, phone):
        new_phone = "".join(filter(str.isdigit, phone))
        # if len(new_phone) != 10:
        #     print(f"Invalid phone length: {new_phone}")
        # try:
        self.phones.append(Phone(new_phone))
        # except:
        #  raise ValueError("Not enough number setter")

    def add_location(self, location):
        self.location = Location(location)

    def add_mail(self, value):
        self.mails.append(Mail(value))

    
    def edit_phone(self, old_phone, new_phone):
        found = False
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                found = True
        if not found:
            raise ValueError(f"The phone {old_phone} is not found.")
            # return f"The phone {old_phone} is not found."
    
    def edit_mail(self, old_mail, new_mail):
        found = False
        for mail in self.mails:
            if mail.value == old_mail:
                mail.value = new_mail
                found = True
        if not found:
            raise ValueError(f"The mail {old_mail} is not found.")
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
        # try:
        #     return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday {self.birthday}, mails: {'; '.join(p.value for p in self.mails)}"
        # except:
        #     return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday {self.birthday}"
        # except:
        #     return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

        return_res = f"Contact name: {self.name.value}"

        if hasattr(self, 'phones') and self.phones:
            return_res += f", phones: {'; '.join(p.value for p in self.phones)}"

        if hasattr(self, 'birthday') and self.birthday:
            return_res += f", birthday: {self.birthday}"

        if hasattr(self, 'mails') and self.mails:
            return_res += f", mail: {'; '.join(m.value for m in self.mails)}"

        if hasattr(self, 'location') and self.location:
            return_res += f", location: {self.location}"

        return return_res


class AddressBook(UserDict):

    def add_record(self, new_contact: Record) -> None:
        self.data[new_contact.name.value] = new_contact
        # print(self.data)
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

    def show_all(self, data):
        for name, obj in self.data.items():
            data[name] = obj
        return data
    
    def pack_user(self):
        self.data = records
        # print(records.data, records, self.data)
        file_name = os.getenv("SystemDrive")+"\\py_robot\\users.bin"
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, "wb") as fh:
            # print(self.data)
            pickle.dump(self.data, fh)

    def unpack_user(self):
        file_name = os.getenv("SystemDrive")+"\\py_robot\\users.bin"
        if exists(file_name):

            with open(file_name, "rb") as fh:
                unpacked = pickle.load(fh)

            for name, object in unpacked.items():
                self[name] = object
        
            return self

def fill_the_record(records:AddressBook):
    users = {}
    users = AddressBook.unpack_user(users)
    if users:
        for name, obj in users.items():
            records.data[name] = obj
        return records
    return records

def fill_the_notes(notates:notes.NoteBook):
    notate_arr = {}
    notate_arr = notes.NoteBook.load_notes(notates)
    if notate_arr:
        for name, obj in notate_arr.items():
            notates.data[name] = obj
        return notates
    return notates

records = AddressBook()
records = fill_the_record(records)

notes_obj = notes.NoteBook()
notes_obj = fill_the_notes(notes_obj)
# print(notes_obj)

def search(*args):
    return records.search(*args)


def user_error(func):
    def inner(*args):
        try:
            return func(*args)
        # except AttributeError:
            # return "ab empty"
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
            if str(e) == "Mail should have the following format nickname@domen.yy":
                return "Mail should have the following format nickname@domen.yy"
            if str(e) == "wrong name, try again":
                return "wrong name, try again"
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
        # print(records)
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

def loc_add(*args):
    name = args[0]
    loc = args[1:]
    location = ""
    for ch in loc:
        location +=  " " + ch
    if not records.data.get(name):
        name_record = Record(name)
        name_record.add_location(location)
        records.add_record(name_record)
    else:
        name_record = records.data.get(name)
        name_record.add_location(location)
    return f"Add record {name = }, {location = }"

@user_error 
def mail_add(*args):
    name = args[0]
    mail = str(args[1])
    if not records.data.get(name):
        name_record = Record(name)
        name_record.add_mail(mail)
        records.add_record(name_record)
    else:
        name_record = records.data.get(name)
        name_record.add_mail(mail)
    return f"Add record {name = }, {mail = }"

@user_error
def mail_change(*args):
    name = args[0]
    old_mail = str(args[1])
    new_mail = str(args[2])
    if not records.data.get(name):
        raise ValueError("wrong name, try again")
    else:
        try:
            name_record = records.data.get(name)
            try:
                name_record.edit_mail(old_mail, new_mail)
                return f"Change record {name = }, {new_mail = }"
            except:
                return f"The mail {new_mail} is not valid."
        except:
            return f"The mail {old_mail} is not found."
        
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
    if len(old_phone_number) == 10 and old_phone_number.isdigit() and len(new_phone_number) == 10 and new_phone_number.isdigit():
        if not records.data.get(name):
            raise ValueError("wrong name")
        else:
            try:
                name_record = records.data.get(name)
                name_record.edit_phone(old_phone_number, new_phone_number)
                return f"Change record {name = }, {new_phone_number = }"
            except:
                return f"The phone {old_phone_number} is not found."
    else:
        return "Old phone and New phone must be 10 digits."


def delete_record(*args):
    name = args[0]
    if name in records:
        records.delete(name)
        return f"Contact name: {name}, delete successfull"
    else:
        return f"Contact name: {name}, not found"

def add_note(*args):
    global notes_obj
    tag = []
    text = ''
    for i in args:
        if "#" in i:
             tag.append(i)
        else:
            text += i+" "
    notes_obj, text = notes.add(notes_obj, tag, text)
    return text


def edit_note(*args):
    global notes_obj
    tag = []
    text = ''
    for i in args:
        if "#" in i:
             tag.append(i)
        else:
            text += i+" "
    result, to_write = notes.edit(notes_obj, tag, text)
    if result == "error":
        return to_write
    else:
        notes_obj = result
        return to_write


def search_note(*args):
    global notes_obj
    tag = args
    result = notes.search(notes_obj, tag)
    if result == "error":
        return f"Note not found with this tags: {tag}"
    else:
        return result

def delete_note(*args):
    global notes_obj
    tag = args
    result, text = notes.delete(notes_obj, tag)
    # if notes_obj == result:
    #     print(f"Tags:{tag} not found")
    # else:
    notes_obj = result
    return text


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
        "add - add record or add additional phone - format 'name phone'",
        "bd_add - add birthdayd - format 'name date birthday (YYYY-MM-DD)'",
        "mail_add - add mail - format 'name nickname@domen.yy'",
        "mail_change - change mail - format 'name old mail new mail'",
        "location_add - add location/or replace, if data olready exist",
        "add_notes - add note - format: #tags text",
        "serch_note - exact match for tags - format: #tags",
        "edit_note - exact match for tags - format: #tags",
        "delete_note - exact match for tags - format: #tags",
        "bd_in_days - show all users who has bd in n(7day max) days format 'bd_in_days 2(n days)'",
        "days_to_bd - days to birthday - format 'name'",
        "change - change record - format 'name old phone new phone'",
        "delete - delete record - format 'name'",
        "phone - get phone by name - format 'phone name'",
        "show_all - show all phone book",
        "sort_folder - sort dirty folder by Audio, Docs, Archives, Music, Images, Other",
        "search - search by name or phone number",
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
    else: 
        return f"Name: {name} not found."

def sort_folder_by_path(*args):
    path = str(input("Write path to folder: "))
    if os.path.exists(path):
        result = sort_folder.main(path)
        return result
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
                        new_ch = (str(ch).strip()
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
        if n is  None:
            return_str = "\n"
            if len(records.data) >=1:
                for _, numbers in records.data.items() :
                    return_str += str(numbers) + "\n"
                return return_str
            else:
                return "Empty"
        else:
            return return_lst_result #"No records to show"


def close_cmd(*args):
    return "Good bye!"

def bd_in_days(*args):
    text = ''
    in_days = int(args[0])
    if in_days > 7:
        print("seven days max")
        in_days = 7
    # print(in_days)
    result_str = show_all()
    result_dct = convert_str_dict(result_str)
    # print(result_dct)
    out_result = birthday_from_now(result_dct, in_days)
    
    for k,v in out_result.items():
        text += k+" - Name: "
        for i in v:
            text += i+", "
        text = text[:-2]+"\n"
        out_result = text
    return out_result

COMMANDS = {
    add_note:"add_note",
    edit_note:"edit_note",
    search_note:"search_note",
    delete_note:"delete_note",
    add_record: "add",
    bd_add: "bd_add",
    mail_add: "mail_add",
    loc_add: "location_add",
    mail_change: "mail_change",
    days_to_bd: "days_to_bd",
    bd_in_days: "bd_in_days",
    delete_record: "delete",
    change_record: "change",
    hello_cmd: "hello",
    get_phone: "phone",
    show_all: "show_all",
    sort_folder_by_path: "sort_folder",
    search: "search",
    help_cmd: "help",
    close_cmd: ("good bye", "close", "exit"),
}

cmd_list = ["hello", "help", "add", "add_note", "edit_note", "search_note", "delete_note", "mail_add", "mail_change", "bd_add", "location_add",
            "days_to_bd", "bd_in_days", "change", "delete", "phone", "show_all", "save_ab", "search", "sort_folder", "load_ab", "good bye", "close", "exit"]

def parser(text: str):
    for func, kw in COMMANDS.items():
        if text.lower().startswith(kw):
            return func, text[len(kw) :].strip().split()
    return unknown_cmd, []


def main():
    book = AddressBook()
    book.unpack_user()
    note = notes.NoteBook()
    note.load_notes()
    # print(note)
    # print(book)
    completer = WordCompleter(cmd_list)
    while True:
        user_input = prompt("Write comand:", completer=completer)
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
            note.save_notes(notes_obj)
            break


if __name__ == "__main__":
    main()

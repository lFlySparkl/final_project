# 1.зберігати контакти з іменами, адресами, номерами телефонів, email та днями народження до книги контактів;       %%% Реализовано
# 2.виводити список контактів, у яких день народження через задану кількість днів від поточної дати;                %%% Создать новую функцию (доработка функции из дз 8) 
# 3.перевіряти правильність введеного номера телефону та email під час створення або редагування запису 
# та повідомляти користувача у разі некоректного введення;                                                          %%% Частично сделанно, доработка проверки при редактировании (возможно исправление проверки)
# 4.здійснювати пошук контактів серед контактів книги;                                                              %%% Реализовано
# 5.редагувати та видаляти записи з книги контактів;                                                                %%% Реализовано
# 6.зберігати нотатки з текстовою інформацією;                                                                      %%% Создать новую функцию (сохраняем как текст, если захотим можно сделать доп функционал под каждый контакт, с выводом в дальнейшем)
# 7.проводити пошук за нотатками;                                                                                   %%% Создать новую функцию
# 8.редагувати та видаляти нотатки;                                                                                 %%% Создать новую функцию (каждый раз вводится новые записи или только одни и их мы сможем редактировать)
# 9.додавати в нотатки "теги", ключові слова, що описують тему та предмет запису;                                   %%% Создать новую функцию (предполагаю что записи будем сохранять в виде ключа(тега) и значения)
# 10.здійснювати пошук та сортування нотаток за ключовими словами (тегами);                                         %%% Создать новую функцию (поиск будет совершатся по ключам и мы сможем редактировать значение, если контакт захочет при регистрации поменять тему записи то значит мы перезапишем, старую удаляем и записываем как новую)
# 11.сортувати файли у зазначеній папці за категоріями (зображення, документи, відео та ін.).                       %%% Нужно итегрировать в проект (переработка под классы)
# 12.Додаткове ускладнене завдання: Бот повинен аналізувати введений текст і намагатися вгадати,                    %%% Пока фиг знает как такое делать (пока забить и так много всего)
# що хоче від нього користувач і запропонувати найближчу команду для виконання
# 13.Реализация команды "help" которая выводит все доступные команды бота                                           %%% Сознадие функции справочника
# 14.Переработка всего проекта под классы, продумать как будут вводится команды                                     %%% Нужно для того чтобы все было красиво и не было стыдно показать проект
# (тоесть через инпут вводим команду, если такая есть в массиве то выводим текстовое сообщение,
#  какое количество и каких данных нужно ввести, или просто через пару инпутов)
# 15.Реализовать управление через команды с консоли пример дз 9                                                     %%% Создать управление всеми функциями
# 16.проєкт має бути збережений в окремому репозиторії та бути загальнодоступним (GitHub, GitLab або BitBucket);    %%% Сохраняем на гите
# 17.проєкт містить докладну інструкцію щодо встановлення та використання;                                          %%% Создать инструкцию
# 18.проєкт встановлюється як Python-пакет та може бути викликаний у будь-якому місці системи                       %%% Создать установщик, пример clean_folder
# відповідною командою після встановлення;
# 19.проєкт повністю реалізує мінімум 8 вимог із 12 описаних у завданні;
# 20.персональний помічник зберігає інформацію на жорсткому диску в папці користувача                               %%% Сохранение аналог 12 дз
# і може бути перезапущений без втрати даних.

# 21.ваши предложения
# так как у нас недостаток людей то первоочередно делаем самые нужные модули если останется время можно допилить еще что-то


from collections import UserDict
from datetime import datetime
import pickle
import re


class Field:
    def __init__(self, value):
        self.__privat_value = None
        self.value = value

    @property
    def value(self):
        return self.__privat_value

    @value.setter
    def value(self, value: str):
        if value.isalpha():
            self.__privat_value = value
        else:
            raise Exception("Wrong value")


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


class Phone(Field):
    def __init__(self, value):
        self.__privat_value = None
        self.value = value

    @property
    def value(self):
        return self.__privat_value

    @value.setter
    def value(self, value: str) -> None:
        if len(value) == 10 and value.isdigit():
            self.__privat_value = value
        else:
            raise ValueError("Phone number most be 10 didgit")


class Birthday(Field):
    def __init__(self, birthday) -> None:
        self.__privat_birthday = None
        self.birthday = birthday

    @property
    def birthday(self):
        return self.__privat_birthday

    @birthday.setter
    def birthday(self, birthday):
        if not self.is_date(self, birthday):
            self.__privat_birthday = birthday
        else:
            ValueError("Invalid phone number format"),

            TypeError("Dont birtday")

    def is_date(self, birthday: str) -> None:
        patern_birth = r"^(1|2)(9|0)[0-2,7-9][0-9]{1}(.|/| )(0|1)[0-9](.|/| )[0-3][0-9]"
        return bool(re.match(patern_birth, birthday))


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday

    def add_phone(self, value: Field):
        self.phones.append(value)

    def remove_phone(self, number):
        if number in self.phones:
            self.phones.remove(number)
        else:
            raise ValueError

    def edit_phone(self, old_number, new_number):
        if old_number in self.phones:
            idx = ""
            for number in self.phones:
                if number == old_number:
                    idx = self.phones.index(number)
            self.phones[idx] = new_number

        else:
            raise ValueError

    def find_phone(self, number):
        if number in self.phones:
            self.value = number
            return self
        else:
            return None

    def days_to_birthday(self, birthday: Birthday):
        self.birthday = birthday
        date_split = datetime.strptime(
            birthday.replace(" ", "-").replace(".", "-"), "%d-%m-%Y"
        )
        new_date_of_bd = date_split.replace(
            year=datetime.today().year, month=date_split.month, day=date_split.day
        )
        result = new_date_of_bd.date() - datetime.today().date()
        return result.days

    def __str__(self):
        if Birthday.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p for p in self.phones)}, birth: {self.birthday} ({self.days_to_birthday(self.birthday)} day to birthday)"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p for p in self.phones)}"


class AddressBook(UserDict):
    # Додати функціонал збереження адресної книги на диск та відновлення з диска.
    # Для цього ви можете вибрати будь-який зручний для вас протокол серіалізації/десеріалізації даних та реалізувати методи,
    # які дозволять зберегти всі дані у файл і завантажити їх із файлу.

    # Додати користувачеві можливість пошуку вмісту книги контактів,
    # щоб можна було знайти всю інформацію про одного або кількох користувачів за кількома цифрами номера телефону
    # або літерами імені тощо.
    def add_record(self, contact: Record):
        self.data[contact.name.value] = contact

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, contact):
        if contact in self.data:
            return self.data.pop(contact)
        else:
            return None

    def search_user(self):
        keyword = input("Enter keyword: ")
        user = ""

        for name, obj in self.data.items():
            if keyword.lower() == name.lower():
                if isinstance(obj.birthday, str):
                    user += f"Name: {name}, phones: {', '.join(p for p in obj.phones)}, birthday: {obj.birthday}\n"
                else:
                    user += (
                        f"Name: {name}, phones: {', '.join(p for p in obj.phones)}\n"
                    )
            elif keyword in obj.phones:
                if isinstance(obj.birthday, str):
                    user += f"Name: {name}, phones: {', '.join(p for p in obj.phones)}, birthday: {obj.birthday}\n"
                else:
                    user += (
                        f"Name: {name}, phones: {', '.join(p for p in obj.phones)}\n"
                    )

        if len(user) > 1:
            print(user)
        else:
            print(f"No name in list with this atribyte {keyword}")

    def pack_user(self):
        file_name = "users.bin"
        with open(file_name, "wb") as fh:
            pickle.dump(self.data, fh)

    def unpack_user(self):
        with open("users.bin", "rb") as fh:
            unpacked = pickle.load(fh)

        for name, object in unpacked.items():
            self.data[name] = object


class Iterator:
    MAX_VALUE = 0

    def __init__(self, adressBook):
        self.current_value = 0
        self.adressBook = AddressBook
        self.MAX_VALUE = len(adressBook.data)

    def __next__(self):
        if self.current_value < self.MAX_VALUE:
            self.current_value += 1
            return self.adressBook.data[self.current_value]
        raise StopIteration


if __name__ == "__main__":
    book = AddressBook()
    unpack_user = book.unpack_user()
    book.search_user()
    # print(unpack_user)
    john_record = Record("Dylan")
    john_record.add_phone("5489789775")
    john_record.add_phone("6666666666")
    book.add_record(john_record)
    # john_record.days_to_birthday("05-12-1976")
    john_record
    book.add_record(john_record)
    john_record
    # print(john_record)
    jane_record = Record("Derek")
    # jane_record.days_to_birthday("20.11.2002")
    jane_record.add_phone("2222222222")
    book.add_record(jane_record)
    # print(jane_record)
    # john = book.find("John")
    # john_record.edit_phone("1234567890", "1112223333")
    # john_record.find_phone("5555555555")
    # john_record.find_phone("1234567890")
    # found_phone2 = john_record.find_phone("1112223333")

    pack_user = book.pack_user()

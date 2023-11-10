import final_project as c
import clean


contacts = {"dima": "0909899", "petr": "9089800"}


def user_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enought params. Try again."
        except KeyError:
            return "Uknown rec_id. Try another or use help."
        except ValueError:
            return "Wrong value. Try again."

    return inner


def hello_func(*args):
    return "How can I help you?"

def add_contact():
    c.Record.add_phone()

@user_error
def add_func(*args):
    contact_name = args[0]
    contact_phone = args[1]
    contacts[contact_name] = contact_phone
    return f"Add contact {contact_name = }, {contact_phone = }"


@user_error
def change_func(*args):
    contact_name = args[0]
    new_phone = args[1]
    contact = contacts[contact_name]
    if contact:
        contacts[contact_name] = new_phone
        return f"Change contact {contact_name = }, {new_phone = }"


def phone_func(*args):
    contact_name = args[0]
    contact_phone = contacts[contact_name]
    if contact_phone:
        return f"Show contact {contact_name = }, {contact_phone = }"


def show_all_func():
    show_all_cont = ""
    for name, phone in contacts.items():
        show_all_cont += f"Name: {name} - Phone: {phone}" + "\n"
    return show_all_cont


def good_bye_func(*args):
    print("Good bye!")
    return exit()


def close_func(*args):
    print("Good bye!")
    return exit()


def exit_func(*args):
    print("Good bye!")
    return exit()


def unknown_comand():
    return "Unknown comand. Try again."


COMANDS = {
    hello_func: "hello",
    add_func: "add",
    change_func: "change",
    phone_func: "phone",
    show_all_func: "show all",
    good_bye_func: "good bye",
    close_func: "close",
    exit_func: "exit",
}


def parcer(text: str):
    for func, kw in COMANDS.items():
        if text.startswith(kw):
            if (
                text == "hello"
                or text == "good bye"
                or text == "close"
                or text == "exit"
            ):
                return func, text
            elif "add" in text or "phone" in text or "change" in text:
                return func, text.replace(kw + " ", "").strip().split()
            else:
                return func, text[len(kw) :].strip().split()
    return unknown_comand, []


def main():
    while True:
        book = c.AddressBook()
        unpack_user = book.unpack_user()
        print(unpack_user)

        user_input = input("Write comand:").lower()
        func, data = parcer(user_input)
        print(func(*data))


if __name__ == "__main__":
    main()

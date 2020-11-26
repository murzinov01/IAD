import time
import json
import os
import datetime
import keyboard
import colorama
from os import system, name
from colorama import Fore, Style
from dateutil.relativedelta import relativedelta

colorama.init()


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


class PhoneBook:
    TAB = "\t\t\t\t\t\t\t"

    MENU = [TAB + "  **\t\t" + "Add new record to the PhoneBook\t\t **\n",
            TAB + "  **\t\t" + "  " * 2 + "Make edits to a record\t\t **\n",
            TAB + "  **\t\t" + " " * 8 + "Delete a record\t\t\t **\n",
            TAB + "  **\t\t" + " " * 6 + "Show the PhoneBook\t\t **\n",
            TAB + "  **\t\t" + " " * 9 + "Find an entry\t\t\t **\n",
            TAB + "  **\t\t" + " " * 2 + "Find out the age of a person\t\t **\n",
            TAB + "  **\t\t" + " " * 4 + "Find record by birth date\t\t **\n",
            TAB + "  **\t" + " " * 6 + "Find person with nearest date of birth\t **\n",
            TAB + "  **\t\t" + " " * 13 + "Exit\t\t\t **\n"]

    DELETE_MENU = [TAB + "  **\t\t" + " " * 3 + "Delete by name and surname\t\t **\n",
                   TAB + "  **\t\t" + " " * 5 + "Delete by phone number\t\t **\n"]

    WARNINGS = {"Name_error": f"Error in {Fore.RED}spelling the name{Style.RESET_ALL}.",
                "Surname_error": f"Error in {Fore.RED}spelling the surname{Style.RESET_ALL}.",
                "Phone_number_error": f"Wrong {Fore.RED}phone number entered{Style.RESET_ALL}.",
                "Work_number_error": f"Wrong {Fore.RED}work phone number entered{Style.RESET_ALL}.",
                "Home_number_error": f"Wrong {Fore.RED}home phone number entered{Style.RESET_ALL}.",
                "Birth_date_error": f"{Fore.RED}Date of birth entered incorrectly{Style.RESET_ALL}.",
                "Notification": f" {Fore.LIGHTMAGENTA_EX}Correct the data and enter it again!{Style.RESET_ALL}"
                                f"\n{Fore.LIGHTCYAN_EX}>>{Style.RESET_ALL} ",
                "Template_error": f"User data {Fore.RED}does not match the template{Style.RESET_ALL}."
                                  f" Correct the errors and enter the data again!\n{Fore.LIGHTCYAN_EX}>>{Style.RESET_ALL} ",
                "User_does_not_exist": "This user does not exist."}

    def __init__(self):
        self._menu_ptr = 0
        self._delete_menu_ptr = 0
        self._options_num = 9
        self._delete_options_num = 2
        self._back_to_menu_flag = False
        self._enter_flag = False
        self._move_flag = False
        self._space_flag = True
        self._exit_flag = False
        self._delete_menu_flag = False
        self.all_records = list()
        self.load_date_base()
        self.print_initial_instruction()

    # ******    Save and Load data
    def save_data_base(self) -> None:
        with open("PhoneBook.json", "w") as file:
            json.dump(self.all_records, file)

    def load_date_base(self) -> None:
        if not os.path.isfile("PhoneBook.json"):
            return
        with open("PhoneBook.json", "r") as file:
            self.all_records = json.load(file)

    # ******    Functions for visual realization     *******
    def print_date_base(self) -> None:
        clear()
        print(f"**********   {Fore.GREEN}PhoneBook{Style.RESET_ALL}   **********")
        for record in self.all_records:
            self.print_record(record)
        self._back_to_menu_flag = True
        print("Press 'LEFT' to return to the menu.")

    @staticmethod
    def print_record(record: dict) -> None:
        print(Fore.LIGHTBLUE_EX + json.dumps(record, indent=4) + Style.RESET_ALL)

    def print_menu(self, line="before", target_menu="default") -> None:
        clear()
        menu_to_print = self.MENU.copy() if target_menu == "default" else self.DELETE_MENU.copy()
        menu_ptr = self._menu_ptr if target_menu == "default" else self._delete_menu_ptr
        if line == "before":
            menu_to_print[menu_ptr] = Style.RESET_ALL + menu_to_print[menu_ptr] + Style.RESET_ALL
        elif line == "after":
            menu_to_print[menu_ptr] = Fore.LIGHTCYAN_EX + menu_to_print[menu_ptr] + Style.RESET_ALL
        print("".join(menu_to_print), end="")

    def print_initial_instruction(self) -> None:
        keyboard.add_hotkey('space', self.start_menu)
        clear()
        print(self.TAB + f"  **\t\t Hello, its your{Fore.GREEN} PhoneBook!{Style.RESET_ALL}\t\t **")
        print(self.TAB + "  **\t      Use the buttons below to navigate\t\t **")
        print(self.TAB + f"  **\t\t   {Fore.BLUE}'UP'{Style.RESET_ALL}, {Fore.BLUE}'DOWN'{Style.RESET_ALL} - to move\t\t **")
        print(self.TAB + f"  **\t\t   {Fore.BLUE}'RIGHT'{Style.RESET_ALL} - to choose \t\t\t **")
        print(self.TAB + f"  **\t\t   {Fore.BLUE}'LEFT'{Style.RESET_ALL} - to back to menu\t\t **")
        print(self.TAB + f"  **\t\t  Press {Fore.RED}'SPACE'{Style.RESET_ALL} to continue\t\t **")
        self.menu_handler()

    def change_menu_ptr(self, direction='up') -> None:
        if self._move_flag:
            if not self._delete_menu_flag:
                self.print_menu(line="before")
                menu_ptr = self._menu_ptr
                options_num = self._options_num
            else:
                self.print_menu(line="before", target_menu="delete")
                menu_ptr = self._delete_menu_ptr
                options_num = self._delete_options_num

            if direction == 'up':
                menu_ptr -= 1
            else:
                menu_ptr += 1

            if menu_ptr < 0:
                menu_ptr = options_num - 1
            if menu_ptr > options_num - 1:
                menu_ptr = 0

            if not self._delete_menu_flag:
                self._menu_ptr = menu_ptr
                self._options_num = options_num
                self.print_menu(line="after")
            else:
                self._delete_menu_ptr = menu_ptr
                self._delete_options_num = options_num
                self.print_menu(line="after", target_menu="delete")

    def change_menu_ptr_down(self) -> None:
        if self._move_flag:
            self.change_menu_ptr(direction="down")

    def menu_handler(self) -> None:
        while self._space_flag:
            pass
        self._move_flag = True
        self._enter_flag = True
        keyboard.add_hotkey('up', self.change_menu_ptr)
        keyboard.add_hotkey('down', self.change_menu_ptr_down)
        keyboard.add_hotkey('left', self.back_to_menu)
        keyboard.add_hotkey('right', self.confirm_choice)
        while not self._exit_flag:
            pass
        print(self.TAB + f"  **\t\t\t   {Fore.RED}Goodbye!{Style.RESET_ALL}\t \t\t **")

    def back_to_menu(self):
        if self._back_to_menu_flag:
            self.print_menu("after")
            self._back_to_menu_flag = False
            self._move_flag = True
            self._enter_flag = True
            self._delete_menu_flag = False
        else:
            print("\nYou can't return to the main menu yet.")

    def start_menu(self):
        if not self._space_flag:
            return
        self._space_flag = False
        self.print_menu(line="after")

    def confirm_choice(self) -> None:
        if not self._enter_flag:
            return
        self._move_flag = False
        self._enter_flag = False
        options = [self.add_user, self.make_edits, self.delete_user, self.print_date_base, self.find_an_entry,
                   self.calculate_age, self.find_record_by_birth_date, self.find_user_with_the_nearest_date_of_birth,
                   self.exit_from_phone_book]
        delete_options = [self.delete_user_by_name_and_surname, self.delete_user_by_phone_number]
        if not self._delete_menu_flag:
            options[self._menu_ptr]()
        else:
            delete_options[self._delete_menu_ptr]()

    # ******    MENU functions  ******
    def add_user(self) -> None:

        clear()
        print(f"You chose to add a new record. Please, enter the user's details ({Fore.RED}required{Style.RESET_ALL}, "
              f"{Fore.MAGENTA}optional{Style.RESET_ALL}):")
        params, user_details = self.get_record_details(optional_params="exists")
        new_entry = self.create_entry(params[0], params[1], params[2], params[3], params[4], params[5])
        user_record = self.find_user_by_params([params[0], params[1]], mode="by_id")
        if user_record is None:
            print("New user added successfully! Press 'LEFT' to return to the menu.")
            self.all_records.append(new_entry)
            self.save_data_base()
            self._back_to_menu_flag = True
        else:
            print("This user already exists.")
            self.print_record(user_record)
            print(f"Do you want to rewrite user's data? ({Fore.RED}'Yes'{Style.RESET_ALL}"
                  f" or {Fore.RED}'No'{Style.RESET_ALL})", end="")
            if self.get_user_permission():
                self.all_records[self.all_records.index(user_record)] = new_entry
                print("The user's data was successfully rewritten! Press 'LEFT' to return to the menu.")
                self.save_data_base()
            else:
                print("Press 'LEFT' to return to the menu.")
            self._back_to_menu_flag = True

    def make_edits(self) -> None:
        clear()
        print("You chose to make edits to a record.\nLet's find a record that needs to be corrected!\n")
        founded_records = self.find_record_in_data_base()
        clear()
        if len(founded_records) == 1:
            self.make_record_edits_in_data_base(founded_records[0])
        elif len(founded_records) > 1:
            print(f"*******   {Fore.GREEN}Founded records:{Style.RESET_ALL}   *******")
            for i, record in enumerate(founded_records):
                print(f"{Fore.RED}{i + 1}){Style.RESET_ALL}", end="")
                self.print_record(record)
            number = self.select_from_multiple_entries(founded_records)
            self.make_record_edits_in_data_base(founded_records[number - 1])
        else:
            print("Unfortunately, the entry was not found for the parameters you specified")
            print("Press 'LEFT' to return to the menu")
        self._back_to_menu_flag = True

    def delete_user(self) -> None:
        clear()
        self.print_menu(line="after", target_menu="delete")
        self._delete_menu_flag = True
        self._enter_flag = True
        self._move_flag = True

    def find_an_entry(self) -> None:
        clear()
        print("You chose to find an entry.")
        founded_records = self.find_record_in_data_base()
        clear()
        if len(founded_records) > 0:
            print(f"*******   {Fore.GREEN}Founded records:{Style.RESET_ALL}   *******")
            for record in founded_records:
                self.print_record(record)
        else:
            print("Unfortunately, the entry was not found for the parameters you specified")
        print("Press 'LEFT' to return to the menu")
        self._back_to_menu_flag = True

    def calculate_age(self) -> None:
        clear()
        print(f"You chose to calculate age of a person in {Fore.GREEN}PhoneBook{Style.RESET_ALL}!")
        params, user_record = self.get_users_name_and_surname()

        if user_record["birth_date"]:
            difference_in_years = relativedelta(datetime.datetime.strptime(user_record["birth_date"], '%d.%m.%Y'),
                                                datetime.datetime.now()).years
            if difference_in_years < 0:
                difference_in_years *= (-1)
            print(f"The user's age is {Fore.RED}{difference_in_years} years{Style.RESET_ALL}")
        else:
            print(f"Unfortunately, this user does not have a {Fore.RED}date of birth{Style.RESET_ALL}")
        print("Press 'LEFT' to return to the menu")
        self._back_to_menu_flag = True

    def find_record_by_birth_date(self) -> None:
        clear()
        print(f"You chose to find record by birth date. Please, Enter the user's {Fore.RED}day{Style.RESET_ALL}"
              f" and {Fore.RED}month{Style.RESET_ALL} of birth day.")
        while True:
            day = input(f"Day ({Fore.RED}DD{Style.RESET_ALL}) {Fore.LIGHTCYAN_EX}>>{Style.RESET_ALL} ").strip()
            month = input(f"Month ({Fore.RED}MM{Style.RESET_ALL}) {Fore.LIGHTCYAN_EX}>>{Style.RESET_ALL} ").strip()
            answer = ""
            if len(day) != 2 or not self.check_day_or_month(day):
                answer += f"Incorrect {Fore.RED}day{Style.RESET_ALL} value."
            if len(month) != 2 or not self.check_day_or_month(month, param="month"):
                if answer:
                    answer += " "
                answer += f"Incorrect {Fore.RED}month{Style.RESET_ALL} value."
            if answer:
                print(answer + " Try again!")
                continue
            break
        founded_records = list()
        clear()
        for record in self.all_records:
            if not record["birth_date"]:
                continue
            birth_date = record["birth_date"].split(".")
            if birth_date[0] == day and birth_date[1] == month:
                founded_records.append(record)
        if len(founded_records) > 0:
            print(f"*******   {Fore.GREEN}Founded records:{Style.RESET_ALL}   *******")
            for record in founded_records:
                self.print_record(record)
        else:
            print("Unfortunately, the entry was not found for the parameters you specified")
        print("Press 'LEFT' to return to the menu")
        self._back_to_menu_flag = True

    def find_user_with_the_nearest_date_of_birth(self):
        clear()
        founded_users = list()
        now_date = datetime.datetime.now()
        nearest_dates = [now_date + datetime.timedelta(days=x) for x in range(0, 31)]

        for record in self.all_records:
            if not record["birth_date"]:
                continue
            birth_date = datetime.datetime.strptime(record["birth_date"], "%d.%m.%Y")
            if abs(birth_date.month - now_date.month) > 1:
                continue
            for nearest_date in nearest_dates:
                if nearest_date.month == birth_date.month and nearest_date.day == birth_date.day:
                    founded_users.append(record["first_name"] + " " + record["second_name"])
                    break

        if len(founded_users) > 0:
            print(f"*******   {Fore.GREEN}Founded records:{Style.RESET_ALL}   *******")
            for i, user in enumerate(founded_users):
                print(f"{Fore.RED}{i + 1}){Style.RESET_ALL}" + user)
        else:
            print("Unfortunately, the entry was not found for the parameters you specified")
        print("Press 'LEFT' to return to the menu")
        self._back_to_menu_flag = True

    def exit_from_phone_book(self):
        self._exit_flag = True

    # Other necessary functions
    @staticmethod
    def create_entry(first_name: str, second_name: str, phone_number: str, birth_date="",
                     work_phone_number="", home_phone_number="") -> dict:
        user_data = {"first_name": first_name,
                     "second_name": second_name,
                     "phone_number": phone_number,
                     "birth_date": birth_date,
                     "work_phone_number": work_phone_number,
                     "home_phone_number": home_phone_number}

        return user_data

    def check_params(self, params: list, mode="default") -> bool:
        answer = ""
        if len(params) < 3:
            print(self.WARNINGS["Template_error"], end="")
            return False
        elif len(params) == 3:
            params.append("")

        # Check Name spelling
        if not params[0].isalpha():
            if mode == "default" or params[0]:
                answer += self.WARNINGS["Name_error"]
        else:
            params[0] = self.correct_name(params[0])

        # Check Surname spelling
        if not params[1].isalpha():
            if mode == "default" or params[1]:
                if answer:
                    answer += " "
                answer += self.WARNINGS["Surname_error"]
        else:
            params[1] = self.correct_name(params[1])

        # Check Phone numbers spelling
        for i in (2, 4, 5):
            phone_number = self.check_phone_number(params[i])
            if phone_number is None:
                if mode == "default" or params[i]:
                    if i != 2 and not params[i]:
                        continue

                    if answer:
                        answer += " "
                    if i == 2:
                        answer += self.WARNINGS["Phone_number_error"]
                    elif i == 4:
                        answer += self.WARNINGS["Work_number_error"]
                    else:
                        answer += self.WARNINGS["Home_number_error"]
            else:
                params[i] = phone_number

        # Check birth date spelling
        if params[3]:
            try:
                time.strptime(params[3], '%d.%m.%Y')
            except Exception as e:
                if mode == "default" or params[3]:
                    if answer:
                        answer += " "
                    answer += self.WARNINGS["Birth_date_error"]

        if answer:
            print(answer + self.WARNINGS["Notification"], end="")
            return False
        else:
            return True

    @staticmethod
    def correct_name(string: str) -> str:
        string = string.lower()
        return string[0].upper() + string[1:]

    @staticmethod
    def check_phone_number(phone_number: str) -> str or None:
        if len(phone_number) < 11:
            return None
        if phone_number[:2] == "+7":
            phone_number = "8" + phone_number[2:]
        if phone_number[0] != "8" or len(phone_number) > 11 or not phone_number.isdigit():
            return None
        return phone_number

    @staticmethod
    def check_day_or_month(day: str, param="day") -> bool:
        if day[0] == '0' and day[1] in [str(i) for i in range(1, 10)]:
            return True
        elif day in [str(i) for i in range(10, 32 if param == "day" else 13)]:
            return True
        return False

    @staticmethod
    def get_user_permission() -> bool:
        print(f"\n{Fore.LIGHTCYAN_EX}>>{Style.RESET_ALL} ", end="")
        while True:
            answer = input().lower()
            if answer == 'yes' or answer == 'y':
                return True
            if answer == 'no' or answer == 'n':
                return False
            print(f"\nI don't understand you. Please, enter {Fore.RED}'Yes'{Style.RESET_ALL} or"
                  f" {Fore.RED}'No'{Style.RESET_ALL} to continue\n{Fore.LIGHTCYAN_EX}>>{Style.RESET_ALL} ", end="")

    @staticmethod
    def select_from_multiple_entries(founded_records: list) -> int:
        print(f"{Fore.LIGHTMAGENTA_EX}Here are a few of the records at your request. Please select a specific entry"
              f" {Fore.RED}number{Style.RESET_ALL}!")
        print(f"{Fore.LIGHTCYAN_EX}>>{Style.RESET_ALL} ", end="")
        while True:
            try:
                number = int(input())
            except Exception as e:
                print(f"{Fore.RED}ERROR{Style.RESET_ALL}: I can not understand this number! Try again!\n"
                      f"{Fore.LIGHTCYAN_EX}>>{Style.RESET_ALL} ", end="")
                continue
            if number < 1 or number > len(founded_records):
                print(f"{Fore.RED}ERROR{Style.RESET_ALL}: This number is out of range! Try again!\n"
                      f"{Fore.LIGHTCYAN_EX}>>{Style.RESET_ALL} ", end="")
                continue
            return number

    def get_record_details(self, mode="default", optional_params="default") -> tuple:
        user_details = {"first_name": "",
                        "second_name": "",
                        "phone_number": "",
                        "birth_date": "",
                        "work_phone_number": "",
                        "home_phone_number": ""}

        while True:
            print("Please, enter the user's details:")
            print(f"Enter the {Fore.RED}Detail{Style.RESET_ALL} or press {Fore.BLUE}Enter{Style.RESET_ALL} to continue")
            user_details["first_name"] = input(f"{Fore.RED}Name{Fore.LIGHTCYAN_EX} >>{Style.RESET_ALL} ").strip()
            user_details["second_name"] = input(f"{Fore.RED}Surname{Fore.LIGHTCYAN_EX} >>{Style.RESET_ALL} ").strip()
            user_details["phone_number"] = input(f"{Fore.RED}Phone number{Fore.LIGHTCYAN_EX} >>{Style.RESET_ALL} ").strip()
            user_details["birth_date"] = input(f"{Fore.RED if optional_params == 'default' else Fore.MAGENTA}"
                                               f"Birth date (DD.MM.YYYY){Fore.LIGHTCYAN_EX} >>{Style.RESET_ALL} ").strip()
            user_details["work_phone_number"] = input(f"{Fore.RED if optional_params == 'default' else Fore.MAGENTA}"
                                                      f"Work phone number{Fore.LIGHTCYAN_EX} >>{Style.RESET_ALL} ").strip()
            user_details["home_phone_number"] = input(f"{Fore.RED if optional_params == 'default' else Fore.MAGENTA}"
                                                      f"Home phone number{Fore.LIGHTCYAN_EX} >>{Style.RESET_ALL} ").strip()

            params = [user_details[key] for key in user_details.keys()]
            if self.check_params(params, mode=mode):
                for i, key in enumerate(user_details.keys()):
                    user_details[key] = params[i]
                return params, user_details

    def get_users_name_and_surname(self) -> tuple:
        print(f"Enter the user's name and surname ({Fore.RED}Name Surname{Style.RESET_ALL})\n{Fore.LIGHTCYAN_EX}"
              f">>{Style.RESET_ALL} ", end="")
        params = list()
        user_record = dict()
        while True:
            try:
                params = [string.strip(" ") for string in input().split()]
            except Exception as e:
                print(self.WARNINGS["Template_error"], end="")
                continue

            if len(params) != 2:
                print(self.WARNINGS["Template_error"], end="")
                continue
            answer = ""
            if not params[0].isalpha():
                answer += self.WARNINGS["Name_error"]
            if not params[1].isalpha():
                if answer:
                    answer += " "
                answer += self.WARNINGS["Surname_error"]
            if answer:
                print(answer + self.WARNINGS["Notification"], end="")
                continue
            else:
                params[0] = self.correct_name(params[0])
                params[1] = self.correct_name(params[1])
                user_record = self.find_user_by_params([params[0], params[1]], mode="by_id")
                if user_record is None:
                    print(self.WARNINGS["User_does_not_exist"] + self.WARNINGS["Notification"], end="")
                    continue
                else:
                    break
        return params, user_record

    def find_user_by_params(self, params: list, mode="by_id") -> dict or list or None:
        founded_records = list()
        for record in self.all_records:
            if mode == "by_id" and record["first_name"] == params[0] and record["second_name"] == params[1]:
                return record
            if mode == "by_phone_number" and params[0] in (record["phone_number"], record["work_phone_number"],
                                                           record["home_phone_number"]):
                founded_records.append(record)
        if len(founded_records) != 0:
            if len(founded_records) == 1:
                return founded_records[0]
            return founded_records
        else:
            return None

    def delete_user_by_params(self, params: list, mode="by_id") -> None:
        self.all_records.remove(self.find_user_by_params(params, mode=mode))
        self._back_to_menu_flag = True
        print("The user was successfully deleted! Press 'LEFT' to return to the menu.")
        self.save_data_base()

    def delete_user_by_phone_number(self) -> None:
        clear()
        print("You chose to delete a record by phone number.")
        phone_number = None
        while phone_number is None:
            phone_number = input(f"Enter user's {Fore.RED}phone number{Style.RESET_ALL} "
                                 f"({Fore.MAGENTA}mobile, work or home{Style.RESET_ALL})\n{Fore.LIGHTCYAN_EX}"
                                 f">>{Style.RESET_ALL} ").strip()
            phone_number = self.check_phone_number(phone_number)

        user_record = self.find_user_by_params([phone_number], mode="by_phone_number")
        if type(user_record) is dict:
            print(f"This user exists in the phone book. Do you want to delete this record? ({Fore.RED}"
                  f"'Yes'{Style.RESET_ALL} or {Fore.RED}'No'{Style.RESET_ALL})")
            self.print_record(user_record)
        elif type(user_record) is list:
            print(f"*******   {Fore.GREEN}Founded records:{Style.RESET_ALL}   *******")
            for i, record in enumerate(user_record):
                print(f"{Fore.RED}{i + 1}){Style.RESET_ALL}", end="")
                self.print_record(record)
            number = self.select_from_multiple_entries(user_record)
            user_record = user_record[number - 1]
            print(f"Do you want to delete this record? ({Fore.RED}"
                  f"'Yes'{Style.RESET_ALL} or {Fore.RED}'No'{Style.RESET_ALL})", end="")
        if self.get_user_permission():
            print("The user was successfully deleted! Press 'LEFT' to return to the menu.")
            self.all_records.remove(user_record)
            self.save_data_base()
        else:
            print("Press 'LEFT' to return to the menu.")
        self._back_to_menu_flag = True

    def delete_user_by_name_and_surname(self) -> None:
        clear()
        print("You chose to delete a record by name and surname.")
        params, user_record = self.get_users_name_and_surname()
        print(f"This user exists in the phone book. Do you want to delete this record? ({Fore.RED}"
              f"'Yes'{Style.RESET_ALL} or {Fore.RED}'No'{Style.RESET_ALL})")
        self.print_record(user_record)
        if self.get_user_permission():
            self.delete_user_by_params([params[0], params[1]], mode="by_id")
        else:
            self._back_to_menu_flag = True
            print("Press 'LEFT' to return to the menu.")

    def find_record_in_data_base(self) -> list:
        params, user_details = self.get_record_details(mode="to_find")

        founded_records = list()
        params_num = 0
        for key in user_details.keys():
            if user_details[key]:
                params_num += 1
        for record in self.all_records:
            counter = 0
            for key in user_details.keys():
                if user_details[key] and record[key] == user_details[key]:
                    counter += 1
            if counter == params_num:
                founded_records.append(record)

        return founded_records

    def make_record_edits_in_data_base(self, record: dict) -> None:
        clear()
        print("You chose the record below to edit")
        self.print_record(record)
        print(f"You can {Fore.RED}make changes to the corresponding fields{Style.RESET_ALL}"
              f" or {Fore.BLUE}press enter to leave the field unchanged{Style.RESET_ALL}")
        while True:
            params, user_details = self.get_record_details(mode="to_find")
            user = self.find_user_by_params([params[0], params[1]], mode="by_id")
            if user is None:
                break
            else:
                print(f"A user with this first and last name {Fore.RED}already exists!{Style.RESET_ALL}")
        record_index = self.all_records.index(record)
        for i, key in enumerate(user_details.keys()):
            if params[i]:
                self.all_records[record_index][key] = params[i]
        self.save_data_base()
        print("Record changed successfully! Press 'LEFT' to return to the menu")


def main():
    phone_book = PhoneBook()


if __name__ == '__main__':
    main()

import datetime
import json


class PhoneBook:
    def __init__(self):
        self.all_records = list()


class Record(PhoneBook):
    def __init__(self):
        super().__init__()
        self.first_name = ""
        self.second_name = ""
        self.phone_number = ""
        self.birth_date = ""


def main():
    pass


if __name__ == '__main__':
    main()
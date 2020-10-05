import os
from datetime import datetime
from datetime import timedelta

# TASK 1
"""
class DirectionHandler:
    
    def __init__(self, dir_path=r".\\"):
        if not os.path.exists(dir_path):
            print("ERROR: Incorrect path name.")
            exit()
        self.dirPath = dir_path
        self.directory = [self.dirPath + file_name for file_name in os.listdir(dir_path)]
        self.directoryFiles = [self.directory[i] for i in range(len(self.directory))
                               if os.path.isfile(self.directory[i]) and os.path.getsize(self.directory[i]) > 140]

    def __iter__(self):
        self.fileNumber = 0
        return self

    def __next__(self):
        if self.fileNumber < len(self.directoryFiles):
            with open(self.directoryFiles[self.fileNumber], 'r', encoding='utf-8') as file:
                for line in file:
                    print(line, end="")
            self.fileNumber += 1
            return None
        else:
            raise StopIteration

    def show_corrected_files(self):
        files_iter = iter(self)
        counter = 0
        while counter < len(self.directoryFiles):
            next(files_iter)
            counter += 1
"""

# example = DirectionHandler(dir_path=r"C:\Users\user\PycharmProjects\IAD\Example\\")
# example.show_corrected_files()


# TASK 2
"""
def generate_file_names(list_file_names: list, path=r".\\") -> None:
    if not os.path.exists(dir_path):
        print("ERROR: Incorrect path name.")
        exit()
    directory = [path + file_path for file_path in os.listdir(path)]
    for obj in directory:
        if os.path.isdir(obj):
            generate_file_names(list_file_names, path=obj + r'\\')
        elif os.path.isfile(obj):
            list_file_names.append(os.path.split(obj)[-1])
"""

# file_names = list()
# generate_file_names(file_names)  # path=r"C:\Users\user\PycharmProjects\IAD\Example\\")
# print(file_names)


# TASK 3

"""

def float_range(*args, **kwargs):
    if len(args) > 3 or len(kwargs) > 3:
        print("ERROR: Incorrect number of arguments")
        return None
    else:
        for key in kwargs.keys():
            if key not in ("start", "end", "step"):
                print("ERROR: Incorrect arguments.")
                return None

    start, end, step = 0.0, 0.0, 1.0
    for key in kwargs.keys():
        if "start" == key:
            start = kwargs["start"]
        elif "end" == key:
            end = kwargs["end"]
        elif "step" == key:
            step = kwargs["step"]

    if len(args) == 1:
        end = args[0]
    elif len(args) == 2:
        end = args[0]
        step = args[1]
    elif len(args) == 3:
        start = args[0]
        end = args[1]
        step = args[2]

    while start <= end:
        yield start
        start += step


example = float_range(6.5)
for el in example:
    print(el, end=", ")    
"""

"""
def minutes_range(*args, **kwargs):
    if len(args) > 3 or len(kwargs) > 3:
        print("ERROR: Incorrect number of arguments")
        return None
    else:
        for key in kwargs.keys():
            if len(kwargs[key]) != 3 or key not in ("start", "end", "step"):
                print("ERROR: Incorrect arguments.")
                return None
    start, end, step = timedelta(hours=0, minutes=0, seconds=0), timedelta(hours=0, minutes=0, seconds=0),\
        timedelta(hours=0, minutes=5, seconds=0)

    for key in kwargs.keys():
        if "start" == key:
            start = timedelta(hours=kwargs["start"][0], minutes=kwargs["start"][1], seconds=kwargs["start"][2])
        elif "end" == key:
            end = timedelta(hours=kwargs["end"][0], minutes=kwargs["end"][1], seconds=kwargs["end"][2])
        elif "step" == key:
            step = timedelta(hours=kwargs["step"][0], minutes=kwargs["step"][1], seconds=kwargs["step"][2])

    if len(args) == 1:
        end = timedelta(hours=args[0], minutes=args[0], seconds=args[0])
    elif len(args) == 2:
        end = timedelta(hours=args[0], minutes=args[0], seconds=args[0])
        step = timedelta(hours=args[1], minutes=args[1], seconds=args[1])
    elif len(args) == 3:
        start = timedelta(hours=args[0], minutes=args[0], seconds=args[0])
        end = timedelta(hours=args[1], minutes=args[1], seconds=args[1])
        step = timedelta(hours=args[2], minutes=args[2], seconds=args[2])

    while start <= end:
        yield start
        start += step


example = minutes_range(start=[2, 10, 0], end=[3, 11, 20], step=[0, 15, 20])
for el in example:
    print(el, end=", ")
"""


# TASK 4
"""
def my_enumerate(_collection):
    if type(_collection) is dict:
        counter = 0
        for key, value in _collection.items():
            yield counter, key, value
            counter += 1
    elif type(_collection) is str or list or tuple:
        for i in range(len(_collection)):
            yield i, _collection[i]
    else:
        print("ERROR: Incorrect type for enumerate.")
        exit()

example_list = [5, 3, 4, 2]
example_str = "Hello World!"
example_tuple = ('h', 1, 2, 't')
example_dict = dict([("hello", "world"), (5, 3), ("paka", "privet")])

for collection in (my_enumerate(example_list), my_enumerate(example_tuple),
                   my_enumerate(example_str), my_enumerate(example_dict)):
    for el in collection:
        print(el, end=", ")
    print()
"""
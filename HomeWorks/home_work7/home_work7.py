import time
import math
"""
Создайте декоратор:

- который будет выводить информацию о времени выполнения функции (на экране должно отображаться название функции и время)

- который будет сохранять информацию о переданных аргументах в файл (название функции, переданные аргументы)

- который будет сохранять аргументы и возвращаемое значение функции; если переданные аргументы повторятся, вернуть
сохранённое значение – не выводить его заново.

- который будет делать паузу до и после выполнения функции, длительность пауз сделать задаваемой
"""


def time_logger(func):
    def wrap(*args):
        start_time = time.time()
        result = func(*args)
        print(f"Time: {time.time() - start_time}")
        return result
    return wrap


def args_logger(func):
    def wrap(*args, **kwargs):
        result = func(*args, **kwargs)
        with open("log.txt", "a+", encoding="utf-8") as file:
            args_str = ""
            kwargs_str = ""
            for arg in args:
                args_str += str(arg) + ", "
            for key in kwargs.keys():
                kwargs_str += str(key) + "=" + str(kwargs[key]) + ", "

            if len(args) > 0 and len(kwargs.keys()) > 0:
                file.write(f"{func.__name__}({args_str[:-2]}, {kwargs_str[:-2]})\n")
            elif len(args) > 0 and len(kwargs.keys()) == 0:
                file.write(f"{func.__name__}({args_str[:-2]})\n")
            elif len(args) == 0 and len(kwargs.keys()) > 0:
                file.write(f"{func.__name__}({kwargs_str[:-2]})\n")
            else:
                file.write(f"{func.__name__}()\n")
        return result

    return wrap


def advanced_args_logger(func):
    def wrap(*args, **kwargs):
        with open("advanced_log.txt", "a+", encoding="utf-8") as file:
            args_str = ""
            kwargs_str = ""
            for arg in args:
                args_str += str(arg) + ", "
            for key in kwargs.keys():
                kwargs_str += str(key) + "=" + str(kwargs[key]) + ", "

            if len(args) > 0 and len(kwargs.keys()) > 0:
                params = f"({args_str[:-2]}, {kwargs_str[:-2]})"
            elif len(args) > 0 and len(kwargs.keys()) == 0:
                params = f"({args_str[:-2]})"
            elif len(args) == 0 and len(kwargs.keys()) > 0:
                params = f"({kwargs_str[:-2]})"
            else:
                params = f"()"

            file.seek(0)
            for line in file:
                if line.startswith(params):
                    return line[len(params) + 4:]
            result = func(*args, **kwargs)
            file.write(params + f" -> {result}\n")
        return result
    return wrap


def set_pause(seconds):
    def set_pause_decorator(func):
        def wrap(*args, **kwargs):
            time.sleep(seconds)
            result = func(*args, **kwargs)
            # print(result)
            time.sleep(seconds)
            return result
        return wrap
    return set_pause_decorator


@time_logger
def fibonacci(number: int):
    def f(n: int) -> int:
        if n == 0:
            return 0
        if n == 1 or n == 2:
            return 1
        return f(n - 1) + f(n - 2)
    return f(number)


@advanced_args_logger
def calculate_distance(x1, y1, x2, y2) -> float:
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


@args_logger
def print_word_and_hello(word: str, second_word="IAD") -> None:
    print(f"{word} hello {second_word}")


@set_pause(seconds=5)
def count_sum(*args):
    _sum = 0
    for i in range(len(args)):
        _sum += args[i]
    return _sum


def main():
    # print(fibonacci(25))
    # print(calculate_distance(0, 2, 5, 4))
    # print(type(calculate_distance(0, 2, 5, 4)))
    # print_word_and_hello("Ivan", second_word="Python")
    print(count_sum(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))


if __name__ == '__main__':
    main()

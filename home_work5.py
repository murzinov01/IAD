import random
import itertools


def generate_sample(size: int, probability: float) -> list:
    return [1 if random.random() < probability else 0 for i in range(size)]


def generate_experience(number_of_exp: int, size: int, probability: float) -> list:
    return [sum(generate_sample(size, probability)) for i in range(number_of_exp)]


def generate_string(string: str, size: int, repeat: False) -> str:
    if not repeat and size > len(string):
        print("ERROR: there are more characters in the output string than in the input string!!")
        exit(1)

    symbols = list(string)
    result = ""

    if not repeat:
        for i in range(size):
            index = random.randint(0, len(symbols) - 1)
            result += symbols[index]
            symbols.remove(symbols[index])
    else:
        for i in range(size):
            index = random.randint(0, len(symbols) - 1)
            result += symbols[index]
    return result


def generate_various_strings_by_str(string: str) -> set:
    return {"".join(item) for item in itertools.permutations(string, len(string))}


def main():
    print(generate_sample(10, 0.5))
    print(generate_experience(10, 10, 0.5))
    print(generate_string("aab", 2, False))
    print(generate_various_strings_by_str("aab"))
    print(generate_various_strings_by_str("hello"))


if __name__ == '__main__':
    main()
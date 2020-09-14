import random


class TextHandler:

    TEXT = ""
    WORDS = list()

    def __init__(self, file_name="test_example.txt"):
        self.file_name = file_name
        self.get_text()
        self.extract_all_words()

    def get_text(self) -> None:
        with open(self.file_name, "r", encoding="utf-8") as file:
            self.TEXT = ".".join([line.rstrip() for line in file.readlines()])

    def extract_all_words(self) -> None:
        self.WORDS = [word.strip(",.!?;'") for word in self.TEXT.split()]

    def count_all_words(self) -> int:
        return len(self.WORDS)

    def find_top_of_words(self, top_n=10) -> list or None:
        words = dict()
        for word in self.WORDS:
            words[word] = 1 if word not in words.keys() else words[word] + 1
        sorted_words = list(words.items())
        sorted_words.sort(key=lambda x: x[1])
        sorted_words = sorted_words[::-1]
        return [sorted_words[i][0] for i in range(top_n)]

    def reverse_text_sentences(self) -> str:
        start_pos = 0
        sentences = list()
        for i in range(len(self.TEXT)):
            if self.TEXT[i] in (".", "!", "?"):
                sentences.append(self.TEXT[start_pos:i + 1])
                start_pos = i + 1
        sentences = [(sentence[:-1].split(), sentence[-1]) for sentence in sentences]
        return "".join([" ".join(sentence[0][::-1]) + sentence[1] + " " for sentence in sentences])


def get_iteration_num(num: int) -> int:
    it_num = 0
    while num != 1:
        it_num += 1
        if num % 2 == 0:
            num = num / 2
        else:
            num = 3*num + 1
    return it_num


def get_strange_prime_number(prime_numbers=1000) -> int:
    numbers = {num: 0 for num in range(1, prime_numbers + 1)}
    for key in numbers.keys():
        numbers[key] = get_iteration_num(key)
    items = list(numbers.items())
    items.sort(key=lambda x: x[1])
    return items[::-1][0][0]


def guessing_game(max_n: int) -> None:
    target_num = random.randint(1, max_n)
    print("Try to guess (enter a number)")
    num = max_n + 1
    counter = 0
    while num != target_num:
        num = int(input())
        if num < target_num:
            print("Above")
        else:
            print("Below")
        counter += 1
    print(f"You guessed it! Number of attempts: {counter}")


def reverse_guessing_game(max_n: int) -> None:
    print("Make a number: ", end="")
    print(f"My number: {input()}")
    min_n = 0
    counter = 0
    target_num = (max_n + min_n) // 2

    while True:
        counter += 1
        print(f"This is the number {target_num}? (Enter 'Yes' or 'No')")
        answer = input()
        if answer.lower() == "yes":
            print(f"I guessed it! Number of attempts: {counter}")
            break
        else:
            print("Is this number greater or less? (Enter 'Greater' or 'Less')")
            answer = input()
            if answer.lower() == "greater":
                min_n = target_num
                target_num = (target_num + max_n) // 2
            else:
                max_n = target_num
                target_num = (target_num + min_n) // 2


def main():

    """ TASK 1"""
    # ex = TextHandler(file_name="text_example.txt")
    # print("Initial Text:")
    # print(ex.TEXT)
    # print("Top list:")
    # print(ex.count_all_words())
    # for num, word in enumerate(ex.find_top_of_words(), 1):
    #     print(f"{num}) {word}")
    # print("Reverse text sentences:")
    # print(ex.reverse_text_sentences())

    # """ TASK 2"""
    # print("Strange prime number is: ", get_strange_prime_number())
    #
    # """ TASK 3"""
    # print("Enter a maximum number: ", end="")
    # n = int(input())
    # guessing_game(n)
    # # reverse_guessing_game()


if __name__ == '__main__':
    main()

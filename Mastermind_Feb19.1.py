"""
Mastermind AI
Version Feb19.1
Made by Ian Pinto

ABOUT
This program uses artificial intelligence to guess a combination in a simulated game of Mastermind, then picks a random
combination and gets you to guess it. Think you can get it in less guesses?

INSTRUCTIONS
- Pick a combination then press Enter. The colours are: red, orange, yellow, green, blue, purple, black, white.
- The AI will try to guess the combination. Enter the result based on the Mastermind system i.e. a red for each colour
  and position match and white for each colour match in the wrong position.
- Repeat until your combination has been guessed.
- Now you try to guess a combination picked randomly by the AI. Enter a guess e.g. red,blue,yellow,green. The program
  picks up typos.
- Repeat until you guess the combination.
- Check the results just to make sure you lost :)
"""
from time import perf_counter, sleep
from random import choice
print("Please note that this program may require some time for processing.")
colours = ["red", "orange", "yellow", "green", "blue", "purple", "black", "white"]  # Purple is also dark blue
all_combos = []
for first in colours:
    for second in colours:
        for third in colours:
            for fourth in colours:
                all_combos.append([first, second, third, fourth])
all_possibilities = all_combos


def get_result(_guess: list, answer: list):
    white = 0
    red = 0
    _answer = [x for x in answer]
    for position in range(4):
        if _guess[position] == _answer[position]:
            _answer[position] = "-"
            white += 1
        elif _guess[position] in _answer:
            _answer[_answer.index(_guess[position])] = "-"
            red += 1
    return [white, red]


def solve():
    time_start = perf_counter()
    global all_possibilities
    time_taken = 0
    guess = ["red", "orange", "yellow", "green"]
    guesses = 0
    while True:
        time_end = perf_counter()
        time_taken += time_end - time_start
        result = input(f"Guess is {guess[0]}, {guess[1]}, {guess[2]}, {guess[3]}. Enter result in format (white) (red) "
                       f"e.g. 2 1: ")
        time_start = perf_counter()
        guesses += 1
        if result == "4 0":
            time_end = perf_counter()
            return {"guesses": guesses, "time": time_taken}
        result = [int(number) for number in result.split(" ")]
        all_possibilities = list(filter(lambda p: get_result(guess, p) == result, all_possibilities))
        if not all_possibilities:
            print("Sorry, you made a mistake somewhere. Resetting...")
            return "ERROR"
        if len(all_possibilities) == 1:
            guess = all_possibilities[0]
        elif guesses == 1:
            guess = ["blue", "purple", "black", "white"]
        else:
            print(f"Now analysing {len(all_possibilities)} possibilities, please be patient...")

            best_score = None
            for test_possibility_no in range(len(all_possibilities)):
                test_possibility = all_possibilities[test_possibility_no]
                score = 0
                for possible_answer in all_possibilities:
                    _filter = filter(lambda _possibility: (get_result(test_possibility, possible_answer) !=
                                                           get_result(_possibility, possible_answer)),
                                     all_possibilities)
                    score += len(list(_filter))
                score = score / len(all_possibilities)
                if best_score is None or score < best_score:
                    guess = test_possibility
                if test_possibility_no == round(len(all_possibilities) / 2):
                    print("Halfway done...")


print("Pick a combination of colours.")
sleep(2)
input("Press Enter when you're ready to go.")
solve_result = solve()
while solve_result == "ERROR":
    solve_result = solve()
print("Guesses taken: " + str(solve_result["guesses"]))
print("Time taken: " + str(round(solve_result["time"] * 100) / 100) + " s")

# Now the user tries to guess a combination
print("\nNow it's your turn!\n")
answer = [choice(colours), choice(colours), choice(colours), choice(colours)]
guesses = 0
result = None
while result != [4, 0]:
    guess = input("Enter a guess: ")
    while True:
        guess_colours = [colour.replace(" ", "").lower() for colour in guess.split(",")]
        if len(guess_colours) == 4:
            for colour in guess_colours:
                if colour not in colours:
                    break
            else:
                break
        guess = input("Enter a valid guess: ")
    guesses += 1
    # todo
    guess_colours = [colour.lower() for colour in guess.split(",")]
    result = get_result(guess_colours, answer)
    print(f"Result: {result[0]} whites and {result[1]} reds")

print(f"\nYou took {guesses} guesses and the AI took " + str(solve_result["guesses"]) + " guesses.")
if guesses < solve_result["guesses"]:
    print("You win!")
elif guesses == solve_result["guesses"]:
    print("Tie!")
else:
    print("You lose!")

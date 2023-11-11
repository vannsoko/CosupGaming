#!/usr/bin/python3
import random
import sys


with open('word_list.txt', 'r') as f:
    word_list: str = f.read()

caracters: list[str] = [
    'a', 'b', 'c', 'd', 'e',
    'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y',
    'z', '-'
]
player_error: int = 0
found_letters: list[str] = []
try_letters: list[str] = []
word_found: bool = False


def hangman_name():
    print("H  A  N  G  M A  N")


def shaft():
    local_player_error: int = len(try_letters)
    print("   +---+")
    if local_player_error >= 1:
        print("   O   |")
    else:
        print("       |")

    if local_player_error == 2:
        print("   |   |")
    elif local_player_error == 3:
        print("  /|   |")
    elif local_player_error >= 4:
        print("  /|\  |")
    else:
        print("       |")

    if local_player_error == 5:
        print("  /    |")
    elif local_player_error == 6:
        print("  / \  |")
    else:
        print("       |")
    print("      ===")


def word_noun():
    word_generated: str = random.choice(word_list)
    print(word_generated)
    word_generated_length: int = len(word_generated)
    word_generated_letters_all: List[str] = [
        word_generated[i] for i in range(len(word_generated))
    ]
    word_generated_letters: List[str] = list(set(word_generated_letters_all))
    return word_generated, word_generated_letters_all, word_generated_letters, word_generated_length


def mysterious_word_invisible():
    print("Missed letters:", end=" ")
    for letter in try_letters:
        print(letter, end=" ")
    print()
    if len(found_letters) == 0:
        print("_ " * word_to_guess_length)
    else:
        for letter in word_to_guess:
            if letter in found_letters:
                print(f"{letter} ", end="")
            else:
                print("_ ", end="")
    print("\nGuess a letter.")


def check_user_entry():
    found_letters_length_init: int = len(found_letters)
    local_player_error: int = player_error
    user_input: str = input().lower()
    if len(user_input) == 1 and user_input in caracters:
        if user_input in found_letters or user_input in try_letters:
            _extracted_from_check_user_entry_7(
                "You have already guessed that letter.", check_user_entry
            )
        else:
            for i in range(len(word_to_guess_letters)):
                if user_input == word_to_guess_letters[i]:
                    found_letters.append(word_to_guess_letters[i])
                    break
                else:
                    if user_input not in try_letters:
                        try_letters.append(user_input)
            found_letters_length_final: int = len(found_letters)
            if found_letters_length_init == found_letters_length_final:
                local_player_error += 1
            for x in word_to_guess_letters:
                if x in try_letters:
                    try_letters.remove(x)
    else:
        _extracted_from_check_user_entry_7("Invalid entry", check_user_entry)
    return found_letters, local_player_error


# TODO Rename this here and in `check_user_entry`
def _extracted_from_check_user_entry_7(arg0, check_user_entry):
    print(arg0)
    print("Guess a letter.")
    check_user_entry()


def end_of_game():
    if set(word_to_guess_letters) == set(found_letters):
        local_word_found = True
        _extracted_from_end_of_game_4("You have won!")
    elif player_error == 6:
        _extracted_from_end_of_game_4("You lose !!!")
        local_word_found = True
    else:
        local_word_found = False
    return local_word_found


# TODO Rename this here and in `end_of_game`
def _extracted_from_end_of_game_4(arg0):
    print(arg0)
    print(f'The secret word is "{word_to_guess}"! ')
    print(f"You have make {player_error} errors ! ")


def rematch():
    play_again_input = input("Do you want to play again? (yes or no)\n").lower()
    if play_again_input == "yes":
        local_player_error: int = 0
        local_word_found: bool = False
        local_found_letters: List[str] = []
        local_try_letters: List[str] = []
        return local_player_error, local_word_found, local_found_letters, local_try_letters
    elif play_again_input == "no":
        sys.exit()
    else:
        print("Incorrect input")


if __name__ == '__main__':
    hangman_name()
    while True:
        word_to_guess, word_to_guess_letters_all, word_to_guess_letters, word_to_guess_length = word_noun()
        while player_error < 6 and not word_found:
            shaft()
            mysterious_word_invisible()
            found_letters, player_error = check_user_entry()
            word_found = end_of_game()
        player_error, word_found, found_letters, try_letters = rematch()
        if word_found:
            break

import random

def hangman_game(words_list, max_attempts=7):
    print("Welcome to Hangman!")
    
    word = random.choice(words_list)
    word = word.lower()  # Ensure the word is in lowercase.
    word_length = len(word)

    attempts = 0
    guessed_letters = set()
    word_progress = ["_"] * word_length
    
    def render_state():
        print(" ".join(word_progress))
        print("Attempts left:", max_attempts - attempts)
        print("Guessed letters:", ", ".join(sorted(guessed_letters)))

    while "_" in word_progress and attempts < max_attempts:
        render_state()
        guess = input("Enter your guess (You can only guess a single letter): ").lower()

        if not guess.isalpha() or len(guess) != 1:
            print("Invalid input. Please guess a single letter.")
            continue
        
        if guess in guessed_letters:
            print("You've already guessed this letter.")
            continue

        guessed_letters.add(guess)

        if guess in word:
            for i, letter in enumerate(word):
                if letter == guess:
                    word_progress[i] = guess
        else:
            attempts += 1

    if "_" not in word_progress:
        print("\nCongratulations! You won the Hangman game. The word was '" + word + "'")
    else:
        print("\nGame Over! You've run out of attempts. The word was '" + word + "'.")

# Example usage:
words_list = ["apple", "banana", "grape", "orange", "mango", "pineapple"]
hangman_game(words_list)
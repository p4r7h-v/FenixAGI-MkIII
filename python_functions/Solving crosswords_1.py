import re
import nltk
from nltk.corpus import words

nltk.download("words")

def solve_crossword(puzzle):
    word_list = words.words()
    pattern = ""
    
    for ch in puzzle:
        if ch == ".":
            pattern += "[a-zA-Z]"
        else:
            pattern += ch

    matching_words = [word for word in word_list if re.match(pattern, word)]

    for word in matching_words:
        print(word)

# Example usage
solve_crossword(".o.ip.")
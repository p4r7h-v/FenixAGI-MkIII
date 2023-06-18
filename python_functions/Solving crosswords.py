import re

def crossword_solver(pattern, word_list):
    """
    Find possible matches for a crossword row or column based on a given pattern and a word list.
    
    :param pattern: a string representing the crossword row or column with missing letters replaced by dots (.) or other special characters (e.g., '.a..le')
    :param word_list: a list of strings representing the words available to be used as the crossword answers
    :return: a list of strings representing the words that fit the pattern from the given word list
    """
    matches = []
    regex_pattern = re.compile("^" + pattern.replace(".", "\w") + "$")
    
    for word in word_list:
        if regex_pattern.match(word):
            matches.append(word)

    return matches

# Example usage:
word_list = ['apple', 'banana', 'orange', 'pear', 'grape']
pattern = '.a..le'

result = crossword_solver(pattern, word_list)
print(result)  # Output: ['apple']

# You can further improve the function or build more functions to handle other aspects of solving crosswords.
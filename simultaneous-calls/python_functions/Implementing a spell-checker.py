import Levenshtein

def spell_checker(word, dictionary, max_distance=3):
    """A simple spell-checker based on Levenshtein distance.
    
    Args:
        word (str): The word to check.
        dictionary (list): A list of known correct words.
        max_distance (int, optional): Maximum allowed Levenshtein distance to consider a word as similar.
    
    Returns:
        list: A list of corrections, sorted by ascending Levenshtein distance.
    """

    corrections = []
    
    if word in dictionary:
        return [word]

    for known_word in dictionary:
        distance = Levenshtein.distance(word, known_word)
        if distance <= max_distance:
            corrections.append((known_word, distance))

    return [correction[0] for correction in sorted(corrections, key=lambda x: x[1])]

# Example usage

dictionary = ["apple", "banana", "grape", "orange", "mango", "kiwi", "pear", "strawberry"]
word = "appla"
corrections = spell_checker(word, dictionary)
print(corrections)
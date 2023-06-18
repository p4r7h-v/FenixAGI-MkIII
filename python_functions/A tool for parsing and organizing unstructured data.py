import re
from collections import defaultdict

def parse_organize_data(text):
    # Build a regular expression pattern to match non-whitespace sequences
    pattern = re.compile('\S+')

    # Initialize a default dictionary to store word frequencies
    word_frequencies = defaultdict(int)

    # Find all words in the given text
    words = pattern.findall(text)

    # Update each word's frequency
    for word in words:
        word_frequencies[word.lower()] += 1

    return word_frequencies
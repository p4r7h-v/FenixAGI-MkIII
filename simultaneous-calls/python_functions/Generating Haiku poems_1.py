import random

def generate_haiku(lines_5, lines_7):
    """
    Generates a Haiku poem by randomly selecting lines from given lists of 5- and 7-syllable lines.

    :param lines_5: a list of 5-syllable lines
    :param lines_7: a list of 7-syllable lines
    :return: a string containing the generated Haiku poem
    """
    if not lines_5 or not lines_7:
        return "Please provide input lists for 5-syllable and 7-syllable lines."
    
    line_1 = random.choice(lines_5)
    line_2 = random.choice(lines_7)
    line_3 = random.choice(lines_5)

    haiku = f"{line_1}\n{line_2}\n{line_3}"
    return haiku


# Sample lists of 5- and 7- syllable lines
lines_5 = [
    "An old silent pond",
    "Autumn moonlight",
    "Light of the moon",
    "A summer river"
]

lines_7 = [
    "A frog jumps into the pond",
    "A worm digs silently",
    "Moves west flowers' shadows",
    "Being scarcely cooled"
]

# Generate and print a Haiku poem
print(generate_haiku(lines_5, lines_7))
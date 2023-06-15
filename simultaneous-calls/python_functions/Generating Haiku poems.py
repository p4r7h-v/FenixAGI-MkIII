import random

def generate_haiku():
    # Lists of words for each line (5-7-5 format)
    five_syllable_words = [
        ["morning", "wind", "disappears"],
        ["bright", "sunlight", "shimmers"],
        ["children", "at", "play", "in", "park"],
        ["flowing", "river", "passes"],
        ["clouds", "cross", "blue", "autumn", "sky"]
    ]

    seven_syllable_words = [
        ["birds", "sing", "in", "the", "branches", "of", "trees"],
        ["rain", "falls", "gently", "on", "asphalt", "roads"],
        ["evening", "stars", "illuminate", "the", "night"],
        ["mountains", "stand", "tall", "above", "green", "valleys"],
        ["blossoms", "in", "spring", "brought", "forth", "by", "life"]
    ]

    # Randomly select lines to create a Haiku
    line1 = random.choice(five_syllable_words)
    line2 = random.choice(seven_syllable_words)
    line3 = random.choice(five_syllable_words)

    # Join the words in each line
    haiku = "\n".join([" ".join(line) for line in [line1, line2, line3]])

    return haiku

# Print a generated Haiku
print(generate_haiku())
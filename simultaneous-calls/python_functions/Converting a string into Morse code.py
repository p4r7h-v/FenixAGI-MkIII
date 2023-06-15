def string_to_morse_code(input_string):
    morse_code_dict = {'A': '.-', 'B': '-...',
                       'C': '-.-.', 'D': '-..', 'E': '.',
                       'F': '..-.', 'G': '--.', 'H': '....',
                       'I': '..', 'J': '.---', 'K': '-.-',
                       'L': '.-..', 'M': '--', 'N': '-.',
                       'O': '---', 'P': '.--.', 'Q': '--.-',
                       'R': '.-.', 'S': '...', 'T': '-',
                       'U': '..-', 'V': '...-', 'W': '.--',
                       'X': '-..-', 'Y': '-.--', 'Z': '--..',
                       '1': '.----', '2': '..---', '3': '...--',
                       '4': '....-', '5': '.....', '6': '-....',
                       '7': '--...', '8': '---..', '9': '----.',
                       '0': '-----'}

    input_string = input_string.upper()
    morse_code = ""

    for char in input_string:
        if char in morse_code_dict:
            morse_code += morse_code_dict[char] + " "

    return morse_code.strip()

# Example usage
input_string = "Python"
morse_code = string_to_morse_code(input_string)
print(f"Morse code for '{input_string}': {morse_code}")
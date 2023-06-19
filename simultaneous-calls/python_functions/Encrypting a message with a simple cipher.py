def caesar_cipher_encrypt(message, shift):
    encrypted_message = ""
    for char in message:
        if char.isalpha():
            shift_amount = shift % 26
            if char.islower():
                new_char = chr(((ord(char) - 97 + shift_amount) % 26) + 97)
            else:
                new_char = chr(((ord(char) - 65 + shift_amount) % 26) + 65)
            encrypted_message += new_char
        else:
            encrypted_message += char

    return encrypted_message
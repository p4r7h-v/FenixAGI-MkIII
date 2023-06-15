import string
import random

def generate_random_password(length=10):
    """Generate a random password with the given length."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Example usage:
password = generate_random_password(12)  # Generate a 12-character random password
print(password)
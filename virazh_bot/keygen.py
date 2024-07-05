import random
import string
from random import randint

def generate_password(length):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def generate_code():
    return randint(1000, 10000)

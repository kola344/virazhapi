import random
import string
from random import randint
import db

def generate_password(length):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

async def generate_birthdayPromo(length):
    characters = string.ascii_letters + string.digits
    promo = ''.join(random.choice(characters) for _ in range(length))
    while await db.birthdayPromocodes.check_promocode(promo):
        promo = ''.join(random.choice(characters) for _ in range(length))
    await db.birthdayPromocodes.add_promocode(promo)
    return promo

def generate_code():
    return randint(1000, 10000)

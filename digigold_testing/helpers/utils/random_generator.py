import uuid
import random


def generate_token(n_size=5) -> str:
    """
    Creates a Random Token
    :param n_size: Size of the generated token
    :return: Random token
    """
    value = str(uuid.uuid4())
    value = value.upper()
    value = value.replace("-", "")
    return value[0:n_size]


def get_random_buy_price():
    value = random.randint(1, 8)
    return value * 10


def get_random_sell_price():
    value = random.randint(8, 15)
    return value * 10

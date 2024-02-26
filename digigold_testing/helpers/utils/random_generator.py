import uuid
import random
import digigold_testing.config as config


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


def get_random_buy_price(min_val=config.BUY_MIN_PRICE, max_val=config.BUY_MAX_PRICE) -> int:
    value = random.randint(min_val, max_val)
    return value * 10


def get_random_sell_price(min_val=config.SELL_MIN_PRICE, max_val=config.SELL_MAX_PRICE) -> int:
    value = random.randint(min_val, max_val)
    return value * 10

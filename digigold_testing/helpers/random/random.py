import uuid


def generate_token(n_size=5) -> str:
    """
    Creates a Random Token
    :param n_size: Size of the generated token
    :return: Random token
    """
    random = str(uuid.uuid4())
    random = random.upper()
    random = random.replace("-", "")
    return random[0:n_size]

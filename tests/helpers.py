import random
import string


def next_random_string(charset=string.ascii_letters, length: int = 20):
    assert length > 0
    assert len(charset) > 0

    return "".join([random.choice(charset) for _ in range(length)])

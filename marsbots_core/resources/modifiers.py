import random
from typing import Optional


def with_probabilities(
    *probabilities: tuple[tuple],
) -> Optional[any]:
    """
    Takes a tuple of ((function, args), probability) pairs and returns a
    the result of a random function call based on the probabilities.
    Returns None if no function is called.
    """
    choices, probs = zip(*probabilities)
    total_prob = sum(probs)
    if total_prob > 1:
        raise (ValueError("Probabilities sum must be less than or equal to 1"))
    if total_prob < 1:
        choices = choices + (None,)
        probs = probs + (1 - total_prob,)
    res = random.choices(choices, weights=probs)[0]
    if res:
        func, args = res
        return func(*args)
    return None

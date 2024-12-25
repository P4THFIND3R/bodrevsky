import random
import string


class Randomizer:
    @staticmethod
    def generate_random_string(k: int = 5):
        return "".join(random.choices(string.ascii_letters + string.digits, k=k))


randomizer = Randomizer()

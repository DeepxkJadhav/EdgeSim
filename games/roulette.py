import random

class Roulette:
    def __init__(self):
        self.numbers = list(range(37))
        self.colors = {i: ("Red" if i % 2 else "Black") for i in self.numbers}

    def payout(self, choice="Red", amount=100):
        spin = random.choice(self.numbers)
        result_color = self.colors[spin]
        payout = amount * 2 if result_color == choice else 0
        return result_color, payout

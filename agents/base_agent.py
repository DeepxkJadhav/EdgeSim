import random

class BaseAgent:
    def __init__(self, bankroll=1000):
        self.bankroll = bankroll

    def choose_bet(self, game):
        return {"choice": random.choice(["Red", "Black"]), "amount": 10}

    def update(self, result):
        self.bankroll += result

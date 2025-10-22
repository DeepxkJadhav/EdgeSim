import random

class SlotMachine:
    def __init__(self):
        self.symbols = ["🍒", "🍋", "🔔", "⭐", "7️⃣"]

    def spin(self):
        result = [random.choice(self.symbols) for _ in range(3)]
        win = 10 if len(set(result)) == 1 else -1
        return result, win

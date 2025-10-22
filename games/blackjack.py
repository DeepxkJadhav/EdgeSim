import random

class Blackjack:
    def play_hand(self, policy):
        # Simplified blackjack logic
        player = random.randint(12, 21)
        dealer = random.randint(17, 23)
        if dealer > 21 or player > dealer:
            return 1  # win
        elif player == dealer:
            return 0
        else:
            return -1

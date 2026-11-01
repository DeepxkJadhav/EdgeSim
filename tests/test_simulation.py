import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from games.blackjack import Blackjack
from games.roulette import Roulette
from games.slots import SlotMachine

def test_blackjack_hand_resolution():
    game = Blackjack()
    outcome = game.play_hand(policy=None)
    assert outcome in [-1, 0, 1], "Blackjack outcome must be -1 (loss), 0 (push), or 1 (win)"

def test_roulette_spin():
    game = Roulette()
    color, payout = game.payout(choice="Red", amount=50)
    assert color in ["Red", "Black"], f"Unexpected roulette color outcome {color}"
    assert payout in [0, 100], f"Unexpected payout {payout} on a $50 bet"

def test_slot_machine_spin():
    game = SlotMachine()
    reels, win = game.spin()
    assert len(reels) == 3, "SlotMachine should return exactly 3 reel symbols"
    assert win in [-1, 10], f"Unexpected slot outcome {win}"

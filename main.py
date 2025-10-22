import os
import sys
import numpy as np

# Import PyQt6 and Dashboard only if available so the app can run headless
try:
    from PyQt6.QtWidgets import QApplication
    from ui.dashboard import Dashboard
    PYQT_AVAILABLE = True
except Exception:
    PYQT_AVAILABLE = False
from games.roulette import Roulette
from games.blackjack import Blackjack
from games.slots import SlotMachine
from agents.base_agent import BaseAgent

# Optional RL stub: dynamically import train_rl_agent from available agent modules
import importlib

def _load_rl_train():
    for mod in ("agents.rl_agent", "agents.r1_agent"):
        try:
            m = importlib.import_module(mod)
            if hasattr(m, "train_rl_agent"):
                return getattr(m, "train_rl_agent")
        except Exception:
            continue
    # final fallback: no-op trainer
    return lambda *args, **kwargs: None

train_rl_agent = _load_rl_train()

from analytics.stats_logger import StatsLogger
from analytics.risk_engine import expected_value, drawdown


class Simulator:
    def __init__(self):
        self.logger = StatsLogger()

    def get_game(self, name):
        if name == "Roulette": return Roulette()
        elif name == "Blackjack": return Blackjack()
        else: return SlotMachine()

    def get_agent(self, name):
        if name == "RL Agent":
            model = train_rl_agent()
            agent = BaseAgent()
        else:
            agent = BaseAgent()
        return agent

    def run_sessions(self, game_name, agent_name, n=100):
        game = self.get_game(game_name)
        agent = self.get_agent(agent_name)
        bankrolls, results = [], []

        for i in range(n):
            if game_name == "Roulette":
                bet = agent.choose_bet(game)
                # games.Roulette.payout returns (result_color, payout_amount)
                _, payout_amount = game.payout(**bet)
                result = payout_amount
            elif game_name == "Blackjack":
                result = game.play_hand(lambda p, d: "hit" if p < 16 else "stand")
            else:
                _, result = game.spin()

            agent.update(result)
            bankrolls.append(agent.bankroll)
            results.append(result)
            self.logger.log(i, result, agent.bankroll)

        # ✅ Ensure logs folder exists
        os.makedirs("logs", exist_ok=True)
        self.logger.to_csv(f"logs/{game_name.lower()}_results.csv")

        stats = {
            "final_bankroll": agent.bankroll,
            "expected_value": expected_value(results),
            "max_drawdown": drawdown(results)
        }
        return bankrolls, stats


if __name__ == "__main__":
    sim = Simulator()
    if PYQT_AVAILABLE:
        app = QApplication(sys.argv)
        dashboard = Dashboard(sim)
        dashboard.show()
        sys.exit(app.exec())
    else:
        # Headless fallback: run a short CLI simulation and print results
        print("PyQt6 not available — running headless simulation fallback.")
        bankrolls, stats = sim.run_sessions("Roulette", "Base Agent", n=20)
        print("Bankrolls:", bankrolls)
        print("Stats:")
        for k, v in stats.items():
            print(f"  {k}: {v}")
        sys.exit(0)

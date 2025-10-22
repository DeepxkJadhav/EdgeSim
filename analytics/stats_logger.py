import pandas as pd
import os

class StatsLogger:
    def __init__(self):
        self.records = []

    def log(self, session_id, result, bankroll):
        self.records.append({"session": session_id, "result": result, "bankroll": bankroll})

    def to_csv(self, filename="logs/results.csv"):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        pd.DataFrame(self.records).to_csv(filename, index=False)

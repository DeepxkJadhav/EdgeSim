import numpy as np

def expected_value(results):
    return np.mean(results) if len(results) else 0

def drawdown(results):
    if not results:
        return 0
    equity_curve = np.cumsum(results)
    peak = np.maximum.accumulate(equity_curve)
    dd = equity_curve - peak
    return abs(np.min(dd)) if len(dd) else 0

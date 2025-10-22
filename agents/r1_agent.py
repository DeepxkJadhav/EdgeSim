from stable_baselines3 import DQN
from gymnasium import Env, spaces
import numpy as np

# Dummy RL environment for placeholder
class RouletteEnv(Env):
    def __init__(self):
        super().__init__()
        self.action_space = spaces.Discrete(37)
        self.observation_space = spaces.Box(low=0, high=36, shape=(1,), dtype=np.int32)
        self.state = np.array([0], dtype=np.int32)

    def reset(self, *, seed=None, options=None):
        self.state = np.array([0], dtype=np.int32)
        return self.state, {}

    def step(self, action):
        winner = np.random.randint(0, 37)
        reward = 35 if int(action) == int(winner) else -1
        self.state = np.array([winner], dtype=np.int32)
        terminated = True   # one-shot roulette spin
        truncated = False
        return self.state, reward, terminated, truncated, {}

def train_rl_agent():
    # Stub for now — replace with real training (DQN/PPO) later.
    print("RL agent training stub — plug in your PPO/DQN later.")
    return None

# Optional: uncomment and use when ready to train
# def train_rl_agent_real():
#     model = DQN("MlpPolicy", RouletteEnv(), verbose=0)
#     model.learn(total_timesteps=10000)
#     model.save("agents/roulette_rl.zip")
#     return model

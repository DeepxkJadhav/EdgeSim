# EdgeSim

> **AI-Powered Casino Strategy Simulator for Research & Education**  
> *Offline • Ethical • Windows-Compatible*

---

## 🎯 Overview

**EdgeSim** is a research-oriented simulation suite designed for AI/ML developers, game theorists, and quantitative enthusiasts to explore **reinforcement learning**, **probabilistic modeling**, and **risk-aware decision-making** in stochastic environments like:
- Roulette  
- Blackjack  
- Slot machines  

⚠️ **This software does NOT interact with real online casinos.**  
All game mechanics, random number generation, and outcome sequences are simulated **locally on your machine**. It is built strictly for **educational, experimental, and algorithmic research purposes**.

> Think of it as a *"flight simulator for gambling strategies"*—you can test theories, train agents, and visualize statistical edges, but you never leave the lab.

---

## 🔬 Core Capabilities

### 🎲 Realistic Game Simulations
- **European & American Roulette** (with accurate house edge modeling)  
- **Blackjack** (standard rules, dealer logic, basic strategy baseline)  
- **Pseudo-slot machines** (configurable RTP, volatility, symbol distributions)

### 🤖 AI-Driven Strategy Engine
- Train **reinforcement learning agents** (PPO, DQN) to optimize betting  
- **Monte Carlo Tree Search (MCTS)** for decision lookahead  
- **Bayesian changepoint detection** to identify simulated "favorable regimes"

### 📊 Edge Detection & Risk Analytics
- Dynamic calculation of **expected value (EV)** per decision  
- **Kelly Criterion**-based bankroll management  
- Confidence intervals and win-rate forecasting over **10,000+ simulated sessions**

### 💻 Interactive Dashboard (Windows GUI)
- Real-time charts: win/loss, edge probability, volatility  
- Session replay & strategy comparison  
- Export logs to **CSV/JSON** for further analysis

---

## 🛠️ Technology Stack

| Layer             | Technology                          |
|-------------------|-------------------------------------|
| **Core Engine**   | Python 3.10+                        |
| **ML/RL**         | PyTorch, Stable-Baselines3, NumPy, SciPy |
| **Simulation**    | Custom Gym-compatible environments  |
| **UI Framework**  | PyQt6 (native Windows look & feel)  |
| **Packaging**     | PyInstaller → Standalone `.exe`     |
| **Visualization** | Matplotlib, Plotly (embedded in GUI)|
| **Logging**       | Structured JSON + CSV output        |

---

## 📦 Installation (Windows)

> **Prerequisites**: Windows 10/11, 8GB+ RAM recommended

### Option 1: Pre-built Executable (Recommended)
1. Download the latest release from [GitHub Releases](https://github.com/DeepxkJadhav/EdgeSim/releases)  
2. Extract the ZIP file  
3. Run `EdgeSim.exe` — **no installation required**

### Option 2: From Source
```bash
git clone https://github.com/DeepxkJadhav/EdgeSim.git
cd EdgeSim
pip install -r requirements.txt
python main.py
```

To build your own `.exe`:
```bash
pyinstaller --onefile --windowed --name EdgeSim main.py
```

---

## 🧪 Example Use Cases

- **Research**: Test how RL agents adapt to changing house edges  
- **Education**: Visualize the law of large numbers in action  
- **Algorithm Development**: Benchmark your custom betting strategy against baselines  
- **Risk Modeling**: Simulate 100,000 sessions to evaluate drawdown risk  

💡 *Tip: Use the **"Strategy Lab"** tab to code your own betting logic in Python and plug it into the simulator.*

---

## ⚖️ Ethical & Legal Disclaimer

**EdgeSim is NOT a gambling tool.**  
- It **never connects to the internet** during simulation (unless you manually load configs).  
- It **does not scrape, automate, or interact** with any real casino website or API.  
- All outcomes use **local pseudorandom generators** with reproducible seeds.  

> Using AI to gain an advantage on real-money gambling platforms violates terms of service and may be illegal. This project exists **solely for simulation, learning, and ethical AI research**.

---

## 🧑‍💻 For Developers

- Extend game rules via `games/` module  
- Plug in custom RL agents in `agents/`  
- Modify risk models in `analytics/risk_engine.py`  
- All UI components are modular (Qt-based)  

Contributions welcome! Please follow the [Code of Conduct](CODE_OF_CONDUCT.md).

---

## 📜 License

**MIT License** — Free for personal, academic, and open-source use.  
*Not for commercial deployment in gambling-adjacent products.*

---

## 🌟 Built With Passion By

**Deepak Jadhav**  
AI/ML Developer | GitHub: [@DeepxkJadhav](https://github.com/DeepxkJadhav)  
*"Code is my jutsu."*

> 🔒 **Remember**: The only guaranteed winning move in gambling is not to play.  
> But in simulation? You can learn, iterate, and master the math—safely.
```


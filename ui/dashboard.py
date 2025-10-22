from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox,
    QHBoxLayout, QProgressBar, QMessageBox, QTabWidget, QFormLayout, QLineEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class SimulationWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(list, dict)

    def __init__(self, sim, game_name, agent_name, sessions):
        super().__init__()
        self.sim = sim
        self.game_name = game_name
        self.agent_name = agent_name
        self.sessions = sessions

    def run(self):
        bankrolls, stats = self.sim.run_sessions(self.game_name, self.agent_name, self.sessions)
        self.finished.emit(bankrolls, stats)


class Dashboard(QWidget):
    def __init__(self, simulator):
        super().__init__()
        self.sim = simulator
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("🎰 EdgeSim — Casino Strategy Simulator")
        self.setGeometry(200, 100, 900, 600)
        self.setStyleSheet("""
            QWidget { background-color: #101820; color: #E0E0E0; font-family: 'Segoe UI'; }
            QLabel { font-size: 16px; }
            QComboBox, QPushButton, QLineEdit {
                background-color: #1E2A38; border-radius: 6px; padding: 6px 10px;
                font-size: 14px; color: #E0E0E0;
            }
            QPushButton:hover { background-color: #2E3C4F; }
            QPushButton:disabled { background-color: #444; color: #999; }
        """)

        main_layout = QVBoxLayout()
        title = QLabel("🎮 EdgeSim Dashboard")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.init_simulation_tab()
        self.init_manual_tab()

        self.setLayout(main_layout)

    # --- Simulation Tab ---
    def init_simulation_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        row = QHBoxLayout()
        self.game_select = QComboBox()
        self.game_select.addItems(["Roulette", "Blackjack", "Slots"])
        self.agent_select = QComboBox()
        self.agent_select.addItems(["Base Agent", "RL Agent"])

        row.addWidget(QLabel("Game:"))
        row.addWidget(self.game_select)
        row.addWidget(QLabel("Agent:"))
        row.addWidget(self.agent_select)
        layout.addLayout(row)

        self.start_btn = QPushButton("▶ Run Simulation")
        self.start_btn.clicked.connect(self.start_simulation)
        layout.addWidget(self.start_btn)

        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.stats_label = QLabel("Results will appear here after simulation.")
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.stats_label)

        self.tabs.addTab(tab, "Simulation Mode")

    # --- Manual Play Tab ---
    def init_manual_tab(self):
        tab = QWidget()
        form = QFormLayout(tab)

        self.bet_amount = QLineEdit("100")
        self.bet_option = QComboBox()
        self.bet_option.addItems(["Red", "Black", "Odd", "Even"])
        self.play_button = QPushButton("🎯 Place Bet")
        self.play_button.clicked.connect(self.play_manual_round)
        self.manual_result = QLabel("Result: —")

        form.addRow("Bet Amount:", self.bet_amount)
        form.addRow("Bet On:", self.bet_option)
        form.addRow(self.play_button)
        form.addRow("Outcome:", self.manual_result)

        self.tabs.addTab(tab, "Manual Play")

    # --- Simulation Logic ---
    def start_simulation(self):
        game_name = self.game_select.currentText()
        agent_name = self.agent_select.currentText()
        self.start_btn.setEnabled(False)
        self.progress.setValue(0)
        self.stats_label.setText(f"Running {game_name} with {agent_name}...")

        self.worker = SimulationWorker(self.sim, game_name, agent_name, 200)
        self.worker.finished.connect(self.display_results)
        self.worker.start()

    def display_results(self, bankrolls, stats):
        self.progress.setValue(100)
        self.ax.clear()
        self.ax.plot(bankrolls, color="#00C853", linewidth=2)
        self.ax.set_title("Bankroll Progression", color="white")
        self.ax.tick_params(colors="white")
        self.ax.set_facecolor("#1E2A38")
        self.canvas.draw()

        msg = (f"🏦 Final Bankroll: {stats['final_bankroll']:.2f}\n"
               f"📊 Expected Value: {stats['expected_value']:.4f}\n"
               f"📉 Max Drawdown: {stats['max_drawdown']:.4f}")
        self.stats_label.setText(msg)
        QMessageBox.information(self, "Simulation Complete", "Simulation finished successfully!")
        self.start_btn.setEnabled(True)

    # --- Manual Play Logic ---
    def play_manual_round(self):
        game = self.sim.get_game("Roulette")
        try:
            amount = float(self.bet_amount.text())
        except ValueError:
            self.manual_result.setText("❌ Invalid amount.")
            return
        bet_type = self.bet_option.currentText()
        result, payout = game.payout(choice=bet_type, amount=amount)
        self.manual_result.setText(f"🎯 You bet {amount} on {bet_type} → Outcome: {result} | Win: {payout:.2f}")

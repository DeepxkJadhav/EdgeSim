from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class BankrollChart(QWidget):
    def __init__(self):
        super().__init__()
        self.fig = Figure()
        self.canvas = FigureCanvasQTAgg(self.fig)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_chart(self, bankrolls):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.plot(bankrolls)
        ax.set_title("Bankroll Over Time")
        self.canvas.draw()

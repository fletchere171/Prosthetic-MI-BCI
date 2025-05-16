# bci_app/ui/widgets/online_training.py
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
class OnlineTrainingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        l = QVBoxLayout(self)
        l.addWidget(QLabel("Online Training — coming soon"))

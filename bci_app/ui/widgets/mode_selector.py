# bci_app/ui/widgets/mode_selector.py
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout

class ModeSelectorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.collectButton = QPushButton("Collect Data")
        self.trainButton   = QPushButton("Online Training")
        self.exportButton  = QPushButton("Export Model")
        self.inferButton   = QPushButton("Run Inference")
        for btn in (self.collectButton, self.trainButton,
                    self.exportButton, self.inferButton):
            layout.addWidget(btn)
        layout.addStretch()

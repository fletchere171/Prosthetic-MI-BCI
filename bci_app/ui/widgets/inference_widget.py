# bci_app/ui/widgets/inference_widget.py
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
class InferenceWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        l = QVBoxLayout(self)
        l.addWidget(QLabel("Inference — coming soon"))

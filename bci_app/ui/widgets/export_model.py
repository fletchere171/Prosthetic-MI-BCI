# bci_app/ui/widgets/export_model.py
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
class ExportModelWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        l = QVBoxLayout(self)
        l.addWidget(QLabel("Export Model — coming soon"))

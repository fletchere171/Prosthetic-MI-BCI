from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QStackedWidget
)
from PyQt6.QtCore import Qt

from .widgets.data_collection   import DataCollectionWidget
from .widgets.online_training   import OnlineTrainingWidget
from .widgets.export_model      import ExportModelWidget
from .widgets.inference_widget  import InferenceWidget

class MainMenuWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        from PyQt6.QtWidgets import QPushButton
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dataBtn   = QPushButton("1. Data Collection")
        self.trainBtn  = QPushButton("2. Online Training")
        self.exportBtn = QPushButton("3. Export Model")
        self.inferBtn  = QPushButton("4. Run Inference")
        for btn in (self.dataBtn, self.trainBtn, self.exportBtn, self.inferBtn):
            btn.setFixedHeight(50)
            layout.addWidget(btn)
        layout.setSpacing(20)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prosthetic-MI-BCI")

        # Central stacked layout
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Pages
        self.mainMenu    = MainMenuWidget()
        self.collectPage = DataCollectionWidget()
        self.trainPage   = OnlineTrainingWidget()
        self.exportPage  = ExportModelWidget()
        self.inferPage   = InferenceWidget()

        # Add pages to stack
        self.stack.addWidget(self.mainMenu)
        self.stack.addWidget(self.collectPage)
        self.stack.addWidget(self.trainPage)
        self.stack.addWidget(self.exportPage)
        self.stack.addWidget(self.inferPage)

        # Wire main menu buttons
        self.mainMenu.dataBtn.clicked.connect(lambda: self.stack.setCurrentWidget(self.collectPage))
        self.mainMenu.trainBtn.clicked.connect(lambda: self.stack.setCurrentWidget(self.trainPage))
        self.mainMenu.exportBtn.clicked.connect(lambda: self.stack.setCurrentWidget(self.exportPage))
        self.mainMenu.inferBtn.clicked.connect(lambda: self.stack.setCurrentWidget(self.inferPage))

        # Add back buttons
        for page in (self.collectPage, self.trainPage, self.exportPage, self.inferPage):
            if hasattr(page, 'add_back_button'):
                page.add_back_button(self.show_main)

        self.show_main()

    def show_main(self):
        self.stack.setCurrentWidget(self.mainMenu)
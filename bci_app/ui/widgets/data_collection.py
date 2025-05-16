import os
import numpy as np
from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout,
    QInputDialog, QMessageBox, QProgressBar, QFrame
)
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, Qt
from PyQt6.QtGui import QFont

from bci_app.core.config import get_session_cfg
from bci_app.hw.fake_board import FakeBoard

class DataCollectionThread(QThread):
    """Continuously read EEG chunks from the board."""
    dataReady = pyqtSignal(object)

    def __init__(self, board, parent=None):
        super().__init__(parent)
        self.board = board
        self._running = False

    def run(self):
        try:
            self.board.connect()
            self.board.start_stream()
            self._running = True
            chunk = int(self.board.sampling_rate * 0.5)  # 500ms chunks
            while self._running:
                buf = self.board.read_buffer(chunk)
                self.dataReady.emit(buf)
        except Exception as e:
            print(f"Board error: {e}")
        finally:
            self.board.stop_stream()
            self.board.disconnect()

    def stop(self):
        self._running = False
        self.wait()

class DataCollectionWidget(QWidget):
    """Widget for EEG data collection with clear cues and focused UI."""

    def __init__(self, parent=None):
        super().__init__(parent)
        cfg = get_session_cfg("demo")
        bc = cfg["board"]
        self.board = FakeBoard(bc["port"], bc["sampling_rate"])
        self.thread = DataCollectionThread(self.board)
        self.thread.dataReady.connect(self._record_chunk)

        # UI
        self._create_ui()

        # Phase tuples: (display, ms, record_label, color)
        self.phases = [
            ("Get ready: SWITCH", 3000, None, "darkblue"),
            ("Focus",             2000, None, "black"),
            ("SWITCH",            2000, None, "blue"),
            ("Imagine SWITCH",    6000, 1,    "blue"),
            ("Focus",             2000, None, "black"),
            ("Get ready: REST",   3000, None, "darkgreen"),
            ("Focus",             2000, None, "black"),
            ("REST",              2000, None, "green"),
            ("Imagine REST",      6000, 0,    "green"),
            ("Focus",             2000, None, "black"),
        ]

        # State
        self.trials_total = 0
        self.trials_done = 0
        self.phase_idx = 0
        self.current_label = None
        self._trial_bufs = []
        self.data_records = []
        self.paused = False
        self._phase_waiting = False
        self._remaining = 0

        # Timers
        self.tick_timer = QTimer(self)
        self.tick_timer.setInterval(50)
        self.tick_timer.timeout.connect(self._on_tick)
        self._phase_ms, self._elapsed_ms = 0, 0

        # Connect controls
        self.startBtn.clicked.connect(self._on_start)
        self.pauseBtn.clicked.connect(self._on_pause)
        self.stopBtn.clicked.connect(self._on_stop)

    def _create_ui(self):
        # Intro
        intro_text = (
            "<h2>SWITCH vs REST Data Collection</h2>"
            "<p>You will be collecting mental imagery data for two classes:</p>"
            "<ul>"
            "<li><b>SWITCH</b>: Imagine making a selection or toggling a switch</li>"
            "<li><b>REST</b>: Remain mentally relaxed with minimal imagery</li>"
            "</ul>"
            "<p>Each trial consists of these phases:</p>"
            "<ol>"
            "<li>Get ready for the task</li>"
            "<li>Focus period (+ sign)</li>"
            "<li>Task cue display</li>"
            "<li>Perform mental imagery</li>"
            "<li>Rest between tasks</li>"
            "</ol>"
            "<p>Please maintain focus throughout each trial and minimize physical movements.</p>"
            "<p>Click <b>Start Collection</b> when ready.</p>"
        )
        self.introLabel = QLabel(intro_text)
        self.introLabel.setWordWrap(True)
        self.introLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.introLabel.setTextFormat(Qt.TextFormat.RichText)

        # Central area
        self.centralFrame = QFrame()
        self.centralFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.centralFrame.setMinimumHeight(300)

        # Phase label (big font)
        self.phaseLabel = QLabel("")
        self.phaseLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        phase_font = QFont()
        phase_font.setPointSize(32)
        phase_font.setBold(True)
        self.phaseLabel.setFont(phase_font)

        # Progress info
        self.progressInfo = QLabel("")
        self.progressInfo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Focus symbol (plus sign)
        self.focusSymbol = QLabel("+")
        focus_font = QFont()
        focus_font.setPointSize(72)
        focus_font.setBold(True)
        self.focusSymbol.setFont(focus_font)
        self.focusSymbol.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.focusSymbol.setVisible(False)

        # Progress bar
        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(False)
        self.progressBar.setFixedHeight(30)
        self.progressBar.setMinimumWidth(400)
        self.progressBar.setMaximumWidth(600)
        self.progressBar.setVisible(False)

        # Central layout
        centralLayout = QVBoxLayout(self.centralFrame)
        centralLayout.addStretch(1)
        centralLayout.addWidget(self.phaseLabel)
        centralLayout.addWidget(self.focusSymbol)
        centralLayout.addWidget(self.progressInfo)
        centralLayout.addWidget(self.progressBar, alignment=Qt.AlignmentFlag.AlignCenter)
        centralLayout.addStretch(1)

        # Session status
        self.statusLabel = QLabel("Ready to start")
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Control buttons
        self.startBtn = QPushButton("Start Collection")
        self.pauseBtn = QPushButton("Pause")
        self.pauseBtn.setEnabled(False)
        self.stopBtn = QPushButton("Stop")
        self.stopBtn.setEnabled(False)

        btns = QHBoxLayout()
        btns.addWidget(self.startBtn)
        btns.addWidget(self.pauseBtn)
        btns.addWidget(self.stopBtn)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.introLabel)
        layout.addWidget(self.centralFrame)
        layout.addWidget(self.statusLabel)
        layout.addLayout(btns)

    def _on_start(self):
        n, ok = QInputDialog.getInt(
            self, "Configure Collection", "Number of full SWITCH+REST blocks:",
            value=20, min=1, max=100
        )
        if not ok:
            return

        self.introLabel.hide()

        # Reset state
        self.trials_total = n
        self.trials_done = 0
        self.phase_idx = 0
        self.current_label = None
        self._trial_bufs.clear()
        self.data_records.clear()
        self.paused = False

        # Update UI
        self.startBtn.setEnabled(False)
        self.pauseBtn.setEnabled(True)
        self.stopBtn.setEnabled(True)
        self.statusLabel.setText(f"Collection in progress: 0/{self.trials_total} blocks completed")

        # Start data collection
        self.thread.start()
        self._next_phase()

    def _on_pause(self):
        self.paused = not self.paused
        self.pauseBtn.setText("Resume" if self.paused else "Pause")

        if self.paused:
            self.tick_timer.stop()
            self.statusLabel.setText("Collection paused - press Resume when ready")
        else:
            self.tick_timer.start()
            self.statusLabel.setText(f"Collection in progress: {self.trials_done}/{self.trials_total} blocks completed")

    def _on_stop(self):
        self.trials_done = self.trials_total
        self._finish_collection()

    
    def _next_phase(self):
        self._elapsed_ms = 0

        if self.paused or self.trials_done >= self.trials_total:
            self._finish_collection()
            return

        prev_lbl = self.current_label
        name, ms, rec_lbl, color = self.phases[self.phase_idx]

        # Save trial if previous phase was a recording one
        if prev_lbl in (0, 1) and self._trial_bufs:
            trial = np.concatenate(self._trial_bufs, axis=1)
            expected_len = int(self.board.sampling_rate * (self._phase_ms / 1000))
            trial = trial[:, :expected_len]  # trim any overrun
            self.data_records.append((prev_lbl, trial))
            self._trial_bufs.clear()

        self.phaseLabel.setStyleSheet(f"color: {color};")
        self.focusSymbol.setVisible(name == "Focus")
        self.phaseLabel.setVisible(name != "Focus")
        if name != "Focus":
            self.phaseLabel.setText(name)

        self.progressInfo.setText(f"Block {self.trials_done+1} of {self.trials_total}")
        self.current_label = rec_lbl

        if rec_lbl in (0, 1):
            self._phase_ms = ms
            self.progressBar.setRange(0, ms)
            self.progressBar.setValue(0)
            self.progressBar.setVisible(True)
        else:
            self._phase_ms = ms
            self.progressBar.setVisible(False)

        self.tick_timer.start()

        self.phase_idx += 1
        if self.phase_idx >= len(self.phases):
            self.phase_idx = 0
            self.trials_done += 1
            self.statusLabel.setText(f"Collection in progress: {self.trials_done}/{self.trials_total} blocks completed")


    def _on_tick(self):
        if self.paused:
            return

        self._elapsed_ms += 50
        progress = min(self._elapsed_ms, self._phase_ms)
        if self.current_label in (0, 1):
            self.progressBar.setValue(progress)

        if self._elapsed_ms >= self._phase_ms:
            self.tick_timer.stop()
            QTimer.singleShot(350, self._next_phase)

    def _record_chunk(self, buf):
        if self.current_label in (0, 1):
            self._trial_bufs.append(buf.copy())

    def _finish_collection(self):
        self.thread.stop()

        self.pauseBtn.setEnabled(False)
        self.stopBtn.setEnabled(False)
        self.startBtn.setEnabled(True)
        self.phaseLabel.setText("Collection Complete!")
        self.phaseLabel.setStyleSheet("color: black;")
        self.focusSymbol.setVisible(False)
        self.progressBar.setVisible(False)
        self.statusLabel.setText(f"Completed {self.trials_done} blocks of SWITCH/REST data")

        # Save collected data
        if self.data_records:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fname = f"bci_data_{ts}.npz"

            labs = np.array([l for l, _ in self.data_records])
            print("Trial shapes:")
            for i, (label, trial) in enumerate(self.data_records):
                print(f"  Trial {i} - Label {label} - Shape {trial.shape}")

            dat = np.stack([d for _, d in self.data_records], axis=0)

            np.savez_compressed(fname, labels=labs, data=dat)

            stats = f"Saved {len(self.data_records)} trials ({len(labs[labs==0])} REST, {len(labs[labs==1])} SWITCH)"
            QMessageBox.information(self, "Data Saved", f"Collection complete!\n\n{stats}\n\nFile saved to: {fname}")
        else:
            QMessageBox.warning(self, "No Data", "No data was collected.")

        self.introLabel.show()
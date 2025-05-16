# bci_app/hw/fake_board.py

import numpy as np
import time
from .interface import EEGBoard

class FakeBoard(EEGBoard):
    def __init__(self, port: str, sampling_rate: int, n_channels: int = 8):
        self.sampling_rate = sampling_rate
        self.n_channels = n_channels
        self.is_streaming = False

    def connect(self):
        print(f"[FakeBoard] Connected (port ignored)")

    def start_stream(self):
        self.is_streaming = True
        print(f"[FakeBoard] Streaming at {self.sampling_rate} Hz")

    def read_buffer(self, num_samples: int) -> np.ndarray:
        # simulate a sine wave + noise
        t = np.arange(num_samples) / self.sampling_rate
        data = np.sin(2*np.pi*1.0*t)[None, :]           # 1 Hz sine
        data = np.repeat(data, self.n_channels, axis=0)
        data += 0.1 * np.random.randn(self.n_channels, num_samples)
        time.sleep(num_samples / self.sampling_rate)   # simulate real-time
        return data

    def stop_stream(self):
        self.is_streaming = False
        print("[FakeBoard] Stream stopped")

    def disconnect(self):
        print("[FakeBoard] Disconnected")

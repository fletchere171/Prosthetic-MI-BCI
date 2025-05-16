# bci_app/hw/interface.py

from abc import ABC, abstractmethod
import numpy as np

class EEGBoard(ABC):
    @abstractmethod
    def __init__(self, port: str, sampling_rate: int):
        pass

    @abstractmethod
    def connect(self) -> None:
        """Open connection to the board."""
        pass

    @abstractmethod
    def start_stream(self) -> None:
        """Begin data streaming."""
        pass

    @abstractmethod
    def read_buffer(self, num_samples: int) -> np.ndarray:
        """
        Read the next chunk of data.
        Returns array of shape (n_channels, num_samples).
        """
        pass

    @abstractmethod
    def stop_stream(self) -> None:
        """Stop data streaming."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Clean up and close connection."""
        pass

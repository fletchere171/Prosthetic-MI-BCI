from bci_app.core.config import get_session_cfg
from bci_app.hw.fake_board import FakeBoard

if __name__ == "__main__":
    cfg = get_session_cfg("demo")
    fb = FakeBoard(cfg["board"]["port"], cfg["board"]["sampling_rate"])
    fb.connect()
    fb.start_stream()
    data = fb.read_buffer(250)    # 1 second of data at 250 Hz
    print("Data shape:", data.shape)
    fb.stop_stream()
    fb.disconnect()

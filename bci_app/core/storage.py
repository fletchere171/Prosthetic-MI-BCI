# bci_app/core/storage.py

from pathlib import Path
import os
import numpy as np
import pickle
from datetime import datetime

BOX_ROOT = "Prosthetic-MI-BCI-Data"

def get_box_drive_path():
    base_path = Path.home() / "Box"
    if base_path.exists():
        return base_path
    else:
        raise FileNotFoundError("Box Drive folder not found. Is Box Drive running?")

def ensure_box_subfolder(*subfolders):
    """
    Returns the path to the desired folder inside Box.
    Will create the directory if it does not exist.
    Example: ensure_box_subfolder('Prosthetic-MI-BCI-Data', 'subject1', 'training')
    """
    box_drive = get_box_drive_path()
    folder = box_drive
    for sub in (BOX_ROOT,) + subfolders:
        folder = folder / sub
        if not folder.exists():
            folder.mkdir(parents=True)
    return folder

def save_npz_to_box(data, labels, user_name, kind="training"):
    """
    Save a labeled dataset to Box as a compressed .npz file.
    - data: numpy array
    - labels: numpy array
    - user_name: str (will create a subfolder for each user)
    - kind: str (e.g., 'training', 'test')
    """
    save_dir = ensure_box_subfolder(user_name, kind)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"eegdata_{ts}.npz"
    save_path = save_dir / fname
    np.savez_compressed(save_path, data=data, labels=labels)
    print(f"Saved EEG data to Box: {save_path}")
    return str(save_path)

def save_pickle_to_box(obj, user_name, kind="training"):
    """
    Save a pickled Python object (if you need to, e.g. for configs).
    """
    save_dir = ensure_box_subfolder(user_name, kind)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"data_{ts}.pkl"
    save_path = save_dir / fname
    with open(save_path, "wb") as f:
        pickle.dump(obj, f)
    print(f"Saved pickle to Box: {save_path}")
    return str(save_path)

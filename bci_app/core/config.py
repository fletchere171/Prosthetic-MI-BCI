import yaml

def load_config(path="config.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)

def get_session_cfg(name, path="config.yaml"):
    cfg = load_config(path)
    return cfg["sessions"][name]

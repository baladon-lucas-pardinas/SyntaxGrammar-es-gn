import yaml

def read_config(config_file: str):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    # Set default values for optional properties
    config.setdefault('output', 'output.txt')

    return config

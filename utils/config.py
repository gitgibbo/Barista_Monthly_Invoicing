import json

def load_configuration():
    with open('./config.json', 'r') as f:
        config = json.load(f)
    
    return config
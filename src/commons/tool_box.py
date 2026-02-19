import os
import config

def check_directories():
    for dir in config.path.values():
        os.makedirs(dir, exist_ok=True)
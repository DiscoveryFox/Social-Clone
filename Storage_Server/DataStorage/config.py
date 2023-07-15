DATABASE_PATH: str = r"C:\Users\Flinn\Documents\Social-Clone\storage\test.db"
DATABASE_TIMEOUT: int = 30
STORAGE_PATH: str = r"storage"

import json


class Config:
    def __init__(self, config_path: str):
        self.config_path = config_path
        with open(config_path) as config_file:
            self.config = json.load(config_file)

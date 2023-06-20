import sqlite3
import config

class Database:
    def __init__(self, database_path: str):
        self.database_path: str = database_path
        self.connection = sqlite3.connect(config.DATABASE_PATH, timeout=config.DATABASE_TIMEOUT)
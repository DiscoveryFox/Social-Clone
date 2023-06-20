import sqlite3
import config


class Database:
    def __init__(self, database_path: str = config.DATABASE_PATH) -> None:
        self.database_path: str = database_path
        self.connection = sqlite3.connect(config.DATABASE_PATH, timeout=config.DATABASE_TIMEOUT)

    def init_database(self) -> None:
        """
        Initializes the database.
        :return: None
        """
        cursor = self.connection.cursor()
        cursor.execute('''
CREATE TABLE IF NOT EXISTS files (
    hash TEXT PRIMARY KEY,
    file_path TEXT UNIQUE 
);''')
        self.connection.commit()
        cursor.close()

    def upload_post(self, post: bytes, hash_val: str):
        with open(f'{config.STORAGE_PATH}/{hash_val}', 'wb') as file_to_store:
            file_to_store.write(post)

        cursor = self.connection.cursor()
        cursor.execute('INSERT INTO files (hash, file_path) VALUES (?, ?);', (hash_val, post))

        self.connection.commit()
        cursor.close()

    def check_for_existence(self, hash_val: str):
        cursor = self.connection.cursor()
        cursor.execute('SELECT FROM files WHERE hash = ?', (hash_val, ))
        result = cursor.fetchone()
        print(result)
        print(type(result))

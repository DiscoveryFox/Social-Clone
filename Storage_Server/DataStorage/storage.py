import sqlite3
import os
from . import config
import mysql.connector
from mysql.connector import pooling
import json
import hashlib


def load_config(config_path: str):
    with open(config_path) as config_file:
        return json.load(config_file)


class Database:
    def __init__(self, db_config: dict | str) -> None:
        self.db_config: dict = (
            db_config if type(db_config) is not str else load_config(db_config)
        )
        self.connection_pool: pooling.MySQLConnectionPool = pooling.MySQLConnectionPool(
            **self.db_config
        )

    class Cursor:
        def __init__(self, database) -> None:
            self.database: Database = database
            self.connection = self.database.connection_pool.get_connection()

        def __enter__(self):
            self.cursor = self.connection.cursor()
            return self.cursor, self.connection

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.cursor.close()
            self.connection.close()

    def init_database(self) -> None:
        """
        Initializes the database.
        :return: None
        """
        with self.Cursor(self) as (cursor, connection):
            cursor.execute(
                """
    CREATE TABLE IF NOT EXISTS files (
    hash VARCHAR(64) PRIMARY KEY,
    file_path TEXT UNIQUE,
    links INT DEFAULT 1
);"""
            )

            connection.commit()

    def check_for_existence(self, hash_val: str):
        """

        :param hash_val:
        :return:
        """
        with self.Cursor(self) as (cursor, connection):
            cursor.execute("SELECT * FROM files WHERE hash = %s", (hash_val,))
            return False if not cursor.fetchone() else True

    def increase_reference(self, hash_val: str):
        print("incresing reference")
        with self.Cursor(self) as (cursor, connection):
            cursor.execute(
                "UPDATE files SET links = links + 1 WHERE hash=%s", (hash_val,)
            )
            connection.commit()

    def decrease_reference(self, hash_val: str):
        with self.Cursor(self) as (cursor, connection):
            cursor.execute(
                "UPDATE files SET links = links - 1 WHERE hash = %s", (hash_val,)
            )
            connection.commit()
            cursor.execute("SELECT links FROM files WHERE hash = %s", (hash_val,))
            result = cursor.fetchone()
            if result and result[0] == 0:
                # Delete the column from the database if 'links' is zero
                cursor.execute(
                    "SELECT file_path FROM files WHERE hash = %s", (hash_val,)
                )
                file_path: str = cursor.fetchone()[0]
                try:
                    os.remove(file_path)
                except FileNotFoundError:
                    pass
                except OSError:
                    return False
                cursor.execute("DELETE FROM files WHERE hash = %s", (hash_val,))
                connection.commit()
                return 0
            else:
                return result[0]

    def upload_post(self, post: bytes, hash_val: str):
        if self.check_for_existence(hash_val):
            self.increase_reference(hash_val)
            return hash_val
        else:
            with open(
                os.path.join(config.STORAGE_PATH, hash_val), "wb"
            ) as file_to_store:
                file_to_store.write(post)
            with self.Cursor(self) as (cursor, connection):
                cursor.execute(
                    "INSERT INTO files (hash, file_path) VALUES (%s, %s);",
                    (hash_val, f"{config.STORAGE_PATH}/{hash_val}"),
                )
                connection.commit()

            return hash_val

    def _delete_post(self, hash_val: str):
        with self.Cursor(self) as (cursor, connection):
            if self.check_for_existence(hash_val):
                cursor.execute(
                    "SELECT file_path FROM files WHERE hash = %s", (hash_val,)
                )
                file_path: str = cursor.fetchone()[0]
                try:
                    os.remove(file_path)
                except FileNotFoundError:
                    pass
                except OSError:
                    return False
                cursor.execute("DELETE FROM files WHERE hash = %s", (hash_val,))
                connection.commit()
                return True
            else:
                return True

    @staticmethod
    def calculate_hash(data: bytes, chunk_size: int = 4096):
        _hash = hashlib.sha256()
        while True:
            byte_block = data[:chunk_size]
            if not byte_block:
                break
            _hash.update(byte_block)
            data = data[chunk_size:]
        return _hash.hexdigest()

    def delete_post(self, hash_val: str):
        self.decrease_reference(hash_val)

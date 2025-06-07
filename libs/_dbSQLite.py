import sqlite3
import os
import sys
from typing import List, Optional
from _path import currentPath

def resource_path(relative_path):
    """ Возвращает путь к файлу, работает и в .py, и в .exe """
    try:
        base_path = sys._MEIPASS  # если в exe
    except AttributeError:
        base_path = os.path.abspath(".")  # если в .py

    return os.path.join(base_path, relative_path)

class Database:
    def __init__(self, db_path=f'{currentPath()}/sql.db'):
        self.conn = sqlite3.connect(resource_path(db_path))
        self.cursor = self.conn.cursor()
        self._prepare_schema()

    def _prepare_schema(self) -> None:
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_number TEXT,
                ean TEXT,
                base varchar
            )
        ''')
        self.conn.commit()

    def pushProducts(self, products: List[dict]):
        self.cursor.executemany('''
            INSERT INTO Products (article_number, ean)
            VALUES (?, ?)
        ''', [(p['articleNumber'], p['ean']) for p in products])
        self.conn.commit()

    def showEan(self, articleNumber: str) -> dict:
        self.cursor.execute(
            "SELECT ean, base FROM Products WHERE LOWER(article_number) = LOWER(?)",
            (articleNumber.strip(),)
        )
        row = self.cursor.fetchone()
        return {'ean':row[0],'base':row[1]} if row else None
    
    def showArtNum(self, ean: str) -> dict:
        self.cursor.execute(
            "SELECT ArticleNumber, base FROM Products WHERE ean = ?",
            (ean,)
        )
        row = self.cursor.fetchone()
        return {'artnum':row[0],'base':row[1]} if row else None

    def showEanLike(self, articleNumber: str) -> List|None:
        self.cursor.execute(
            'SELECT ean, base FROM Products WHERE article_number LIKE ?',
            (f'{articleNumber}%',)
        )
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            return None
        data = []
        for row in rows:
            data.append({
                'ean':row[0],
                'base':row[1]
                })
        return data

    def executeRaw(self, query: str):
        self.cursor.execute(query)
        self.conn.commit()

    def fetchAllRaw(self, query: str):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()
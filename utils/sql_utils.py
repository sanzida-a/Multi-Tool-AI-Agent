# utils/sql_utils.py
import sqlite3
from typing import List, Tuple

class SQLiteDB:
    def __init__(self, path):
        self.path = path

    def _conn(self):
        # read-only mode is safer if you don't need to write
        return sqlite3.connect(self.path, check_same_thread=False)

    def get_table_schema(self, table_name: str) -> List[Tuple[str,str]]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info({table_name})")
        rows = cur.fetchall()  # cid, name, type, notnull, dflt_value, pk
        conn.close()
        return [(r[1], r[2]) for r in rows]

    def execute_query(self, sql: str, params: tuple = ()):
        conn = self._conn()
        cur = conn.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
        conn.close()
        return rows

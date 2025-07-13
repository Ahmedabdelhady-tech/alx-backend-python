#!/usr/bin/env python3
"""Reusable context manager to execute a query with parameters."""

import sqlite3
from typing import Optional, Type


class ExecuteQuery:
    """Context manager to execute a SQL query with parameters."""

    def __init__(self, query: str, params: tuple = ()):
        self.query = query
        self.params = params
        self.conn: Optional[sqlite3.Connection] = None
        self.result = None

    def __enter__(self):
        self.conn = sqlite3.connect("users.db")
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.result = cursor.fetchall()
        return self.result

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb,
    ) -> bool:
        if self.conn:
            if exc_type:
                self.conn.rollback()
            else:
                try:
                    self.conn.commit()
                except sqlite3.ProgrammingError:
                    pass
            self.conn.close()
        return False  # Don't suppress exceptions


# ------------- Example usage -------------
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery(query, params) as results:
        for row in results:
            print(row)

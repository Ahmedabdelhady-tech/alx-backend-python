#!/usr/bin/env python3

import sqlite3
from typing import Optional, Type


class DatabaseConnection:
    """Context manager that opens a connection to `users.db`
    and closes it automatically on exit."""

    def __init__(self, db_path: str = "users.db") -> None:
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None

    def __enter__(self) -> sqlite3.Connection:
        """Open the DB connection and return it to the `with` block."""
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb,
    ) -> bool:
        """Commit on success, roll back on error, then close the connection."""
        if self.conn:
            if exc_type is None:
                # No exception → commit if there were writes (safe even for SELECT)
                try:
                    self.conn.commit()
                except sqlite3.ProgrammingError:
                    # Happens if no transaction is open (pure SELECTs) – ignore
                    pass
            else:
                # Exception occurred → roll back any partial changes
                self.conn.rollback()
            self.conn.close()
        # Return False so exceptions (if any) propagate outward
        return False


# ---------------- Example usage ----------------
if __name__ == "__main__":
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

    # Print results after the `with` block (connection already closed).
    for row in rows:
        print(row)

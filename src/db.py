import os
import json
import sqlite3
from datetime import datetime, timedelta
from contextlib import contextmanager
from typing import Tuple, List, NamedTuple

from dateutil.parser import parse

from .util import print_red


def main():
    test_db()


class User(NamedTuple):
    username: str
    followers: List[str]
    date_added: datetime

    def __bool__(self):
        return any(self)


class Database:
    def __init__(self, filepath: str, from_scratch: bool = False):
        self.con = sqlite3.connect(filepath)
        self.insert_stmt = "INSERT INTO user_followers VALUES (?,?,date('now'))"
        if from_scratch:
            self._init_table()

    def insert(self, user: str, followers: List[str]):
        followers_JSON = json.dumps(followers)
        with self.con:
            try:
                self.con.execute(self.insert_stmt, (user, followers_JSON))
            except sqlite3.IntegrityError:
                print_red(f"caught error trying to insert {user} into db")
                raise

    def insert_many(self, entries: List[Tuple[str, List[str]]]):
        entries_JSON = [(user, json.dumps(followers)) for user, followers in entries]
        with self.con:
            self.con.executemany(self.insert_stmt, entries_JSON)

    def get_user(self, username: str) -> User:
        user = self.con.execute(
            "SELECT * FROM user_followers WHERE username=?", (username,)
        ).fetchone()

        if user:
            username, followers, date_added = user
            followers = json.loads(followers)
            date_added = parse(date_added)
            return User(username, followers, date_added)
        else:
            return User("", [], "")

    def has_user(self, username: str, expiry_days: int = 0) -> bool:
        """Checks if `username` in table and that it was entered less than `expiry_days` days ago (if expiry_days > 0)"""
        user = self.get_user(username)
        expiry_date = datetime.now() - timedelta(days=expiry_days)
        expired = user.date_added < expiry_date if user else False

        return user and not (expiry_days and expired)

    def _init_table(self):
        with self.con:
            self.con.execute("DROP TABLE IF EXISTS user_followers")
            self.con.execute(
                """CREATE TABLE user_followers(
                    username TEXT UNIQUE NOT NULL, 
                    followers JSON NOT NULL, 
                    date_added TEXT
                    )"""
            )


@contextmanager
def database_connection(filepath: str):
    if not os.path.exists(filepath):
        db = Database(filepath, from_scratch=True)
    else:
        db = Database(filepath)
    try:
        yield db
    finally:
        db.con.close()


def test_db():
    db = Database(":memory:", from_scratch=True)

    # inserting one and many rows
    db.insert("test2", ["this", "that"])
    test_data = [
        ("hhza", ["lilo", "layla", "tom"]),
        ("huf", ["me", "mimi", "talis"]),
    ]
    db.insert_many(test_data)
    all_entries = db.con.execute("SELECT * FROM user_followers").fetchall()
    assert len(all_entries) == 3

    # json entries working correctly
    hhza = db.get_user("hhza")
    assert hhza.followers[2] == "tom"

    # checking user presence
    assert db.has_user("huf")
    assert not db.has_user("hufffy")

    # checking expiry date logic
    patched_JSON = json.dumps(["something", "else"])
    with db.con:
        db.con.execute(
            f"INSERT INTO user_followers VALUES ('ez', '{patched_JSON}', '2021-08-21')"
        )
    assert db.has_user("ez")
    assert not db.has_user("ez", expiry_days=30)

    db.con.close()


if __name__ == "__main__":
    main()

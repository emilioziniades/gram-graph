import os
import json
import sqlite3
from datetime import datetime, timedelta
from contextlib import contextmanager
from typing import Tuple, List, Optional, NamedTuple


from dateutil.parser import parse


def main():
    test_db()


class User(NamedTuple):
    username: str
    followers: List[str]
    date_added: datetime

    def __bool__(self):
        return all(self)


class Database:
    def __init__(self, location: str, from_scratch: bool = False):
        self.con = sqlite3.connect(location)
        self.insert_stmt = "INSERT INTO user_followers VALUES (?,?,date('now'))"
        if from_scratch:
            self._init_table()

    def insert(self, user: str, followers: List[str]):
        followers_JSON = json.dumps(followers)
        with self.con:
            self.con.execute(self.insert_stmt, (user, followers_JSON))

    def insert_many(self, entries: List[Tuple[str, List[str]]]):
        entries_JSON = [(user, json.dumps(followers)) for user, followers in entries]
        with self.con:
            self.con.executemany(self.insert_stmt, entries_JSON)

    def get_user(self, username: str) -> User:
        user = self.con.execute(
            "SELECT * FROM user_followers WHERE username=?", (username,)
        ).fetchone()

        if user:
            username, followers, entry_date = user
            followers = json.loads(followers)
            entry_date = parse(entry_date)
            return User(username, followers, entry_date)
        else:
            return User("", [], datetime(year=2050, month=1, day=1))

    def has_user(self, username: str, expiry: int = 0) -> bool:
        """Checks if `username` in table and that it was entered less than `expiry` days ago (if expiry > 0)"""
        user = self.get_user(username)
        entry_date = user.date_added
        expiry_date = datetime.now() - timedelta(days=expiry)
        expired = entry_date < expiry_date

        return user and not (expiry and expired)

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
def database_connection(location: str):
    if not os.path.exists(location):
        db = Database(location, from_scratch=True)
    else:
        db = Database(location)
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
    assert not db.has_user("ez", expiry=30)

    db.con.close()


if __name__ == "__main__":
    main()

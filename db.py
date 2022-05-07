import sqlite3
import json
from typing import Tuple, List, Optional
from datetime import datetime, timedelta

from dateutil.parser import parse


def main():
    test_db()


Entry = Tuple[str, List[str]]


class Database:
    def __init__(self, location: str):
        self.con = sqlite3.connect(location)
        self.insert_stmt = "INSERT INTO user_followers VALUES (?,?,date('now'))"

    def init_table(self):
        with self.con:
            self.con.execute("DROP TABLE IF EXISTS user_followers")
            self.con.execute(
                """CREATE TABLE user_followers(
                    username TEXT UNIQUE NOT NULL, 
                    followers JSON NOT NULL, 
                    date_added TEXT
                    )"""
            )

    def insert(self, entry: Entry):
        user, followers = entry
        followers = json.dumps(followers)
        with self.con:
            self.con.execute(self.insert_stmt, (user, followers))

    def insert_many(self, entries: List[Entry]):
        entries_JSON = [(user, json.dumps(followers)) for user, followers in entries]
        with self.con:
            self.con.executemany(self.insert_stmt, entries_JSON)

    def get_user(self, username: str) -> Optional[Tuple[str, List[str], str]]:
        user = self.con.execute(
            "SELECT * FROM user_followers WHERE username=?", (username,)
        ).fetchone()

        if user:
            username, followers, entry_date = user
            followers = json.loads(followers)
            return username, followers, entry_date
        else:
            return user

    def has_user(self, username: str, expiry: int = 0) -> bool:
        """Checks if `username` in table and that it was entered less than `expiry` days ago (if expiry > 0)"""
        user = self.get_user(username) or False
        entry_date = parse(user[2] if user else "2030-1-1")
        expiry_date = datetime.now() - timedelta(days=expiry)
        expired = entry_date < expiry_date

        return user and not (expiry and expired)


def test_db():
    db = Database(":memory:")
    db.init_table()

    # inserting one and many rows
    db.insert(("test2", ["this", "that"]))
    test_data = [
        ("hhza", ["lilo", "layla", "tom"]),
        ("huf", ["me", "mimi", "talis"]),
    ]
    db.insert_many(test_data)
    all_entries = db.con.execute("SELECT * FROM user_followers").fetchall()
    assert len(all_entries) == 3

    # json entries working correctly
    hhza = db.get_user("hhza")
    print(hhza)
    assert hhza[1][2] == "tom"

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

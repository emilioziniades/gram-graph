import sqlite3
import json


test_data = [
    ("hhza", ["lilo", "layla", "tom"]),
    ("huf", ["me", "mimi", "talis"]),
]

test_data = [(user, json.dumps(followers)) for user, followers in test_data]

con = sqlite3.connect("example.db")
cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS followers")
cur.execute(
    """CREATE TABLE followers (
        username TEXT UNIQUE NOT NULL,
        follows_user JSON NOT NULL,
        date_added TEXT
        )"""
)

con.commit()

# cur.executemany(
#     "INSERT INTO followers values (?, ?, date('now'))",
#     test_data,
# )

cur.execute(
    "INSERT INTO followers VALUES ('hhza', ?, date('now'))", json.dumps(["a", "b"])
)

con.commit()

print(cur.fetchall())
con.close()

# rough and dirty way of logging progress of database
import os
from datetime import datetime

from .config import DATABASE_FILENAME
from .db import database_connection

LOG_FILE = "eeaz.log"


def main():
    with open(LOG_FILE, "a") as f, database_connection(DATABASE_FILENAME) as db:
        n_rows = len(db.con.execute("SELECT * from user_followers").fetchall())
        now = datetime.now()
        log_line = f"{now.strftime('%d-%m-%Y %H:%M:%S')} - {n_rows} rows\n"
        print(log_line)
        f.write(log_line)


if __name__ == "__main__":
    main()

import os
from typing import List, Tuple

from instapy import InstaPy, smart_run
import dotenv

from .db import database_connection
from .config import DATABASE_FILENAME
from .util import print_red, print_green, print_yellow, print_header


def main():
    collect_data()


def collect_data(user: str = "happyhoundsza"):
    username, password = get_username_password()
    global session, db, max_depth
    session = InstaPy(
        username=username,
        password=password,
        headless_browser=True,
        want_check_browser=False,
    )
    max_depth = 2
    with smart_run(session), database_connection(DATABASE_FILENAME) as db:
        recursively_get_followers([user], 0)


def get_followers(user: str) -> List[str]:
    global session
    try:
        followers = session.grab_followers(
            username=user, amount="full", live_match=True, store_locally=True  # type: ignore
        )
    except TypeError as e:
        if str(e) != "'NoneType' object is not subscriptable":
            raise
        print_red("could not find user")
        return []
    else:
        return followers


def recursively_get_followers(users: List[str], depth: int):
    # print(f"recursively_get_followers(depth={depth}, users={users})")
    global db, max_depth
    if depth >= max_depth:
        return
    for user in users:
        print_header(f"getting followers for {user}")
        if db.has_user(user):
            print_green(f"found {user} in database")
            followers = db.get_user(user).followers
        else:
            print_yellow(f"{user} not in database, fetching from Instagram")
            followers = get_followers(user)
            db.insert(user, followers)
        recursively_get_followers(followers, depth + 1)


def get_username_password() -> Tuple[str, str]:
    dotenv.load_dotenv()
    username_env = "INSTAGRAM_USERNAME"
    password_env = "INSTAGRAM_PASSWORD"
    username = os.getenv(username_env)
    password = os.getenv(password_env)

    if username is None:
        raise ValueError(f"{username_env} not in environment variables")
    if password is None:
        raise ValueError(f"{password_env} not in environment variables")

    return username, password


if __name__ == "__main__":
    main()

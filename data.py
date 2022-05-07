import os
from typing import List

from instapy import InstaPy, smart_run
import dotenv

from db import database_connection


def main():
    dotenv.load_dotenv()
    username = os.getenv("INSTAGRAM_USERNAME") or "empty"
    password = os.getenv("INSTAGRAM_PASSWORD") or "empty"
    main_user = "happyhoundsza"
    global session, db, max_depth
    session = InstaPy(
        username=username,
        password=password,
        headless_browser=True,
        want_check_browser=False,
    )
    max_depth = 2
    with smart_run(session), database_connection("followers.db") as db:
        rec_get_followers([main_user], 0)


def get_followers(user: str) -> List[str]:
    global session
    print(f"getting followers for {user}")
    followers = session.grab_followers(
        username=user, amount="full", live_match=True, store_locally=True  # type: ignore
    )
    print(user, f"{len(followers)} followers")
    return followers


def rec_get_followers(users: List[str], depth: int):
    print(f"rec_get_followers(depth={depth}, users={users})")
    global session, db, max_depth
    if depth >= max_depth:
        return
    for user in users:
        if db.has_user(user):
            followers = db.get_user(user).followers
        else:
            followers = get_followers(user)
            db.insert(user, followers)
        rec_get_followers(followers, depth + 1)


if __name__ == "__main__":
    main()

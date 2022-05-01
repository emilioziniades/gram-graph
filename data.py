import os
from typing import List

from instapy import InstaPy
import dotenv


def main():
    dotenv.load_dotenv()
    username = os.getenv("INSTAGRAM_USERNAME") or "empty"
    password = os.getenv("INSTAGRAM_PASSWORD") or "empty"
    session = InstaPy(
        username=username,
        password=password,
        headless_browser=True,
        want_check_browser=False,
    )
    session.login()

    global user_to_followers, max_depth
    user_to_followers = dict()
    max_depth = 2
    main_user = "happyhoundsza"
    rec_get_followers(session, [main_user], 0)

    # do work here

    session.end()
    breakpoint()


def get_followers(session: InstaPy, user: str) -> List[str]:
    print(f"getting followers for {user}")
    followers = session.grab_followers(
        username=user, amount=50, live_match=True, store_locally=True
    )
    print(user, followers)
    return followers


def rec_get_followers(session: InstaPy, users: List[str], depth: int):
    print(f"rec_get_followers(depth={depth}, users={users})")
    global user_to_followers, max_depth
    if depth >= max_depth:
        return
    for user in users:
        if user in user_to_followers:
            continue
        followers = get_followers(session, user)
        user_to_followers[user] = followers
        rec_get_followers(session, followers, depth + 1)


if __name__ == "__main__":
    main()

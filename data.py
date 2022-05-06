import os
import pickle
from typing import List

from instapy import InstaPy, smart_run
import dotenv


def main():
    dotenv.load_dotenv()
    username = os.getenv("INSTAGRAM_USERNAME") or "empty"
    password = os.getenv("INSTAGRAM_PASSWORD") or "empty"
    main_user = "happyhoundsza"
    global user_to_followers, max_depth
    user_to_followers = dict()
    max_depth = 2
    session = InstaPy(
        username=username,
        password=password,
        headless_browser=True,
        want_check_browser=False,
    )
    with smart_run(session):
        session.login()
        rec_get_followers(session, [main_user], 0)
        session.end()

    with open("followers.pickle", "wb") as f:
        pickle.dump(user_to_followers, f, pickle.HIGHEST_PROTOCOL)

    breakpoint()


def get_followers(session: InstaPy, user: str) -> List[str]:
    print(f"getting followers for {user}")
    followers = session.grab_followers(
        username=user, amount="full", live_match=True, store_locally=True
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

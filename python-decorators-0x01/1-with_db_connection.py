import sqlite3
import functools


# wrapper that creates connection, passes it to function, closes after
def with_db_connection(func):
    @functools.wraps(func)
    def connect_db(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        kwargs['conn'] = conn
        res = func(*args, **kwargs)
        conn.close()
        return res
    return connect_db


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    # cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return cursor.fetchone()


if __name__ == "__main__":
    # Fetch user by ID with automatic connection handling
    user = get_user_by_id(user_id=1)
    print(user)

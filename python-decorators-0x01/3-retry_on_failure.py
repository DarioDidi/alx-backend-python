import time
import sqlite3
import functools

# paste your with_db_decorator here


def with_db_connection(func):
    print("in with db func name", func.__name__)
    """Decorator that automatically handles opening and closing database connections"""

    @functools.wraps(func)
    def connect_db(*args, **kwargs):
        # try partial func
        conn = sqlite3.connect('users.db', False, isolation_level=None)
        try:
            return func(conn, *args, **kwargs)
        except sqlite3.OperationalError as err:
            print("transaction/connection error:", err)
        finally:
            conn.close()
    return connect_db


def retry_on_failure(retries=3, delay=2):
    print("in retry on failure")

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            n = retries
            while n > 0:
                try:
                    res = func(*args, **kwargs)
                except sqlite3.OperationalError as err:
                    n -= 1
                    time.sleep(delay)
                    print(f"RETRYING ON FAILURE due to {err}, {n} tries left")
                    continue
                else:
                    return res
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# attempt to fetch users with automatic retry on failure
if __name__ == '__main__':
    users = fetch_users_with_retry()
    print(users[5])

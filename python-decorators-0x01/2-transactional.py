import sqlite3
import functools


# wrapper that creates connection, passes it to function, closes after


def with_db_connection(func):
    print("in with db func name", func.__name__)
    """Decorator that automatically handles opening and closing database connections"""

    @functools.wraps(func)
    def connect_db(*args, **kwargs):
        conn = sqlite3.connect('users.db', False, isolation_level=None)
        try:
            res = func(conn, *args, **kwargs)
            return res
        except sqlite3.OperationalError as err:
            print("transaction/connection error:", err)
        finally:
            conn.close()
    return connect_db

# Update user's email with automatic transaction handling


def transactional(func):
    print("in transactional funct name:", func.__name__)

    """Decorator that manages database transactions (commit/rollback)"""
    @functools.wraps(func)
    def atomic_wrapper(*args, **kwargs):
        conn = args[0]

        try:
            func(*args, **kwargs)
        except sqlite3.OperationalError as err:
            print("transaction error:", err)
            conn.rollback()
        else:
            conn.commit()
            print("no errors, transaction commited")

    return atomic_wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?",
                   (new_email, user_id))


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id  = {user_id}")
    return cursor.fetchone()


# Update user's email with automatic transaction handling
# update_user_email(user_id=1, new_email='Johnnie_Mayer@hotmail.com')
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
print(get_user_by_id(user_id=1))

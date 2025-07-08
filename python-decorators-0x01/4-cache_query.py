
import time
import sqlite3
import functools


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


'''create a decorator that caches the results of a database queries inorder to avoid redundant calls'''
query_cache = {}


def cache_query(func):
    def wrapper(*args, **kwargs):
        q = kwargs['query']
        if q in query_cache.keys():
            print("returning cached")
            return query_cache[q]
        else:
            print("first time, caching query")
            query_cache[q] = func(*args, **kwargs)
            return query_cache[q]
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users[:5])
# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again[:5])
print("VALID?", users[:5] == users_again[:5])

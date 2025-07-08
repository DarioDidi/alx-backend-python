import sqlite3
import functools
import logging
from datetime import datetime
# decorator to lof SQL queries

logging.basicConfig(
    level=logging.INFO,
    format=('%(asctime)s - %(levelname)s - %(message)s')
)

logger = logging.getLogger('query_logger')


def log_queries(func):
    @functools.wraps(func)
    def wrapper_log_query(*args, **kwargs):
        q = kwargs['query']
        start = datetime.now()
        logger.info(
            f"Executing query: {q} [Started at {start.strftime('%Y-%m-%d %H:%M:%S.%f')}]")
        try:
            res = func(*args, **kwargs)
            end = datetime.now()
            duration = (end - start).total_seconds()
            logger.info(
                f"Query completed successfully in {duration:.4f} seconds [Rows affected: {len(res) if res is not None else 0}]")

        except sqlite3.OperationalError as err:
            logger.error(f"Query failed: {str(err)} [Query: {q}]")
            raise

    return wrapper_log_query


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")

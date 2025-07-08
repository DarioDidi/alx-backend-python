'''Write two asynchronous functions: async_fetch_users() and async_fetch_older_users() that fetches all users and users older than 40 respectively.

Use the asyncio.gather() to execute both queries concurrently.

Use asyncio.run(fetch_concurrently()) to run the concurrent fetch'''

import aiosqlite
import asyncio

import logging
import functools
from datetime import datetime


logger = logging.getLogger('query_logger')


def log_queries(func):
    @functools.wraps(func)
    async def wrapper_log_query(*args, **kwargs):
        print("in log query")
        start = datetime.now()
        print(
            f"Executing query: [Started at {start.strftime('%Y-%m-%d %H:%M:%S.%f')}]")
        try:
            res = await func(*args, **kwargs)
            end = datetime.now()
            duration = (end - start).total_seconds()
            # logger.info(
            print(
                f"Query completed successfully in {duration:.4f} seconds [Rows affected: {len(res) if res is not None else 0}]")

        except aiosqlite.OperationalError as err:
            print(f"Query failed: {str(err)} func:{func.__name__}")
            raise
    return wrapper_log_query


@log_queries
async def async_fetch_users():
    async with aiosqlite.connect('../python-decorators-0x01/users.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            res = await cursor.fetchall()
            # print("\n\n\n\n\nUSERS", list(res)[:5])
            print("\n\n\n\n\nUSERS", list(res)[:5])


@log_queries
async def async_fetch_older_users():
    async with aiosqlite.connect('../python-decorators-0x01/users.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            res = await cursor.fetchall()
            # print("\n\n\n\n\nUSERS OVER 40:", list(res)[:5])
            print("\n\n\n\n\nUSERS OVER 40:", list(res)[:5])


async def fetch_concurrently():
    await asyncio.gather(async_fetch_users(), async_fetch_older_users())

if __name__ == '__main__':
    asyncio.run(fetch_concurrently())

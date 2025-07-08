'''
    create a reusable context manager that takes a query as input and executes it, managing both connection and the query execution
'''
import sqlite3


class ExecuteQuery():
    def __init__(self, query, value):
        self.query = query
        self.value = value

    def __enter__(self):
        self.connection = sqlite3.connect('../python-decorators-0x01/users.db')
        self.cursor = self.connection.cursor()
        res = self.cursor.execute(self.query, (self.value,))
        return self

    def __exit__(self, exception_type, exception_value, exception_tb):
        if exception_type is not None:
            print(f'an error occurred: {exception_value}')
        self.connection.close()


if __name__ == '__main__':
    with ExecuteQuery("SELECT * FROM users WHERE age > ?", 25) as executor:
        print(len(executor.cursor.fetchall()))

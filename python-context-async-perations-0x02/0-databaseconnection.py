import sqlite3


class DatabaseConnection:
    def __init__(self, path: str):
        self.path = path

    def __enter__(self):
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exception_type, exception_value, exception_tb):
        if exception_type is not None:
            print(f'an error occurred: {exception_value}')
        self.connection.close()


if __name__ == '__main__':
    query = "SELECT * FROM users"
    with DatabaseConnection('../python-decorators-0x01/users.db') as db:
        db.cursor.execute(query)
        print(db.cursor.fetchall()[:5])

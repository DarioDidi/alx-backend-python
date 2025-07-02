import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def stream_users():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),  # Replace with your MySQL username
            # Replace with your MySQL password
            password=os.getenv('DB_PWD'),
            database=os.getenv('DB_NAME')
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        while (row := cursor.fetchone()) is not None:
            yield row
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")


if __name__ == '__main__':
    stream_users()

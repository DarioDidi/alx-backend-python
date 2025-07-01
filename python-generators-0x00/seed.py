import uuid
import os
import csv
import mysql.connector
from mysql.connector import Error

from dotenv import load_dotenv

load_dotenv()


def connect_db():
    """Connect to the MySQL database server"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password=os.getenv('DB_PWD')   # Replace with your MySQL password
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """Create the database ALX_prodev if it does not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created or already exists")
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connect to the ALX_prodev database in MySQL"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password=os.getenv('DB_PWD'),   # Replace with your MySQL password
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None


def create_table(connection):
    """Create a table user_data if it does not exist with the required fields"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(10,0) NOT NULL,
                INDEX(user_id)
            )
        """)
        print("Table user_data created or already exists")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, filename):
    data = read_csv_data(filename)
    if connection and connection.is_connected():
        print("in insert data connection exists")
        cursor = connection.cursor()
        for line in data:
            try:
                # Check if email already exists (assuming emails are unique)
                cursor.execute(
                    "SELECT email FROM user_data WHERE email=%s", (line['email'],))
                if cursor.fetchone():
                    print(
                        f"User with email {line['email']} already exists. Skipping.")
                    return

                query = """
                  INSERT INTO user_data(user_id, name, email, age)
                  VALUES (%s, %s, %s, %s)
                  """

                cursor.execute(
                    query, (line['user_id'], line['name'], line['email'], line['age']))
                connection.commit()
                print(f"Inserted user: {line['name']}")
            except mysql.connector.Error as err:
                print(f"Error inserting data: {err}")


def read_csv_data(filename):
    """Read data from CSV file and return a list of dictionaries"""
    data = []
    with open(filename, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({
                'user_id': str(uuid.uuid4()),
                'name': row['name'],
                'email': row['email'],
                'age': row['age']
            })
    return data


def main():
    # Step 1: Connect to MySQL server
    connection = connect_db()
    if not connection:
        return

    # Step 2: Create database
    create_database(connection)
    connection.close()

    # Step 3: Connect to ALX_prodev database
    connection = connect_to_prodev()
    if not connection:
        return

    # Step 4: Create table
    create_table(connection)

    # Step 5: Read and insert data from CSV
    try:
        data = read_csv_data('user_data.csv')
        for user in data:
            insert_data(connection, user)
    except FileNotFoundError:
        print("Error: user_data.csv file not found")

    connection.close()
    print("Database setup complete")


if __name__ == "__main__":
    main()

from mysql.connector import errorcode
import mysql.connector
import os
import time
import csv
import uuid
from dotenv import load_dotenv

load_dotenv()


def connect_db(attempts=3):
    # try connecting attempts times
    config = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PWD'),
    }
    print(config)
    attempt = 1
    delay = 2
    while attempt < attempts + 1:
        try:
            conn = mysql.connector.connect(**config)
            return conn
        except (mysql.connector.Error, IOError) as err:
            if attempts == attempt:
                print("Failed to connect, exiting without a connection:", err)
                return None
            print(
                "Connection failed: {}. Retrying ({}/{})...".format(err, attempt, attempts-1))

            # progressive reconnect delay
            time.sleep(delay ** attempt)
            attempt += 1
    return None


def create_database(connection):
    if connection and connection.is_connected():
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                    DROP DATABASE IF EXISTS {};
                    CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'
                """.format(os.getenv('DB_NAME'), os.getenv('DB_NAME'))
            )
            print("Database ALX_prodev created")

        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
        cursor.close()


def connect_to_prodev():
    connection = connect_db(attempts=3)
    """Connect to the ALX_prodev database in MySQL"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password='new-password',   # Replace with your MySQL password
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev database: {err}")
        return None


def connect_to_prodev2():
    connection = connect_db(attempts=3)
    prodev_details = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PWD'),
        'database': os.getenv('DB_NAME')
    }
    if connection and connection.is_connected():
        cursor = connection.cursor()
        try:
            cursor.execute("USE {}".format(os.getenv('DB_NAME')))
            print("database exists")
            return connection
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(os.getenv('DB_NAME')))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                create_database(connection)
                print("Database {} created successfully.".format(
                    os.getenv('DB_NAME')))
                connection.database = os.getenv('DB_NAME')
                return connection
            else:
                print(err)
                exit(1)
        cursor.close()


USER_TABLE = (
    '''
    DROP TABLE IF EXISTS user_data;
    CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(10,0) NOT NULL,
                INDEX(user_id)
            )
    '''
)


def create_table(connection):
    if connection and connection.is_connected():
        cursor = connection.cursor()
        try:
            cursor.execute(USER_TABLE)
            print("Table user_data created")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print('USER table already exists')
            else:
                print(err.msg)
        else:
            print("TABLE CREATED")
            print("connection exists:", connection.is_connected())


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
                # print(f"Inserted user: {line['name']}")
            except mysql.connector.Error as err:
                print(f"Error inserting data: {err}")


def read_csv_data(filename):
    """Read data from CSV file and return a list of dictionaries"""
    data = []
    with open(filename, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'user_id': str(uuid.uuid4()),
                'name': row['name'],
                'email': row['email'],
                'age': row['age']
            })
    return data

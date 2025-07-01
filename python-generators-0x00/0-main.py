#!/usr/bin/python3

seed = __import__('seed')

connection = seed.connect_db()
if connection:
    seed.create_database(connection)
    connection.close()
    print(f"connection successful")

    connection = seed.connect_to_prodev()

    if connection:
        print('in main before create table, connection:',
              connection.is_connected())
        seed.create_table(connection)
        print('in main before inserting data, connection:',
              connection.is_connected())
        seed.insert_data(connection, 'user_data.csv')
        print('in main before cursor, connection:', connection.is_connected())
        cursor = connection.cursor()
        print('in main after cursor, connection:', connection)
        cursor.execute(
            f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print(f"Database ALX_prodev is present ")
        cursor.execute(f"SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print(rows)
        cursor.close()

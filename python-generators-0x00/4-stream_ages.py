seed = __import__('seed')


def stream_user_ages():
    conn = seed.connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    rows = cursor.fetchall()

    for row in rows:
        yield row['age']

    conn.close()


if __name__ == '__main__':
    avg = 0
    res = stream_user_ages()

    # while res is not None:
    for num in res:
        avg = (avg + num)/2

    print(f"Average age of users: {avg}")

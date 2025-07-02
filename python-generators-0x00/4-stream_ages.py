seed = __import__('seed')


def stream_user_ages():
    conn = seed.connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")
    # print(cursor.execute("SELECT AVG(age) FROM user_data;"))
    rows = cursor.fetchall()

    for row in rows:
        yield row['age']
       # print(row)

    conn.close()


if __name__ == '__main__':
    avg = 0
    count = 1
    res = stream_user_ages()

    # while res is not None:
    for num in res:
        avg += num
        count += 1
    avg /= count
    print(f"Average age of users: {avg}")

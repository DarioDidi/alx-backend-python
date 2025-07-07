import csv
import sqlite3


def read_csv_data(filename):
    data = []
    with open(filename, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({
                # 'user_id': str(uuid.uuid4()),
                'name': row['name'],
                'email': row['email'],
                'age': row['age']
            })
    return data


def insert_data(connection, filename):
    data = read_csv_data(filename)
    for line in data:
        try:
            with connection:
                # Check if email already exists (assuming emails are unique)
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT email FROM users WHERE email=?", (line['email'],))
                if cursor.fetchone():
                    print(
                        f"User with email {line['email']} already exists. Skipping.")
                    return

                query = """
                      INSERT INTO users( name, email, age)
                      VALUES (?, ?, ?)
                      """

                cursor.execute(
                    query,
                    (line['name'], line['email'], line['age'])
                )
                connection.commit()
                # print(f"Inserted user: {line['name']}")

        except sqlite3.OperationalError as err:
            print(f"Error inserting data: {err}")


if __name__ == '__main__':
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    age DECIMAL(10,0) NOT NULL
                )
            """)
    insert_data(con, 'user_data.csv')

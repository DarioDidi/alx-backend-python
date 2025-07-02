import os
import mysql.connector
import dotenv

dotenv.load_dotenv()


def stream_users_in_batches(batch_size):
    print("streaming")
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),  # Replace with your MySQL username
            # Replace with your MySQL password
            password=os.getenv('DB_PWD'),
            database=os.getenv('DB_NAME')
        )
        cursor = conn.cursor(dictionary=True)
        # cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_data")

        # yield cursor.fetchmany(batch_size)

        while True:
            # collect batch
            batch = []
            for _ in range(batch_size):
                if (row := cursor.fetchone()) is None:
                    break
                batch.append(row)

            # ensure not empty
            if not batch:
                break

            yield batch

    except mysql.connector.Error as err:
        print(f"error conenctiong and fetching:\n {err}")
        return None


def batch_processing(batch_size):
    print('in batch processing')
    results = stream_users_in_batches(batch_size)
    if results is not None:
        for batch in results:
            for user in (u for u in batch if u['age'] > 25):
                print(user)

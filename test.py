import sqlite3


def fetch_testing_stats():
    try:
        with sqlite3.connect("team_app.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM testing_stats")
            rows = cursor.fetchall()

            # Get column names
            column_names = [description[0] for description in cursor.description]

            # Print column names
            print("\t".join(column_names))
            print("-" * 50)

            # Print rows
            for row in rows:
                print("\t".join(str(cell) for cell in row))
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")


if __name__ == "__main__":
    fetch_testing_stats()
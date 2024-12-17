import sqlite3


def main() -> None:
    connection = sqlite3.connect("my_db.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    print(data)
    cursor.close()
    connection.close()


main()

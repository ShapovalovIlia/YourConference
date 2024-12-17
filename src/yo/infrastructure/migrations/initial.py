import sqlite3
import argparse


def make() -> None:
    connection = sqlite3.connect("my_db.db")
    users_data = [
        ("Иван", "password123"),
        ("Мария", "qwerty"),
        ("Алексей", "12345"),
        ("Екатерина", "passw0rd"),
        ("Дмитрий", "letmein"),
    ]

    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        password TEXT NOT NULL)
    """)
    cursor.executemany(
        "INSERT INTO users (name, password) VALUES (?, ?)", users_data
    )
    cursor.close()

    connection.commit()
    connection.close()


def cancel() -> None:
    connection = sqlite3.connect("my_db.db")
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.close()

    connection.commit()
    connection.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action", choices=["make", "delete"], help="make or cancel migration"
    )
    args = parser.parse_args()

    if args.action == "make":
        make()
    elif args.action == "cancel":
        cancel()

if __name__ == "__main__":
    main()

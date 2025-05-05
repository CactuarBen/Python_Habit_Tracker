import sqlite3

DATABASE = 'habits.db'

def create_connection():
    return sqlite3.connect(DATABASE)

def create_table():
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            priority INTEGER NOT NULL,
            current_streak INTEGER NOT NULL,
            periodicity TEXT CHECK(periodicity IN ('daily', 'weekly', 'monthly')) NOT NULL,
            created_at TEXT NOT NULL
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completed_at TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits (id)
        );
        """)
        connection.commit()
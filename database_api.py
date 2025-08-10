from datetime import datetime

import habit
from database import *
from habit import *
from habit import Habit


def create_habit(name, description, priority, periodicity):
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM habits WHERE name = ?", (name,))
        if cursor.fetchone():
            print(f"Habit '{name}' already exists.")
            return
        cursor.execute("INSERT INTO habits (name, description, priority, periodicity, created_at) VALUES (?, ?, ?, ?, ?)",
                       (name, description, priority, periodicity, datetime.now().replace(microsecond=0).isoformat()))
        connection.commit()
        print(f"Habit '{name}' created successfully.")


def get_habit(identifier) -> Habit | None:
    """
    Look up a habit by ID (int or digit-string) or by name (string in lowercase).
    Returns a Habit instance.
    """
    with create_connection() as connection:
        cursor = connection.cursor()

        # Search by ID in case a number ID is written in CLI
        if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.strip().isdigit()):
            cursor.execute("SELECT * FROM habits WHERE id = ?", (int(identifier),))
            row = cursor.fetchone()
            return Habit(id=row[0], name=row[1], description=row[2], priority=row[3], periodicity=row[4], created_at=row[5]) if row else None

        # 2) Search by name (lowercase) if a string is written in CLI
        key = identifier.strip()
        cursor.execute("SELECT * FROM habits WHERE lower(name) = lower(?)", (key,))
        row = cursor.fetchone()
        if row:
            return Habit(id=row[0], name=row[1], description=row[2], priority=row[3], periodicity=row[4], created_at=row[5])


def remove_habit(name):
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM habits WHERE name = ?", (name,))
        row = cursor.fetchone()
        if row is None:
            print(f"Habit '{name}' not found.")
            return
        habit_id = row[0]
        cursor.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))
        cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        connection.commit()
        print(f"Habit '{name}' and its completions removed.")


def get_habits_by_periodicity(periodicity):
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM habits WHERE periodicity = ?", (periodicity,))
        row = cursor.fetchall()
        return row

def get_all_habits():
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM habits")
        rows = cursor.fetchall()
        return [Habit(id=row[0], name=row[1], description=row[2], priority=row[3], periodicity=row[4], created_at=row[5]) for row in rows]

def check_off_habit(name):
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM habits WHERE name = ?", (name,))
        row = cursor.fetchone()
        if row is None:
            print(f"Habit '{name}' not found.")
            return
        habit_id = row[0]
        cursor.execute("INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)",
                       (habit_id, datetime.now().replace(microsecond=0).isoformat()))
        connection.commit()
        print(f"Habit '{name}' checked off.")

def get_completed_habits(name):
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM habits WHERE name = ?", (name,))
        row = cursor.fetchone()
        if row is None:
            print(f"Habit '{name}' not found.")
            return []
        habit_id = row[0]
        cursor.execute("SELECT completed_at FROM completions WHERE habit_id = ? ORDER BY completed_at", (habit_id,))
        rows = cursor.fetchall()
        return [r[0] for r in rows]


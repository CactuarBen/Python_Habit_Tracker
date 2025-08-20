from datetime import datetime
from database import *
from habit import Habit


def prompt_priority() -> int:
    while True:
        priority = input("Enter Habit Priority (1-highest, 5-lowest): ").strip()
        if priority in {"1", "2", "3", "4", "5"}:
            return int(priority)
        print("Invalid priority. Please enter a number 1–5.")


def prompt_periodicity() -> str:
    valid = {"daily", "weekly", "monthly"}
    while True:
        per = input("Enter Habit Periodicity (daily, weekly, monthly): ").strip().lower()
        if per in valid:
            return per
        print("Invalid periodicity. Choose: daily, weekly, or monthly.")


def create_habit(name, description, priority, periodicity):
    """
    Creates a new habit.
    """
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM habits WHERE name = ?", (name,))
        if cursor.fetchone():
            print(f"Habit '{name}' already exists.")
            return
        cursor.execute(
            "INSERT INTO habits (name, description, priority, periodicity, created_at) VALUES (?, ?, ?, ?, ?)",
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
            return Habit(id=row[0], name=row[1], description=row[2], priority=row[3], periodicity=row[4],
                         created_at=row[5]) if row else None

        # Search by name (lowercase) if a string is written in CLI
        key = identifier.strip()
        cursor.execute("SELECT * FROM habits WHERE lower(name) = lower(?)", (key,))
        row = cursor.fetchone()
        if row:
            return Habit(id=row[0], name=row[1], description=row[2], priority=row[3], periodicity=row[4],
                         created_at=row[5])


def update_habit(name):
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, name, description, priority, periodicity, created_at FROM habits WHERE lower(name) = lower(?)",
            (name,)
        )
        row = cursor.fetchone()
        if row is None:
            print(f"Habit '{name}' not found.")
            return
        habit_id, old_name, old_description, old_priority, old_periodicity, created_at = row

        print(f"Would you like to update the habit '{old_name}'? (y/n)")
        if input().strip().lower() != "y":
            print("No changes made.")
            return
        new_name = input("Enter new habit name: ")
        new_description = input("Enter new habit description: ")
        new_priority = prompt_priority()
        new_periodicity = prompt_periodicity()

        # leaves original "created_at"
        cursor.execute(
            "UPDATE habits SET name = ?, description = ?, priority = ?, periodicity = ? WHERE id = ?",
            (new_name, new_description, new_priority, new_periodicity, habit_id)
        )
        connection.commit()
        print(f"Habit '{old_name}' changed successfully.")


def remove_habit(name):
    """
    Removes a habit.
    """
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


def get_habits_by_periodicity(periodicity) -> Habit:
    """
    Returns a list of habits by periodicity.
    """
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM habits WHERE periodicity = ?", (periodicity,))
        row = cursor.fetchall()
        return row


def get_all_habits():
    """
    Returns a list of all habits.
    """
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM habits")
        rows = cursor.fetchall()
        return [
            Habit(id=row[0], name=row[1], description=row[2], priority=row[3], periodicity=row[4], created_at=row[5])
            for row in rows]


def check_off_habit(name):
    """
    Checks off a habit as done today.
    """
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM habits WHERE lower(name) = lower(?)", (name,))
        row = cursor.fetchone()
        if row is None:
            print(f"Habit '{name}' not found.")
            return
        habit_id = row[0]

        cursor.execute("""
            SELECT 1 FROM completions
            WHERE habit_id = ?
                AND DATE(completed_at) = DATE('now', 'localtime')
            LIMIT 1
            """, (habit_id,))
        if cursor.fetchone():
            print(f"Habit '{name}' already checked.")
            return

        print(row)
        habit_id = row[0]
        cursor.execute("INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)",
                       (habit_id, datetime.now().replace(microsecond=0).isoformat()))
        connection.commit()
        print(f"Habit '{name}' checked off.")


def get_completed_habits(name):
    """
    Returns completed habits that are used for analytics calculation.
    """
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
        return [row[0] for row in rows]

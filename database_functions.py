from datetime import datetime
from database import *
from habit import *

def create_habit(name, description, priority, current_streak, periodicity, created_at):
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO habits (name, description, priority, current_streak, periodicity, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, description, priority, current_streak, periodicity, datetime.now().isoformat()))
        connection.commit()

def get_habit(habitId):
    with create_connection( ) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM habits WHERE id = ?", (habitId,))
        row = cursor.fetchone()
        return row

def get_habits_by_periodicity(habitPeriodicity):
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM habits WHERE periodicity = ?", (habitPeriodicity,))
        row = cursor.fetchone()
        return row

def get_all_habits():
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM habits")
        rows = cursor.fetchall()
        return rows

def check_off_habit(habitId):
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)",
                       (habitId, datetime.now().isoformat()))
        connection.commit()

def get_completed_habits(habitId):
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT completed_at FROM completions WHERE habit_id = ? ORDER BY completed_at",
                       (habitId,))
        rows = cursor.fetchall()
        return rows


from typing import *
from database_api import *
from analytics import longest_streak, max_overall_streak


def press_enter(msg: str = "Press enter to continue..."):
    input(msg)


def prompt_priority() -> int:
    while True:
        p = input("Enter Habit Priority (1-highest, 5-lowest): ").strip()
        if p in {"1", "2", "3", "4", "5"}:
            return int(p)
        print("Invalid priority. Please enter a number 1–5.")


def prompt_periodicity() -> str:
    valid = {"daily", "weekly", "monthly"}
    while True:
        per = input("Enter Habit Periodicity (daily, weekly, monthly): ").strip().lower()
        if per in valid:
            return per
        print("Invalid periodicity. Choose: daily, weekly, or monthly.")


def show_menu() -> str:
    print("Welcome to the Habit Tracker!")
    print("1) Create Habit")
    print("2) View Habit")
    print("3) View all Habits")
    print("4) Check Habit Off")
    print("5) Show all Habits checked off Today")
    print("6) Remove Habit")
    print("7) Show Habit Analytics")
    print("8) Exit")
    return input("Choose: ").strip()


def create_habit_logic():
    name = input("Enter Habit Name: ").strip()
    description = input("Enter Habit Description: ").strip()
    priority = prompt_priority()
    periodicity = prompt_periodicity()
    create_habit(name, description, priority, periodicity)


def view_habit_logic():
    habit_key = input("Enter Habit ID or Name: ").strip()
    h = get_habit(habit_key)
    print(h if h else "Habit not found.")


def list_habits_logic():
    habits = get_all_habits()
    if not habits:
        print("No habits found.")
    else:
        for h in habits:
            print(h)


def check_off_logic():
    print("Habits already checked today:")

    today = datetime.now().date().isoformat()
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT DISTINCT habits.name
            FROM completions
            JOIN habits ON habits.id = completions.habit_id
            WHERE substr(completions.completed_at, 1, 10) = ?
            ORDER BY habits.name
        """, (today,))
        rows = cursor.fetchall()

        if not rows:
            print("(No habits checked today)")
        else:
            for (name,) in rows:
                print(f"  - {name}")

        list_habits_logic()
        habit_name = input("Enter Habit Name to check off: ").strip()
        check_off_habit(habit_name)


def show_all_checked_off_logic():
    print("All habits checked today:")
    today = datetime.now().date().isoformat()

    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT DISTINCT habits.name 
                       FROM completions 
                       JOIN habits ON habits.id = completions.habit_id 
                       WHERE substr(completions.completed_at, 1,10) = ? 
                       ORDER BY habits.name
                       """, (today,))
        rows = cursor.fetchall()
        if not rows:
            print("(No habits checked today)")
        else:
            for (name,) in rows:
                print(f"  - {name}")


def remove_habit_logic():
    habit_name = input("Enter Name of the Habit to be removed: ").strip()
    remove_habit(habit_name)


def analytics_logic():
    habits = get_all_habits()
    if not habits:
        print("No habits found.")
    else:
        print("Habit Streaks:")
        for h in habits:
            streak = longest_streak(h)
            unit = "day" if h.periodicity == "daily" else ("week" if h.periodicity == "weekly" else "month")
            plural = "" if streak == 1 else "s"
            print(f"  - {h.name}: {streak} {unit}{plural} streak")
        print(f"Longest Overall Streak: {max_overall_streak()}")


def run_cli():
    create_table()
    actions: Dict[str, Callable[[], None]] = {
        "1": create_habit_logic,
        "2": view_habit_logic,
        "3": list_habits_logic,
        "4": check_off_logic,
        "5": show_all_checked_off_logic,
        "6": remove_habit_logic,
        "7": analytics_logic,
    }

    while True:
        choice = show_menu()
        if choice == "8":
            print("Goodbye!")
            break

        action = actions.get(choice)
        if action:
            action()
            press_enter()
        else:
            print("Invalid choice. Please select 1–7.")


if __name__ == "__main__":
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\nGoodbye!")

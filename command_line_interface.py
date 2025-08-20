from typing import *
from analytics import *


def press_enter(msg: str = "Press enter to continue..."):
    input(msg)


def show_menu() -> str:
    print("Welcome to the Habit Tracker!")
    print("1) Create Habit")
    print("2) View Habit")
    print("3) Edit Habit")
    print("4) View all Habits")
    print("5) Check Habit Off")
    print("6) Show all Habits checked off Today")
    print("7) Remove Habit")
    print("8) Show Habit Analytics (Longest Streaks)")
    print("9) Show Current Streaks")
    print("10) Show Habits by Periodicity")
    print("11) Exit")
    return input("Choose: ").strip()


def create_habit_logic():
    """
    Create Habit
    """
    name = input("Enter Habit Name: ").strip()
    description = input("Enter Habit Description: ").strip()
    priority = prompt_priority()
    periodicity = prompt_periodicity()
    create_habit(name, description, priority, periodicity)


def view_habit_logic():
    """
    View Habit
    """
    habit_key = input("Enter Habit ID or Name: ").strip()
    habit = get_habit(habit_key)
    print(habit if habit else "Habit not found.")


def edit_habit_logic():
    """
    Edit Habit
    """
    habit_name = input("Enter Name: ").strip()
    update_habit(habit_name)


def list_habits_logic():
    """
    List all Habits
    """
    habits = get_all_habits()
    if not habits:
        print("No habits found.")
    else:
        for habit in habits:
            print(habit)


def check_off_logic():
    """
    Check Habit Off by ID or Name
    """
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
    """
    Show all Habits that were checked off today
    """
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
            for (name) in rows:
                print(f"  - {name}")


def remove_habit_logic():
    """
    Remove Habit
    """
    habit_name = input("Enter Name of the Habit to be removed: ").strip()
    remove_habit(habit_name)


def analytics_logic():
    """
    Return the longest streaks for each habit and one longest streak
    """
    habits = get_all_habits()
    if not habits:
        print("No habits found.")
    else:
        print("Habit Streaks:")
        for habit in habits:
            streak = longest_streak(habit)
            unit = "day" if habit.periodicity == "daily" else ("week" if habit.periodicity == "weekly" else "month")
            plural = "" if streak == 1 else "s"
            print(f"  - {habit.name}: {streak} {unit}{plural} streak")
        print(f"Longest Overall Streak: {max_overall_streak()}")


def current_streaks_logic():
    """
    Return the current streaks for each Habit
    """
    habits = get_all_habits()
    if not habits:
        print("No habits found.")
        return
    print("Current Streaks:")
    for habit in habits:
        streak = current_streak(habit)
        unit = "day" if habit.periodicity == "daily" else ("week" if habit.periodicity == "weekly" else "month")
        plural = "" if streak == 1 else "streak"
        print(f"  - {habit.name}: {streak} {unit}{plural} current")


def show_habits_by_periodicity_logic():
    """
    Return all habits based off their periodicity
    """
    print("Habits by periodicity: daily, weekly, monthly")
    periodicity = input("What periodicity would you like to check? ").strip().lower()

    if periodicity not in {"daily", "weekly", "monthly"}:
        print("Invalid periodicity")
        return

    names = habits_by_periodicity(periodicity)
    if not names:
        print(f"No {periodicity} habits found.")
    else:
        print(f"{periodicity.title()} habits:")
        for name in names:
            print(f"  - {name}")


def run_cli():
    """
    Creates the tables in the database and lists the maps the actions
    """
    create_table()
    actions: Dict[str, Callable[[], None]] = {
        "1": create_habit_logic,  # creates a habit
        "2": view_habit_logic,  # views a habit by ID or name
        "3": edit_habit_logic,  # edits the habit (update)
        "4": list_habits_logic,  # simply lists all habits
        "5": check_off_logic,  # checks off an action as done
        "6": show_all_checked_off_logic,  # shows all checked off actions today
        "7": remove_habit_logic,  # removes the habit
        "8": analytics_logic,  # longest streaks
        "9": current_streaks_logic,  # current streaks
        "10": show_habits_by_periodicity_logic,  # show the habits filtered by periodicity
    }

    while True:
        choice = show_menu()
        if choice == "11":
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
        # exiting the console with ctrl+c posts this note :)
    except KeyboardInterrupt:
        print("\nGoodbye!")

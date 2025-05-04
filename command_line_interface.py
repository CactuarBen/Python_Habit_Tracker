from database import *
from database_functions import *

def initialisation():
    create_table()
    while True:
        print("Option 1: Create Habit")
        print("Option 2: View Habit")
        print("Option 3: View all Habits")
        print("Option 4: Check Habit Off")
        choice = input("Choose: ")

        if choice == "1":
            name = input("Enter Habit Name: ")
            description = input("Enter Habit Description: ")
            priority = input("Enter Habit Priority: ")
            periodicity = input("Enter Habit Periodicity: ")
            create_habit(name, description, priority, periodicity, created_at=datetime.now().isoformat())
        elif choice == "2":
            habitId = int(input("Enter Habit ID: "))
            habit = get_habit(habitId)
            print(habit)
        elif choice == "3":
            habits = get_all_habits()
            for habit in habits:
                print(habit)
        elif choice == "4":
            habit_id = int(input("Enter Habit ID to check off: "))
            check_off_habit(habit_id)
        elif choice == "5":
            break

if __name__ == "__main__":
    initialisation()
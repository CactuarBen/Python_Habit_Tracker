from database_api import *
from datetime import *
from dateutil.relativedelta import relativedelta
from functools import *

def longest_streak(habit):
    completions = list(map(lambda x: datetime.fromisoformat(x), get_completed_habits(habit.name)))
    if not completions:
        return 0  # no streak if no completions

    if habit.periodicity == 'daily':
        delta = timedelta(days=1)
    elif habit.periodicity == 'weekly':
        delta = timedelta(weeks=1)
    else:
        delta = relativedelta(months=1)

    completions.sort()
    streak = max_streak = 1
    previous_streak = completions[0]

    for current_streak in completions[1:]:
        if habit.periodicity in ['daily', 'weekly']:
            if current_streak - previous_streak <= delta + timedelta(hours=12):
                streak += 1
            else:
                streak = 1
        else:  # monthly
            expected = previous_streak + delta
            if current_streak.month == expected.month and current_streak.year == expected.year:
                streak += 1
            else:
                streak = 1

        max_streak = max(max_streak, streak)
        previous_streak = current_streak

    return max_streak

def all_habit_names():
    return list(map(lambda h: h.name, get_all_habits()))

def habits_by_periodicity(periodicity):
    items = get_habits_by_periodicity(periodicity)
    if not items:
        return []
    if isinstance(items, list):
        return [getattr(x, 'name', x[1]) for x in items]
    return [getattr(items, 'name', items[1])]

def max_overall_streak():
    return reduce(lambda acc, h: max(acc, longest_streak(h)), get_all_habits(), 0)

if __name__ == "__main__":
    habits = get_all_habits()

    if not habits:
        print("No habits found.")
    else:
        for habit in habits:
            streak = longest_streak(habit)
            print(f"Habit: {habit.name} — Longest Streak: {streak}")
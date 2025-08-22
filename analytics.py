from typing import List
from database_api import *
from datetime import datetime, timedelta
from functools import reduce


def longest_streak(habit):
    """
    Longest streak recorded historically.
    """
    completion_timestamp_string_list = get_completed_habits(habit.name)
    completion_datetime_object_list = list(map(lambda timestamp_str: datetime.fromisoformat(timestamp_str), completion_timestamp_string_list))
    periodicity_value = habit.periodicity

    if periodicity_value == "daily":
        convert_datetime_to_period_key = lambda date_and_time: date_and_time.date().toordinal()
        step_size_between_periods = 1
    elif periodicity_value == "weekly":
        convert_datetime_to_period_key = lambda date_and_time: (date_and_time - timedelta(days=date_and_time.weekday())).date().toordinal()
        step_size_between_periods = 7
    else:  # "monthly"
        convert_datetime_to_period_key = lambda date_and_time: date_and_time.year * 12 + date_and_time.month
        step_size_between_periods = 1

    sorted_period_key_list = sorted(map(convert_datetime_to_period_key, completion_datetime_object_list))
    sorted_period_key_list = sorted(set(sorted_period_key_list))
    if not sorted_period_key_list:
        return 0

    initial_streak = (None, 0, 0)
    _, _, longest_streak = reduce(
        lambda state, key: (
            key,
            (1 if state[0] is None or (key - state[0]) != step_size_between_periods else state[1] + 1),
            max((1 if state[0] is None or (key - state[0]) != step_size_between_periods else state[1] + 1), state[2])
        ),
        sorted_period_key_list,
        initial_streak
    )
    return longest_streak


def current_streak(habit):
    """
    Current streak ending at the most recent completion.
    """
    completion_timestamp_string_list = get_completed_habits(habit.name)
    completion_datetime_object_list = list(map(lambda timestamp_str: datetime.fromisoformat(timestamp_str), completion_timestamp_string_list))
    periodicity_value = habit.periodicity
    now_datetime_object = datetime.now()

    if periodicity_value == "daily":
        convert_datetime_to_period_key = lambda date_and_time: date_and_time.date().toordinal()
        step_size_between_periods = 1
        one_period_timedelta = lambda most_recent: (now_datetime_object - most_recent) <= timedelta(days=1)
    elif periodicity_value == "weekly":
        convert_datetime_to_period_key = lambda date_and_time: (date_and_time - timedelta(days=date_and_time.weekday())).date().toordinal()
        step_size_between_periods = 7
        one_period_timedelta = lambda most_recent: (now_datetime_object - most_recent) <= timedelta(weeks=1)
    else:  # "monthly"
        convert_datetime_to_period_key = lambda date_and_time: date_and_time.year * 12 + date_and_time.month
        step_size_between_periods = 1
        one_period_timedelta = lambda most_recent: (convert_datetime_to_period_key(now_datetime_object) - convert_datetime_to_period_key(most_recent)) <= 1

    if not completion_datetime_object_list:
        return 0

    completion_datetime_object_list.sort()
    most_recent = completion_datetime_object_list[-1]
    if not one_period_timedelta(most_recent):
        return 0

    sorted_keys = sorted(map(convert_datetime_to_period_key, completion_datetime_object_list))
    sorted_keys = sorted(set(sorted_keys))
    last_key = sorted_keys[-1]

    keys_to_reduce = list(reversed(sorted_keys[:-1]))
    initial_streak = (1, last_key, True)
    current_run, _, _ = reduce(
        lambda state, key: state if not state[2] else (
            (state[0] + 1, key, True) if key == state[1] - step_size_between_periods else (state[0], key, False)
        ),
        keys_to_reduce,
        initial_streak
    )
    return current_run


def all_habit_names() -> List[str]:
    """
    Return a list of all habit names.
    """
    return list(map(lambda habit: habit.name, get_all_habits()))


def habits_by_periodicity(periodicity) -> List[str]:
    """
    Return a list of habit names sorted by habit periodicity.
    """
    habits = get_habits_by_periodicity(periodicity)
    if isinstance(habits, list):
        return [getattr(habit, 'name', habit[1]) for habit in habits]
    return [getattr(habits, 'name', habits[1])]


def max_overall_streak() -> int:
    """
    Return the maximum streak overall.
    """
    return reduce(lambda accumulator, habit: max(accumulator, longest_streak(habit)), get_all_habits(), 0)


if __name__ == "__main__":
    habits = get_all_habits()

    if not habits:
        print("No habits found.")
    else:
        for habit in habits:
            streak = longest_streak(habit)
            print(f"Habit: {habit.name} — Longest Streak: {streak}")

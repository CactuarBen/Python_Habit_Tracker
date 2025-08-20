from typing import List
from database_api import *
from datetime import datetime, timedelta
from functools import reduce


def longest_streak(habit):
    """
    Longest streak recorded historically.
    """
    completion_timestamp_string_list = get_completed_habits(habit.name)
    completion_datetime_object_list = list(
        map(lambda timestamp_str: datetime.fromisoformat(timestamp_str), completion_timestamp_string_list)
    )
    periodicity_value = habit.periodicity

    if periodicity_value == "daily":
        convert_datetime_to_period_key = lambda date_and_time: date_and_time.date().toordinal()
        step_size_between_periods = 1
    elif periodicity_value == "weekly":
        convert_datetime_to_period_key = lambda date_and_time: (
                date_and_time - timedelta(days=date_and_time.weekday())).date().toordinal()
        step_size_between_periods = 7
    else:  # "monthly"
        convert_datetime_to_period_key = lambda date_and_time: date_and_time.year * 12 + date_and_time.month
        step_size_between_periods = 1

    sorted_period_key_list = sorted(map(convert_datetime_to_period_key, completion_datetime_object_list))
    if len(sorted_period_key_list) == 0:
        return 0

    previous_period_key = None
    current_run_length = 0
    longest_run_length = 0
    for current_period_key in sorted_period_key_list:
        if previous_period_key is None or (current_period_key - previous_period_key) != step_size_between_periods:
            current_run_length = 1
        else:
            current_run_length += 1

        if current_run_length > longest_run_length:
            longest_run_length = current_run_length

        previous_period_key = current_period_key
    return longest_run_length


def current_streak(habit):
    """
    Current streak ending at the most recent completion.
    """
    completion_timestamp_string_list = get_completed_habits(habit.name)
    completion_datetime_object_list = list(
        map(lambda timestamp_str: datetime.fromisoformat(timestamp_str), completion_timestamp_string_list)
    )

    periodicity_value = habit.periodicity
    now_datetime_object = datetime.now()

    if periodicity_value == "daily":
        convert_datetime_to_period_key = lambda date_and_time: date_and_time.date().toordinal()
        step_size_between_periods = 1
        one_period_timedelta = timedelta(days=1)
    elif periodicity_value == "weekly":
        convert_datetime_to_period_key = lambda date_and_time: (
                date_and_time - timedelta(days=date_and_time.weekday())).date().toordinal()
        step_size_between_periods = 7
        one_period_timedelta = timedelta(weeks=1)
    else:  # "monthly"
        convert_datetime_to_period_key = lambda date_and_time: date_and_time.year * 12 + date_and_time.month
        step_size_between_periods = 1

    if not completion_datetime_object_list:
        return 0

    completion_datetime_object_list.sort()
    most_recent_completion_datetime = completion_datetime_object_list[-1]

    if periodicity_value in ("daily", "weekly"):
        time_since_last_completion = now_datetime_object - most_recent_completion_datetime
        if time_since_last_completion > one_period_timedelta:
            return 0
    else:  # monthly
        now_month_key = convert_datetime_to_period_key(now_datetime_object)
        last_month_key = convert_datetime_to_period_key(most_recent_completion_datetime)
        if (now_month_key - last_month_key) > 1:
            return 0

    sorted_period_key_list = sorted(map(convert_datetime_to_period_key, completion_datetime_object_list))
    last_completion_period_key = sorted_period_key_list[-1]

    current_run_length = 1
    previous_period_key = last_completion_period_key
    still_counting = True
    for current_earlier_key in reversed(sorted_period_key_list[:-1]):
        if not still_counting:
            break
        expected_previous_key = previous_period_key - step_size_between_periods
        if current_earlier_key == expected_previous_key:
            current_run_length += 1
            previous_period_key = current_earlier_key
        else:
            still_counting = False
    return current_run_length


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

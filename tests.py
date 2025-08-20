import unittest
from unittest.mock import patch

from database_api import *
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from database import create_connection
from analytics import *
from database_api import *

TEST_HABIT_NAMES = ["TestHabitOne", "TestHabitTwo", "TestHabitThree"]


def clean_habits(habit_names):
    for name in habit_names:
        remove_habit(name)


def get_habit_id(name: str) -> int | None:
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM habits WHERE name = ?", (name,))
        row = cursor.fetchone()
        return row[0] if row else None


def insert_completion(habit_id: int, date_and_time: datetime) -> None:
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)",
            (habit_id, date_and_time.replace(microsecond=0).isoformat()),
        )
        connection.commit()


def count_today(habit_id: int) -> int:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM completions WHERE habit_id = ? AND DATE(completed_at) = DATE('now','localtime')",
            (habit_id,),
        )
        return cursor.fetchone()[0]


class TrackerTests(unittest.TestCase):
    def test_create_and_list_habits(self):
        clean_habits(TEST_HABIT_NAMES)
        create_habit("TestHabitOne", "Testing habits", 1, 'daily')
        habits = get_all_habits()
        self.assertTrue(any(h.name == "TestHabitOne" for h in habits), "Habit 'TestHabit' not found")
        self.assertTrue(any(h.description == "Testing habits" for h in habits),
                        "Habit description 'Testing habits' not found")
        self.assertTrue(any(h.priority == 1 for h in habits), "Habit priority '1' not found")
        self.assertTrue(any(h.periodicity == 'daily' for h in habits), "Habit 'daily' not found")
        clean_habits(TEST_HABIT_NAMES)

    def test_create_and_remove_habits(self):
        clean_habits(TEST_HABIT_NAMES)
        create_habit("TestHabitOne", "Testing habits", 1, 'daily')
        habits_before_deletion = get_all_habits()
        number_of_habits_before_deletion = len(habits_before_deletion)
        remove_habit("TestHabitOne")
        habits_after_deletion = get_all_habits()
        number_of_habits_after_deletion = len(habits_after_deletion)
        self.assertTrue(number_of_habits_after_deletion == number_of_habits_before_deletion - 1,
                        "Habit 'TestHabitOne' was not deleted successfully")
        clean_habits(TEST_HABIT_NAMES)

    def test_return_all_habits(self):
        clean_habits(TEST_HABIT_NAMES)
        habits = get_all_habits()
        habits_number = len(habits)
        print("Number of habits before 3 new ones: ", habits_number)
        create_habit("TestHabitOne", "Testing habits", 1, 'daily')
        create_habit("TestHabitTwo", "Testing habits", 1, 'daily')
        create_habit("TestHabitThree", "Testing habits", 1, 'daily')

        habits_after_3_new_ones = get_all_habits()
        habits_after_3_new_ones_number = len(habits_after_3_new_ones)
        print("Number of habits after 3 new ones: ", habits_number)
        self.assertTrue(habits_after_3_new_ones_number == habits_number + 3,
                        "Incorrect number of total habits after 3 new ones")
        clean_habits(TEST_HABIT_NAMES)

    def test_update_habit(self):
        clean_habits(["UpdateTestHabit", "UpdateTestNewHabit"])
        create_habit("UpdateTestHabit", "old description", 2, "daily")
        before = get_habit("UpdateTestHabit")
        self.assertIsNotNone(before)

        with patch("database_api.input", side_effect=["y", "UpdateTestNewHabit", "new desc"]):
            with patch("database_api.prompt_priority", return_value=3):
                with patch("database_api.prompt_periodicity", return_value="weekly"):
                    update_habit("UpdateTestHabit")

        after = get_habit("UpdateTestNewHabit")
        self.assertIsNotNone(after, "Renamed habit not found after update")
        self.assertEqual(after.description, "new desc")
        self.assertEqual(after.priority, 3)
        self.assertEqual(after.periodicity, "weekly")
        self.assertEqual(after.created_at, before.created_at, "created_at should not change")
        clean_habits(["UpdateTestHabit", "UpdateTestNewHabit"])

    def test_get_habit_case_insensitive_and_by_id(self):
        clean_habits(TEST_HABIT_NAMES)
        create_habit("CaseTest", "c", 3, "daily")

        habit = get_habit("casetest")
        self.assertIsNotNone(habit, "Case-insensitive lookup failed")
        self.assertEqual(habit.name, "CaseTest")

        habit2 = get_habit(habit.id)
        self.assertIsNotNone(habit2, "ID lookup failed")
        self.assertEqual(habit2.id, habit.id)
        clean_habits(TEST_HABIT_NAMES + ["CaseTest"])

    def test_check_off_habit_only_once_per_day(self):
        clean_habits(TEST_HABIT_NAMES)
        create_habit("CheckOnce", "d", 2, "daily")
        habit_id = get_habit_id("CheckOnce")
        self.assertIsNotNone(habit_id)

        before = count_today(habit_id)
        check_off_habit("checkonce")
        check_off_habit("CheckOnce")
        after = count_today(habit_id)

        self.assertEqual(after, before + 1, "Should only record one completion per day")
        clean_habits(TEST_HABIT_NAMES + ["CheckOnce"])

    def test_get_habits_by_periodicity_returns_multiple(self):
        clean_habits(TEST_HABIT_NAMES)
        create_habit("DH1", "x", 1, "daily")
        create_habit("DH2", "y", 2, "daily")
        create_habit("WH1", "z", 3, "weekly")

        items = get_habits_by_periodicity("daily")
        names = [getattr(x, "name", x[1]) for x in items] if items else []
        self.assertTrue({"DH1", "DH2"}.issubset(set(names)))
        self.assertFalse("WH1" in names)
        clean_habits(TEST_HABIT_NAMES + ["DH1", "DH2", "WH1"])

    def test_longest_streak_daily(self):
        clean_habits(TEST_HABIT_NAMES)
        create_habit("StreakDaily", "s", 1, "daily")
        habit_id = get_habit_id("StreakDaily")
        self.assertIsNotNone(habit_id)

        # 3-day consecutive streak ending today
        today = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
        for d in [2, 1, 0]:
            insert_completion(habit_id, today - timedelta(days=d))

        # Add a gap far in the past (shouldn't increase the longest streak)
        insert_completion(habit_id, today - timedelta(days=10))

        habit = get_habit("StreakDaily")
        self.assertEqual(longest_streak(habit), 3)
        clean_habits(TEST_HABIT_NAMES + ["StreakDaily"])

    def test_longest_streak_monthly(self):
        clean_habits(TEST_HABIT_NAMES)
        create_habit("StreakMonthly", "m", 1, "monthly")
        habit_id = get_habit_id("StreakMonthly")
        self.assertIsNotNone(habit_id)

        base = datetime.now().replace(day=15, hour=12, minute=0, second=0, microsecond=0)
        # Three consecutive months
        insert_completion(habit_id, base - relativedelta(months=2))
        insert_completion(habit_id, base - relativedelta(months=1))
        insert_completion(habit_id, base)

        habit = get_habit("StreakMonthly")
        self.assertEqual(longest_streak(habit), 3)
        clean_habits(TEST_HABIT_NAMES + ["StreakMonthly"])

    def test_current_streak_daily(self):
        clean_habits(["DailyHabit"])
        create_habit("DailyHabit", "daily habit", 2, "daily")
        habit_id = get_habit_id("DailyHabit")
        self.assertIsNotNone(habit_id)

        base = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)

        # Current streak should be 1 day today, and two older days (4 and 3) not taken into account.
        insert_completion(habit_id, base - timedelta(days=4))  # one day and a break
        insert_completion(habit_id, base - timedelta(days=3))  # yesterday
        insert_completion(habit_id, base)  # today

        habit = get_habit("DailyHabit")
        self.assertEqual(current_streak(habit), 1)

        # Add the two days in the middle to bridge the older days and today.
        insert_completion(habit_id, base - timedelta(days=2))  # one day and a break
        insert_completion(habit_id, base - timedelta(days=1))  # yesterday

        habit = get_habit("DailyHabit")
        self.assertEqual(current_streak(habit), 5)

        clean_habits(["DailyHabit"])

    def test_current_streak_weekly(self):
        clean_habits(["WeeklyHabit"])
        create_habit("WeeklyHabit", "weekly habit", 3, "weekly")
        habit_id = get_habit_id("WeeklyHabit")
        self.assertIsNotNone(habit_id)

        base = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)

        # Two weeks really old, two weeks break and current week.
        insert_completion(habit_id, base - timedelta(weeks=4))  # four weeks ago
        insert_completion(habit_id, base - timedelta(weeks=3))  # three week ago
        insert_completion(habit_id, base)  # today

        habit = get_habit("WeeklyHabit")
        self.assertEqual(current_streak(habit), 1)

        # Two consecutive weeks bridging the gap between the older ones and the today one
        insert_completion(habit_id, base - timedelta(weeks=2))  # two weeks ago
        insert_completion(habit_id, base - timedelta(weeks=1))  # one week ago

        habit = get_habit("WeeklyHabit")
        self.assertEqual(current_streak(habit), 5)

        clean_habits(["WeeklyHabit"])

    def test_current_streak_monthly(self):
        clean_habits(["MonthlyHabit"])
        create_habit("MonthlyHabit", "monthly habit", 1, "monthly")
        habit_id = get_habit_id("MonthlyHabit")
        self.assertIsNotNone(habit_id)

        # Pick mid-month to avoid month-start/end edges
        base = datetime.now().replace(day=15, hour=12, minute=0, second=0, microsecond=0)

        # Two months really old, two months break and current month
        insert_completion(habit_id, base - relativedelta(months=4))  # four months ago
        insert_completion(habit_id, base - relativedelta(months=3))  # three month ago
        insert_completion(habit_id, base)  # this month

        habit = get_habit("MonthlyHabit")
        self.assertEqual(current_streak(habit), 1)

        # Two more months to bridge the gap between the two old months and the current one
        insert_completion(habit_id, base - relativedelta(months=2))  # two months ago
        insert_completion(habit_id, base - relativedelta(months=1))  # one month ago

        habit = get_habit("MonthlyHabit")
        self.assertEqual(current_streak(habit), 5)

        clean_habits(["MonthlyHabit"])

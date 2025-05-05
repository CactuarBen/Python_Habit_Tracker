from datetime import datetime

class Habit:
    def __init__(self, id, habit_name, description, priority, current_streak, periodicity, created_at):
        self.id = id
        self.habitName = habit_name
        self.description = description
        self.priority = priority
        self.current_streak = current_streak
        self.periodicity = periodicity
        self.created_at = created_at
from datetime import datetime

class Habit:
    def __init__(self, id, habitName, description, priority, periodicity, created_at):
        self.id = id
        self.habitName = habitName
        self.description = description
        self.priority = priority
        self.periodicity = periodicity
        self.created_at = created_at
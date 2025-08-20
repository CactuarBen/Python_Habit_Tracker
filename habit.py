class Habit:
    def __init__(self, id, name, description, priority, periodicity, created_at):
        self.__id = id
        self.__name = name
        self.__description = description
        self.__priority = priority
        self.__periodicity = periodicity
        self.__created_at = created_at

    def __str__(self):
        return f'{self.__name}: {self.__description}, priority: {self.__priority}, periodicity: {self.__periodicity}, created_at: {self.__created_at}'

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def priority(self):
        return self.__priority

    @property
    def periodicity(self):
        return self.__periodicity

    @property
    def created_at(self):
        return self.__created_at

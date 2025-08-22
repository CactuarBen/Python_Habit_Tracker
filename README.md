# Python_Habit_Tracker
Habit Tracker Backend written in Python that runs in CLI

## Installation procedure
1) Either clone the repository or download the zip archive 
2) Open the project in the IDE of your preference (make sure your path to the project is correct)
3) Open the terminal and execute the command: ``python command_line_interface.py``
- Extra: You can now connect to the habits.db that was created and run an SQL script from "sample data" to populate the database with mock data
4) You will be greeted by the CLI and you will see the options to choose from
```
Welcome to the Habit Tracker!
1) Create Habit
2) View Habit
3) Edit Habit
4) View all Habits
5) Check Habit Off
6) Show all Habits checked off Today
7) Remove Habit
8) Show Habit Analytics (Longest Streaks)
9) Show Current Streaks
10) Show Habits by Periodicity
11) Exit
```
5) For creating a habit you should input the following information
```
Choose: 1
Enter Habit Name: Name
Enter Habit Description: Description
Enter Habit Priority (1-highest, 5-lowest): 1
Enter Habit Periodicity (daily, weekly, monthly): daily
Habit 'Name' created successfully.
Press enter to continue...
```
6) For viewing or editing a habit you can input either a name or the ID of the habit
```
Choose: 2
Enter Habit ID or Name: 1
Name: Description, priority: 1, periodicity: daily, created_at: 2025-08-20T23:06:55
Press enter to continue... 
```
```
Choose: 3
Enter Name: name
Would you like to update the habit 'Name'? (y/n)
y
Enter new habit name: NewName
Enter new habit description: Changed habit
Enter Habit Priority (1-highest, 5-lowest): 3
Enter Habit Periodicity (daily, weekly, monthly): weekly
Habit 'Name' changed successfully.
```
7) You can also view all habits
```
Choose: 4
NewName: Changed habit, priority: 3, periodicity: weekly, created_at: 2025-08-20T23:06:55
First: Attempt, priority: 1, periodicity: daily, created_at: 2025-08-20T23:10:22
CASETEST: c, priority: 4, periodicity: daily, created_at: 2025-08-21T06:59:03
```
8) Once you are done with the habit for the day, choose to check it off
```
Choose: 5
Habits already checked today:
(No habits checked today)
NewName: Changed habit, priority: 3, periodicity: weekly, created_at: 2025-08-20T23:06:55
First: Attempt, priority: 1, periodicity: daily, created_at: 2025-08-20T23:10:22
CASETEST: c, priority: 4, periodicity: daily, created_at: 2025-08-21T06:59:03
Enter Habit Name to check off: First
Habit 'First' checked off.
```
9) Then you can show all the habits that you checked off today
```
Choose: 6
All habits checked today:
  - First
  - Read Book
```
10) You can choose a habit to delete by writing in name or id
```
Choose: 7
Enter Name of the Habit to be removed: REMOVE
Habit 'REMOVE' and its completions removed.
```
11) Finally, you can output various analytics. For example this one for the longest streak in history:
```
Choose: 8
Habit Streaks:
  - NewName: 2 weeks streak
  - First: 1 day streak
  - CASETEST: 0 days streak
  - Exercise: 0 days streak
  - Weekly Review: 0 weeks streak
  - Read Book: 0 days streak
  - Meditation: 0 days streak
  - Monthly Budget: 0 months streak
Longest Overall Streak: 2
```
12) Or for the current streak that is going
```
Current Streaks:
  - NewName: 0 weekstreak current
  - First: 1 day current
  - CASETEST: 0 daystreak current
  - Exercise: 0 daystreak current
  - Weekly Review: 0 weekstreak current
  - Read Book: 0 daystreak current
  - Meditation: 0 daystreak current
  - Monthly Budget: 0 monthstreak current
```
13) And lastly, you can output information on Habits by periodicity
```
Choose: 10
Habits by periodicity: daily, weekly, monthly
What periodicity would you like to check? daily
Daily habits:
  - First
  - CASETEST
  - Exercise
  - Read Book
  - Meditation
```
14) Write "11" to exit

## Extra:
If you wanted to run tests, navigate to the same director and run
```
pytest tests.py
```
Via the terminal
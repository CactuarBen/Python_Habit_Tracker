INSERT INTO habits (name, description, priority, periodicity, created_at)
VALUES ('Exercise', 'Morning workout', 2, 'daily', '2025-04-01T08:00:00'),
       ('Weekly Review', 'Reflect on the week', 1, 'weekly', '2025-04-01T08:00:00'),
       ('Read Book', 'Read at least 20 pages', 3, 'daily', '2025-04-01T08:00:00'),
       ('Meditation', '10 minutes mindfulness', 2, 'daily', '2025-04-01T08:00:00'),
       ('Monthly Budget', 'Review finances', 1, 'monthly', '2025-04-01T08:00:00');

INSERT INTO completions (habit_id, completed_at)
VALUES (1, '2025-04-01T09:00:00'),
       (1, '2025-04-02T09:00:00'),
       (1, '2025-04-03T09:00:00'),
       (1, '2025-04-04T09:00:00'),
       (1, '2025-04-06T09:00:00'),
       (1, '2025-04-07T09:00:00'),
       (1, '2025-04-08T09:00:00');

INSERT INTO completions (habit_id, completed_at)
VALUES (2, '2025-04-06T10:00:00'),
       (2, '2025-04-13T10:00:00'),
       (2, '2025-04-20T10:00:00'),
       (2, '2025-04-27T10:00:00');

INSERT INTO completions (habit_id, completed_at)
VALUES (3, '2025-04-01T21:00:00'),
       (3, '2025-04-02T21:00:00'),
       (3, '2025-04-03T21:00:00'),
       (3, '2025-04-04T21:00:00'),
       (3, '2025-04-05T21:00:00'),
       (3, '2025-04-06T21:00:00'),
       (3, '2025-04-07T21:00:00');

INSERT INTO completions (habit_id, completed_at)
VALUES (4, '2025-04-01T07:30:00'),
       (4, '2025-04-02T07:30:00'),
       (4, '2025-04-04T07:30:00'),
       (4, '2025-04-05T07:30:00');

INSERT INTO completions (habit_id, completed_at)
VALUES (5, '2025-04-05T12:00:00'),
       (5, '2025-05-05T12:00:00');

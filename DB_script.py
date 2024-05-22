import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('team_app.db')
cursor = conn.cursor()

# 1. Добавление новой строки в таблицу tests
cursor.execute("""
    INSERT INTO tests (test_name, test_type)
    VALUES ('Произношение', 4)
""")

# 2. Изменение значений поля test_name
cursor.execute("""
    UPDATE tests
    SET test_name = 'Перевод'
    WHERE test_type = 1
""")

cursor.execute("""
    UPDATE tests
    SET test_name = 'Написание'
    WHERE test_type = 2
""")

cursor.execute("""
    UPDATE tests
    SET test_name = 'Прослушивание'
    WHERE test_type = 3
""")

# 3. Изменение наименования и типа поля в таблице testing_stats
# SQLite не поддерживает прямое изменение типа столбца или его переименование.
# Поэтому нужно создать новую таблицу с нужной структурой, перенести данные и удалить старую таблицу.

# Создание новой таблицы с нужной структурой и внешними ключами
# cursor.execute("""
#     CREATE TABLE testing_stats_new (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         user_id INTEGER,
#         test_id INTEGER,
#         score INTEGER,
#         test_datetime DATETIME,
#         FOREIGN KEY (user_id) REFERENCES users(id),
#         FOREIGN KEY (test_id) REFERENCES tests(test_id)
#     )
# """)
#
# # Перенос данных из старой таблицы в новую
# cursor.execute("""
#     INSERT INTO testing_stats_new (id, user_id, test_id, score, test_datetime)
#     SELECT id, user_id, test_id, score, note1
#     FROM testing_stats
# """)
#
# # Удаление старой таблицы
# cursor.execute("DROP TABLE testing_stats")
#
# # Переименование новой таблицы в старое название
# cursor.execute("ALTER TABLE testing_stats_new RENAME TO testing_stats")
#
# # Сохранение изменений и закрытие подключения
conn.commit()
conn.close()

import sqlite3
from datetime import datetime

# Путь к базе данных
db_path = 'team_app.db'

def populate_database_for_achievements(db_path, user_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    # Создаем записи в таблице lesson для выполнения условий
    lessons = [
        (1, 1, True, '', ''), # lesson_id, topic_id, done, note1, note2
        (2, 3, True, '', ''),
        (3, 2, True, '', ''),
        (4, 3, True, '', ''),
        (5, 1, True, '', '')
    ]
    cursor.executemany('''
        INSERT OR REPLACE INTO lesson (lesson_id, topic_id, done, note1, note2)
        VALUES (?, ?, ?, ?, ?)
    ''', lessons)

    # Создаем записи в таблице user_progress для выполнения условий
    user_progress = [
        (1, user_id, 1, 1, 5, 0, datetime.now().strftime('%Y-%m-%d'), False, False, '', ''), # progress_id, user_id, word_id, lesson_id, success_counter, failes_counter, success_date, off_rotation, dictionary, note1, note2
        (2, user_id, 2, 1, 5, 0, datetime.now().strftime('%Y-%m-%d'), False, False, '', ''),
        (3, user_id, 3, 2, 5, 0, datetime.now().strftime('%Y-%m-%d'), False, False, '', ''),
        (4, user_id, 4, 2, 5, 0, datetime.now().strftime('%Y-%m-%d'), False, False, '', ''),
        (5, user_id, 5, 3, 5, 0, datetime.now().strftime('%Y-%m-%d'), False, False, '', ''),
        (6, user_id, 6, 3, 5, 0, datetime.now().strftime('%Y-%m-%d'), False, False, '', ''),
        (7, user_id, 7, 4, 5, 0, datetime.now().strftime('%Y-%m-%d'), False, False, '', ''),
        (8, user_id, 8, 4, 5, 0, datetime.now().strftime('%Y-%m-%d'), False, False, '', ''),
        (9, user_id, 9, 5, 5, 0, datetime.now().strftime('%Y-%m-%d'), False, False, '', ''),
        (10, user_id, 10, 5, 5, 0, datetime.now().strftime('%Y-%m-%d'), False, False, '', '')
    ]
    cursor.executemany('''
        INSERT OR REPLACE INTO user_progress (progress_id, user_id, word_id, lesson_id, success_counter, failes_counter, success_date, off_rotation, dictionary, note1, note2)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', user_progress)

    conn.commit()
    conn.close()

# Пример вызова метода для пользователя с user_id = 1
populate_database_for_achievements(db_path, 1)

# Проверка, что данные добавлены корректно
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

# Проверка добавленных уроков
cursor.execute('SELECT * FROM lesson')
lessons = cursor.fetchall()
print("Lessons:")
for lesson in lessons:
    print(lesson)

# Проверка добавленного прогресса пользователя
cursor.execute('SELECT * FROM user_progress')
progress = cursor.fetchall()
print("\nUser Progress:")
for prog in progress:
    print(prog)

conn.close()

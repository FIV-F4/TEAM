import sqlite3
import math

# Укажите абсолютный путь к базе данных
db_path = "C:/Users/iv.frolov/Documents/GitHub/TEAM/team_app.db"

# Очистка таблицы user_progress
def clear_user_progress():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user_progress')
    conn.commit()
    conn.close()

# Заполнение прогресса
def fill_user_progress():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Получение user_id первого пользователя
    cursor.execute("SELECT user_id FROM users WHERE nickname = 'zerocoder'")
    user_id = cursor.fetchone()[0]

    # Получение всех тем и количество слов в каждой теме
    cursor.execute('''
        SELECT t.topic_id, t.topic_name, COUNT(wg.word_id) as word_count
        FROM topics t
        JOIN words_groupings wg ON t.topic_id = wg.topic_id
        GROUP BY t.topic_id, t.topic_name
    ''')
    topics = cursor.fetchall()

    # Определение процентов для каждой темы
    percentages = [0.30, 0.40, 0.70]

    # Добавление прогресса для первого пользователя
    for i, topic in enumerate(topics):
        topic_id, topic_name, word_count = topic
        percentage = percentages[i % len(percentages)]  # Используем циклический доступ к процентам
        words_to_learn = math.ceil(word_count * percentage)

        # Получение слов для данной темы
        cursor.execute('''
            SELECT wg.word_id
            FROM words_groupings wg
            WHERE wg.topic_id = ?
            LIMIT ?
        ''', (topic_id, words_to_learn))
        word_ids = [row[0] for row in cursor.fetchall()]

        # Добавление прогресса для этих слов
        user_progress_data = [(user_id, word_id, 10, 0) for word_id in word_ids]
        cursor.executemany('''
            INSERT INTO user_progress (user_id, word_id, success_counter, failes_counter)
            VALUES (?, ?, ?, ?)
        ''', user_progress_data)

    # Подтверждение изменений и закрытие соединения
    conn.commit()
    conn.close()

# Очистка и заполнение прогресса
clear_user_progress()
fill_user_progress()

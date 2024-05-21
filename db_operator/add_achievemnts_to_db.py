import sqlite3
import time

# Параметры новых ачивок и пути к изображениям
achievements = [
    ('Пройденная тема: Бизнес', 'Пройти тему "Бизнес"', '''
        SELECT CASE WHEN COUNT(*) = (SELECT COUNT(*) FROM lesson WHERE topic_id = 3 AND user_id = ?) 
        THEN 1 ELSE 0 END FROM lesson WHERE topic_id = 3 AND user_id = ? AND done = 1
    ''', 'db_operator/src/achievments/1.png'),
    ('50% слов в теме: Бизнес', 'Выучить 50% слов в теме "Бизнес"', '''
        SELECT CASE WHEN (SELECT COUNT(DISTINCT word_id) FROM user_progress WHERE user_id = ? AND word_id IN 
        (SELECT word_id FROM words_groupings WHERE topic_id = 3) AND success_counter > 0) >= 
        (SELECT COUNT(*) FROM words_groupings WHERE topic_id = 3) / 2 THEN 1 ELSE 0 END
    ''', 'db_operator/src/achievments/2.png'),
    ('100% слов в теме: Бизнес', 'Выучить все слова в теме "Бизнес"', '''
        SELECT CASE WHEN (SELECT COUNT(DISTINCT word_id) FROM user_progress WHERE user_id = ? AND word_id IN 
        (SELECT word_id FROM words_groupings WHERE topic_id = 3) AND success_counter > 0) = 
        (SELECT COUNT(*) FROM words_groupings WHERE topic_id = 3) THEN 1 ELSE 0 END
    ''', 'db_operator/src/achievments/3.png'),
    ('Пройденная тема: Еда', 'Пройти тему "Еда"', '''
        SELECT CASE WHEN COUNT(*) = (SELECT COUNT(*) FROM lesson WHERE topic_id = 1 AND user_id = ?) 
        THEN 1 ELSE 0 END FROM lesson WHERE topic_id = 1 AND user_id = ? AND done = 1
    ''', 'db_operator/src/achievments/4.png'),
    ('50% слов в теме: Еда', 'Выучить 50% слов в теме "Еда"', '''
        SELECT CASE WHEN (SELECT COUNT(DISTINCT word_id) FROM user_progress WHERE user_id = ? AND word_id IN 
        (SELECT word_id FROM words_groupings WHERE topic_id = 1) AND success_counter > 0) >= 
        (SELECT COUNT(*) FROM words_groupings WHERE topic_id = 1) / 2 THEN 1 ELSE 0 END
    ''', 'db_operator/src/achievments/5.png'),
    ('100% слов в теме: Еда', 'Выучить все слова в теме "Еда"', '''
        SELECT CASE WHEN (SELECT COUNT(DISTINCT word_id) FROM user_progress WHERE user_id = ? AND word_id IN 
        (SELECT word_id FROM words_groupings WHERE topic_id = 1) AND success_counter > 0) = 
        (SELECT COUNT(*) FROM words_groupings WHERE topic_id = 1) THEN 1 ELSE 0 END
    ''', 'db_operator/src/achievments/6.png'),
    ('Пройденная тема: Путешествия', 'Пройти тему "Путешествия"', '''
        SELECT CASE WHEN COUNT(*) = (SELECT COUNT(*) FROM lesson WHERE topic_id = 2 AND user_id = ?) 
        THEN 1 ELSE 0 END FROM lesson WHERE topic_id = 2 AND user_id = ? AND done = 1
    ''', 'db_operator/src/achievments/7.png'),
    ('50% слов в теме: Путешествия', 'Выучить 50% слов в теме "Путешествия"', '''
        SELECT CASE WHEN (SELECT COUNT(DISTINCT word_id) FROM user_progress WHERE user_id = ? AND word_id IN 
        (SELECT word_id FROM words_groupings WHERE topic_id = 2) AND success_counter > 0) >= 
        (SELECT COUNT(*) FROM words_groupings WHERE topic_id = 2) / 2 THEN 1 ELSE 0 END
    ''', 'db_operator/src/achievments/8.png'),
    ('100% слов в теме: Путешествия', 'Выучить все слова в теме "Путешествия"', '''
        SELECT CASE WHEN (SELECT COUNT(DISTINCT word_id) FROM user_progress WHERE user_id = ? AND word_id IN 
        (SELECT word_id FROM words_groupings WHERE topic_id = 2) AND success_counter > 0) = 
        (SELECT COUNT(*) FROM words_groupings WHERE topic_id = 2) THEN 1 ELSE 0 END
    ''', 'db_operator/src/achievments/9.png'),
    ('Новое слово', 'Выучить 1 слово', '''
        SELECT CASE WHEN (SELECT COUNT(DISTINCT word_id) FROM user_progress WHERE user_id = ? AND success_counter > 0) >= 1 THEN 1 ELSE 0 END
    ''', 'db_operator/src/achievments/10.png'),
    ('10 новых слов', 'Выучить 10 слов', '''
        SELECT CASE WHEN (SELECT COUNT(DISTINCT word_id) FROM user_progress WHERE user_id = ? AND success_counter > 0) >= 10 THEN 1 ELSE 0 END
    ''', 'db_operator/src/achievments/11.png'),
    ('50 новых слов', 'Выучить 50 слов', '''
        SELECT CASE WHEN (SELECT COUNT(DISTINCT word_id) FROM user_progress WHERE user_id = ? AND success_counter > 0) >= 50 THEN 1 ELSE 0 END
    ''', 'db_operator/src/achievments/12.png'),
    ('100 новых слов', 'Выучить 100 слов', '''
        SELECT CASE WHEN (SELECT COUNT(DISTINCT word_id) FROM user_progress WHERE user_id = ? AND success_counter > 0) >= 100 THEN 1 ELSE 0 END
    ''', 'db_operator/src/achievments/13.png'),
    ('500 новых слов', 'Выучить 500 слов', '''
        SELECT CASE WHEN (SELECT COUNT(DISTINCT word_id) FROM user_progress WHERE user_id = ? AND success_counter > 0) >= 500 THEN 1 ELSE 0 END
    ''', 'db_operator/src/achievments/14.png'),
    ('Первый урок', 'Пройти 1 урок', '''
        SELECT CASE WHEN (SELECT COUNT(*) FROM lesson WHERE user_id = ? AND done = 1) >= 1 THEN 1 ELSE 0 END
    ''', 'db_operator/src/achievments/15.png'),
    ('10 уроков', 'Пройти 10 уроков', '''
        SELECT CASE WHEN (SELECT COUNT(*) FROM lesson WHERE user_id = ? AND done = 1) >= 10 THEN 1 ELSE 0 END
    ''', 'db_operator/src/achievments/16.png'),
    ('50 уроков', 'Пройти 50 уроков', '''
        SELECT CASE WHEN (SELECT COUNT(*) FROM lesson WHERE user_id = ? AND done = 1) >= 50 THEN 1 ELSE 0 END
    ''', 'db_operator/src/achievments/17.png'),
    ('100 уроков', 'Пройти 100 уроков', '''
        SELECT CASE WHEN (SELECT COUNT(*) FROM lesson WHERE user_id = ? AND done = 1) >= 100 THEN 1 ELSE 0 END
    ''', 'db_operator/src/achievments/18.png'),
    ('Первый тест', 'Пройти 1 тест', '''
        SELECT CASE WHEN (SELECT COUNT(*) FROM testings_stats WHERE user_id = ? AND testing_counter >= 1) >= 1 THEN 1 ELSE 0 END
    ''', 'db_operator/src/achievments/19.png'),
    ('10 тестов', 'Пройти 10 тестов', '''
        SELECT CASE WHEN (SELECT COUNT(*) FROM testings_stats WHERE user_id = ? AND testing_counter >= 1) >= 10 THEN 1 ELSE 0 END
    ''', 'db_operator/src/achievments/20.png'),
    ('50 тестов', 'Пройти 50 тестов', '''
        SELECT CASE WHEN (SELECT COUNT(*) FROM testings_stats WHERE user_id = ? AND testing_counter >= 1) >= 50 THEN 1 ELSE 0 END
    ''', 'db_operator/src/achievments/21.png'),
    ('100 тестов', 'Пройти 100 тестов', '''
        SELECT CASE WHEN (SELECT COUNT(*) FROM testings_stats WHERE user_id = ? AND testing_counter >= 1) >= 100 THEN 1 ELSE 0 END
    ''', 'db_operator/src/achievments/22.png')
]

def add_achievements_with_queries(db_path, achievements):
    for _ in range(5):  # Попробуем выполнить запрос до 5 раз
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Включение внешних ключей
            cursor.execute('PRAGMA foreign_keys = ON')

            # Удаление всех записей из user_achievemnts
            cursor.execute('DELETE FROM user_achievemnts')

            # Удаление всех существующих записей из achievemnts
            cursor.execute('DELETE FROM achievemnts')

            # Добавление новых ачивок в таблицу achievemnts
            for name, description, query, image_path in achievements:
                with open(image_path, 'rb') as file:
                    image = file.read()
                cursor.execute('''
                    INSERT INTO achievemnts (achievemnt_name, achievemnt_description, achievemnt_image, note2)
                    VALUES (?, ?, ?, ?)
                ''', (name, description, image, query))

            conn.commit()
            break  # Если запрос выполнен успешно, выходим из цикла
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                time.sleep(1)  # Ждем 1 секунду перед повторной попыткой
            else:
                raise
        finally:
            if conn:
                conn.close()

# Путь к базе данных
db_path = 'team_app.db'

# Добавление новых ачивок в таблицу
add_achievements_with_queries(db_path, achievements)

# Проверка, что ачивки добавлены
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('PRAGMA foreign_keys = ON')
cursor.execute('SELECT achievemnt_id, achievemnt_name, achievemnt_description FROM achievemnts')
achievements = cursor.fetchall()
conn.close()

for achievement in achievements:
    print(achievement)

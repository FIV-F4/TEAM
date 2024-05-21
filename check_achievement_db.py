import sqlite3
import time


def populate_user_achievements(db_path, user_id):
    for _ in range(5):  # Попробуем выполнить запрос до 5 раз
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Включение внешних ключей
            cursor.execute('PRAGMA foreign_keys = ON')

            # Получение всех ачивок
            cursor.execute('SELECT achievemnt_id, note2 FROM achievemnts')
            achievements = cursor.fetchall()

            for achievemnt_id, note2 in achievements:
                if note2:
                    try:
                        # Проверка, существует ли уже эта ачивка у пользователя
                        cursor.execute('''
                            SELECT COUNT(*) FROM user_achievemnts
                            WHERE user_id = ? AND achievement_id = ?
                        ''', (user_id, achievemnt_id))
                        achievement_exists = cursor.fetchone()[0]

                        if achievement_exists == 0:
                            # Подстановка параметра user_id в запрос
                            note2_query = note2.replace("user_id", "?")

                            # Выполнение запроса из note2 для проверки условия
                            cursor.execute(note2_query, (user_id, user_id))
                            result = cursor.fetchone()[0]

                            if result == 1:
                                # Если условие выполнено, добавляем ачивку пользователю
                                cursor.execute('''
                                    INSERT INTO user_achievemnts (user_id, achievement_id, note1, note2)
                                    VALUES (?, ?, ?, ?)
                                ''', (user_id, achievemnt_id, '', ''))

                    except sqlite3.Error as e:
                        print(f"Ошибка при выполнении запроса для ачивки {achievemnt_id}: {e}")

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

# Пример вызова метода для пользователя с user_id = 1
populate_user_achievements(db_path, 1)

# Проверка, что ачивки добавлены пользователю
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('PRAGMA foreign_keys = ON')
cursor.execute('SELECT * FROM user_achievemnts WHERE user_id = ?', (1,))
user_achievements = cursor.fetchall()
conn.close()

for user_achievement in user_achievements:
    print(user_achievement)

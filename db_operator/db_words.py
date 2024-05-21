import sqlite3
import os

# Установка соединения с базой данных
conn = sqlite3.connect('team_app.db')
cursor = conn.cursor()

# Включение поддержки внешних ключей
cursor.execute('PRAGMA foreign_keys = ON')


# Функция для получения topic_id по названию topic_name
def get_topic_id(topic_name):
    cursor.execute('SELECT topic_id FROM topics WHERE topic_name = ?', (topic_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute('INSERT INTO topics (topic_name) VALUES (?)', (topic_name,))
        conn.commit()
        return cursor.lastrowid


# Функция для вставки слов из файла в базу данных
def insert_words_from_file(file_path, topic):
    topic_id = get_topic_id(topic)

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():
                russian, english = line.strip().split(' - ')

                # Проверка на существование слова
                cursor.execute('SELECT word_id FROM words WHERE russian = ?', (russian,))
                if cursor.fetchone():
                    print(f'Слово "{russian}" уже существует в базе данных. Пропуск вставки.')
                    continue

                # Путь к изображению и звуковому файлу
                img_path = f'db_operator/multimedia/img/{topic}/{english}.png'
                audio_path = f'db_operator/multimedia/audio/{topic}/{english}.mp3'

                # Проверка наличия файлов
                if not os.path.exists(img_path):
                    img_path = None
                if not os.path.exists(audio_path):
                    audio_path = None

                # Чтение содержимого файлов
                picture = None
                sound = None

                if img_path:
                    with open(img_path, 'rb') as img_file:
                        picture = img_file.read()

                if audio_path:
                    with open(audio_path, 'rb') as audio_file:
                        sound = audio_file.read()

                # Вставка данных в таблицу words
                cursor.execute('''
                    INSERT INTO words (russian, english, picture, sound)
                    VALUES (?, ?, ?, ?)
                ''', (russian, english, picture, sound))

                word_id = cursor.lastrowid

                # Вставка данных в таблицу words_groupings
                cursor.execute('''
                    INSERT INTO words_groupings (word_id, topic_id)
                    VALUES (?, ?)
                ''', (word_id, topic_id))

    conn.commit()


# Вставка данных из файлов
insert_words_from_file('db_operator/src/food.txt', 'food')
insert_words_from_file('db_operator/src/travel.txt', 'travel')
insert_words_from_file('db_operator/src/business.txt', 'business')

# Закрытие соединения с базой данных
conn.close()

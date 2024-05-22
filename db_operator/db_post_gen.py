import sqlite3

avatar = None
ach_first_lesson = None
ach_first_test = None
ach_first_words = None

ava_path = f'db_operator/src/avatar/ava.png'
ach1_path = f'db_operator/src/achievments/01.png'
ach2_path = f'db_operator/src/achievments/02.png'
ach3_path = f'db_operator/src/achievments/03.png'

conn = sqlite3.connect('team_app.db')
cursor = conn.cursor()

# Enabling foreign keys
cursor.execute('PRAGMA foreign_keys = ON')

with open(ava_path, 'rb') as f:
    avatar = f.read()

cursor.execute('INSERT INTO users (nickname, image) VALUES (?, ?)', ('zerocoder',  avatar))

with open(ach1_path, 'rb') as f:
    ach_first_lesson = f.read()

with open(ach2_path, 'rb') as f:
    ach_first_test = f.read()

with open(ach3_path, 'rb') as f:
    ach_first_words = f.read()

cursor.execute('INSERT INTO achievemnts (achievemnt_name, achievemnt_description, achievemnt_image) VALUES (?, ?, ?)', ('первооткрыватель', 'Открыт первый урок!',  ach_first_lesson))
cursor.execute('INSERT INTO achievemnts (achievemnt_name, achievemnt_description, achievemnt_image) VALUES (?, ?, ?)', ('исследователь', 'Открыт первый тест!',  ach_first_test))
cursor.execute('INSERT INTO achievemnts (achievemnt_name, achievemnt_description, achievemnt_image) VALUES (?, ?, ?)', ('мегамозг', 'Выучены первые слова!',  ach_first_words))

cursor.execute('''INSERT INTO tests (test_name, test_type)
VALUES
    ('выбор правильного перевода', 1),
    ('соответствие слова и изображения', 2),
    ('написание слова по аудио', 3);
''')

cursor.execute('update topics set topic_name = "ЕДА" where topic_name = "food"')
cursor.execute('update topics set topic_name = "ПУТЕШЕСТВИЯ" where topic_name = "travel"')
cursor.execute('update topics set topic_name = "БИЗНЕС" where topic_name = "business"')


conn.commit()
conn.close()

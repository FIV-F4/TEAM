import sqlite3
import random
import tkinter as tk


def center_window(window, width=800, height=600):
    # Получаем ширину и высоту экрана
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    # Рассчитываем координаты x и y для размещения окна по центру
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.minsize(800, 600)    # Минимальные размеры окна
    window.maxsize(800, 600)    # Максимальные размеры окна


# Базовый класс окна
class BaseWindow:
    def __init__(self, root, main_root):
        self.root = root
        self.main_root = main_root
        center_window(self.root)

    def go_back(self, new_window_class):
        self.root.destroy()
        new_window = tk.Toplevel(self.main_root)
        new_window_class(new_window, self.main_root)

    def open_new_window(self, new_window_class):
        self.root.withdraw()
        new_window = tk.Toplevel(self.main_root)
        new_window_class(new_window, self.main_root)

    def exit_program(self):
        self.root.destroy()
        self.main_root.destroy()


# Функция создания таблиц
def create_tables():
    # Подключаемся к базе данных SQLite (создаем файл базы данных, если он не существует)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Создаем таблицу words
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS words (
            word_id INTEGER PRIMARY KEY,
            russian TEXT NOT NULL UNIQUE,
            transcription_russian TEXT,
            english TEXT,
            transcription_english TEXT,
            picture BLOB,
            picture_front BLOB,
            picture_back BLOB,
            sound BLOB,
            note1 TEXT,
            note2 TEXT
        )
    ''')

    # Создаем таблицу topics
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS topics (
            topic_id INTEGER PRIMARY KEY,
            topic_name TEXT NOT NULL UNIQUE,
            note1 TEXT,
            note2 TEXT
        )
    ''')

    # Создаем таблицу words_groupings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS words_groupings (
            group_id INTEGER PRIMARY KEY,
            word_id INTEGER,
            topic_id INTEGER,
            note1 TEXT,
            note2 TEXT,
            FOREIGN KEY(word_id) REFERENCES words(word_id),
            FOREIGN KEY(topic_id) REFERENCES topics(topic_id)
        )
    ''')

    # Создаем таблицу tests
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tests (
            test_id INTEGER PRIMARY KEY,
            test_name TEXT NOT NULL UNIQUE,
            test_type INTEGER,
            note1 TEXT,
            note2 TEXT
        )
    ''')

    # Создаем таблицу achievements
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS achievements (
            achievement_id INTEGER PRIMARY KEY,
            achievement_name TEXT NOT NULL UNIQUE,
            achievement_description TEXT,
            achievement_image BLOB,
            note1 TEXT,
            note2 TEXT
        )
    ''')

    # Создаем таблицу users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            nickname TEXT NOT NULL UNIQUE,
            image BLOB,
            note1 TEXT,
            note2 TEXT
        )
    ''')

    # Создаем таблицу user_achievements
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_achievements (
            user_stat_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            achievement_id INTEGER,
            note1 TEXT,
            note2 TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            FOREIGN KEY(achievement_id) REFERENCES achievements(achievement_id)
        )
    ''')

    # Создаем таблицу user_progress
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_progress (
            progress_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            word_id INTEGER,
            lesson_id INTEGER,
            success_counter INTEGER,
            fails_counter INTEGER,
            success_date DATE,
            off_rotation BOOLEAN,
            dictionary BOOLEAN,
            note1 TEXT,
            note2 TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            FOREIGN KEY(word_id) REFERENCES words(word_id),
            FOREIGN KEY(lesson_id) REFERENCES lesson(lesson_id)
        )
    ''')

    # Создаем таблицу testing_stats
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS testing_stats (
            testing_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            test_id INTEGER,
            testing_counter INTEGER,
            note1 TEXT,
            note2 TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            FOREIGN KEY(test_id) REFERENCES tests(test_id)
        )
    ''')

    # Создаем таблицу lesson
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lesson (
            lesson_id INTEGER PRIMARY KEY,
            topic_id INTEGER,
            done BOOLEAN,
            note1 TEXT,
            note2 TEXT,
            FOREIGN KEY(topic_id) REFERENCES topics(topic_id)
        )
    ''')

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()


# Заполнение таблиц
def fill_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Добавляем темы
    topics = [
        (1, 'Еда', 'Заметка1 для Еда', 'Заметка2 для Еда'),
        (2, 'Путешествия', 'Заметка1 для Путешествия', 'Заметка2 для Путешествия'),
        (3, 'Бизнес', 'Заметка1 для Бизнес', 'Заметка2 для Бизнес'),
    ]
    cursor.executemany("INSERT INTO topics (topic_id, topic_name, note1, note2) VALUES (?, ?, ?, ?)", topics)

    # Добавляем слова
    words = [
        ('яблоко', 'yabloko', 'apple', 'æpəl', None, None, None, None, 'Фрукт', 'Красный'),
        ('поезд', 'poezd', 'train', 'treɪn', None, None, None, None, 'Транспорт', 'Железнодорожный'),
        ('компания', 'kompaniya', 'company', 'ˈkʌmpəni', None, None, None, None, 'Организация', 'Бизнес'),
        ('кот', 'kot', 'cat', 'kæt', None, None, None, None, 'Животное', 'Домашний'),
        ('собака', 'sobaka', 'dog', 'dɔg', None, None, None, None, 'Животное', 'Домашний'),
        ('машина', 'mashina', 'car', 'kɑr', None, None, None, None, 'Транспорт', 'Автомобильный'),
        ('здание', 'zdanie', 'building', 'ˈbɪldɪŋ', None, None, None, None, 'Строение', 'Высокое'),
        ('телефон', 'telefon', 'phone', 'foʊn', None, None, None, None, 'Устройство', 'Мобильный'),
        ('мороженое', 'morozhenoe', 'ice cream', 'aɪs krim', None, None, None, None, 'Десерт', 'Сладкий'),
        ('чай', 'chai', 'tea', 'ti', None, None, None, None, 'Напиток', 'Горячий'),
        ('кофе', 'kofe', 'coffee', 'ˈkɔfi', None, None, None, None, 'Напиток', 'Горячий'),
        ('велосипед', 'velosiped', 'bicycle', 'ˈbaɪsɪkəl', None, None, None, None, 'Транспорт', 'Экологичный'),
        ('море', 'more', 'sea', 'si', None, None, None, None, 'Природа', 'Водный'),
        ('река', 'reka', 'river', 'ˈrɪvər', None, None, None, None, 'Природа', 'Водный'),
        ('птица', 'ptitsa', 'bird', 'bɜrd', None, None, None, None, 'Животное', 'Летающее'),
        ('самолет', 'samolet', 'airplane', 'ˈɛrˌpleɪn', None, None, None, None, 'Транспорт', 'Воздушный'),
        ('автобус', 'avtobus', 'bus', 'bʌs', None, None, None, None, 'Транспорт', 'Общественный'),
        ('поездка', 'poezdka', 'trip', 'trɪp', None, None, None, None, 'Путешествие', 'Кратковременное'),
        ('праздник', 'prazdnik', 'holiday', 'ˈhɑləˌdeɪ', None, None, None, None, 'Событие', 'Праздничное'),
        ('работа', 'rabota', 'work', 'wɜrk', None, None, None, None, 'Деятельность', 'Профессиональная'),
    ]
    cursor.executemany('''
        INSERT INTO words (russian, transcription_russian, english, transcription_english, picture, picture_front, picture_back, sound, note1, note2)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', words)

    # Добавляем связи слов и тем
    words_groupings = [
        (1, 1, 1, 'Заметка1 для группы', 'Заметка2 для группы'),
        (2, 2, 2, 'Заметка1 для группы', 'Заметка2 для группы'),
        (3, 3, 3, 'Заметка1 для группы', 'Заметка2 для группы'),
    ]
    for i in range(17):
        words_groupings.append((i + 4, random.randint(1, 20), random.randint(1, 3), f'Заметка1_{i}', f'Заметка2_{i}'))

    cursor.executemany('''
        INSERT INTO words_groupings (group_id, word_id, topic_id, note1, note2)
        VALUES (?, ?, ?, ?, ?)
    ''', words_groupings)

    # Добавляем тесты
    tests = [
        (1, 'Тест по еде', 1, 'Заметка1 для теста', 'Заметка2 для теста'),
        (2, 'Тест по путешествиям', 2, 'Заметка1 для теста', 'Заметка2 для теста'),
        (3, 'Тест по бизнесу', 3, 'Заметка1 для теста', 'Заметка2 для теста'),
    ]
    for i in range(17):
        tests.append((i + 4, f'Тест_{i}', random.randint(1, 3), f'Заметка1_{i}', f'Заметка2_{i}'))

    cursor.executemany('''
        INSERT INTO tests (test_id, test_name, test_type, note1, note2)
        VALUES (?, ?, ?, ?, ?)
    ''', tests)

    # Добавляем достижения
    achievements = [
        (1, 'Первое достижение', 'Описание первого достижения', None, 'Заметка1 для достижения',
         'Заметка2 для достижения'),
        (2, 'Второе достижение', 'Описание второго достижения', None, 'Заметка1 для достижения',
         'Заметка2 для достижения'),
        (3, 'Третье достижение', 'Описание третьего достижения', None, 'Заметка1 для достижения',
         'Заметка2 для достижения'),
    ]
    for i in range(17):
        achievements.append((i + 4, f'Достижение_{i}', f'Описание_{i}', None, f'Заметка1_{i}', f'Заметка2_{i}'))

    cursor.executemany('''
        INSERT INTO achievements (achievement_id, achievement_name, achievement_description, achievement_image, note1, note2)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', achievements)

    # Добавляем пользователей
    users = [
        (1, 'user1', None, 'Заметка1 для user1', 'Заметка2 для user1'),
        (2, 'user2', None, 'Заметка1 для user2', 'Заметка2 для user2'),
        (3, 'user3', None, 'Заметка1 для user3', 'Заметка2 для user3'),
    ]
    for i in range(17):
        users.append((i + 4, f'user_{i}', None, f'Заметка1_{i}', f'Заметка2_{i}'))

    cursor.executemany('''
        INSERT INTO users (user_id, nickname, image, note1, note2)
        VALUES (?, ?, ?, ?, ?)
    ''', users)

    # Добавляем пользовательские достижения
    user_achievements = [
        (1, 1, 1, 'Заметка1 для user_achievements', 'Заметка2 для user_achievements'),
        (2, 2, 2, 'Заметка1 для user_achievements', 'Заметка2 для user_achievements'),
        (3, 3, 3, 'Заметка1 для user_achievements', 'Заметка2 для user_achievements'),
    ]
    for i in range(17):
        user_achievements.append(
            (i + 4, random.randint(1, 20), random.randint(1, 20), f'Заметка1_{i}', f'Заметка2_{i}'))

    cursor.executemany('''
        INSERT INTO user_achievements (user_stat_id, user_id, achievement_id, note1, note2)
        VALUES (?, ?, ?, ?, ?)
    ''', user_achievements)

    # Добавляем прогресс пользователей
    user_progress = [
        (1, 1, 1, 1, 10, 0, '2023-01-01', False, True, 'Заметка1 для user_progress', 'Заметка2 для user_progress'),
        (2, 2, 2, 2, 5, 5, '2023-01-02', True, False, 'Заметка1 для user_progress', 'Заметка2 для user_progress'),
        (3, 3, 3, 3, 8, 2, '2023-01-03', False, True, 'Заметка1 для user_progress', 'Заметка2 для user_progress'),
    ]
    for i in range(17):
        user_progress.append((i + 4, random.randint(1, 20), random.randint(1, 20), random.randint(1, 20),
                              random.randint(0, 10), random.randint(0, 10), '2023-01-01', random.choice([True, False]),
                              random.choice([True, False]), f'Заметка1_{i}', f'Заметка2_{i}'))

    cursor.executemany('''
        INSERT INTO user_progress (progress_id, user_id, word_id, lesson_id, success_counter, fails_counter, success_date, off_rotation, dictionary, note1, note2)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', user_progress)

    # Добавляем статистику тестирования
    testing_stats = [
        (1, 1, 1, 10, 'Заметка1 для testing_stats', 'Заметка2 для testing_stats'),
        (2, 2, 2, 5, 'Заметка1 для testing_stats', 'Заметка2 для testing_stats'),
        (3, 3, 3, 8, 'Заметка1 для testing_stats', 'Заметка2 для testing_stats'),
    ]
    for i in range(17):
        testing_stats.append((i + 4, random.randint(1, 20), random.randint(1, 20), random.randint(0, 10),
                              f'Заметка1_{i}', f'Заметка2_{i}'))

    cursor.executemany('''
        INSERT INTO testing_stats (testing_id, user_id, test_id, testing_counter, note1, note2)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', testing_stats)

    # Добавляем уроки
    lessons = [
        (1, 1, True, 'Заметка1 для lesson', 'Заметка2 для lesson'),
        (2, 2, False, 'Заметка1 для lesson', 'Заметка2 для lesson'),
        (3, 3, True, 'Заметка1 для lesson', 'Заметка2 для lesson'),
    ]
    for i in range(17):
        lessons.append((i + 4, random.randint(1, 3), random.choice([True, False]), f'Заметка1_{i}', f'Заметка2_{i}'))

    cursor.executemany('''
        INSERT INTO lesson (lesson_id, topic_id, done, note1, note2)
        VALUES (?, ?, ?, ?, ?)
    ''', lessons)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    # create_tables()       # Для создания таблиц
    # fill_tables()         # Для заполнения таблиц данными
    from main_window import MainWindow

    root = tk.Tk()          # Инициализация главного окна
    center_window(root)     # Центрирование окна
    app = MainWindow(root, root)    # Инициализация главного окна
    root.mainloop()         # Запуск главного цикла

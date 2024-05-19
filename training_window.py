import tkinter as tk
import sqlite3
from main import BaseWindow
from lessons import Lessons


class TrainingWindow(BaseWindow):
    def __init__(self, root, main_root, current_user):
        super().__init__(root, main_root, current_user)
        self.root.title("Программа обучения английскому языку - Обучение")

        self.current_user = current_user

        # Создаем основной лейбл
        self.main_label = tk.Label(root, text="Обучение", font=("Arial", 24))
        self.main_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        # Подключаемся к базе данных и получаем названия тем
        self.topics = self.get_topics_from_db()

        # Дополняем недостающие темы "N/A"
        while len(self.topics) < 4:
            self.topics.append("N/A")

        # Создаем кнопки с текстом из базы данных
        self.lesson1_button = tk.Button(root, text=f"Урок ({self.topics[0]})", width=20, height=5,
                                        command=lambda: self.start_lesson(self.topics[0]))
        self.lesson2_button = tk.Button(root, text=f"Урок ({self.topics[1]})", width=20, height=5,
                                        command=lambda: self.start_lesson(self.topics[1]))
        self.lesson3_button = tk.Button(root, text=f"Урок ({self.topics[2]})", width=20, height=5,
                                        command=lambda: self.start_lesson(self.topics[2]))
        self.lesson4_button = tk.Button(root, text=f"Урок ({self.topics[3]})", width=20, height=5,
                                        command=lambda: self.start_lesson(self.topics[3]))
        self.back_button = tk.Button(root, text="Назад", width=10, height=2, command=self.go_back_main)
        self.forward_button = tk.Button(root, text="Вперед", width=10, height=2, command=self.open_testing_window)
        self.exit_button = tk.Button(root, text="Выход", width=10, height=2, command=self.exit_program)

        # Размещаем кнопки
        self.lesson1_button.place(relx=0.25, rely=0.4, anchor=tk.CENTER)
        self.lesson2_button.place(relx=0.75, rely=0.4, anchor=tk.CENTER)
        self.lesson3_button.place(relx=0.25, rely=0.6, anchor=tk.CENTER)
        self.lesson4_button.place(relx=0.75, rely=0.6, anchor=tk.CENTER)
        self.back_button.place(relx=0.2, rely=0.8, anchor=tk.CENTER)
        self.forward_button.place(relx=0.8, rely=0.8, anchor=tk.CENTER)
        self.exit_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    def get_topics_from_db(self):
        conn = sqlite3.connect('team_app.db')  # Укажите путь к вашей базе данных
        cursor = conn.cursor()

        cursor.execute("SELECT topic_name FROM topics ORDER BY topic_id")
        topics = cursor.fetchall()

        conn.close()

        # Возвращаем список названий тем
        return [topic[0] for topic in topics]

    def start_lesson(self, topic):
        self.root.withdraw()
        lesson_window = tk.Toplevel(self.main_root)
        Lessons(lesson_window, self.main_root, self.current_user, topic)

    def go_back_main(self):
        from main_window import MainWindow
        self.go_back(MainWindow)

    def open_testing_window(self):
        from testing_window import TestingWindow
        self.open_new_window(TestingWindow)

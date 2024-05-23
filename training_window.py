import tkinter as tk
import sqlite3
from main import BaseWindow
from lessons import Lessons
from styles import StyledCanvas, StyledButton

class TrainingWindow(BaseWindow):
    def __init__(self, root, main_root, current_user):
        super().__init__(root, main_root, current_user)
        self.root.title("Программа обучения английскому языку - Обучение")

        self.current_user = current_user

        # Создаем холст для фона
        self.canvas = StyledCanvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Создаем основной текст на холсте
        self.canvas.create_text(400, 50, text="Обучение", font=("Helvetica", 24), fill="black")

        # Подключаемся к базе данных и получаем названия тем
        self.topics = self.get_topics_from_db()

        # Дополняем недостающие темы "N/A"
        while len(self.topics) < 4:
            self.topics.append("N/A")

        # Создаем кнопки с текстом из базы данных
        self.lesson1_button = StyledButton(self.canvas, 200, 200, text=f"Урок ({self.topics[0]})", command=lambda: self.start_lesson(self.topics[0]))
        self.lesson2_button = StyledButton(self.canvas, 600, 200, text=f"Урок ({self.topics[1]})", command=lambda: self.start_lesson(self.topics[1]))
        self.lesson3_button = StyledButton(self.canvas, 200, 400, text=f"Урок ({self.topics[2]})", command=lambda: self.start_lesson(self.topics[2]))
        self.lesson4_button = StyledButton(self.canvas, 600, 400, text=f"Урок ({self.topics[3]})", command=lambda: self.start_lesson(self.topics[3]))

        # Создаем навигационные кнопки с меньшими размерами
        self.back_button = StyledButton(self.canvas, 200, 500, text="Назад", command=self.go_back_main, width=100, height=40)
        self.forward_button = StyledButton(self.canvas, 600, 500, text="Вперед", command=self.open_testing_window, width=100, height=40)
        self.exit_button = StyledButton(self.canvas, 400, 500, text="Выход", command=self.exit_program, width=100, height=40)

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

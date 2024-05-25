import tkinter as tk
from tkinter import Label, Frame, Canvas, Scrollbar
from PIL import Image, ImageTk
import sqlite3
import io

from check_achievement_db import populate_user_achievements
from main import BaseWindow
from styles import StyledCanvas, StyledButton

class ProgressWindow(BaseWindow):
    def __init__(self, root, main_root, current_user):
        super().__init__(root, main_root, current_user)
        self.root.title("Программа обучения английскому языку - Прогресс")

        # Получаем никнейм текущего пользователя
        self.nickname = self.get_user_nickname()

        # Создаем холст для фона
        self.canvas = StyledCanvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Отображение текущего пользователя
        self.current_user_label = Label(self.canvas, text=f"Пользователь: {self.nickname}", font=("Arial", 16), bg='white')
        self.canvas.create_window(400, 30, window=self.current_user_label, anchor="center")

        # Создаем фреймы
        self.achievements_frame = Frame(self.canvas)
        self.canvas.create_window(100, 100, window=self.achievements_frame, anchor="nw", width=470, height=350)

        self.statistics_frame = Frame(self.canvas)
        self.canvas.create_window(600, 100, window=self.statistics_frame, anchor="nw")

        self.button_frame = Frame(self.canvas)
        self.canvas.create_window(400, 550, window=self.button_frame, anchor="center")

        # Добавляем канвас и скроллинг для ачивок
        self.achievements_canvas = Canvas(self.achievements_frame)
        self.scrollbar = Scrollbar(self.achievements_frame, orient="vertical", command=self.achievements_canvas.yview)
        self.scrollable_frame = Frame(self.achievements_canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.achievements_canvas.configure(
                scrollregion=self.achievements_canvas.bbox("all")
            )
        )

        self.achievements_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.achievements_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.achievements_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.images = []  # Список для хранения изображений
        self.load_achievements()
        self.load_statistics()

        # Создаем кнопки
        self.back_button = StyledButton(self.canvas, 200, 500, text="Назад", command=self.go_back_dictionary, width=100, height=40)
        self.forward_button = StyledButton(self.canvas, 600, 500, text="Вперед", command=self.open_main_window, width=100, height=40)
        self.exit_button = StyledButton(self.canvas, 400, 500, text="Выход", command=self.exit_program, width=100, height=40)

    def get_user_nickname(self):
        conn = sqlite3.connect('team_app.db')
        cursor = conn.cursor()

        cursor.execute('SELECT nickname FROM users WHERE user_id = ?', (self.current_user,))
        nickname = cursor.fetchone()[0]
        conn.close()
        return nickname

    def load_achievements(self):
        # Перед загрузкой ачивок проверяем, базу и записываем новые -1-
        populate_user_achievements('team_app.db', self.current_user)

        #-1-
        conn = sqlite3.connect('team_app.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT achievemnts.achievemnt_image, achievemnts.achievemnt_name
            FROM user_achievemnts
            JOIN achievemnts ON user_achievemnts.achievement_id = achievemnts.achievemnt_id
            WHERE user_achievemnts.user_id = ?
        ''', (self.current_user,))
        achievements = cursor.fetchall()
        conn.close()
        print(self.current_user)
        if not achievements:
            return

        column = 0
        row = 0

        for achievemnt_image, achievemnt_name in achievements:
            image = Image.open(io.BytesIO(achievemnt_image))
            image = image.resize((100, 100), Image.LANCZOS)  # Уменьшаем размер изображения
            photo = ImageTk.PhotoImage(image)
            self.images.append(photo)  # Сохраняем ссылку на изображение
            img_label = Label(self.scrollable_frame, image=photo, text=achievemnt_name, compound="top")
            img_label.grid(row=row, column=column, padx=10, pady=10)

            column += 1
            if column >= 3:  # Перенос на следующую строку после 3 изображений
                column = 0
                row += 1

    def load_statistics(self):
        conn = sqlite3.connect('team_app.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT topics.topic_name, 
                   (SELECT COUNT(DISTINCT word_id) FROM user_progress WHERE user_id = ? AND word_id IN 
                    (SELECT word_id FROM words_groupings WHERE topic_id = topics.topic_id) AND success_counter > 0) * 100.0 / 
                   (SELECT COUNT(*) FROM words_groupings WHERE topic_id = topics.topic_id)
            FROM topics
        ''', (self.current_user,))
        statistics = cursor.fetchall()
        conn.close()

        for topic_name, progress in statistics:
            stat_label = Label(self.statistics_frame, text=f"{topic_name}: {progress:.2f}%")
            stat_label.pack(pady=5)

    def go_back_dictionary(self):
        from dictionary_window import DictionaryWindow
        self.go_back(DictionaryWindow)

    def open_main_window(self):
        from main_window import MainWindow
        self.open_new_window(MainWindow)

"""if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Скрыть основное окно

    # Пример вызова окна прогресса для пользователя с user_id = 1
    main_root = tk.Tk()
    progress_window = ProgressWindow(main_root, main_root, current_user=1)
    main_root.mainloop()"""

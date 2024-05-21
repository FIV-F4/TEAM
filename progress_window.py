import tkinter as tk
from tkinter import Label, Frame, Button, Canvas, Scrollbar
from PIL import Image, ImageTk
import sqlite3
import io

from check_achievement_db import populate_user_achievements
from main import BaseWindow

class ProgressWindow(BaseWindow):
    def __init__(self, root, main_root, current_user):

        super().__init__(root, main_root, current_user)
        self.root.title("Программа обучения английскому языку - Прогресс")

        # Создаем фреймы
        self.achievements_frame = Frame(self.root)
        self.achievements_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.statistics_frame = Frame(self.root)
        self.statistics_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.button_frame = Frame(self.root)
        self.button_frame.pack(side="bottom", fill="x", pady=10)

        self.exit_button = Button(self.button_frame, text="Выход", command=self.exit_program, width=10, height=2)
        self.exit_button.pack()

        # Добавляем канвас и скроллинг для ачивок
        self.canvas = Canvas(self.achievements_frame)
        self.scrollbar = Scrollbar(self.achievements_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.images = []  # Список для хранения изображений
        self.load_achievements()
        self.load_statistics()

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

        for achievemnt_image, achievemnt_name in achievements:
            image = Image.open(io.BytesIO(achievemnt_image))
            image = image.resize((100, 100), Image.Resampling.LANCZOS)  # Уменьшаем размер изображения
            photo = ImageTk.PhotoImage(image)
            self.images.append(photo)  # Сохраняем ссылку на изображение
            img_label = Label(self.scrollable_frame, image=photo, text=achievemnt_name, compound="top")
            img_label.pack(pady=10)

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

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Скрыть основное окно

    # Пример вызова окна прогресса для пользователя с user_id = 1
    main_root = tk.Tk()
    progress_window = ProgressWindow(main_root, main_root, current_user=1)
    main_root.mainloop()

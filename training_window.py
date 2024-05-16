import tkinter as tk
from main import BaseWindow


class TrainingWindow(BaseWindow):
    def __init__(self, root, main_root):
        super().__init__(root, main_root)
        self.root.title("Программа обучения английскому языку - Обучение")

        # Создаем основной лейбл
        self.main_label = tk.Label(root, text="Обучение", font=("Arial", 24))
        self.main_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        # Создаем кнопки
        self.lesson1_button = tk.Button(root, text="Урок (Тема1)", width=20, height=5)
        self.lesson2_button = tk.Button(root, text="Урок (Тема2)", width=20, height=5)
        self.lesson3_button = tk.Button(root, text="Урок (Тема3)", width=20, height=5)
        self.lesson4_button = tk.Button(root, text="Урок (Тема4)", width=20, height=5)
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

    def go_back_main(self):
        from main_window import MainWindow
        self.go_back(MainWindow)

    def open_testing_window(self):
        from testing_window import TestingWindow
        self.open_new_window(TestingWindow)

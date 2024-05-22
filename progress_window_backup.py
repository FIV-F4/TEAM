import tkinter as tk
from main import BaseWindow

class ProgressWindow(BaseWindow):
    def __init__(self, root, main_root, current_user):
        super().__init__(root, main_root, current_user)
        self.root.title("Программа обучения английскому языку - Информация по прогрессу")

        self.current_user = current_user

        # Создаем основной лейбл
        self.main_label = tk.Label(root, text="Прогресс", font=("Arial", 24))
        self.main_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        # Создаем кнопки
        self.view_lessons_button = tk.Button(root, text="Просмотрено уроков", width=20, height=5)
        self.completed_tests_button = tk.Button(root, text="Пройдено тестирований", width=20, height=5)
        self.achievements_button = tk.Button(root, text="Ачивка каждые 10 тем", width=20, height=5)
        self.others_button = tk.Button(root, text="Другое", width=20, height=5)
        self.back_button = tk.Button(root, text="Назад", width=10, height=2, command=self.go_back_dictionary)
        self.forward_button = tk.Button(root, text="Вперед", width=10, height=2, command=self.open_main_window)
        self.exit_button = tk.Button(root, text="Выход", width=10, height=2, command=self.exit_program)

        # Размещаем кнопки
        self.view_lessons_button.place(relx=0.25, rely=0.4, anchor=tk.CENTER)
        self.completed_tests_button.place(relx=0.75, rely=0.4, anchor=tk.CENTER)
        self.achievements_button.place(relx=0.25, rely=0.6, anchor=tk.CENTER)
        self.others_button.place(relx=0.75, rely=0.6, anchor=tk.CENTER)
        self.back_button.place(relx=0.2, rely=0.8, anchor=tk.CENTER)
        self.forward_button.place(relx=0.8, rely=0.8, anchor=tk.CENTER)
        self.exit_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    def go_back_dictionary(self):
        from dictionary_window import DictionaryWindow
        self.go_back(DictionaryWindow)

    def open_main_window(self):
        from main_window import MainWindow
        self.open_new_window(MainWindow)

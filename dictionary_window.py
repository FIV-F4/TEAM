import tkinter as tk
from main import BaseWindow


class DictionaryWindow(BaseWindow):
    def __init__(self, root, main_root, current_user):
        super().__init__(root, main_root, current_user)
        self.root.title("Программа обучения английскому языку - Словарь")

        self.current_user = current_user

        # Создаем основной лейбл
        self.main_label = tk.Label(root, text="Словарь", font=("Arial", 24))
        self.main_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        # Создаем кнопки
        self.view_button = tk.Button(root, text="Просмотр слов", width=20, height=5)
        self.add_button = tk.Button(root, text="Добавление слов", width=20, height=5)
        self.test_button = tk.Button(root, text="Тестирование \n (слова из словаря)", width=20, height=5)
        self.delete_button = tk.Button(root, text="Удаление слов", width=20, height=5)
        self.back_button = tk.Button(root, text="Назад", width=10, height=2, command=self.go_back_testing)
        self.forward_button = tk.Button(root, text="Вперед", width=10, height=2, command=self.open_progress_window)
        self.exit_button = tk.Button(root, text="Выход", width=10, height=2, command=self.exit_program)

        # Размещаем кнопки
        self.view_button.place(relx=0.25, rely=0.4, anchor=tk.CENTER)
        self.add_button.place(relx=0.75, rely=0.4, anchor=tk.CENTER)
        self.test_button.place(relx=0.25, rely=0.6, anchor=tk.CENTER)
        self.delete_button.place(relx=0.75, rely=0.6, anchor=tk.CENTER)
        self.back_button.place(relx=0.2, rely=0.8, anchor=tk.CENTER)
        self.forward_button.place(relx=0.8, rely=0.8, anchor=tk.CENTER)
        self.exit_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    def go_back_testing(self):
        from testing_window import TestingWindow
        self.go_back(TestingWindow)

    def open_progress_window(self):
        from progress_window import ProgressWindow
        self.open_new_window(ProgressWindow)

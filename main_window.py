import tkinter as tk
from main import BaseWindow

class MainWindow(BaseWindow):
    def __init__(self, root, main_root, current_user):
        super().__init__(root, main_root, current_user)
        self.root.title("Программа обучения английскому языку - Главное меню")

        self.current_user = current_user

        # Создаем основной лейбл
        self.main_label = tk.Label(root, text="Главное меню", font=("Arial", 24))
        self.main_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Создаем кнопки
        self.training_button = tk.Button(root, text="Обучение", width=20, height=5, command=self.open_training_window)
        self.testing_button = tk.Button(root, text="Тестирование", width=20, height=5, command=self.open_testing_window)
        self.dictionary_button = tk.Button(root, text="Словарь", width=20, height=5, command=self.open_dictionary_window)
        self.progress_button = tk.Button(root, text="Прогресс", width=20, height=5, command=self.open_progress_window)

        # Размещаем кнопки
        self.training_button.place(relx=0.25, rely=0.3, anchor=tk.CENTER)
        self.testing_button.place(relx=0.75, rely=0.3, anchor=tk.CENTER)
        self.dictionary_button.place(relx=0.25, rely=0.7, anchor=tk.CENTER)
        self.progress_button.place(relx=0.75, rely=0.7, anchor=tk.CENTER)

    def open_training_window(self):
        from training_window import TrainingWindow
        self.open_new_window(TrainingWindow)

    def open_testing_window(self):
        from testing_window import TestingWindow
        self.open_new_window(TestingWindow)

    def open_dictionary_window(self):
        from dictionary_window import DictionaryWindow
        self.open_new_window(DictionaryWindow)

    def open_progress_window(self):
        from progress_window import ProgressWindow
        self.open_new_window(ProgressWindow)

import tkinter as tk
from main import BaseWindow
from styles import StyledCanvas, StyledButton


class MainWindow(BaseWindow):
    def __init__(self, root, main_root, current_user):
        super().__init__(root, main_root, current_user)
        self.root.title("Программа обучения английскому языку - Главное меню")

        self.current_user = current_user

        # Создаем холст для фона
        self.canvas = StyledCanvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Создаем основной текст на холсте
        self.canvas.create_text(400, 50, text="Главное меню", font=('Helvetica', 24), fill='black')

        # Создаем кнопки
        self.training_button = StyledButton(self.canvas, 200, 200, text="Обучение", command=self.open_training_window)
        self.testing_button = StyledButton(self.canvas, 600, 200, text="Тестирование", command=self.open_testing_window)
        self.dictionary_button = StyledButton(self.canvas, 200, 400, text="Словарь",
                                              command=self.open_dictionary_window)
        self.progress_button = StyledButton(self.canvas, 600, 400, text="Прогресс", command=self.open_progress_window)

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

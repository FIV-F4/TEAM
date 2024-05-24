import tkinter as tk
from main import BaseWindow
from styles import StyledCanvas, StyledButton

class DictionaryWindow(BaseWindow):
    def __init__(self, root, main_root, current_user):
        super().__init__(root, main_root, current_user)
        self.root.title("Программа обучения английскому языку - Словарь")

        self.current_user = current_user

        # Создаем холст для фона
        self.canvas = StyledCanvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Создаем основной текст на холсте
        self.canvas.create_text(400, 50, text="Словарь", font=("Helvetica", 24), fill="black")

        # Создаем кнопки с текстом
        self.view_button = StyledButton(self.canvas, 200, 200, text="Просмотр слов")
        self.add_button = StyledButton(self.canvas, 600, 200, text="Добавление слов")
        self.test_button = StyledButton(self.canvas, 200, 400, text="Тестирование \n (слова из словаря)")
        self.delete_button = StyledButton(self.canvas, 600, 400, text="Удаление слов")

        # Создаем навигационные кнопки с меньшими размерами
        self.back_button = StyledButton(self.canvas, 200, 500, text="Назад", command=self.go_back_testing, width=100, height=40)
        self.forward_button = StyledButton(self.canvas, 600, 500, text="Вперед", command=self.open_progress_window, width=100, height=40)
        self.exit_button = StyledButton(self.canvas, 400, 500, text="Выход", command=self.exit_program, width=100, height=40)

    def go_back_testing(self):
        from testing_window import TestingWindow
        self.go_back(TestingWindow)

    def open_progress_window(self):
        from progress_window import ProgressWindow
        self.open_new_window(ProgressWindow)

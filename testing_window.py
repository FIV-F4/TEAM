import tkinter as tk
from main import BaseWindow
from styles import StyledCanvas, StyledButton

class TestingWindow(BaseWindow):
    def __init__(self, root, main_root, current_user):
        super().__init__(root, main_root, current_user)
        self.root.title("Программа обучения английскому языку - Тестирование")

        self.current_user = current_user

        # Создаем холст для фона
        self.canvas = StyledCanvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Создаем основной текст на холсте
        self.canvas.create_text(400, 50, text="Тестирование по темам", font=("Helvetica", 24), fill="black")

        # Создаем кнопки с текстом
        self.var1_button = StyledButton(self.canvas, 200, 200, text="Тестирование (вар.1)")
        self.var2_button = StyledButton(self.canvas, 600, 200, text="Тестирование (вар.2)")
        self.var3_button = StyledButton(self.canvas, 200, 400, text="Тестирование (вар.3)")
        self.var4_button = StyledButton(self.canvas, 600, 400, text="Тестирование (вар.4)")

        # Создаем навигационные кнопки с меньшими размерами
        self.back_button = StyledButton(self.canvas, 200, 500, text="Назад", command=self.go_back_training, width=100, height=40)
        self.forward_button = StyledButton(self.canvas, 600, 500, text="Вперед", command=self.open_dictionary_window, width=100, height=40)
        self.exit_button = StyledButton(self.canvas, 400, 500, text="Выход", command=self.exit_program, width=100, height=40)

    def go_back_training(self):
        from training_window import TrainingWindow
        self.go_back(TrainingWindow)

    def open_dictionary_window(self):
        from dictionary_window import DictionaryWindow
        self.open_new_window(DictionaryWindow)

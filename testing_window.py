import tkinter as tk
from main import BaseWindow


class TestingWindow(BaseWindow):
    def __init__(self, root, main_root, current_user):
        super().__init__(root, main_root)
        self.root.title("Программа обучения английскому языку - Тестирование")

        self.current_user = current_user

        # Создаем основной лейбл
        self.main_label = tk.Label(root, text="Тестирование по темам", font=("Arial", 24))
        self.main_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        # Создаем кнопки
        self.var1_button = tk.Button(root, text="Тестирование (вар.1)", width=20, height=5)
        self.var2_button = tk.Button(root, text="Тестирование (вар.2)", width=20, height=5)
        self.var3_button = tk.Button(root, text="Тестирование (вар.3)", width=20, height=5)
        self.var4_button = tk.Button(root, text="Тестирование (вар.4)", width=20, height=5)
        self.back_button = tk.Button(root, text="Назад", width=10, height=2, command=self.go_back_training)
        self.forward_button = tk.Button(root, text="Вперед", width=10, height=2, command=self.open_dictionary_window)
        self.exit_button = tk.Button(root, text="Выход", width=10, height=2, command=self.exit_program)

        # Размещаем кнопки
        self.var1_button.place(relx=0.25, rely=0.4, anchor=tk.CENTER)
        self.var2_button.place(relx=0.75, rely=0.4, anchor=tk.CENTER)
        self.var3_button.place(relx=0.25, rely=0.6, anchor=tk.CENTER)
        self.var4_button.place(relx=0.75, rely=0.6, anchor=tk.CENTER)
        self.back_button.place(relx=0.2, rely=0.8, anchor=tk.CENTER)
        self.forward_button.place(relx=0.8, rely=0.8, anchor=tk.CENTER)
        self.exit_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    def go_back_training(self):
        from training_window import TrainingWindow
        self.go_back(TrainingWindow)

    def open_dictionary_window(self):
        from dictionary_window import DictionaryWindow
        self.open_new_window(DictionaryWindow)

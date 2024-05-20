import tkinter as tk
from tkinter import Label, Button, Entry, filedialog
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import sqlite3
import io
from main import BaseWindow


class ErrorWindow:
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("Ошибка!")
        self.root.geometry("400x150")
        self.root.resizable(False, False)
        self.center_window()

        Label(self.root, text="Ошибка! Выберите пользователя!", font=("Arial", 14)).pack(pady=20)
        Button(self.root, text="OK", command=self.root.destroy, font=("Arial", 14)).pack(pady=10)

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 150) // 2
        self.root.geometry(f"400x150+{x}+{y}")


class LoginWindow(BaseWindow):
    def __init__(self, root, main_root, current_user):
        super().__init__(root, main_root, current_user)
        self.root = root
        self.current_user = current_user
        self.main_root = main_root
        self.conn = sqlite3.connect('team_app.db')
        self.cursor = self.conn.cursor()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Выбор пользователя")

        # Получаем данные пользователей из БД
        self.cursor.execute("SELECT user_id, nickname, image FROM users")
        self.users = self.cursor.fetchall()

        # Создаем выпадающий список для выбора пользователя
        self.user_combobox = Combobox(self.root, font=("Arial", 14), state="readonly")
        self.user_combobox['values'] = [user[1] for user in self.users]
        self.user_combobox.pack(pady=20)
        self.user_combobox.bind("<<ComboboxSelected>>", self.show_user_details)

        # Поля для отображения аватарки и имени пользователя
        self.avatar_label = Label(self.root)
        self.avatar_label.pack(pady=10)

        self.nickname_label = Label(self.root, font=("Arial", 14))
        self.nickname_label.pack(pady=10)

        # Кнопка для выбора пользователя
        select_user_button = Button(self.root, text="Выбрать пользователя", font=("Arial", 14),
                                    command=self.select_user)
        select_user_button.pack(pady=10)

        # Кнопка для создания новой учетной записи
        self.create_account_button = Button(self.root, text="Создать учетную запись", font=("Arial", 14),
                                            command=self.open_create_account_window)
        self.create_account_button.pack(pady=10)

        # Кнопка для выхода из программы
        exit_button = Button(self.root, text="Выход", font=("Arial", 14), command=self.exit_program)
        exit_button.pack(pady=20)

    def show_user_details(self, event):
        selected_nickname = self.user_combobox.get()
        selected_user = next(user for user in self.users if user[1] == selected_nickname)
        user_id, nickname, image = selected_user

        avatar_image = Image.open(io.BytesIO(image)).resize((100, 100), Image.Resampling.LANCZOS)
        avatar_photo = ImageTk.PhotoImage(avatar_image)

        self.avatar_label.config(image=avatar_photo)
        self.avatar_label.image = avatar_photo  # Сохранение ссылки на изображение
        self.nickname_label.config(text=nickname)

    def select_user(self):
        selected_nickname = self.user_combobox.get()
        if not selected_nickname:
            ErrorWindow(self.root)
            return
        selected_user = next(user for user in self.users if user[1] == selected_nickname)
        self.current_user = selected_user[0]

        self.root.withdraw()
        from main_window import MainWindow
        new_window = tk.Toplevel(self.main_root)
        MainWindow(new_window, self.main_root, self.current_user)

    def open_create_account_window(self):
        self.root.withdraw()
        new_window = tk.Toplevel(self.main_root)
        CreateAccountWindow(new_window, self.main_root, self, self.current_user)

    def reset_ui(self):
        # Удаляем все виджеты из окна
        for widget in self.root.winfo_children():
            widget.destroy()
        # Пересоздаем UI
        self.setup_ui()


class CreateAccountWindow(BaseWindow):
    def __init__(self, root, main_root, login_window, current_user):
        super().__init__(root, main_root, current_user)
        self.root = root
        self.current_user = current_user
        self.main_root = main_root
        self.login_window = login_window
        self.conn = sqlite3.connect('team_app.db')
        self.cursor = self.conn.cursor()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Новая учетная запись")

        Label(self.root, text="Введите имя:", font=("Arial", 14)).pack(pady=10)
        self.name_entry = Entry(self.root, font=("Arial", 14))
        self.name_entry.pack(pady=10)

        Label(self.root, text="Выберите аватарку:", font=("Arial", 14)).pack(pady=10)
        self.avatar_button = Button(self.root, text="Аватарка", font=("Arial", 14), command=self.choose_avatar)
        self.avatar_button.pack(pady=10)

        self.avatar_image = None
        self.avatar_photo = None

        create_button = Button(self.root, text="Создать", font=("Arial", 14), command=self.create_account)
        create_button.pack(pady=10)

        exit_button = Button(self.root, text="Выход", font=("Arial", 14), command=self.exit_program)
        exit_button.pack(pady=10)

    def choose_avatar(self):
        avatar_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if avatar_path:
            self.avatar_image = Image.open(avatar_path).resize((150, 150), Image.Resampling.LANCZOS)
            self.avatar_photo = ImageTk.PhotoImage(self.avatar_image)
            self.avatar_button.config(image=self.avatar_photo, text="")

    def create_account(self):
        nickname = self.name_entry.get()
        if nickname and self.avatar_image:
            avatar_bytes = io.BytesIO()
            self.avatar_image.save(avatar_bytes, format="PNG")
            avatar_blob = avatar_bytes.getvalue()

            self.cursor.execute("INSERT INTO users (nickname, image) VALUES (?, ?)", (nickname, avatar_blob))
            self.conn.commit()
            self.conn.close()

            self.root.destroy()
            self.login_window.root.deiconify()
            self.login_window.reset_ui()

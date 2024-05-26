import io
import tkinter as tk
from tkinter import ttk, PhotoImage, filedialog, messagebox
from main import BaseWindow
from styles import StyledCanvas, StyledButton, PlacedStyledButton
import sqlite3
from PIL import Image, ImageTk

class DictionaryWindow(BaseWindow):
    def __init__(self, root, main_root, current_user):
        super().__init__(root, main_root, current_user)
        self.root.title("Программа обучения английскому языку - Словарь")
        self.current_user = current_user

        # Создаем кастомный Canvas для фона
        self.canvas = StyledCanvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_dictionary()

    def start_dictionary(self):
        # Подключение к базе данных
        conn = self.connect_db()

        self.default_image = PhotoImage(file='db_operator/src/button.png')

        # Текстовое поле для ввода английского слова
        self.canvas.create_text(50, 50, text="Введите слово на английском:", font=("Helvetica", 16), fill="black", anchor="nw")
        self.entry = ttk.Entry(self.canvas, font=('Arial', 24))
        self.canvas.create_window(50, 80, window=self.entry, anchor="nw")
        self.entry.bind('<KeyRelease>', self.on_key_release)

        # Текстовое поле для ввода русского слова
        self.canvas.create_text(50, 130, text="Введите слово на русском:", font=("Helvetica", 16), fill="black", anchor="nw")
        self.russian_entry = ttk.Entry(self.canvas, font=('Arial', 24), state='readonly')
        self.canvas.create_window(50, 160, window=self.russian_entry, anchor="nw")

        # Метка для отображения изображения
        self.image_label = tk.Label(self.canvas, borderwidth=2, relief="solid", width=250, height=250, background="lightgrey")
        self.canvas.create_window(110, 220, window=self.image_label, anchor="nw")
        self.image_label.bind('<Button-1>', self.on_image_click)
        self.image_label.config(image=self.default_image)
        self.image_label.image = self.default_image

        # Кнопка для сохранения слова
        self.save_button = ttk.Button(self.canvas, text="Сохранить", state='disabled', command=self.on_save, width=40)
        self.canvas.create_window(110, 480, window=self.save_button, anchor="nw")

        # Фрейм для списка тем
        self.topics_frame = tk.Frame(self.canvas, bg='white', width=400)
        self.canvas.create_window(500, 50, window=self.topics_frame, anchor="nw")

        # Загрузка тем из базы данных
        self.topic_vars = {}
        self.checkboxes = {}
        topics = self.get_topics(conn)
        for idx, (topic_id, topic_name) in enumerate(topics):
            var = tk.IntVar()
            chk = ttk.Checkbutton(self.topics_frame, text=topic_name, variable=var, state="disabled")
            chk.grid(row=idx + 1, column=0, sticky='w', pady=2)
            self.topic_vars[topic_id] = var
            self.checkboxes[topic_id] = chk

        # Поле для ввода новой темы и кнопка добавления темы
        self.new_topic_entry = ttk.Entry(self.topics_frame, font=('Arial', 14), state='disabled')
        self.new_topic_entry.grid(row=len(topics) + 1, column=0, pady=10, sticky='ew')
        self.add_topic_button = ttk.Button(self.topics_frame, text="Добавить тему", state='disabled', command=self.on_add_topic)
        self.add_topic_button.grid(row=len(topics) + 2, column=0, pady=10)

        # Создаем навигационные кнопки
        self.back_button = StyledButton(self.canvas, 160, 540, text="Назад", command=self.go_back_main, width=100, height=40)
        self.exit_button = StyledButton(self.canvas, 310, 540, text="Выход", command=self.exit_program, width=100, height=40)

    def go_back_main(self):
        from main_window import MainWindow
        self.go_back(MainWindow)

    def connect_db(self):
        # Подключение к базе данных SQLite
        conn = sqlite3.connect('team_app.db')
        return conn

    def get_topics(self, conn):
        # Получение списка тем из базы данных
        cursor = conn.cursor()
        cursor.execute('SELECT topic_id, topic_name FROM topics')
        return cursor.fetchall()

    def search_word(self, conn, prefix):
        # Поиск слова в базе данных по префиксу
        cursor = conn.cursor()
        cursor.execute('''
            SELECT english, russian, picture, word_id 
            FROM words 
            WHERE english LIKE ? 
            LIMIT 1
        ''', (prefix + '%',))
        result = cursor.fetchone()
        return result if result else (None, None, None, None)

    def get_word_topics(self, conn, word_id):
        # Получение списка тем, к которым относится слово
        cursor = conn.cursor()
        cursor.execute('''
            SELECT topic_id 
            FROM words_groupings 
            WHERE word_id = ?
        ''', (word_id,))
        return [row[0] for row in cursor.fetchall()]

    def insert_word(self, conn, english, russian, picture):
        # Вставка нового слова в базу данных
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO words (english, russian, picture) VALUES (?, ?, ?)
        ''', (english, russian, picture))
        conn.commit()
        return cursor.lastrowid

    def insert_word_groupings(self, conn, word_id, topic_id):
        # Вставка записи в таблицу связей слова и темы
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO words_groupings (word_id, topic_id) VALUES (?, ?)
        ''', (word_id, topic_id))
        conn.commit()

    def insert_topic(self, conn, topic_name):
        # Вставка новой темы в базу данных
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO topics (topic_name) VALUES (?)
        ''', (topic_name,))
        conn.commit()
        return cursor.lastrowid

    def on_key_release(self, event):
        # Обработка события нажатия клавиши
        conn = self.connect_db()
        prefix = self.entry.get()
        if prefix and event.keysym not in ('BackSpace', 'Delete', 'Left', 'Right'):
            english_word, russian_word, picture, word_id = self.search_word(conn, prefix)
            if english_word:
                self.display_word(prefix, english_word, russian_word, picture)
                self.mark_word_topics(conn, word_id)
                self.save_button.config(state='disabled')
                self.russian_entry.config(state='readonly')
                self.disable_topic_selection()
            else:
                self.russian_entry.config(state='normal')
                self.russian_entry.delete(0, tk.END)
                self.image_label.config(image=self.default_image)
                self.save_button.config(state='normal')
                self.unmark_all_topics()
                self.enable_topic_selection()
        elif not prefix:
            self.entry.delete(0, tk.END)
            self.russian_entry.config(state='normal')
            self.russian_entry.delete(0, tk.END)
            self.russian_entry.config(state='readonly')
            self.image_label.config(image=self.default_image)
            self.save_button.config(state='disabled')
            self.unmark_all_topics()
            self.disable_topic_selection()

    def display_word(self, prefix, english_word, russian_word, picture):
        # Отображение найденного слова и его данных
        self.entry.delete(0, tk.END)
        self.entry.insert(0, english_word)
        self.entry.select_range(len(prefix), tk.END)
        self.entry.icursor(len(prefix))
        self.russian_entry.config(state='normal')
        self.russian_entry.delete(0, tk.END)
        if russian_word:
            self.russian_entry.insert(0, russian_word)
        self.russian_entry.config(state='readonly')
        if picture:
            image = ImageTk.PhotoImage(Image.open(io.BytesIO(picture)).resize((300, 300), Image.LANCZOS))
            self.image_label.config(image=image)
            self.image_label.image = image
        else:
            self.image_label.config(image=self.default_image)
            self.image_label.image = self.default_image

    def mark_word_topics(self, conn, word_id):
        # Отметка тем, к которым относится найденное слово
        word_topics = self.get_word_topics(conn, word_id)
        for topic_id, var in self.topic_vars.items():
            if topic_id in word_topics:
                var.set(1)
            else:
                var.set(0)

    def unmark_all_topics(self):
        # Сброс всех отметок тем
        for var in self.topic_vars.values():
            var.set(0)

    def enable_topic_selection(self):
        # Включение возможности выбора тем
        for chk in self.checkboxes.values():
            chk.config(state='normal')
        self.new_topic_entry.config(state='normal')
        self.add_topic_button.config(state='normal')

    def disable_topic_selection(self):
        # Отключение возможности выбора тем
        for chk in self.checkboxes.values():
            chk.config(state='disabled')
        self.new_topic_entry.config(state='disabled')
        self.add_topic_button.config(state='disabled')

    def on_save(self):
        # Обработка события сохранения слова
        conn = self.connect_db()
        english_word = self.entry.get()
        russian_word = self.russian_entry.get()
        if english_word and russian_word:
            picture = getattr(self.image_label, 'image_data', None)
            word_id = self.insert_word(conn, english_word, russian_word, picture)
            selected_topics = [topic_id for topic_id, var in self.topic_vars.items() if var.get() == 1]
            for topic_id in selected_topics:
                self.insert_word_groupings(conn, word_id, topic_id)
            self.save_button.config(state='disabled')
            self.russian_entry.config(state='readonly')
            self.disable_topic_selection()
            self.new_topic_entry.delete(0, tk.END)
            self.unmark_all_topics()
        else:
            messagebox.showinfo("Ошибка", "Пожалуйста, введите слова на английском и русском языках.")

    def on_image_click(self, event):
        # Обработка события выбора изображения
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            with open(file_path, 'rb') as image_file:
                image_data = image_file.read()
            original_image = Image.open(file_path)
            resized_image = original_image.resize((250, 250), Image.LANCZOS)
            image = ImageTk.PhotoImage(resized_image)
            self.image_label.config(image=image)
            self.image_label.image = image
            self.image_label.image_data = image_data  # Сохраняем исходные данные изображения
            self.save_button.config(state='normal')

    def on_add_topic(self):
        # Обработка события добавления новой темы
        conn = self.connect_db()
        new_topic_name = self.new_topic_entry.get()
        if new_topic_name:
            topic_id = self.insert_topic(conn, new_topic_name)
            var = tk.IntVar()
            chk = ttk.Checkbutton(self.topics_frame, text=new_topic_name, variable=var, state="normal")
            chk.grid(row=len(self.topic_vars) + 1, column=0, sticky='w', pady=2)
            self.topic_vars[topic_id] = var
            self.checkboxes[topic_id] = chk
            self.new_topic_entry.delete(0, tk.END)

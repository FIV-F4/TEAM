import tkinter as tk
from tkinter import ttk, PhotoImage, filedialog
from main import BaseWindow
from styles import StyledCanvas, StyledButton
import sqlite3

class DictionaryWindow(BaseWindow):
    def __init__(self, root, main_root, current_user):
        super().__init__(root, main_root, current_user)
        self.root.title("Программа обучения английскому языку - Словарь")

        self.current_user = current_user

        self.start_dictionary()

    def start_dictionary(self):
        conn = self.connect_db()

        self.default_image = PhotoImage(file='db_operator/src/button.png')

        # Используем grid для всего окна
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        main_frame = tk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky='nsew')
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)

        self.entry = ttk.Entry(main_frame, font=('Arial', 24))
        self.entry.grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky='ew')
        self.entry.bind('<KeyRelease>', self.on_key_release)

        self.russian_entry = ttk.Entry(main_frame, font=('Arial', 24), state='readonly')
        self.russian_entry.grid(row=1, column=0, columnspan=2, pady=20, padx=20, sticky='ew')

        self.image_label = tk.Label(main_frame, borderwidth=2, relief="solid", width=300, height=300, background="lightgrey")
        self.image_label.grid(row=2, column=0, columnspan=2, pady=(20, 0), padx=20, sticky='n')
        self.image_label.bind('<Button-1>', self.on_image_click)
        self.image_label.config(image=self.default_image)
        self.image_label.image = self.default_image

        self.save_button = ttk.Button(main_frame, text="Сохранить", state='disabled', command=self.on_save)
        self.save_button.grid(row=3, column=0, columnspan=2, pady=20, padx=20)

        self.topics_frame = ttk.Frame(main_frame)
        self.topics_frame.grid(row=0, column=2, rowspan=4, padx=20, pady=20, sticky='ns')

        self.topic_vars = {}
        self.checkboxes = {}
        topics = self.get_topics(conn)
        for idx, (topic_id, topic_name) in enumerate(topics):
            var = tk.IntVar()
            chk = ttk.Checkbutton(self.topics_frame, text=topic_name, variable=var, state="disabled")
            chk.grid(row=idx+1, column=0, sticky='w', pady=2)
            self.topic_vars[topic_id] = var
            self.checkboxes[topic_id] = chk

        # New topic entry and button
        self.new_topic_entry = ttk.Entry(self.topics_frame, font=('Arial', 14), state='disabled')
        self.new_topic_entry.grid(row=len(topics)+1, column=0, pady=10, sticky='ew')
        self.add_topic_button = ttk.Button(self.topics_frame, text="Добавить тему", state='disabled', command=self.on_add_topic)
        self.add_topic_button.grid(row=len(topics)+2, column=0, pady=10)

    def connect_db(self):
        conn = sqlite3.connect('team_app.db')
        return conn

    def get_topics(self, conn):
        cursor = conn.cursor()
        cursor.execute('SELECT topic_id, topic_name FROM topics')
        return cursor.fetchall()

    def search_word(self, conn, prefix):
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
        cursor = conn.cursor()
        cursor.execute('''
            SELECT topic_id 
            FROM words_groupings 
            WHERE word_id = ?
        ''', (word_id,))
        return [row[0] for row in cursor.fetchall()]

    def insert_word(self, conn, english, russian, picture):
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO words (english, russian, picture) VALUES (?, ?, ?)
        ''', (english, russian, picture))
        conn.commit()
        return cursor.lastrowid

    def insert_word_groupings(self, conn, word_id, topic_id):
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO words_groupings (word_id, topic_id) VALUES (?, ?)
        ''', (word_id, topic_id))
        conn.commit()

    def insert_topic(self, conn, topic_name):
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO topics (topic_name) VALUES (?)
        ''', (topic_name,))
        conn.commit()
        return cursor.lastrowid

    def on_key_release(self, event):
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
            image = PhotoImage(data=picture)
            self.image_label.config(image=image)
            self.image_label.image = image
        else:
            self.image_label.config(image=self.default_image)
            self.image_label.image = self.default_image

    def mark_word_topics(self, conn, word_id):
        word_topics = self.get_word_topics(conn, word_id)
        for topic_id, var in self.topic_vars.items():
            if topic_id in word_topics:
                var.set(1)
            else:
                var.set(0)

    def unmark_all_topics(self):
        for var in self.topic_vars.values():
            var.set(0)

    def enable_topic_selection(self):
        for chk in self.checkboxes.values():
            chk.config(state='normal')
        self.new_topic_entry.config(state='normal')
        self.add_topic_button.config(state='normal')

    def disable_topic_selection(self):
        for chk in self.checkboxes.values():
            chk.config(state='disabled')
        self.new_topic_entry.config(state='disabled')
        self.add_topic_button.config(state='disabled')

    def on_save(self):
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

    def on_image_click(self, event):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
        if file_path:
            with open(file_path, 'rb') as image_file:
                image_data = image_file.read()
            image = PhotoImage(data=image_data)
            self.image_label.config(image=image)
            self.image_label.image = image
            self.image_label.image_data = image_data
            self.save_button.config(state='normal')

    def on_add_topic(self):
        conn = self.connect_db()
        new_topic_name = self.new_topic_entry.get()
        if new_topic_name:
            topic_id = self.insert_topic(conn, new_topic_name)
            var = tk.IntVar()
            chk = ttk.Checkbutton(self.topics_frame, text=new_topic_name, variable=var, state="normal")
            chk.grid(row=len(self.topic_vars)+1, column=0, sticky='w', pady=2)
            self.topic_vars[topic_id] = var
            self.checkboxes[topic_id] = chk
            self.new_topic_entry.delete(0, tk.END)


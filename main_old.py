import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import sqlite3
import random
import io
import pygame
import os

# Глобальная переменная для активного пользователя
ACTIVE_USER = {}

# Функция для загрузки активного пользователя
def load_active_user():
    global ACTIVE_USER
    try:
        with sqlite3.connect("team_app.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT nickname, image FROM users LIMIT 1")
            user = cursor.fetchone()
            if user:
                ACTIVE_USER['nickname'] = user[0]
                ACTIVE_USER['image'] = user[1] if user[1] else None
            else:
                ACTIVE_USER['nickname'] = 'Unknown'
                ACTIVE_USER['image'] = None
    except sqlite3.Error as e:
        messagebox.showerror("Ошибка базы данных", f"Не удалось загрузить пользователя: {e}")

# Загрузка активного пользователя при старте программы
load_active_user()

class TopicSelectionScreen:
    def __init__(self, master, on_topic_selected, on_test_selected, on_start_test):
        self.master = master
        self.on_topic_selected = on_topic_selected
        self.on_test_selected = on_test_selected
        self.on_start_test = on_start_test
        self.selected_topic = None
        self.selected_test = None
        self.topic_buttons = {}
        self.test_buttons = {}
        self.setup_ui()

    def setup_ui(self):
        self.clear_window()
        self.master.geometry('800x600')
        self.master.configure(bg='#f0f0f0')
        self.master.title("Выбор темы урока")

        self.top_frame = tk.Frame(self.master, height=50, bg='white')
        self.top_frame.pack(fill=tk.X)

        self.user_image_label = tk.Label(self.top_frame, bg='white')
        self.user_image_label.place(x=10, y=5)
        self.show_user_info()

        self.title_label = tk.Label(self.top_frame, text="Выберите тему урока", font=('Helvetica', 24, 'bold'), bg='white')
        self.title_label.pack(pady=10)

        self.topic_frame = tk.Frame(self.master, bg='#f0f0f0')
        self.topic_frame.pack(side=tk.LEFT, padx=20, pady=20, anchor=tk.N)

        topics = self.load_topics()
        for topic in topics:
            topic_button = tk.Button(self.topic_frame, text=topic[1], font=('Helvetica', 18),
                                     command=lambda t=topic: self.select_topic(t), width=25, relief=tk.RAISED)
            topic_button.pack(pady=5)
            self.topic_buttons[topic[0]] = topic_button

        self.test_frame = tk.Frame(self.master, bg='#f0f0f0')
        self.test_frame.pack(side=tk.RIGHT, padx=20, pady=20, anchor=tk.N)

        tests = self.load_tests()
        for test in tests:
            test_button = tk.Button(self.test_frame, text=test[1], font=('Helvetica', 18),
                                    command=lambda t=test: self.select_test(t), width=25, relief=tk.RAISED)
            test_button.pack(pady=5)
            self.test_buttons[test[0]] = test_button

        self.start_button = tk.Button(self.master, text="Начать тестирование", command=self.start_test, font=('Helvetica', 14))
        self.start_button.place(relx=0.5, rely=0.95, anchor=tk.S)

        self.exit_button = tk.Button(self.master, text="Выход", command=self.master.quit, font=('Helvetica', 12))
        self.exit_button.place(x=750, y=550, anchor=tk.SE)

    def show_user_info(self):
        global ACTIVE_USER
        nickname = ACTIVE_USER.get('nickname', 'Unknown')
        image_data = ACTIVE_USER.get('image')

        if image_data:
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((40, 40))
            photo = ImageTk.PhotoImage(image)
        else:
            # Создаем черный квадрат, если изображение отсутствует
            image = Image.new('RGB', (40, 40), color='black')
            photo = ImageTk.PhotoImage(image)

        self.user_image_label.configure(image=photo)
        self.user_image_label.image = photo

        self.user_name_label = tk.Label(self.top_frame, text=nickname, font=('Helvetica', 16), bg='white')
        self.user_name_label.place(x=60, y=10)

    def load_topics(self):
        topics = []
        try:
            with sqlite3.connect("team_app.db") as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT topic_id, topic_name FROM topics")
                topics = cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось загрузить темы: {e}")
        return topics

    def load_tests(self):
        tests = []
        try:
            with sqlite3.connect("team_app.db") as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT test_id, test_name FROM tests")
                tests = cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось загрузить тесты: {e}")
        return tests

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def select_topic(self, topic):
        self.selected_topic = topic
        self.on_topic_selected(topic)
        for btn in self.topic_buttons.values():
            btn.config(relief=tk.RAISED, bg='#f0f0f0')
        self.topic_buttons[topic[0]].config(relief=tk.SUNKEN, bg='#d3d3d3')

    def select_test(self, test):
        self.selected_test = test
        self.on_test_selected(test)
        for btn in self.test_buttons.values():
            btn.config(relief=tk.RAISED, bg='#f0f0f0')
        self.test_buttons[test[0]].config(relief=tk.SUNKEN, bg='#d3d3d3')

    def start_test(self):
        if self.selected_topic and self.selected_test:
            self.on_start_test()
        else:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите тему и тест.")

class WordLearningApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry('800x600')
        self.master.minsize(800, 600)
        self.master.maxsize(800, 600)
        self.master.configure(bg='#f0f0f0')

        pygame.mixer.init()

        self.topic_name = ""
        self.topic_id = None
        self.test_name = ""
        self.test_id = None
        self.words = []
        self.score = 0
        self.current_word_index = 0

        self.topic_selection_screen = TopicSelectionScreen(self.master, self.select_topic, self.select_test, self.start_test)

    def select_topic(self, topic):
        self.topic_id = topic[0]
        self.topic_name = topic[1]

    def select_test(self, test):
        self.test_id = test[0]
        self.test_name = test[1]

    def start_test(self):
        if not (self.topic_id and self.test_id):
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите тему и тест.")
            return

        self.words = self.load_words(self.topic_id)
        if not self.words:
            messagebox.showerror("Ошибка", "Слова для выбранной темы не найдены.")
            return

        random.shuffle(self.words)
        self.words = self.words[:8]  # Ограничиваем количество слов до 8
        self.show_learning_screen()

    def load_words(self, topic_id):
        words = []
        try:
            with sqlite3.connect("team_app.db") as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT w.english, w.russian, w.picture, w.sound
                    FROM words w
                    JOIN words_groupings wg ON w.word_id = wg.word_id
                    JOIN topics t ON wg.topic_id = t.topic_id
                    WHERE t.topic_id = ?
                """, (topic_id,))
                words = cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось загрузить слова: {e}")
        return words

    def show_learning_screen(self):
        self.clear_window()
        self.master.title(f"Тема: {self.topic_name}")

        self.top_frame = tk.Frame(self.master, height=50, bg='white')
        self.top_frame.pack(fill=tk.X)

        self.user_image_label = tk.Label(self.top_frame, bg='white')
        self.user_image_label.place(x=10, y=5)
        self.show_user_info()

        self.topic_label = tk.Label(self.top_frame, text=f"Тема: {self.topic_name}", font=('Helvetica', 20, 'bold'),
                                    bg='white')
        self.topic_label.pack(pady=10)

        self.image_label = tk.Label(self.master)
        self.image_label.pack(pady=10)

        self.progress_frame = tk.Frame(self.master)
        self.progress_frame.pack(pady=10)
        self.create_progress_bar()

        self.word_label = tk.Label(self.master, font=('Helvetica', 24, 'bold'))
        self.word_label.pack(pady=10)

        self.prev_button = tk.Button(self.master, text="Предыдущее слово", command=self.prev_word, font=('Helvetica', 12))
        self.prev_button.place(x=10, y=350, anchor=tk.W)

        self.next_button = tk.Button(self.master, text="Следующее слово", command=self.next_word, font=('Helvetica', 12))
        self.next_button.place(x=790, y=350, anchor=tk.E)

        self.buttons_frame = tk.Frame(self.master)
        self.buttons_frame.pack(pady=10)

        self.message_label = tk.Label(self.master, font=('Helvetica', 16, 'bold'))  # Уменьшен шрифт
        self.message_label.pack(pady=10)

        self.score_label = tk.Label(self.master, text=f"Баллы: {self.score}/8", font=('Helvetica', 14))
        self.score_label.place(x=790, y=60, anchor=tk.NE)

        self.exit_button = tk.Button(self.master, text="Выход", command=self.master.quit, font=('Helvetica', 12))
        self.exit_button.place(x=790, y=590, anchor=tk.SE)

        self.back_button = tk.Button(self.master, text="Вернуться", command=self.return_to_selection, font=('Helvetica', 12))
        self.back_button.place(x=10, y=590, anchor=tk.SW)

        self.show_word()

    def return_to_selection(self):
        self.clear_window()
        self.topic_id = None
        self.topic_name = ""
        self.test_id = None
        self.test_name = ""
        self.words = []
        self.score = 0
        self.current_word_index = 0
        self.topic_selection_screen.selected_topic = None
        self.topic_selection_screen.selected_test = None
        self.topic_selection_screen.setup_ui()

    def show_user_info(self):
        global ACTIVE_USER
        nickname = ACTIVE_USER.get('nickname', 'Unknown')
        image_data = ACTIVE_USER.get('image')

        if image_data:
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((40, 40))
            photo = ImageTk.PhotoImage(image)
        else:
            # Создаем черный квадрат, если изображение отсутствует
            image = Image.new('RGB', (40, 40), color='black')
            photo = ImageTk.PhotoImage(image)

        self.user_image_label.configure(image=photo)
        self.user_image_label.image = photo

        self.user_name_label = tk.Label(self.top_frame, text=nickname, font=('Helvetica', 16), bg='white')
        self.user_name_label.place(x=60, y=10)

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def create_progress_bar(self):
        self.progress_canvas = tk.Canvas(self.progress_frame, width=240, height=20)
        self.progress_canvas.pack()
        self.progress_segments = []
        for i in range(8):
            segment = self.progress_canvas.create_oval(i * 30, 0, (i + 1) * 30 - 10, 20, fill="gray")
            self.progress_segments.append(segment)

    def update_progress(self, correct):
        color = "green" if correct else "red"
        self.progress_canvas.itemconfig(self.progress_segments[self.current_word_index], fill=color)

    def show_word(self):
        self.message_label.config(text="")
        if self.words:
            english, russian, picture_data, sound_data = self.words[self.current_word_index]
            image = Image.open(io.BytesIO(picture_data))
            image = image.resize((256, 256))
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo
            self.word_label.config(text=russian)

            for widget in self.buttons_frame.winfo_children():
                widget.destroy()
            correct_button = random.randint(0, 5)
            used_translations = [english]
            for i in range(6):
                if i == correct_button:
                    btn_text = english
                else:
                    while True:
                        random_word = random.choice(self.words)[0]
                        if random_word not in used_translations:
                            btn_text = random_word
                            used_translations.append(random_word)
                            break
                btn = tk.Button(self.buttons_frame, text=btn_text, font=('Helvetica', 12),
                                command=lambda b=btn_text, s=sound_data: self.check_answer(b, english, s))
                btn.pack(side=tk.LEFT, padx=5)

    def check_answer(self, chosen, correct, sound_data):
        for btn in self.buttons_frame.winfo_children():
            btn.config(state=tk.DISABLED)

        if chosen == correct:
            self.score += 1
            self.message_label.config(text="Правильно!", fg='green')
            self.play_sound(sound_data)
            self.update_progress(True)
        else:
            self.message_label.config(text="Неправильно!", fg='red')
            self.update_progress(False)
        self.score_label.config(text=f"Баллы: {self.score}/8")

    def next_word(self):
        if self.current_word_index < len(self.words) - 1:
            self.current_word_index += 1
            self.show_word()
        else:
            self.message_label.config(text=f"Тест окончен! Ваши баллы: {self.score}/8", fg='black')

    def prev_word(self):
        if self.current_word_index > 0:
            self.current_word_index -= 1
            self.show_word()

    def play_sound(self, sound_data):
        try:
            with open("temp_sound.mp3", "wb") as f:
                f.write(sound_data)
            pygame.mixer.music.load("temp_sound.mp3")
            pygame.mixer.music.play()
            # Удаляем файл после окончания воспроизведения звука
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            self.master.bind("<Destroy>", self.cleanup_temp_file)
            self.master.after(100, self.check_music_end)
        except Exception as e:
            messagebox.showerror("Ошибка воспроизведения звука", f"Не удалось воспроизвести звук: {e}")

    def check_music_end(self):
        if not pygame.mixer.music.get_busy():
            self.cleanup_temp_file()
        else:
            self.master.after(100, self.check_music_end)

    def cleanup_temp_file(self, event=None):
        try:
            if os.path.exists("temp_sound.mp3"):
                os.remove("temp_sound.mp3")
        except Exception as e:
            print(f"Ошибка при удалении временного файла: {e}")

root = tk.Tk()
app = WordLearningApp(root)
root.mainloop()

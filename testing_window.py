import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import random
import io
import pygame
import speech_recognition as sr
from main import BaseWindow
from styles import StyledCanvas, StyledButton, TransparentLabel

# Глобальная переменная для активного пользователя
ACTIVE_USER = {}


# Функция для загрузки активного пользователя
def load_active_user():
    global ACTIVE_USER
    try:
        with sqlite3.connect("team_app.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT user_id, nickname, image FROM users LIMIT 1")
            user = cursor.fetchone()
            if user:
                ACTIVE_USER['user_id'] = user[0]
                ACTIVE_USER['nickname'] = user[1]
                ACTIVE_USER['image'] = user[2] if user[2] else None
            else:
                ACTIVE_USER = {'user_id': None, 'nickname': 'Unknown', 'image': None}
    except sqlite3.Error as e:
        messagebox.showerror("Ошибка базы данных", f"Не удалось загрузить пользователя: {e}")


# Загрузка активного пользователя при старте программы
load_active_user()
pygame.mixer.init()  # Инициализация pygame.mixer


class BaseLessonScreen(BaseWindow):
    def __init__(self, root, main_root, current_user, topic, test):
        super().__init__(root, main_root, current_user)
        self.topic = topic
        self.test = test
        self.score = 0
        self.current_word_index = 0
        self.words = []
        self.main_root = main_root  # Сохраняем ссылку на главное окно тестирования
        self.setup_ui()

    def setup_ui(self):
        self.clear_window()
        self.canvas = StyledCanvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        self.canvas.create_text(400, 50, text=f"Тема: {self.topic[1]}", font=('Helvetica', 24, 'bold'), fill='black')

        # Индикация пользователя
        self.user_image_label = tk.Label(self.canvas, bg='white')
        self.canvas.create_window(50, 50, window=self.user_image_label, anchor="nw")
        self.show_user_info()

        # Баллы
        self.score_label = TransparentLabel(self.canvas, 700, 70, text=f"Баллы: {self.score}/8", font=('Helvetica', 14),
                                            fill='black')

        # Прогресс бар
        self.progress_frame = tk.Frame(self.canvas)
        self.canvas.create_window(400, 500, window=self.progress_frame, anchor="center")
        self.create_progress_bar()

        # Изображение
        self.image_label = tk.Label(self.canvas)
        self.canvas.create_window(400, 200, window=self.image_label, anchor="center")

        # Слово (наложено на изображение)
        self.word_label = TransparentLabel(self.canvas, 400, 550, font=('Helvetica', 24, 'bold'), fill='red')

        # Кнопки
        self.buttons_frame = tk.Frame(self.canvas)
        self.canvas.create_window(400, 390, window=self.buttons_frame, anchor="center")

        # Сообщение
        self.message_label = TransparentLabel(self.canvas, 400, 460, text="", font=('Helvetica', 16, 'bold'),
                                              fill='white')

        # Навигационные кнопки
        self.prev_button = StyledButton(self.canvas, 150, 500, text="Предыдущее слово", command=self.prev_word,
                                        width=200, height=40)
        self.next_button = StyledButton(self.canvas, 650, 500, text="Следующее слово", command=self.next_word,
                                        width=200, height=40)
        self.exit_button = StyledButton(self.canvas, 700, 550, text="Выход", command=self.exit_program, width=100,
                                        height=40)
        self.back_button = StyledButton(self.canvas, 100, 550, text="Назад", command=self.return_to_test_selection,
                                        width=100, height=40)

    def return_to_test_selection(self):
        self.root.destroy()  # Закрываем текущее окно урока
        self.main_root.deiconify()  # Возвращаем главное окно тестирования

    def show_user_info(self):
        global ACTIVE_USER
        nickname = ACTIVE_USER.get('nickname', 'Unknown')
        image_data = ACTIVE_USER.get('image')

        if image_data:
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((40, 40))
            photo = ImageTk.PhotoImage(image)
        else:
            image = Image.new('RGB', (40, 40), color='black')
            photo = ImageTk.PhotoImage(image)

        self.user_image_label.configure(image=photo)
        self.user_image_label.image = photo

        # Никнейм пользователя
        self.user_name_label = TransparentLabel(self.canvas, 150, 70, text=nickname, font=('Helvetica', 16),
                                                fill='black')

    def create_progress_bar(self):
        self.progress_canvas = tk.Canvas(self.progress_frame, width=240, height=20, bg='lightgray')
        self.progress_canvas.pack(padx=10, pady=10)
        self.progress_segments = []
        for i in range(8):
            segment = self.progress_canvas.create_oval(i * 30 + 5, 5, (i + 1) * 30 - 10, 20, fill="gray")
            self.progress_segments.append(segment)

    def update_progress(self, correct):
        color = "green" if correct else "red"
        self.progress_canvas.itemconfig(self.progress_segments[self.current_word_index], fill=color)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def return_to_main_testing_window(self):
        self.root.destroy()
        self.main_root.deiconify()

    def prev_word(self):
        pass

    def next_word(self):
        pass

    def check_answer(self, chosen, correct, sound_data):
        for btn in self.buttons_frame.winfo_children():
            btn.config(state=tk.DISABLED)

        if chosen == correct:
            self.score += 1
            self.message_label.update_text("Правильно!")
            self.message_label.set_fill('green')
            self.play_sound(sound_data)
            self.update_progress(True)
        else:
            self.message_label.update_text("Неправильно!")
            self.message_label.set_fill('red')
            self.update_progress(False)
        self.score_label.update_text(f"Баллы: {self.score}/8")

        if self.current_word_index == len(self.words) - 1:
            self.end_test()
        else:
            self.next_button.set_command(self.next_word)

    def show_word(self):
        pass

    def play_sound(self, sound_data):
        try:
            sound = io.BytesIO(sound_data)
            pygame.mixer.music.load(sound)
            pygame.mixer.music.play()
        except Exception as e:
            messagebox.showerror("Ошибка воспроизведения звука", f"Не удалось воспроизвести звук: {e}")

    def save_test_result(self):
        global ACTIVE_USER
        try:
            with sqlite3.connect("team_app.db") as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO testing_stats (user_id, test_id, testing_counter)
                    VALUES (?, ?, ?)
                """, (ACTIVE_USER['user_id'], self.test[0], self.score))
                connection.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось сохранить результаты теста: {e}")


class WordLessonScreen(BaseLessonScreen):
    def __init__(self, root, main_root, current_user, topic, test):
        super().__init__(root, main_root, current_user, topic, test)
        self.all_words = []
        self.load_words()
        self.show_word()

    def load_words(self):
        try:
            with sqlite3.connect("team_app.db") as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT w.english, w.russian, w.picture, w.sound
                    FROM words w
                    JOIN words_groupings wg ON w.word_id = wg.word_id
                    JOIN topics t ON wg.topic_id = t.topic_id
                    WHERE t.topic_id = ?
                """, (self.topic[0],))
                self.all_words = cursor.fetchall()
                self.words = random.sample(self.all_words, 8)
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось загрузить слова: {e}")

    def show_word(self):
        self.message_label.update_text("")
        if self.words:
            english, russian, picture_data, sound_data = self.words[self.current_word_index]
            image = Image.open(io.BytesIO(picture_data))
            image = image.resize((256, 256))
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo
            self.word_label.update_text(russian)

            for widget in self.buttons_frame.winfo_children():
                widget.destroy()

            all_words = [word[0] for word in self.all_words if word[0] != english]
            random_words = random.sample(all_words, 5)
            random_words.append(english)
            random.shuffle(random_words)

            for btn_text in random_words:
                btn = tk.Button(self.buttons_frame, text=btn_text, font=('Helvetica', 12),
                                command=lambda b=btn_text, s=sound_data: self.check_answer(b, english, s))
                btn.pack(side=tk.LEFT, padx=5)

    def check_answer(self, chosen, correct, sound_data):
        for btn in self.buttons_frame.winfo_children():
            btn.config(state=tk.DISABLED)

        if chosen == correct:
            self.score += 1
            self.message_label.update_text("Правильно!")
            self.message_label.set_fill('green')
            self.play_sound(sound_data)
            self.update_progress(True)
        else:
            self.message_label.update_text("Неправильно!")
            self.message_label.set_fill('red')
            self.update_progress(False)
        self.score_label.update_text(f"Баллы: {self.score}/8")

        if self.current_word_index == len(self.words) - 1:
            self.end_test()
        else:
            self.next_button.enable()

    def next_word(self):
        if self.current_word_index < len(self.words) - 1:
            self.current_word_index += 1
            self.show_word()

    def prev_word(self):
        if self.current_word_index > 0:
            self.current_word_index -= 1
            self.show_word()

    def end_test(self):
        self.message_label.update_text(f"Тест окончен! Ваши баллы: {self.score}/8")
        self.message_label.set_fill('black')
        for btn in self.buttons_frame.winfo_children():
            btn.config(state=tk.DISABLED)
        self.prev_button.disable()
        self.next_button.disable()
        self.save_test_result()


class WordWriteScreen(BaseLessonScreen):
    def __init__(self, root, main_root, current_user, topic, test):
        super().__init__(root, main_root, current_user, topic, test)
        self.load_words()
        self.show_word()

    def load_words(self):
        try:
            with sqlite3.connect("team_app.db") as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT w.english, w.russian, w.picture, w.sound
                    FROM words w
                    JOIN words_groupings wg ON w.word_id = wg.word_id
                    JOIN topics t ON wg.topic_id = t.topic_id
                    WHERE t.topic_id = ?
                """, (self.topic[0],))
                self.words = cursor.fetchall()
                random.shuffle(self.words)
                self.words = self.words[:8]
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось загрузить слова: {e}")

    def show_word(self):
        self.message_label.update_text("")
        if self.words:
            english, russian, picture_data, sound_data = self.words[self.current_word_index]
            image = Image.open(io.BytesIO(picture_data))
            image = image.resize((256, 256))
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo
            self.word_label.update_text(russian)

            for widget in self.buttons_frame.winfo_children():
                widget.destroy()

            input_label = tk.Label(self.buttons_frame, text="Введите это слово на английском языке:",
                                   font=('Helvetica', 12))
            input_label.pack(pady=5)

            self.input_entry = tk.Entry(self.buttons_frame, font=('Helvetica', 12))
            self.input_entry.pack(pady=5)

            check_button = tk.Button(self.buttons_frame, text="Проверить", font=('Helvetica', 12),
                                     command=lambda s=sound_data: self.check_answer(self.input_entry.get(), english, s))
            check_button.pack(pady=5)

    def check_answer(self, chosen, correct, sound_data):
        if chosen.strip().lower() == correct.lower():
            self.score += 1
            self.message_label.update_text("Правильно!")
            self.message_label.set_fill('green')
            self.play_sound(sound_data)
            self.update_progress(True)
        else:
            self.message_label.update_text("Неправильно!")
            self.message_label.set_fill('red')
            self.update_progress(False)
        self.score_label.update_text(f"Баллы: {self.score}/8")

        self.input_entry.config(state=tk.DISABLED)

        if self.current_word_index == len(self.words) - 1:
            self.end_test()
        else:
            self.next_button.enable()

    def next_word(self):
        if self.current_word_index < len(self.words) - 1:
            self.current_word_index += 1
            self.show_word()

    def prev_word(self):
        if self.current_word_index > 0:
            self.current_word_index -= 1
            self.show_word()

    def end_test(self):
        self.message_label.update_text(f"Тест окончен! Ваши баллы: {self.score}/8")
        self.message_label.set_fill('black')
        self.input_entry.config(state=tk.DISABLED)
        self.prev_button.disable()
        self.next_button.disable()
        self.save_test_result()


class WordAudioScreen(BaseLessonScreen):
    def __init__(self, root, main_root, current_user, topic, test):
        super().__init__(root, main_root, current_user, topic, test)
        self.all_words = []
        self.load_words()
        self.show_word()

    def load_words(self):
        try:
            with sqlite3.connect("team_app.db") as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT w.english, w.russian, w.picture, w.sound
                    FROM words w
                    JOIN words_groupings wg ON w.word_id = wg.word_id
                    JOIN topics t ON wg.topic_id = t.topic_id
                    WHERE t.topic_id = ?
                """, (self.topic[0],))
                self.all_words = cursor.fetchall()
                self.words = random.sample(self.all_words, 8)
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось загрузить слова: {e}")

    def show_word(self):
        self.message_label.update_text("")
        if self.words:
            english, russian, picture_data, sound_data = self.words[self.current_word_index]

            image = Image.new('RGB', (256, 256), color='gray')
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo

            for widget in self.buttons_frame.winfo_children():
                widget.destroy()

            play_audio_button = tk.Button(self.buttons_frame, text="Воспроизвести аудио", font=('Helvetica', 24),
                                          command=lambda s=sound_data: self.play_sound(s))
            play_audio_button.pack(pady=5)

            all_words = [word[1] for word in self.all_words if word[1] != russian]
            random_words = random.sample(all_words, 5)
            random_words.append(russian)
            random.shuffle(random_words)

            for btn_text in random_words:
                btn = tk.Button(self.buttons_frame, text=btn_text, font=('Helvetica', 12),
                                command=lambda b=btn_text: self.check_answer(b, russian, sound_data))
                btn.pack(side=tk.LEFT, padx=5)

    def check_answer(self, chosen, correct, sound_data):
        for btn in self.buttons_frame.winfo_children():
            btn.config(state=tk.DISABLED)

        if chosen == correct:
            self.score += 1
            self.message_label.update_text("Правильно!")
            self.message_label.set_fill('green')
            self.play_sound(sound_data)
            self.update_progress(True)
        else:
            self.message_label.update_text("Неправильно!")
            self.message_label.set_fill('red')
            self.update_progress(False)
        self.score_label.update_text(f"Баллы: {self.score}/8")

        if self.current_word_index == len(self.words) - 1:
            self.end_test()
        else:
            self.next_button.enable()

    def next_word(self):
        if self.current_word_index < len(self.words) - 1:
            self.current_word_index += 1
            self.show_word()

    def prev_word(self):
        if self.current_word_index > 0:
            self.current_word_index -= 1
            self.show_word()

    def end_test(self):
        self.message_label.update_text(f"Тест окончен! Ваши баллы: {self.score}/8")
        self.message_label.set_fill('black')
        for btn in self.buttons_frame.winfo_children():
            btn.config(state=tk.DISABLED)
        self.prev_button.disable()
        self.next_button.disable()
        self.save_test_result()


class WordSpeakScreen(BaseLessonScreen):
    def __init__(self, root, main_root, current_user, topic, test):
        super().__init__(root, main_root, current_user, topic, test)
        self.all_words = []
        self.load_words()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.show_word()

    def load_words(self):
        try:
            with sqlite3.connect("team_app.db") as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT w.english, w.russian, w.picture, w.sound
                    FROM words w
                    JOIN words_groupings wg ON w.word_id = wg.word_id
                    JOIN topics t ON wg.topic_id = t.topic_id
                    WHERE t.topic_id = ?
                """, (self.topic[0],))
                self.all_words = cursor.fetchall()
                self.words = random.sample(self.all_words, 8)
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось загрузить слова: {e}")

    def show_word(self):
        self.message_label.update_text("")
        if self.words:
            english, russian, picture_data, sound_data = self.words[self.current_word_index]
            image = Image.open(io.BytesIO(picture_data))
            image = image.resize((256, 256))
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo
            self.word_label.update_text(russian)

            for widget in self.buttons_frame.winfo_children():
                widget.destroy()

            speak_button = tk.Button(self.buttons_frame, text="Произнесите слово на английском", font=('Helvetica', 12),
                                     command=lambda: self.recognize_speech(english, sound_data))
            speak_button.pack(pady=5)

    def recognize_speech(self, correct_word, sound_data):
        with self.microphone as source:
            audio = self.recognizer.listen(source)

        try:
            recognized_text = self.recognizer.recognize_google(audio, language="en-US").lower()
            self.check_answer(recognized_text, correct_word, sound_data)
        except sr.UnknownValueError:
            self.message_label.update_text("Не удалось распознать речь. Попробуйте еще раз.")
            self.message_label.set_fill('red')

        except sr.RequestError as e:
            messagebox.showerror("Ошибка распознавания", f"Ошибка сервиса распознавания речи: {e}")

    def check_answer(self, chosen, correct, sound_data):
        if chosen.strip().lower() == correct.lower():
            self.score += 1
            self.message_label.update_text("Правильно!")
            self.message_label.set_fill('green')
            self.play_sound(sound_data)
            self.update_progress(True)
        else:
            self.message_label.update_text("Неправильно!")
            self.message_label.set_fill('red')
            self.update_progress(False)
        self.score_label.update_text(f"Баллы: {self.score}/8")

        if self.current_word_index == len(self.words) - 1:
            self.end_test()
        else:
            self.next_button.enable()

    def next_word(self):
        if self.current_word_index < len(self.words) - 1:
            self.current_word_index += 1
            self.show_word()

    def prev_word(self):
        if self.current_word_index > 0:
            self.current_word_index -= 1
            self.show_word()

    def end_test(self):
        self.message_label.update_text(f"Тест окончен! Ваши баллы: {self.score}/8")
        self.message_label.set_fill('black')
        self.next_button.disable()
        self.save_test_result()


class TopicSelectionScreen(BaseWindow):
    def __init__(self, root, main_root, current_user, on_start_test):
        super().__init__(root, main_root, current_user)
        self.on_start_test = on_start_test
        self.selected_topic = None
        self.selected_test = None
        self.topic_buttons = {}
        self.test_buttons = {}
        self.setup_ui()

    def setup_ui(self):
        self.clear_window()
        self.canvas = StyledCanvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        self.canvas.create_text(400, 50, text="Выберите тему урока", font=('Helvetica', 24, 'bold'), fill='black')

        # Фреймы
        self.topic_frame = tk.Frame(self.canvas, bg='#f0f0f0')
        self.canvas.create_window(50, 150, window=self.topic_frame, anchor="nw")

        self.test_frame = tk.Frame(self.canvas, bg='#f0f0f0')
        self.canvas.create_window(380, 150, window=self.test_frame, anchor="nw")

        topics = self.load_topics()
        for topic in topics:
            topic_button = tk.Button(self.topic_frame, text=topic[1], font=('Helvetica', 16),
                                     command=lambda t=topic: self.select_topic(t), width=25, relief=tk.RAISED)
            topic_button.pack(pady=5)
            self.topic_buttons[topic[0]] = topic_button

        tests = self.load_tests()
        for test in tests:
            test_button = tk.Button(self.test_frame, text=test[1], font=('Helvetica', 16),
                                    command=lambda t=test: self.select_test(t), width=30, relief=tk.RAISED)
            test_button.pack(pady=5)
            self.test_buttons[test[0]] = test_button

        self.start_button = StyledButton(self.canvas, 400, 450, text="Начать тестирование", command=self.start_test,
                                         width=200, height=50)
        self.exit_button = StyledButton(self.canvas, 700, 550, text="Выход", command=self.exit_program, width=100,
                                        height=40)
        self.back_button = StyledButton(self.canvas, 100, 550, text="Назад", command=self.return_to_main_menu,
                                        width=100, height=40)

    def show_user_info(self):
        global ACTIVE_USER
        nickname = ACTIVE_USER.get('nickname', 'Unknown')
        image_data = ACTIVE_USER.get('image')

        if image_data:
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((40, 40))
            photo = ImageTk.PhotoImage(image)
        else:
            image = Image.new('RGB', (40, 40), color='black')
            photo = ImageTk.PhotoImage(image)

        self.user_image_label.configure(image=photo)
        self.user_image_label.image = photo

        self.user_name_label = tk.Label(self.canvas, text=nickname, font=('Helvetica', 16), bg='white')
        self.canvas.create_window(100, 50, window=self.user_name_label, anchor="nw")

    def load_topics(self):
        try:
            with sqlite3.connect("team_app.db") as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT topic_id, topic_name FROM topics")
                return cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось загрузить темы: {e}")
            return []

    def load_tests(self):
        try:
            with sqlite3.connect("team_app.db") as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT test_id, test_name, test_type FROM tests")
                return cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось загрузить тесты: {e}")
            return []

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def select_topic(self, topic):
        self.selected_topic = topic
        for btn in self.topic_buttons.values():
            btn.config(relief=tk.RAISED, bg='#f0f0f0')
        self.topic_buttons[topic[0]].config(relief=tk.SUNKEN, bg='#d3d3d3')

    def select_test(self, test):
        self.selected_test = test
        for btn in self.test_buttons.values():
            btn.config(relief=tk.RAISED, bg='#f0f0f0')
        self.test_buttons[test[0]].config(relief=tk.SUNKEN, bg='#d3d3d3')

    def start_test(self):
        if self.selected_topic and self.selected_test:
            self.on_start_test(self.selected_topic, self.selected_test)
        else:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите тему и тест.")

    def return_to_main_menu(self):
        from main_window import MainWindow  # Импортируем здесь, чтобы избежать циклических импортов
        self.go_back(MainWindow)


class MainTestApp:
    def __init__(self, root):
        self.root = root
        self.show_topic_selection_screen()

    def show_topic_selection_screen(self):
        self.topic_selection_screen = TopicSelectionScreen(self.root, self.root, ACTIVE_USER['user_id'],
                                                           self.start_lesson)

    def start_lesson(self, topic, test):
        self.root.withdraw()  # Скрываем главное окно тестирования
        lesson_window = tk.Toplevel(self.root)
        test_type = test[2]
        if test_type == 1:
            WordLessonScreen(lesson_window, self.root, ACTIVE_USER['user_id'], topic, test)
        elif test_type == 2:
            WordWriteScreen(lesson_window, self.root, ACTIVE_USER['user_id'], topic, test)
        elif test_type == 3:
            WordAudioScreen(lesson_window, self.root, ACTIVE_USER['user_id'], topic, test)
        elif test_type == 4:
            WordSpeakScreen(lesson_window, self.root, ACTIVE_USER['user_id'], topic, test)


class TestingWindow(BaseWindow):
    def __init__(self, root, main_root, current_user):
        super().__init__(root, main_root, current_user)
        self.root.title("Программа обучения английскому языку - Тестирование")
        app = MainTestApp(self.root)

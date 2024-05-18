import tkinter as tk
from tkinter import Label, Button, Entry, Frame
from tkinter.font import Font
from PIL import Image, ImageTk
import random
import sqlite3
import io
import pygame
from datetime import datetime
from main import BaseWindow


class Lessons(BaseWindow):
    def __init__(self, root, main_root, current_user, topic, width=250, height=300):
        super().__init__(root, main_root)
        self.current_user = current_user
        self.width = width
        self.height = height
        self.topic = topic
        self.current_card = 0
        self.total_cards = 8
        self.correct_answers = 0  # Количество правильных ответов
        self.answers_results = {}  # Временный словарь для хранения результатов ответов
        self.root.title("Программа обучения английскому языку - Обучение")
        self.cards, self.answers, self.back_texts, self.sounds, self.word_ids = self.get_lesson_data()
        self.is_image_shown = True
        self.button_states = [False] * self.total_cards  # Хранение состояния кнопок

        pygame.mixer.init()  # Инициализация микшера pygame

        # Настройка шрифтов и текста
        self.font1 = Font(family="Helvetica", size=20, weight="bold")
        self.font2 = Font(family="Helvetica", size=12, weight="bold")
        self.font3 = Font(family="Helvetica", size=14, weight="normal")
        self.title_label = Label(root, text="Название карточки", font=self.font1)
        self.title_label.pack()

        # Инициализация виджета для отображения текста задания
        self.question_label = Label(root, font=self.font2)
        self.question_label.pack()

        # Фрейм для карточки
        self.card_frame = Frame(root)
        self.card_frame.pack(pady=10)

        # Инициализация карточки с изображением
        self.label = Label(self.card_frame)
        self.label.pack()

        # Индикаторы прогресса
        self.indicator_frame = Frame(root)
        self.indicator_frame.pack(pady=10)
        self.indicators = [Label(self.indicator_frame, text="•", font=("Helvetica", 40), fg="lightgray") for _ in
                           range(self.total_cards)]
        for indicator in self.indicators:
            indicator.pack(side="left", padx=1)

        # Кнопки выбора ответа
        self.button_frame = Frame(root)
        self.button_frame.pack(pady=10)
        self.option_buttons = []

        # Поле ввода для ответа
        self.answer_entry = Entry(root, font=self.font2)
        self.answer_entry.pack(pady=20)
        self.answer_entry.pack_forget()

        # Навигационные кнопки
        self.nav_frame = Frame(root)
        self.nav_frame.pack(pady=10)
        self.prev_button = Button(self.nav_frame, text="Предыдущая", command=self.prev_card, font=self.font3)
        self.prev_button.pack(side="left", padx=10)
        self.next_button = Button(self.nav_frame, text="Следующая", command=self.next_card, font=self.font3)
        self.next_button.pack(side="left", padx=10)
        self.exit_button = Button(self.nav_frame, text="Выход", command=self.exit_to_main, font=self.font3)
        self.exit_button.pack(side="left", padx=10)
        self.label.bind("<Button-1>", self.flip_card)

        self.update_card()

    def get_lesson_data(self):
        conn = sqlite3.connect('team_app.db')
        cursor = conn.cursor()

        # Получаем слова по теме
        cursor.execute("""
            SELECT words.word_id, words.picture, words.english, words.russian, words.sound
            FROM words
            JOIN words_groupings ON words.word_id = words_groupings.word_id
            JOIN topics ON words_groupings.topic_id = topics.topic_id
            WHERE topics.topic_name = ?
            ORDER BY RANDOM()
            LIMIT 8
        """, (self.topic,))
        lesson_data = cursor.fetchall()

        cards = [item[1] for item in lesson_data]  # Изображения карточек
        answers = [item[2] for item in lesson_data]  # Английские слова (ответы)
        back_texts = [item[3] for item in lesson_data]  # Русские слова (обратная сторона)
        sounds = [item[4] for item in lesson_data]  # Звуковые файлы
        word_ids = [item[0] for item in lesson_data]  # word_id для каждого слова

        conn.close()
        return cards, answers, back_texts, sounds, word_ids

    def load_image(self, image_data):
        # Загрузка изображения из бинарных данных
        original_image = Image.open(io.BytesIO(image_data))
        image = original_image.resize((self.width, self.height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.label.config(image=photo)
        self.label.image = photo

    def update_card(self):
        if self.current_card < self.total_cards:
            # Обновление текущей карточки с отображением номера и описания вопроса
            self.title_label.config(text=f"Карточка № {self.current_card + 1}")
            self.question_label.config(text="Выберите правильный перевод слова:")
            self.load_image(self.cards[self.current_card])
            self.display_options()  # Обновление вариантов ответа и элементов ввода
            self.update_indicators()
        else:
            self.show_results()

    def display_options(self):
        # Очистка текущих виджетов в button_frame
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        correct_answer = self.answers[self.current_card]  # Пример правильного ответа
        random_answers = random.sample([ans for ans in self.answers if ans != correct_answer], 2)
        all_answers = random.sample(random_answers + [correct_answer], 3)

        self.option_buttons = []  # Сброс списка кнопок
        for answer in all_answers:
            btn = Button(self.button_frame, text=answer, font=self.font3)
            if self.button_states[self.current_card]:
                btn.config(state=tk.DISABLED)
            else:
                btn.config(command=lambda ans=answer: self.check_answer(ans, correct_answer, btn))
            btn.pack(side="left", padx=10)
            self.option_buttons.append(btn)

    def check_answer(self, chosen_answer, correct_answer, button):
        # Проверка ответа и обновление визуального отображения результата
        word_id = self.word_ids[self.current_card]
        if chosen_answer == correct_answer:
            button.config(fg='green')  # Зеленый текст, если ответ верный
            self.correct_answers += 1  # Увеличение счетчика правильных ответов
            self.answers_results[word_id] = 1
        else:
            button.config(fg='red')  # Красный текст, если ответ неверный
            self.answers_results[word_id] = 0

        # Деактивация всех кнопок
        for btn in self.option_buttons:
            if btn.winfo_exists():  # Проверка на существование кнопки
                btn.config(state=tk.DISABLED)

        # Обновление состояния кнопок для текущей карточки
        self.button_states[self.current_card] = True

        print(f"Всего правильных ответов: {self.correct_answers}")  # Опционально, вывод в консоль

    def flip_card(self, event):
        # Анимация переворота карточки
        steps = 10  # Количество шагов в анимации
        delay = 25  # Задержка между шагами в миллисекундах

        if self.is_image_shown:
            # Переворот от изображения к тексту
            for i in range(steps, -1, -1):
                alpha = i / steps
                self.update_alpha(alpha)
                self.root.update()
                self.root.after(delay)
            self.label.pack_forget()
            self.draw_backside()  # Рисуем обратную сторону
            self.is_image_shown = False
        else:
            # Переворот обратно к изображению
            self.canvas.pack_forget()
            for i in range(steps + 1):
                alpha = i / steps
                self.update_alpha(alpha)
                self.root.update()
                self.root.after(delay)
            self.label.pack()  # Уточнение расположения карточки при перепаковке
            self.is_image_shown = True

    def draw_backside(self):
        # Создание холста для рисования обратной стороны карточки
        self.canvas = tk.Canvas(self.card_frame, width=self.width, height=self.height, bg='white')
        self.canvas.pack()
        # Рисуем белый прямоугольник в качестве фона
        self.canvas.create_rectangle(10, 10, self.width - 10, self.height - 10, fill="white", outline="black")
        # Добавляем текст поверх прямоугольника
        self.canvas.create_text(self.width / 2, self.height / 2, text=self.back_texts[self.current_card],
                                font=self.font1, fill="black")
        # Привязываем событие клика мыши к холсту для обратного переворота
        self.canvas.bind("<Button-1>", self.flip_card)

        # Добавляем кнопку для воспроизведения звука
        sound_button = Button(self.canvas, text="Воспроизвести", command=self.play_sound)
        self.canvas.create_window(self.width / 2, self.height - 30, window=sound_button)

    def play_sound(self):
        # Воспроизведение звукового файла из базы данных
        sound_data = self.sounds[self.current_card]
        sound = io.BytesIO(sound_data)
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()

    def update_alpha(self, alpha):
        # Загрузка изображения и его конвертация в формат с поддержкой альфа-канала
        image = Image.open(io.BytesIO(self.cards[self.current_card])).convert("RGBA")
        # Получение данных изображения для манипуляции с прозрачностью
        data = image.getdata()

        # Создание нового списка данных, где прозрачность каждого пикселя изменяется
        newData = []
        for item in data:
            if item[3] != 0:  # Проверяем, что пиксель изначально не полностью прозрачный
                newData.append((item[0], item[1], item[2], int(item[3] * alpha)))
            else:
                newData.append(item)  # Если пиксель полностью прозрачный, оставляем его без изменений

        # Применение новых данных к изображению
        image.putdata(newData)
        # Изменение размера изображения под размеры виджета
        image = image.resize((self.width, self.height), Image.Resampling.LANCZOS)
        # Создание объекта PhotoImage из изменённого изображения
        photo = ImageTk.PhotoImage(image)
        # Обновление изображения на виджете
        self.label.config(image=photo)
        self.label.image = photo  # Сохранение ссылки на изображение для предотвращения его удаления сборщиком мусора

    def update_indicators(self):
        # Обновление индикаторов прогресса
        for i, indicator in enumerate(self.indicators):
            indicator.config(fg="black" if i == self.current_card else "lightgray")

    def prev_card(self):
        # Переход к предыдущей карточке
        if self.current_card > 0:
            if not self.is_image_shown:
                self.flip_card(None)
            self.current_card -= 1
            self.next_button.config(text="Следующая")
            self.update_card()

    def next_card(self):
        # Переход к следующей карточке или подсчет очков
        if self.current_card < self.total_cards - 1:
            if not self.is_image_shown:
                self.flip_card(None)
            self.current_card += 1
            self.update_card()
        elif self.current_card == self.total_cards - 1:
            self.next_button.config(text="Результаты сохранены")
            self.disable_navigation_buttons()
            self.save_results()

    def disable_navigation_buttons(self):
        # Деактивация навигационных кнопок
        self.prev_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)

        # Деактивация всех кнопок
        for btn in self.option_buttons:
            if btn.winfo_exists():  # Проверка на существование кнопки
                btn.config(state=tk.DISABLED)

    def enable_navigation_buttons(self):
        # Активация навигационных кнопок
        self.prev_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.NORMAL)

    def show_results(self):
        # Показывает результаты
        self.title_label.config(text="Результаты")
        self.question_label.config(text=f"Правильных ответов: {self.correct_answers} из {self.total_cards}")
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        self.disable_navigation_buttons()

    def save_results(self):
        conn = sqlite3.connect('team_app.db')
        cursor = conn.cursor()

        # Сохраняем результаты в таблицу lesson
        cursor.execute("SELECT MAX(lesson_id) FROM lesson")
        lesson_id = cursor.fetchone()[0]
        if lesson_id is None:
            lesson_id = 0
        lesson_id += 1

        cursor.execute("""
            INSERT INTO lesson (lesson_id, topic_id, done, note1, note2)
            VALUES (?, (SELECT topic_id FROM topics WHERE topic_name = ?), ?, ?, ?)
        """, (lesson_id, self.topic, True, '', ''))

        # Обновляем результаты в таблице user_progress
        for word_id in self.word_ids:
            success_counter = self.answers_results.get(word_id, 0)
            fails_counter = 1 - success_counter

            cursor.execute("""
                INSERT INTO user_progress (
                    user_id, word_id, lesson_id, success_counter, failes_counter, success_date, off_rotation, dictionary, note1, note2
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.current_user, word_id, lesson_id, success_counter, fails_counter,
                datetime.now().strftime('%Y-%m-%d'), False, False, '', ''
            ))

        conn.commit()
        conn.close()

    def exit_to_main(self):
        # Выход из программы
        print("Выход в меню уроков")
        self.go_back_training()

    def go_back_training(self):
        from training_window import TrainingWindow
        self.go_back(TrainingWindow)

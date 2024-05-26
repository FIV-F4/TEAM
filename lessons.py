import tkinter as tk
from tkinter import Frame, Entry, Label, Button
from tkinter.font import Font
from PIL import Image, ImageTk
import random
import sqlite3
import io
import pygame
from datetime import datetime
from main import BaseWindow
from styles import StyledCanvas, StyledButton, TransparentLabel

class Lessons(BaseWindow):
    def __init__(self, root, main_root, current_user, topic, width=250, height=250):
        super().__init__(root, main_root, current_user)
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

        # Canvas
        self.canvas = StyledCanvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Инициализация виджета для отображения текста задания
        self.question_label = self.canvas.create_text(400, 80, font=self.font2, fill="black")

        # Фрейм для карточки
        self.card_frame = Frame(self.canvas)
        self.canvas.create_window(400, 230, window=self.card_frame, anchor="center")

        # Инициализация карточки с изображением
        self.label = Label(self.card_frame)
        self.label.pack()

        # Индикаторы прогресса
        self.indicator_frame = Frame(self.canvas)
        self.canvas.create_window(400, 390, window=self.indicator_frame, anchor="center")
        self.indicators = [Label(self.indicator_frame, text="[]", font=("Helvetica", 20), fg="lightgray") for _ in range(self.total_cards)]
        for indicator in self.indicators:
            indicator.pack(side="left", padx=1)

        # Кнопки выбора ответа
        self.button_frame = Frame(self.canvas)
        self.canvas.create_window(400, 450, window=self.button_frame, anchor="center")

        # Навигационные кнопки
        self.prev_button = StyledButton(self.canvas, 200, 520, text="Предыдущая", command=self.prev_card, width=200, height=40)
        self.next_button = StyledButton(self.canvas, 600, 520, text="Следующая", command=self.next_card, width=200, height=40)
        self.exit_button = StyledButton(self.canvas, 400, 560, text="Выход", command=self.exit_to_main, width=100, height=40)
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
        # Очистка предыдущих меток
        if hasattr(self, 'title_label') and isinstance(self.title_label, TransparentLabel):
            self.canvas.delete(self.title_label.text_id)
        if hasattr(self, 'question_label') and isinstance(self.question_label, TransparentLabel):
            self.canvas.delete(self.question_label.text_id)

        if self.current_card < self.total_cards:
            # Обновление текущей карточки с отображением номера и описания вопроса
            self.title_label = TransparentLabel(self.canvas, 400, 40, text=f"Карточка № {self.current_card + 1}",
                                                font=('Helvetica', 20, 'bold'), fill='black')
            self.question_label = TransparentLabel(self.canvas, 400, 80, text="Выберите правильный перевод слова:",
                                                   font=('Helvetica', 16), fill='black')

            if not self.is_image_shown:
                self.flip_card(None)

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
        steps = 3  # Количество шагов в анимации
        delay = 1  # Задержка между шагами в миллисекундах

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
            self.backside_canvas.pack_forget()
            for i in range(steps + 1):
                alpha = i / steps
                self.update_alpha(alpha)
                self.root.update()
                self.root.after(delay)
            self.label.pack()  # Уточнение расположения карточки при перепаковке
            self.is_image_shown = True

    def draw_backside(self):
        # Создание холста для рисования обратной стороны карточки
        self.backside_canvas = tk.Canvas(self.card_frame, width=self.width, height=self.height, bg='white')
        self.backside_canvas.pack()
        # Рисуем белый прямоугольник в качестве фона
        self.backside_canvas.create_rectangle(10, 10, self.width - 10, self.height - 10, fill="white", outline="black")
        # Добавляем текст поверх прямоугольника
        self.backside_canvas.create_text(self.width / 2, self.height / 2, text=self.back_texts[self.current_card],
                                         font=self.font1, fill="black")
        # Привязываем событие клика мыши к холсту для обратного переворота
        self.backside_canvas.bind("<Button-1>", self.flip_card)

        # Добавляем кнопку для воспроизведения звука
        sound_button = Button(self.backside_canvas, text="Воспроизвести", command=self.play_sound)
        self.backside_canvas.create_window(self.width / 2, self.height - 30, window=sound_button)

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
        # Очистка предыдущих меток
        if hasattr(self, 'title_label') and isinstance(self.title_label, TransparentLabel):
            self.canvas.delete(self.title_label.text_id)
        if hasattr(self, 'question_label') and isinstance(self.question_label, TransparentLabel):
            self.canvas.delete(self.question_label.text_id)

        # Переход к предыдущей карточке
        if self.current_card > 0:
            self.current_card -= 1
            self.update_card()

    def next_card(self):
        # Очистка предыдущих меток
        if hasattr(self, 'title_label') and isinstance(self.title_label, TransparentLabel):
            self.canvas.delete(self.title_label.text_id)
        if hasattr(self, 'question_label') and isinstance(self.question_label, TransparentLabel):
            self.canvas.delete(self.question_label.text_id)

        # Переход к следующей карточке или подсчет очков
        if self.current_card < self.total_cards - 1:
            self.current_card += 1
            self.update_card()
        else:
            self.current_card += 1
            self.show_results()

    def disable_navigation_buttons(self):
        # Деактивация навигационных кнопок
        self.prev_button.disable()
        self.next_button.disable()

    def enable_navigation_buttons(self):
        # Активация навигационных кнопок
        self.prev_button.enable()
        self.next_button.enable()

    def show_results(self):
        # Очистка предыдущих меток
        if hasattr(self, 'title_label') and isinstance(self.title_label, TransparentLabel):
            self.canvas.delete(self.title_label.text_id)
        if hasattr(self, 'question_label') and isinstance(self.question_label, TransparentLabel):
            self.canvas.delete(self.question_label.text_id)

        # Показывает результаты
        self.title_label = TransparentLabel(self.canvas, 400, 40, text="Результаты", font=('Helvetica', 20, 'bold'),
                                            fill='black')
        self.question_label = TransparentLabel(self.canvas, 400, 80, text=f"Правильных ответов: "
                                                                          f"{self.correct_answers} из {self.total_cards}",
                                               font=('Helvetica', 16), fill='black')
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

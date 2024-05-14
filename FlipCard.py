import tkinter as tk
from tkinter import Label, Button, Entry, Frame
from tkinter.font import Font
from PIL import Image, ImageTk
import random


class FlipCard:
    def __init__(self, parent, width=250, height=300):
        self.parent = parent
        self.width = width
        self.height = height
        self.current_card = 0
        self.total_cards = 8
        self.correct_answers = 0  # Количество правильных ответов
        self.cards = [f"./PIC/Image_{i}.png" for i in range(1, 9)]  # Изображения карточек
        self.task_types = [random.choice(['a', 'b', 'c']) for _ in range(self.total_cards)]  # Типы задач на карточках
        self.answers = ["Вариант 1", "Вариант 2", "Вариант 3"]  # Возможные ответы
        self.back_texts = ["Перевод 1", "Перевод 2", "Перевод 3", "Перевод 4",
                           "Перевод 5", "Перевод 6", "Перевод 7", "Перевод 8"]  # Тексты для обратной стороны
        self.is_image_shown = True

        # Настройка шрифтов и текста
        self.font1 = Font(family="Helvetica", size=20, weight="bold")
        self.font2 = Font(family="Helvetica", size=12, weight="bold")
        self.font3 = Font(family="Helvetica", size=14, weight="normal")
        self.title_label = Label(parent, text="Название карточки", font=self.font1)
        self.title_label.pack()

        # Инициализация виджета для отображения текста задания
        self.question_label = Label(parent, font=self.font2)
        self.question_label.pack()

        # Фрейм для карточки
        self.card_frame = Frame(parent)
        self.card_frame.pack(pady=10)

        # Инициализация карточки с изображением
        self.label = Label(self.card_frame)
        self.label.pack()

        # Индикаторы прогресса
        self.indicator_frame = Frame(parent)
        self.indicator_frame.pack(pady=10)
        self.indicators = [Label(self.indicator_frame, text="•", font=("Helvetica", 40), fg="lightgray") for _ in
                           range(self.total_cards)]
        for indicator in self.indicators:
            indicator.pack(side="left", padx=1)

        # Кнопки выбора ответа
        self.button_frame = Frame(parent)
        self.button_frame.pack(pady=10)
        self.option_buttons = []
        for answer in self.answers:
            btn = Button(self.button_frame, text=answer, font=self.font2,
                         command=lambda ans=answer: self.check_answer(ans))
            btn.pack(side="left", padx=10)
            self.option_buttons.append(btn)

        # Поле ввода для ответа
        self.answer_entry = Entry(parent, font=self.font2)
        self.answer_entry.pack(pady=20)
        self.answer_entry.pack_forget()

        # Навигационные кнопки
        self.nav_frame = Frame(parent)
        self.nav_frame.pack(pady=10)
        self.prev_button = Button(self.nav_frame, text="Предыдущая", command=self.prev_card, font=self.font3)
        self.prev_button.pack(side="left", padx=10)
        self.next_button = Button(self.nav_frame, text="Следующая", command=self.next_card, font=self.font3)
        self.next_button.pack(side="left", padx=10)
        self.exit_button = Button(self.nav_frame, text="Выход", command=self.exit_to_main, font=self.font3)
        self.exit_button.pack(side="left", padx=10)
        self.label.bind("<Button-1>", self.flip_card)

        self.update_card()

    def load_image(self, image_path):
        # Загрузка изображения
        original_image = Image.open(image_path)
        image = original_image.resize((self.width, self.height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.label.config(image=photo)
        self.label.image = photo

    def update_card(self):
        # Обновление текущей карточки с отображением номера и описания вопроса
        self.title_label.config(text=f"Карточка № {self.current_card + 1}")
        task_type = self.task_types[self.current_card]
        if task_type == 'a':
            self.question_label.config(text="Выберите правильный перевод слова:")
        elif task_type == 'b':
            self.question_label.config(text="Какое слово соответствует этому переводу?")
        elif task_type == 'c':
            self.question_label.config(text="Введите слово, соответствующее картинке:")
        self.load_image(self.cards[self.current_card])
        self.display_options()  # Обновление вариантов ответа и элементов ввода
        self.update_indicators()

    def display_options(self):
        # Очистка текущих виджетов в button_frame
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        task_type = self.task_types[self.current_card]
        if task_type == 'c':
            # Для варианта "c" показываем текстовое поле вместо кнопок
            self.answer_entry.pack(in_=self.button_frame, fill='x', padx=20)  # Размещаем поле ввода внутри frame кнопок
        else:
            # Для вариантов "a" и "b" показываем кнопки и скрываем текстовое поле
            self.answer_entry.pack_forget()
            correct_answer = random.choice(self.answers)  # Пример правильного ответа
            for answer in self.answers:
                btn = Button(self.button_frame, text=answer, font=self.font3)
                btn.config(command=lambda ans=answer, gtn=btn: self.check_answer(ans, correct_answer, gtn))
                btn.pack(side="left", padx=10)
                self.option_buttons.append(btn)

    def check_answer(self, chosen_answer, correct_answer, button):
        # Проверка ответа и обновление визуального отображения результата
        if chosen_answer == correct_answer:
            button.config(fg='green')  # Зеленый текст, если ответ верный
            self.correct_answers += 1  # Увеличение счетчика правильных ответов
        else:
            button.config(fg='red')  # Красный текст, если ответ неверный
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
                self.parent.update()
                self.parent.after(delay)
            self.label.pack_forget()
            self.draw_backside()  # Рисуем обратную сторону
            self.is_image_shown = False
        else:
            # Переворот обратно к изображению
            self.canvas.pack_forget()
            for i in range(steps + 1):
                alpha = i / steps
                self.update_alpha(alpha)
                self.parent.update()
                self.parent.after(delay)
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

    def update_alpha(self, alpha):
        # Загрузка изображения и его конвертация в формат с поддержкой альфа-канала
        image = Image.open(self.cards[self.current_card]).convert("RGBA")
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
            self.current_card -= 1
        self.update_card()

    def next_card(self):
        # Переход к следующей карточке или подсчет очков
        if self.current_card < self.total_cards - 1:
            self.current_card += 1
        elif self.current_card == self.total_cards - 1:
            self.next_button.config(text="Посчитать очки")
            print(f"Всего правильных ответов: {self.correct_answers}")
        self.update_card()

    def exit_to_main(self):
        # Выход из программы
        print("Выход в главное меню")
        self.parent.destroy()


# Главное окно
root = tk.Tk()
root.title("Переворот карточки")
root.geometry("600x600")

app = FlipCard(root)

root.mainloop()

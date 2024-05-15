import tkinter as tk
import speech_recognition as sr
import pygame
import json
from PIL import Image, ImageTk

# Словарь со словами и их переводами и путями к аудиофайлам
with open('audio_words.json', 'r', encoding='utf-8') as f:
    audio_words = json.load(f)

words = audio_words['FOOD']
for key in words:
    words[key].append(f'IMAGES/FOOD/{key}.png')

# Инициализация Pygame для воспроизведения аудио
pygame.mixer.init()

class SpeakingTest:
    def __init__(self, master, words):
        self.master = master
        master.title("Language Learning App")
        master.geometry("600x600")  # Изменение размера экрана

        # Словарь со словами и их переводами
        self.words = words
        self.words_list = list(self.words.keys())
        self.current = 0

        # Добавление изображения
        self.image_label = tk.Label(master)
        self.image_label.grid(row=0, column=0, columnspan=3, pady=50)

        # Текстовое поле для вывода слова на русском
        self.word_label = tk.Label(master, text="", font=("Helvetica", 36))
        self.word_label.grid(row=1, column=0, columnspan=3, pady=10)

        # Кнопка для начала распознавания
        self.recognize_button = tk.Button(master, text="Speak English!", command=self.recognize_speech)
        self.recognize_button.grid(row=2, column=0, padx=28, pady=30)

        # Кнопка для перехода к следующему слову
        self.next_button = tk.Button(master, text="Следующее слово", command=self.next_word)
        self.next_button.grid(row=2, column=1, padx=28, pady=30)

        # Кнопка для воспроизведения правильного произношения (изначально неактивна)
        self.play_audio_button = tk.Button(master, text="Прослушать ответ", command=self.play_audio, state="disabled")
        self.play_audio_button.grid(row=2, column=2, padx=28, pady=30)

        # Кнопка для выхода из программы
        self.exit_button = tk.Button(master, text="Выход", command=master.quit)
        self.exit_button.grid(row=4, column=1, pady=10)

        # Метка для вывода результата
        self.result_label = tk.Label(master, text="", font=("Helvetica", 36))
        self.result_label.grid(row=3, column=0, columnspan=3, pady=20)

        # Инициализация распознавателя речи
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Начальное слово
        self.next_word()

    def next_word(self):
        if self.current < len(self.words_list):
            english_word = self.words_list[self.current]
            russian_translation = self.words[english_word][0]
            image_path = self.words[english_word][2]

            self.word_label.config(text=russian_translation)
            self.result_label.config(text="")
            self.play_audio_button.config(state="disabled")

            # Загрузка и отображение изображения
            image = Image.open(image_path)
            image = image.resize((200, 200))
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo

        else:
            self.word_label.config(text="Finished!")
            self.recognize_button.config(state="disabled")
            self.next_button.config(state="disabled")
            self.play_audio_button.config(state="disabled")

    def recognize_speech(self):
        with self.microphone as source:
            print("Please speak now...")
            audio = self.recognizer.listen(source)
            try:
                # Распознавание на английском языке
                spoken_text = self.recognizer.recognize_google(audio, language="en-US")
                english_word = self.words_list[self.current]
            #    correct_text, audio_path = self.words[english_word][:2]
                if spoken_text.lower() == english_word.lower():
                    self.result_label.config(text="Правильно!")
                    self.play_audio_button.config(state="disabled")
                else:
                    self.result_label.config(text=f"Неверно! ({english_word})")
                    self.play_audio_button.config(state="normal")
                self.current += 1
            except sr.UnknownValueError:
                self.result_label.config(text="Не удалось распознать речь.")
            except sr.RequestError as e:
                self.result_label.config(text="Ошибка сервиса распознавания.")

    def play_audio(self):
        english_word = self.words_list[self.current - 1]
        _, audio_path = self.words[english_word][:2]
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeakingTest(root, words)
    root.mainloop()

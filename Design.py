import tkinter as tk
from tkinter import PhotoImage

def on_button_click():
    print("Button clicked!")

root = tk.Tk()
root.title("Image Button Example")

# Загрузка изображения
button_image = PhotoImage(file="db_operator/src/food.png")

# Создание кнопки с изображением
button = tk.Button(root, image=button_image, command=on_button_click, borderwidth=0)
button.pack(pady=20)

root.mainloop()

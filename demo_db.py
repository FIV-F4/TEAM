import sqlite3
from tkinter import Tk, Canvas, Button
from PIL import Image, ImageTk
import io


# Создание базы данных и таблицы
def create_database():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS mytable (
            id INTEGER PRIMARY KEY,
            image BLOB)''')
    with open('db_operator/src/food.png', 'rb') as f:
        image_data = f.read()
    cursor.execute('INSERT INTO mytable (image) VALUES (?)', (image_data,))
    conn.commit()
    conn.close()


# Получение изображения из базы данных
def get_image_from_db():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT image FROM mytable WHERE id = 1')
    image_data = cursor.fetchone()[0]
    conn.close()
    return image_data


# Отображение изображения в Tkinter
def show_image():
    root = Tk()
    root.title('Image Viewer')

    image_data = get_image_from_db()
    image = Image.open(io.BytesIO(image_data))
    photo = ImageTk.PhotoImage(image)

    canvas = Canvas(root, width=image.width, height=image.height)
    canvas.pack()
    canvas.create_image(0, 0, anchor='nw', image=photo)

    button = Button(root, text='Exit', command=root.quit)
    button.pack()

    root.mainloop()


if __name__ == '__main__':
    create_database()
    show_image()

import tkinter as tk
from PIL import Image, ImageTk

# Пути к изображениям
BACKGROUND_IMAGE_PATH = './PIC/background_image.png'
NORMAL_BUTTON_IMAGE_PATH = './PIC/normal_button.png'
PRESSED_BUTTON_IMAGE_PATH = './PIC/pressed_button.png'


class StyledCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(width=800, height=600)
        self.background_image = Image.open(BACKGROUND_IMAGE_PATH)
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.bg_image_id = self.create_image(0, 0, image=self.background_photo, anchor="nw")
        self.bind("<Configure>", self._resize_image)

    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height
        resized_image = self.background_image.resize((new_width, new_height), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(resized_image)
        self.itemconfig(self.bg_image_id, image=self.background_photo)


class StyledButton:
    def __init__(self, canvas, x, y, text="", command=None, width=250, height=60):
        self.canvas = canvas
        self.command = command
        self.normal_image = Image.open(NORMAL_BUTTON_IMAGE_PATH).convert("RGBA").resize((width, height), Image.LANCZOS)
        self.pressed_image = Image.open(PRESSED_BUTTON_IMAGE_PATH).convert("RGBA").resize((width, height), Image.LANCZOS)

        self.normal_photo = ImageTk.PhotoImage(self.normal_image)
        self.pressed_photo = ImageTk.PhotoImage(self.pressed_image)

        self.button_id = self.canvas.create_image(x, y, image=self.normal_photo, anchor=tk.CENTER)
        self.text_id = self.canvas.create_text(x, y, text=text, fill="black", font=("Helvetica", 12, "bold"))

        self.canvas.tag_bind(self.button_id, "<ButtonPress-1>", self.on_button_press)
        self.canvas.tag_bind(self.button_id, "<ButtonRelease-1>", self.on_button_release)
        self.canvas.tag_bind(self.text_id, "<ButtonPress-1>", self.on_button_press)
        self.canvas.tag_bind(self.text_id, "<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.canvas.itemconfig(self.button_id, image=self.pressed_photo)

    def on_button_release(self, event):
        self.canvas.itemconfig(self.button_id, image=self.normal_photo)
        if self.command:
            self.command()

    def set_image(self, image):
        self.canvas.itemconfig(self.button_id, image=image)
        self.normal_photo = image

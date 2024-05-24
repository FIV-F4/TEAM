import tkinter as tk

def center_window(window, width=800, height=600):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height - 100) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.minsize(800, 600)
    window.maxsize(800, 600)

# Базовый класс окна
class BaseWindow:
    def __init__(self, root, main_root, current_user):
        self.root = root
        self.main_root = main_root
        self.current_user = current_user
        self.main_root_closed = False
        center_window(self.root)
        self.root.protocol("WM_DELETE_WINDOW", self.exit_program)

    def go_back(self, new_window_class, *args):
        self.root.withdraw()  # Скрываем текущее окно
        new_window = tk.Toplevel(self.main_root)
        new_window_class(new_window, self.main_root, self.current_user, *args)

    def open_new_window(self, new_window_class, *args):
        self.root.withdraw()
        new_window = tk.Toplevel(self.main_root)
        new_window_class(new_window, self.main_root, self.current_user, *args)

    def exit_program(self):
        if not self.main_root_closed:
            self.main_root_closed = True
            self.main_root.destroy()
        else:
            self.root.destroy()

if __name__ == "__main__":
    from login import LoginWindow

    root = tk.Tk()
    center_window(root)
    app = LoginWindow(root, root, None)
    root.mainloop()

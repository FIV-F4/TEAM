import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage, filedialog


def connect_db():
    conn = sqlite3.connect('team_app.db')
    return conn


def get_topics(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT topic_id, topic_name FROM topics')
    return cursor.fetchall()


def search_word(conn, prefix):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT english, russian, picture, word_id 
        FROM words 
        WHERE english LIKE ? 
        LIMIT 1
    ''', (prefix + '%',))
    result = cursor.fetchone()
    return result if result else (None, None, None, None)


def get_word_topics(conn, word_id):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT topic_id 
        FROM words_groupings 
        WHERE word_id = ?
    ''', (word_id,))
    return [row[0] for row in cursor.fetchall()]


def insert_word(conn, english, russian, picture):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO words (english, russian, picture) VALUES (?, ?, ?)
    ''', (english, russian, picture))
    conn.commit()
    return cursor.lastrowid


def insert_word_groupings(conn, word_id, topic_id):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO words_groupings (word_id, topic_id) VALUES (?, ?)
    ''', (word_id, topic_id))
    conn.commit()


def insert_topic(conn, topic_name):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO topics (topic_name) VALUES (?)
    ''', (topic_name,))
    conn.commit()
    return cursor.lastrowid


def on_key_release(event):
    prefix = entry.get()
    if prefix and event.keysym not in ('BackSpace', 'Delete', 'Left', 'Right'):
        english_word, russian_word, picture, word_id = search_word(conn, prefix)
        if english_word:
            display_word(prefix, english_word, russian_word, picture)
            mark_word_topics(word_id)
            save_button.config(state='disabled')
            russian_entry.config(state='readonly')
            disable_topic_selection()
        else:
            russian_entry.config(state='normal')
            russian_entry.delete(0, tk.END)
            image_label.config(image=default_image)
            save_button.config(state='normal')
            unmark_all_topics()
            enable_topic_selection()
    elif not prefix:
        entry.delete(0, tk.END)
        russian_entry.config(state='normal')
        russian_entry.delete(0, tk.END)
        russian_entry.config(state='readonly')
        image_label.config(image=default_image)
        save_button.config(state='disabled')
        unmark_all_topics()
        disable_topic_selection()


def display_word(prefix, english_word, russian_word, picture):
    entry.delete(0, tk.END)
    entry.insert(0, english_word)
    entry.select_range(len(prefix), tk.END)
    entry.icursor(len(prefix))
    russian_entry.config(state='normal')
    russian_entry.delete(0, tk.END)
    if russian_word:
        russian_entry.insert(0, russian_word)
    russian_entry.config(state='readonly')
    if picture:
        image = PhotoImage(data=picture)
        image_label.config(image=image)
        image_label.image = image
    else:
        image_label.config(image=default_image)
        image_label.image = default_image


def mark_word_topics(word_id):
    word_topics = get_word_topics(conn, word_id)
    for topic_id, var in topic_vars.items():
        if topic_id in word_topics:
            var.set(1)
        else:
            var.set(0)


def unmark_all_topics():
    for var in topic_vars.values():
        var.set(0)


def enable_topic_selection():
    for chk in checkboxes.values():
        chk.config(state='normal')
    new_topic_entry.config(state='normal')
    add_topic_button.config(state='normal')


def disable_topic_selection():
    for chk in checkboxes.values():
        chk.config(state='disabled')
    new_topic_entry.config(state='disabled')
    add_topic_button.config(state='disabled')


def on_save():
    english_word = entry.get()
    russian_word = russian_entry.get()
    if english_word and russian_word:
        picture = getattr(image_label, 'image_data', None)
        word_id = insert_word(conn, english_word, russian_word, picture)
        selected_topics = [topic_id for topic_id, var in topic_vars.items() if var.get() == 1]
        for topic_id in selected_topics:
            insert_word_groupings(conn, word_id, topic_id)
        save_button.config(state='disabled')
        russian_entry.config(state='readonly')
        disable_topic_selection()
        # Clear new topic entry
        new_topic_entry.delete(0, tk.END)
        unmark_all_topics()


def on_image_click(event):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
    if file_path:
        with open(file_path, 'rb') as image_file:
            image_data = image_file.read()
        image = PhotoImage(data=image_data)
        image_label.config(image=image)
        image_label.image = image
        image_label.image_data = image_data
        save_button.config(state='normal')


def on_add_topic():
    new_topic_name = new_topic_entry.get()
    if new_topic_name:
        topic_id = insert_topic(conn, new_topic_name)
        var = tk.IntVar()
        chk = ttk.Checkbutton(topics_frame, text=new_topic_name, variable=var, state="normal")
        chk.grid(row=len(topic_vars)+1, column=0, sticky='w', pady=2)
        topic_vars[topic_id] = var
        checkboxes[topic_id] = chk
        new_topic_entry.delete(0, tk.END)


conn = connect_db()

root = tk.Tk()
root.title("Word Search")
root.geometry("800x600")

default_image = PhotoImage(file='db_operator/src/button.png')

entry = ttk.Entry(root, font=('Arial', 24))
entry.grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky='ew')
entry.bind('<KeyRelease>', on_key_release)

russian_entry = ttk.Entry(root, font=('Arial', 24), state='readonly')
russian_entry.grid(row=1, column=0, columnspan=2, pady=20, padx=20, sticky='ew')

image_label = tk.Label(root, borderwidth=2, relief="solid", width=300, height=300, background="lightgrey")
image_label.grid(row=2, column=0, columnspan=2, pady=(20, 0), padx=20, sticky='n')
image_label.bind('<Button-1>', on_image_click)
image_label.config(image=default_image)
image_label.image = default_image

save_button = ttk.Button(root, text="Сохранить", state='disabled', command=on_save)
save_button.grid(row=3, column=0, columnspan=2, pady=20, padx=20)

topics_frame = ttk.Frame(root)
topics_frame.grid(row=0, column=2, rowspan=4, padx=20, pady=20, sticky='ns')

topic_vars = {}
checkboxes = {}
topics = get_topics(conn)
for idx, (topic_id, topic_name) in enumerate(topics):
    var = tk.IntVar()
    chk = ttk.Checkbutton(topics_frame, text=topic_name, variable=var, state="disabled")
    chk.grid(row=idx+1, column=0, sticky='w', pady=2)
    topic_vars[topic_id] = var
    checkboxes[topic_id] = chk

# New topic entry and button
new_topic_entry = ttk.Entry(topics_frame, font=('Arial', 14), state='disabled')
new_topic_entry.grid(row=len(topics)+1, column=0, pady=10, sticky='ew')
add_topic_button = ttk.Button(topics_frame, text="Добавить тему", state='disabled', command=on_add_topic)
add_topic_button.grid(row=len(topics)+2, column=0, pady=10)

root.mainloop()

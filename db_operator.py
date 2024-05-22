import subprocess
import sys

def run_script(script_path):
    try:
        # Определите путь к интерпретатору Python
        python_executable = sys.executable
        result = subprocess.run([python_executable, script_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_path}: {e}")
        return False

def main():
    scripts = [
        ("генерация аудио", "db_operator/audio_gen.py"),
       # ("размножение картинок", "db_operator/fake_img_gen.py"),
        ("генерация базы данных", "db_operator/db_gen.py"),
        ("заполнение и связывание таблиц words и topics", "db_operator/db_words.py"),
        ("заполнение таблиц achievements, tests, users и перевод тем для отображения", "db_operator/db_post_gen.py"),
        ("добавленеи ачивок", "db_operator/add_achievemnts_to_db.py"),
        ("добавленеи ачивок", "db_operator/addProgress.py")
    ]

    for message, script in scripts:
        print(message)
        if run_script(script):
            print(f"{message} завершено успешно.")
        else:
            print(f"{message} завершено с ошибкой. Прекращение выполнения.")
            return

    print(
        "База данных готова! При работе с ней обязательно после инициализации курсора используйте "
        "cursor.execute('PRAGMA foreign_keys = ON')")


if __name__ == "__main__":
    main()



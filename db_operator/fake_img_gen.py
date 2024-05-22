import os
import shutil


# Функция чтения файла и создания списка переводов
def read_translation_file(file_path):
    translation_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(' - ')
            if len(parts) == 2:
                translation_list.append(parts[1].strip())
    return translation_list


# Копирование файла в новую папку с новым именем
def copy_file_with_new_name(src_path, dst_dir, new_name):
    # Создание директории, если она не существует
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    dst_path = os.path.join(dst_dir, new_name + '.png')
    shutil.copy(src_path, dst_path)
    print(f'Файл {src_path} скопирован в {dst_path}')


# Основная логика
def main():
    base_src_dir = 'db_operator/src/'
    base_dst_dir = 'db_operator/multimedia/img/'

    files = {
        'food.png': 'db_operator/src/food.txt',
        'travel.png': 'db_operator/src/travel.txt',
        'business.png': 'db_operator/src/business.txt'
    }

    for file_name, translation_file in files.items():
        src_path = os.path.join(base_src_dir, file_name)
        translation_list = read_translation_file(translation_file)

        # Получение имени файла без расширения
        base_name = os.path.splitext(file_name)[0]
        # Создание полного пути до директории
        dst_dir = os.path.join(base_dst_dir, base_name)

        # Копирование файла с каждым именем из списка переводов
        for translation in translation_list:
            copy_file_with_new_name(src_path, dst_dir, translation)


if __name__ == '__main__':
    main()

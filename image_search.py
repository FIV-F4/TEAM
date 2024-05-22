import os
import requests
from PIL import Image
from io import BytesIO

# Путь к вашему текстовому файлу и папке для сохранения изображений
txt_file_path = 'db_operator/src/food.txt'
output_folder = 'db_operator/multimedia/img'

# Убедитесь, что папка для изображений существует
os.makedirs(output_folder, exist_ok=True)


def download_image(word, url, output_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        image.save(output_path, 'PNG')
        print(f"Image for '{word}' saved as {output_path}")
    except Exception as e:
        print(f"Failed to download image for '{word}': {e}")


def search_image_url(word):
    # Это пример использования DuckDuckGo для поиска изображения
    search_url = f"https://duckduckgo.com/?q={word}&t=h_&iax=images&ia=images"
    response = requests.get(search_url)
    response.raise_for_status()

    # Найдите URL первой картинки
    # Примечание: Это упрощённый пример, для настоящего проекта лучше использовать официальный API для поиска изображений
    start_index = response.text.find('"image":"') + len('"image":"')
    end_index = response.text.find('"', start_index)
    if start_index > len('"image":"') and end_index > start_index:
        return response.text[start_index:end_index]
    return None


def read_words_and_download_images(txt_file_path, output_folder):
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2:
                russian_word, english_word = parts
                image_url = search_image_url(english_word)
                if image_url:
                    output_path = os.path.join(output_folder, f"{english_word}.png")
                    download_image(english_word, image_url, output_path)



# Запуск основной функции
read_words_and_download_images(txt_file_path, output_folder)

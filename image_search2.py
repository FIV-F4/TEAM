import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import urllib.parse

# Путь к вашему текстовому файлу и папке для сохранения изображений
txt_file_path = 'db_operator/src/food.txt'
output_folder = 'db_operator/multimedia/img/food2'

# Убедитесь, что папка для изображений существует
os.makedirs(output_folder, exist_ok=True)


def download_image(word, url, output_path):
    try:
        print(f"Attempting to download image for '{word}' from URL: {url}")
        response = requests.get(url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        image.save(output_path, 'PNG')
        print(f"Image for '{word}' saved as {output_path}")
    except Exception as e:
        print(f"Failed to download image for '{word}': {e}")


def search_image_url(word):
    try:
        print(f"Searching for image URL for '{word}'")
        search_query = urllib.parse.quote(word)
        url = f"https://www.bing.com/images/search?q={search_query}&form=HDRSC2&first=1&tsc=ImageBasicHover"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        image_elements = soup.select('a.iusc')
        for a in image_elements:
            m = a.get('m')
            if m:
                image_url = eval(m).get('murl')
                if image_url and image_url.startswith('http'):
                    print(f"Found image URL for '{word}': {image_url}")
                    return image_url
        print(f"No valid image URL found for '{word}'")
        return None
    except Exception as e:
        print(f"Error while searching for image URL for '{word}': {e}")
        return None


def read_words_and_download_images(txt_file_path, output_folder):
    if not os.path.exists(txt_file_path):
        print(f"File not found: {txt_file_path}")
        return

    print(f"Reading words from file: {txt_file_path}")
    try:
        with open(txt_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            print(f"Found {len(lines)} lines in file.")
            if not lines:
                print(f"No words found in file: {txt_file_path}")
                return

            for line in lines:
                parts = line.strip().split(' - ')
                if len(parts) == 2:
                    russian_word, english_word = parts
                    print(f"Processing word pair: {russian_word} -> {english_word}")
                    image_url = search_image_url(english_word)
                    if image_url:
                        output_path = os.path.join(output_folder, f"{english_word}.png")
                        download_image(english_word, image_url, output_path)
                    else:
                        print(f"Skipping download for '{english_word}' as no valid image URL was found")
                else:
                    print(f"Invalid line format: {line}")
    except Exception as e:
        print(f"Error reading file: {e}")


# Запуск основной функции
read_words_and_download_images(txt_file_path, output_folder)

import os
from bing_image_downloader import downloader


def process_word_list(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except IOError as e:
        print(f"Error reading file: {e}")
        return

    # Общая папка для всех изображений
    output_folder = 'db_operator/multimedia/img'
    os.makedirs(output_folder, exist_ok=True)

    print(f"Found {len(lines)} lines in file.")
    for line in lines:
        if '.' in line and '-' in line:
            parts = line.strip().split('.')
            if len(parts) > 1:
                word_pair = parts[1].strip().split('-')
                if len(word_pair) == 2:
                    russian_word, english_word = word_pair
                    russian_word, english_word = russian_word.strip(), english_word.strip()
                    print(f"Processing word pair: {russian_word} -> {english_word}")

                    # Загрузка изображения с помощью bing-image-downloader
                    try:
                        downloader.download(english_word, limit=1, output_dir=output_folder, adult_filter_off=True,
                                            force_replace=False, timeout=60)
                        print(f"Image for '{english_word}' downloaded successfully.")
                    except Exception as e:
                        print(f"Failed to download image for '{english_word}': {e}")
                else:
                    print(f"Invalid word pair format: {line.strip()}")
            else:
                print(f"Invalid line format: {line.strip()}")
        else:
            print(f"Invalid line format: {line.strip()}")


if __name__ == "__main__":
    process_word_list("db_operator/src/travel.txt")

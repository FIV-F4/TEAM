from gtts import gTTS
import os

# Функция для чтения файла и создания словаря
def read_file_to_dict(filepath):
    translation_dict = {}
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            parts = line.split(' - ')
            if len(parts) == 2:
                key = parts[1].strip()
                value = parts[0].split('. ')[1].strip()
                translation_dict[key] = value
    return translation_dict

# Функция для создания нового словаря с аудио файлами
def create_audio_dictionary(input_dict, category):
    new_dict = {}
    for english_word, russian_translation in input_dict.items():
        # Генерация аудио файла
        tts = gTTS(english_word, lang='en')
        audio_file_path = f'db_operator/multimedia/audio/{category}/{english_word}.mp3'
        os_path = f'db_operator/multimedia/audio/{category}'
        if not os.path.exists(os_path):
            os.makedirs(os_path)
        tts.save(audio_file_path)

        # Добавление в новый словарь
        new_dict[english_word] = [russian_translation, audio_file_path]

    return new_dict

# Пути к файлам
file_paths = {
    'food': 'db_operator/src/food.txt',
    'business': 'db_operator/src/business.txt',
    'travel': 'db_operator/src/travel.txt'
}

# Чтение файлов и создание аудио файлов
audio_words_dictionary = {}
for category, filepath in file_paths.items():
    print(f"читаю файл {filepath}")
    words_dict = read_file_to_dict(filepath)
    audio_words_dictionary[category] = create_audio_dictionary(words_dict, category)

# Вывод результата для проверки
for category, dict in audio_words_dictionary.items():
    for key, value in dict.items():
        print(f"{category}:\n {key} : {value}")

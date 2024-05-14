from gtts import gTTS
import os
import json

# Исходный словарь
food_dictionary = {
    "apple": "яблоко",
    "banana": "банан",
    "carrot": "морковь",
    "potato": "картофель",
    "chicken": "курица",
    "beef": "говядина",
    "fish": "рыба",
    "bread": "хлеб",
    "cheese": "сыр",
    "rice": "рис",
    "pasta": "паста",
    "salad": "салат",
    "soup": "суп",
    "egg": "яйцо",
    "milk": "молоко",
    "butter": "масло"
}

business_dictionary = {
    "investment": "инвестиция",
    "revenue": "доход",
    "profit": "прибыль",
    "loss": "убыток",
    "market": "рынок",
    "strategy": "стратегия",
    "management": "управление",
    "employee": "сотрудник",
    "customer": "клиент",
    "supplier": "поставщик",
    "contract": "контракт",
    "negotiation": "переговоры",
    "partnership": "партнерство",
    "innovation": "инновация",
    "brand": "бренд",
    "merger": "слияние"
}

travel_dictionary = {
    "airplane": "самолет",
    "airport": "аэропорт",
    "baggage": "багаж",
    "passport": "паспорт",
    "ticket": "билет",
    "hotel": "отель",
    "reservation": "бронирование",
    "tourist": "турист",
    "destination": "направление",
    "itinerary": "маршрут",
    "excursion": "экскурсия",
    "guide": "гид",
    "map": "карта",
    "souvenir": "сувенир",
    "currency": "валюта",
    "visa": "виза"
}


words_dictionary = {
    'FOOD': food_dictionary,
    'BUSINESS': business_dictionary,
    'TRAVEL': travel_dictionary
}
audio_words_dictionary ={}
for key in words_dictionary:
 # Функция для создания нового словаря с аудио файлами
    def create_audio_dictionary(input_dict):
        new_dict = {}
        for english_word, russian_translation in input_dict.items():
        # Генерация аудио файла
            tts = gTTS(english_word, lang='en')
            audio_file_path = f'AUDIO/{key}/{english_word}.mp3'
            os_path = f'AUDIO/{key}'
            dir_path = f'AUDIO/{key}'
            if not os.path.exists(os_path):
                os.makedirs(dir_path)
            tts.save(audio_file_path)

        # Добавление в новый словарь
            new_dict[english_word] = [russian_translation, audio_file_path]

        return new_dict


# Создание нового словаря с аудио файлами

    audio_words_dictionary[key] = create_audio_dictionary(words_dictionary[key])



with open('audio_words.json', 'w', encoding='utf-8') as f:
    json.dump(audio_words_dictionary, f, ensure_ascii=False, indent=4)




with open('audio_words.json', 'r', encoding='utf-8') as f:
    loaded_dictionary = json.load(f)

# Вывод результата для проверки
for category, dict in loaded_dictionary.items():
    for key, value in dict.items():
        print(f"{category}:\n {key} : {value}")

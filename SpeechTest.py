import pyaudio
import speech_recognition as sr

def listen_and_recognize():
    # Инициализация распознавателя речи
    recognizer = sr.Recognizer()

    # Использование микрофона для захвата входящего звука
    with sr.Microphone() as source:
        print("Please speak now...")
        audio = recognizer.listen(source)

        try:
            # Использование Google Web Speech API для распознавания речи
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    listen_and_recognize()



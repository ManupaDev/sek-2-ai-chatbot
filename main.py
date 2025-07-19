from dotenv import load_dotenv
import os
from openai import OpenAI
# import speech_recognition as sr
import pyttsx3

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)
# recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak_response(text):
    print(f"AI Response: {text}")
    engine.say(text)
    engine.runAndWait()


def get_ai_response(messages):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        ai_response = completion.choices[0].message.content
        return ai_response
    except Exception as e:
        print(f"Error getting response from openai: {e}")


# def listen_for_query():
#     with sr.Microphone() as source:
#         print("Listening... Speak your query now.")
#         recognizer.adjust_for_ambient_noise(source, duration=1)
#         try:
#             audio = recognizer.listen(source, timeout=10)
#             print("Proceesing speech...")
#             query = recognizer.recognize_google(audio)
#             print(query)
#             return query
#         except sr.WaitTimeoutError:
#             print("No speech detected within timeout period.")
#             return None
#         except sr.UnknownValueError:
#             print("Could not understand audio")
#             return None
#         except sr.RequestError as e:
#             print(f"Could not request results; {e}")
#             return None



messages = [{"role": "developer", "content": "You are a helpful assistant."}]

while True:
    query = input("Enter what you want to ask from the AI Assistant: ").lower().strip()
    # query = listen_for_query()
    messages.append({"role": "user", "content": query})

    ai_response = get_ai_response(messages)
    messages.append({"role": "assistant", "content": ai_response})

    speak_response(ai_response)
    if query == "goodbye":
        break
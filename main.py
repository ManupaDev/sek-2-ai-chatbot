import speech_recognition as sr
import openai
import pyttsx3

# Put the OPENAI API key here. You can find it in the Resources.
openai.api_key = ""

recognizer = sr.Recognizer()

engine = pyttsx3.init()

def get_ai_reponse(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages = messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print(e)
        print(f"Error getting response from openai")

def listen_for_prompt():
    with sr.Microphone() as source:
        print("Listening... Speak your prompt now.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=10)
            print("Processing speech...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("No speech detected within timeout period.")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None

def speak_response(text):
    print(f"AI response: {text}")
    engine.say(text)
    engine.runAndWait()

def display_menu():
    """Display the main menu"""
    print("\n===== Voice-Enabled AI Chatbot =====")
    print("1. Start a conversation")
    print("2. Exit")
    choice = input("Enter your choice (1-2): ")
    return choice


print("Welcome to the Voice-Enabled AI Chatbot!")
print("Make sure your microphone is connected and working.")
while True:
    choice = display_menu()
    print(choice)
    if choice == "1":
        print("Starting conversation. Say 'goodbye' to end the session.")
        messages=[{"role":"system", "content":"You are a helpful assistant."}]

        while True:
            prompt = listen_for_prompt()

            if prompt is None:
                print("Let's try again.")
                continue

            if "goodbye" in prompt.lower():
                speak_response("Goodbye! Have a great day.")
                break

            messages.append({"role":"user", "content":prompt})
            ai_response = get_ai_reponse(messages)
            messages.append({"role":"assistant", "content":ai_response})
            speak_response(ai_response)

    elif choice == "2":
        print("Thank you for using the Voice-Enabled AI Chatbot. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")




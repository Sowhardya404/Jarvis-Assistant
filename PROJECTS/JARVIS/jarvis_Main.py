import os
import re
import time
import webbrowser
import requests
import pyttsx4
import speech_recognition as sr
from dotenv import load_dotenv
import datetime
from weather import get_weather
import platform
import ctypes


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out.")
        except sr.UnknownValueError:
            print("Sorry, I could not understand.")
        except sr.RequestError:
            print("Sorry, there was an issue with the speech recognition service.")
        return None


def get_current_time():
    now = datetime.datetime.now()
    return now.strftime("It's %I:%M %p") 

def get_current_date():
    today = datetime.date.today()
    return f"Today's date is {today.strftime('%B %d, %Y')}" 


# Load environment variables
load_dotenv()

# OpenRouter Client (Perplexity)
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("PERPLEXITY_API_KEY"),
    base_url="https://api.perplexity.ai"
)

conversation_history = [
    {"role": "system", "content": "You are a helpful AI assistant named Jarvis. You provide concise and accurate answers."}
]
MAX_CONVERSATION_MESSAGES = 10

# Initialize TTS and recognizer
engine = pyttsx4.init()
recognizer = sr.Recognizer()

def clean_llm_output(text):
    text = re.sub(r'^\s*\|.*\|\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'(\*\*|\*|__|_)', '', text)
    text = text.replace('`', '')
    text = re.sub(r'\[[^\[\]\n]+\]', '', text)
    text = re.sub(r' +', ' ', text)
    text = re.sub(r' +([.,:;?!])', r'\1', text)
    text = re.sub(r'^\s*[-•–]+\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n{2,}', '\n', text)
    return text.strip()

def speak(text):
    cleaned_text = clean_llm_output(text)
    print("Jarvis:", cleaned_text)
    engine.say(cleaned_text)
    engine.runAndWait()

def get_global_news():
    news_api_key = os.getenv("NEWSAPI_KEY")
    if not news_api_key:
        speak("News API key is missing. Please set NEWSAPI_KEY in your .env file.")
        return

    url = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=5&apiKey={news_api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if data["status"] == "ok":
            articles = data["articles"]
            speak("Here are the top global news headlines.")
            for i, article in enumerate(articles[:5]):
                title = article["title"]
                print(f"{i + 1}. {title}")
                speak(title)
        else:
            speak("Sorry, I couldn't fetch the news.")
            print("NewsAPI Error:", data.get("message"))
    except Exception as e:
        speak("An error occurred while fetching news.")
        print("News Fetch Error:", e)

def get_openai_response(prompt):
    global conversation_history
    conversation_history.append({"role": "user", "content": prompt})
    if len(conversation_history) > MAX_CONVERSATION_MESSAGES:
        conversation_history = [conversation_history[0]] + conversation_history[-(MAX_CONVERSATION_MESSAGES - 1):]
    
    try:
        response = client.chat.completions.create(
            model="sonar-pro",
            messages=conversation_history
        )
        reply = response.choices[0].message.content.strip()
        conversation_history.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        print("Perplexity API Error:", e)
        if conversation_history and conversation_history[-1]["role"] == "user":
            conversation_history.pop()
        return "Sorry, I couldn't get a response at the moment."

def processCommand(command):
    command = command.lower()
    if "time" in command:
        speak(get_current_time())
        return

    elif "date" in command:
        speak(get_current_date())
        return

    elif "open google" in command:
        webbrowser.open("https://www.google.co.in/")
        speak("Opening Google")

    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com/")
        speak("Opening YouTube")

    elif "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com/")
        speak("Opening WhatsApp")

    elif command.startswith("play"):
        from musiclibrary import play_song
        song = command.replace("play", "").strip()
        speak(play_song(song))

    elif "pause music" in command:
        from musiclibrary import pause_music
        speak(pause_music())

    elif "resume music" in command:
        from musiclibrary import resume_music
        speak(resume_music())

    elif "stop music" in command:
        from musiclibrary import stop_music
        speak(stop_music())

    elif "tell me news" in command or "news" in command:
        get_global_news()

    elif "wait" in command:
        speak("Okay, I will wait for a moment.")
        time.sleep(10)  # Pause for 10 seconds
    elif any(phrase in command for phrase in ["stop", "shutdown", "exit", "jarvis stop"]):
        speak("Stopping Jarvis. Goodbye!")
        exit(0)
    
    # Shutdown
    elif "shutdown" in command:
        speak("Shutting down the system.")
        if platform.system() == "Windows":
            os.system("shutdown /s /t 1")
        elif platform.system() == "Linux":
            os.system("shutdown now")

    # Restart
    elif "restart" in command:
        speak("Restarting the system.")
        if platform.system() == "Windows":
            os.system("shutdown /r /t 1")
        elif platform.system() == "Linux":
            os.system("reboot")

    # Lock Screen
    elif "lock screen" in command or "lock the screen" in command:
        speak("Locking the screen.")
        if platform.system() == "Windows":
            ctypes.windll.user32.LockWorkStation()
        elif platform.system() == "Linux":
            os.system("gnome-screensaver-command -l")

    # Volume Control
    elif "volume up" in command:
        from jarvis_controls import increase_volume
        increase_volume()
        speak("Volume increased.")

    elif "volume down" in command:
        from jarvis_controls import decrease_volume
        decrease_volume()
        speak("Volume decreased.")

    # Brightness Control
    elif "brightness up" in command:
        from jarvis_controls import increase_brightness
        increase_brightness()
        speak("Brightness increased.")

    elif "brightness down" in command:
        from jarvis_controls import decrease_brightness
        decrease_brightness()
        speak("Brightness decreased.")

    # Open Applications
    elif "open" in command:
        app_name = command.replace("open", "").strip()
        from jarvis_controls import open_application
        response = open_application(app_name)
        speak(response)
    
    elif "weather" in command:
        WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
        speak("Which city?")
        city = listen()
        print("City received:", city)
        weather_report = get_weather(city, WEATHER_API_KEY)
        speak(weather_report)
        return

    else:
        speak("Let me think...")
        reply = get_openai_response(command)
        speak(reply)

def listen_for_command():
    try:
        with sr.Microphone() as source:
            print("Listening for the wake word 'Jarvis'...")
            recognizer.adjust_for_ambient_noise(source)
            speak("Listening now.")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            if any(phrase in text.lower() for phrase in ["stop", "shutdown", "exit", "wait", "jarvis stop", "jarvis wait"]):
                processCommand(text.lower())
                return

            # Wake word check and command extraction
            wake_phrases = ["jarvis", "hey jarvis", "ok jarvis", "hello jarvis"]
            if any(phrase in text.lower() for phrase in wake_phrases):
                speak("Wake word detected. Hi Sowhardya.")

                # Remove wake phrase to extract command
                for phrase in wake_phrases:
                    text = text.lower().replace(phrase, "").strip()

                if text:
                    print("Command extracted:", text)
                    processCommand(text)
                else:
                    with sr.Microphone() as source2:
                        recognizer.adjust_for_ambient_noise(source2)
                        speak("Listening now.")
                        audio2 = recognizer.listen(source2, timeout=5, phrase_time_limit=8)
                        command = recognizer.recognize_google(audio2)
                        print("Command received:", command)
                        processCommand(command)
            else:
                print("No wake word detected.")
    except sr.WaitTimeoutError:
        print("No input detected.")
    except sr.UnknownValueError:
        print("Could not understand audio.")
        speak("I didn't understand that.")
    except sr.RequestError as e:
        print("Network error:", e)
        speak("Network issue. Please check your connection.")
    except Exception as e:
        print("Microphone Error:", e)
        speak("There was an error with the microphone.")
    finally:
        time.sleep(1)  # Prevent CPU overuse

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        listen_for_command()
        # After wake word, stay in conversation until "stop" is said
        while True:
            command = listen()
            if command is None:
                continue
            if any(word in command for word in ["stop", "exit", "shutdown", "jarvis stop"]):
                speak("Okay, stopping conversation. Say 'Jarvis' to wake me again.")
                break  # Go back to wake word mode
            else:
                processCommand(command)

import speech_recognition as sr
import pyttsx3
import requests
import datetime
import time
import threading

# --- Configuration ---
# Replace with your actual API keys
OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY" # Get from https://openweathermap.org/api
NEWSAPI_API_KEY = "YOUR_NEWSAPI_API_KEY"       # Get from https://newsapi.org/

# --- Initialize Speech Recognizer and Text-to-Speech Engine ---
r = sr.Recognizer()
engine = pyttsx3.init()

# Configure voice properties (optional)
voices = engine.getProperty('voices')
# You can try different voices if available
# for voice in voices:
#     print(f"ID: {voice.id}, Name: {voice.name}, Lang: {voice.languages}")
# engine.setProperty('voice', voices[0].id) # Set a specific voice if desired (e.g., voices[0].id for male, voices[1].id for female)
engine.setProperty('rate', 180) # Speed of speech
engine.setProperty('volume', 0.9) # Volume (0.0 to 1.0)

# --- Global Variables for Reminders ---
reminders = []
reminder_check_interval = 10 # Check for reminders every 10 seconds

# --- Helper Functions ---

def speak(text):
    """Converts text to speech and plays it."""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen_for_command():
    """
    Listens for audio input from the microphone and converts it to text.
    Returns:
        str: The recognized text, or None if recognition fails.
    """
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1) # Adjust for ambient noise
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5) # Listen for up to 5 seconds
            print("Recognizing...")
            command = r.recognize_google(audio).lower() # Using Google Web Speech API
            print(f"You said: {command}")
            return command
        except sr.WaitTimeoutError:
            print("No speech detected within timeout.")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
            speak("Sorry, I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            speak("My speech service is currently unavailable. Please check your internet connection.")
            return None

def get_weather(city):
    """Fetches current weather information for a given city."""
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(complete_url)
        data = response.json()

        if data["cod"] == 200: # Check if API call was successful
            main = data["main"]
            weather_desc = data["weather"][0]["description"]
            temperature = main["temp"]
            humidity = main["humidity"]

            speak(f"The weather in {city} is {weather_desc}, with a temperature of {temperature:.1f} degrees Celsius and humidity of {humidity} percent.")
        else:
            speak(f"Sorry, I couldn't find weather information for {city}. Please check the city name.")
    except requests.exceptions.RequestException as e:
        speak(f"I'm having trouble connecting to the weather service. Please check your internet connection. Error: {e}")
    except Exception as e:
        speak(f"An unexpected error occurred while fetching weather. Error: {e}")

def get_news(category="general"):
    """Fetches top news headlines for a given category."""
    base_url = "https://newsapi.org/v2/top-headlines?"
    # You can specify country, e.g., 'us' for United States news
    params = {
        "apiKey": NEWSAPI_API_KEY,
        "category": category,
        "language": "en",
        "pageSize": 5 # Get top 5 headlines
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data["status"] == "ok" and data["articles"]:
            speak(f"Here are the top {category} headlines:")
            for i, article in enumerate(data["articles"]):
                speak(f"Headline {i+1}: {article['title']}")
                # Optional: Open article in browser
                # import webbrowser
                # webbrowser.open(article['url'])
                time.sleep(1) # Pause between headlines
        else:
            speak(f"Sorry, I couldn't find any news for the '{category}' category or there was an issue with the news service.")
    except requests.exceptions.RequestException as e:
        speak(f"I'm having trouble connecting to the news service. Please check your internet connection. Error: {e}")
    except Exception as e:
        speak(f"An unexpected error occurred while fetching news. Error: {e}")

def set_reminder():
    """Guides the user to set a reminder."""
    speak("What should I remind you about?")
    task = listen_for_command()
    if not task:
        return

    speak("And when should I remind you? For example, 'tomorrow at 5 PM' or 'in 10 minutes'.")
    time_str = listen_for_command()
    if not time_str:
        return

    # Simple time parsing (can be improved for more complex inputs)
    reminder_time = None
    now = datetime.datetime.now()

    try:
        if "tomorrow" in time_str:
            date_part = (now + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            time_part_match = re.search(r'at (\d{1,2}(?::\d{2})?\s*(?:am|pm)?)', time_str)
            if time_part_match:
                time_part = time_part_match.group(1).replace(' ', '').upper()
                # Handle 'PM' conversion
                if 'PM' in time_part and ':' not in time_part:
                    hour = int(time_part.replace('PM', ''))
                    if hour < 12: hour += 12
                    time_part = f"{hour}:00"
                elif 'AM' in time_part and ':' not in time_part:
                    hour = int(time_part.replace('AM', ''))
                    time_part = f"{hour}:00"
                reminder_time = datetime.datetime.strptime(f"{date_part} {time_part}", '%Y-%m-%d %I:%M%p')
            else:
                speak("I couldn't understand the time for tomorrow. Please be more specific.")
                return
        elif "in" in time_str and "minutes" in time_str:
            minutes_match = re.search(r'in (\d+) minutes', time_str)
            if minutes_match:
                minutes = int(minutes_match.group(1))
                reminder_time = now + datetime.timedelta(minutes=minutes)
            else:
                speak("I couldn't understand the number of minutes. Please try again.")
                return
        elif "at" in time_str: # Try to parse a specific time today
            time_only_str = time_str.split("at")[-1].strip()
            # Try various common time formats
            formats = ["%I %p", "%I:%M %p", "%H:%M"]
            for fmt in formats:
                try:
                    parsed_time = datetime.datetime.strptime(time_only_str, fmt).time()
                    reminder_time = now.replace(hour=parsed_time.hour, minute=parsed_time.minute, second=0, microsecond=0)
                    if reminder_time < now: # If time is already past today, set for tomorrow
                        reminder_time += datetime.timedelta(days=1)
                    break
                except ValueError:
                    continue
            if not reminder_time:
                speak("I couldn't understand the time. Please try a format like 'at 5 PM' or 'at 14:30'.")
                return
        else:
            speak("I couldn't understand the time you specified. Please try again with a clear time.")
            return

    except Exception as e:
        print(f"Error parsing time: {e}")
        speak("I had trouble understanding the time you provided. Please try again.")
        return

    if reminder_time:
        reminders.append({"task": task, "time": reminder_time, "set_time": now})
        speak(f"Okay, I'll remind you to {task} on {reminder_time.strftime('%B %d at %I:%M %p')}.")
    else:
        speak("I couldn't set the reminder. Please provide a clearer time.")

def check_reminders():
    """Checks and announces active reminders."""
    global reminders
    while True:
        now = datetime.datetime.now()
        reminders_to_remove = []
        for i, reminder in enumerate(reminders):
            if now >= reminder["time"]:
                speak(f"Reminder: It's time to {reminder['task']}!")
                reminders_to_remove.append(i)
        
        # Remove announced reminders in reverse order to avoid index issues
        for index in sorted(reminders_to_remove, reverse=True):
            del reminders[index]
        
        time.sleep(reminder_check_interval)

# Start reminder checking in a separate thread
reminder_thread = threading.Thread(target=check_reminders, daemon=True)
reminder_thread.start()

# --- Main Assistant Loop ---
def start_assistant():
    """Main loop for the personal assistant."""
    speak("Hello! I am your personal assistant. How can I help you today?")
    import re # Import regex here to avoid circular dependency if not used before

    while True:
        command = listen_for_command()

        if command:
            if "hello" in command or "hi assistant" in command:
                speak("Hello there! How can I assist you?")
            elif "what is your name" in command:
                speak("I am your personal assistant, designed to help you.")
            elif "set a reminder" in command or "remind me" in command:
                set_reminder()
            elif "check weather" in command or "what's the weather" in command:
                speak("Which city would you like the weather for?")
                city = listen_for_command()
                if city:
                    get_weather(city)
                else:
                    speak("I didn't hear a city name. Please try again.")
            elif "read news" in command or "tell me the news" in command:
                speak("What kind of news are you interested in? For example, 'technology', 'sports', or 'general'.")
                category = listen_for_command()
                if category:
                    get_news(category)
                else:
                    get_news("general") # Default to general news
            elif "stop" in command or "exit" in command or "goodbye" in command:
                speak("Goodbye! Have a great day!")
                break
            else:
                speak("I'm sorry, I don't understand that command yet. Please try saying 'set a reminder', 'check weather', or 'read news'.")

if __name__ == "__main__":
    # Ensure API keys are set before running
    if OPENWEATHER_API_KEY == "YOUR_OPENWEATHER_API_KEY" or NEWSAPI_API_KEY == "YOUR_NEWSAPI_API_KEY":
        print("\n--- IMPORTANT ---")
        print("Please replace 'YOUR_OPENWEATHER_API_KEY' and 'YOUR_NEWSAPI_API_KEY' with your actual API keys.")
        print("You can get them from: https://openweathermap.org/api and https://newsapi.org/")
        print("The assistant will not function correctly without valid API keys.")
        print("-----------------\n")
        # Optionally, you can exit here or proceed with limited functionality
        # exit()

    start_assistant()

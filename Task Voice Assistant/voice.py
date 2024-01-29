import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def main():
    speak("Hello! How can I assist you today?")
    
    while True:
        command = get_command()

        if "hello" in command:
            speak("Hello! How can I help you?")
        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%H:%M")
            speak(f"The current time is {current_time}")
        elif "date" in command:
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            speak(f"Today's date is {current_date}")
        elif "search" in command:
            query = command.replace("search", "").strip()
            search_url = f"https://www.google.com/search?q={query}"
            speak(f"Searching the web for {query}")
            webbrowser.open(search_url)
        elif "exit" in command:
            speak("Goodbye!")
            break
        else:
            speak("Sorry, I don't understand that command. Can you please repeat?")
            
if __name__ == "__main__":
    main()

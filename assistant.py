import pyttsx3, speech_recognition as sr, wikipedia, cv2, numpy as np,webbrowser
import os, requests, pyjokes,shutil,time, operator, random
from googletrans import Translator
from datetime import datetime
from bs4 import BeautifulSoup
from quotes_library import get_quotes

MASTER = "manas"
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
reminders = []

def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning " + MASTER)
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon " + MASTER)
    else:
        speak("Good Evening " + MASTER)

    speak("I am Wolverine. How may I help you?")

def takecommand():
    r = sr.Recognizer()
    try:
        mic_names = sr.Microphone.list_microphone_names()
        if mic_names:  
            with sr.Microphone() as source:
                speak("Listening...")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                
            speak("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            speak(f"user said: {query}\n")
            return query
        else:
            #speak("No microphone found. Please type your command:")
            query = input("You: ")
            speak(f"user typed: {query}\n")
            return query
        
    except OSError as e:
        #speak("No microphone available, please type your command.")
        query = input("You: ")
        #print(f"user typed: {query}\n")
        return query
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand that.")
        return None
    except sr.RequestError:
        speak("Sorry, there was an issue with the speech service.")
        return None

def set_reminder():
    speak("What do you want to be reminded about?")
    task = takecommand()
    speak("When should I remind you? for example 27 November 2024 11:53:00 AM")
    time_str = takecommand() 
     # Remove ordinal suffixes like 'st', 'nd', 'rd', 'th' from the date part of the input
    time_str = time_str.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "")
    try:
        # Parse the date-time string (e.g., '27 November 2024 11:31:00 AM')
        reminder_time = datetime.strptime(time_str, "%d %B %Y %I:%M:%S %p")
    except ValueError:
        try:
            reminder_time = datetime.strptime(time_str, "%d %B %Y %I:%M %p")  # If no seconds are provided
        except ValueError:
            speak("Sorry, I couldn't understand the date and time format. Please try again.")
            return
        
    reminders.append({'task': task, 'time': reminder_time})
    speak(f"Reminder set: {task} at {reminder_time.strftime('%I:%M %p')} on {reminder_time.strftime('%dth %B %Y')}.")

def check_reminders():
    current_time = datetime.now()
    for reminder in reminders:
        if current_time >= reminder['time']:
            speak(f"Reminder: {reminder['task']}")
            reminders.remove(reminder)

def track_motion():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():

        speak("No camera detected. Using a sample video.")  
        cap = cv2.VideoCapture("D:\\video\855564-hd_1920_1080_24fps.mp4")  #..................................

        if not cap.isOpened():
            speak("Sample video not found.")
            return  
    back_sub = cv2.createBackgroundSubtractorMOG2(history=700, varThreshold=25, detectShadows=True)
    kernel = np.ones((20, 20), np.uint8)

    while True:
        ret, frame = cap.read()

        if not ret:
            speak("Failed to capture frame.")
            break  

        fg_mask = back_sub.apply(frame)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
        fg_mask = cv2.medianBlur(fg_mask, 5)
        _, fg_mask = cv2.threshold(fg_mask, 127, 255, cv2.THRESH_BINARY)

        contours, hierarchy = cv2.findContours(fg_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        areas = [cv2.contourArea(c) for c in contours]

        if len(areas) < 1:
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue
        else:
            max_index = np.argmax(areas)
        cnt = contours[max_index]
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        x2 = x + int(w / 2)
        y2 = y + int(h / 2)
        cv2.circle(frame, (x2, y2), 4, (0, 255, 0), -1)
        text = f"x: {x2}, y: {y2}"
        cv2.putText(frame, text, (x2 - 10, y2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def check_weather():
    speak("tell me the location")
    api_key = str("b4423b61c6748cb7b0f4d33197adb664")
    location = takecommand()
    complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q=" + location + "&appid=" + api_key
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()
    temp_city = int(((api_data['main']['temp']) - 273.15))
    weather_desc = api_data['weather'][0]['description']
    hmdt = api_data['main']['humidity']
    wind_spd = api_data['wind']['speed']
    date_time = datetime.datetime.now().strftime("%d %b %Y | %I:%M:%S %p")
    speak(f"{MASTER} the current weather is temperature {temp_city} degree celcius . is {weather_desc} having humidity {hmdt} and {wind_spd} at {date_time}")

def translate_text(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text

def get_news():
    speak("Fetching the latest news...")
    url = 'https://www.thehindu.com/news'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find('body').find_all('h3')
    news_info = ""  
    count = 0  
    for x in headlines:
        news_info += x.text.strip()  
        count += 1
        if count == 5:
            break 
    speak(news_info)

def get_random_trivia():
    url = "https://opentdb.com/api.php?amount=3&type=multiple"  # You can specify the number of questions here
    response = requests.get(url)
    data = response.json()

    questions = []
    for item in data['results']:
        question = item['question']
        correct_answer = item['correct_answer']
        options = item['incorrect_answers'] + [correct_answer]
        random.shuffle(options)
        questions.append({
            "question": question,
            "answer": correct_answer,
            "options": options
        })
    return questions

def trivia_game():
    score = 0
    # Fetch random trivia questions
    questions = get_random_trivia()
    
    for question in questions:
        speak(question["question"])
        # Speak available options if you want to
        for idx, option in enumerate(question["options"], 1):
            speak(f"Option {idx}: {option}")
        
        answer = takecommand().lower()
        if answer == question["answer"].lower():
            score += 1
            speak("Correct!")
        else:
            speak(f"Wrong! The correct answer is {question['answer']}.")
    
    speak(f"Game Over! Your score is {score} out of {len(questions)}.")

def start_trivia():
    speak("Let's play a trivia game!")
    trivia_game()

def calculate(query):
    operators = {
        'add': operator.add,
        'subtract': operator.sub,
        'multiply': operator.mul,
        'divide': operator.truediv
    }
    words = query.split()
    if 'and' in words:
        operator_word = words[0]
        num1 = float(words[1])
        num2 = float(words[3])

        if operator_word in operators:
            result = operators[operator_word](num1, num2)
            return result
        else:
            return "Sorry, I couldn't understand the operation."
    else:
        return "Sorry, I couldn't understand the query format."

def voice_calculator():
    speak("What calculation would you like to do? Example: 'add 5 and 3'.")
    query = takecommand()
    result = calculate(query)
    speak(f"The result is: {result}")

def change_voice():
    speak("Would you like to change the voice? Say 'yes' to continue.")
    response = takecommand().lower()
    
    if 'yes' in response:
        speak("What voice would you prefer? Male or female?")
        gender = takecommand().lower()
        voices = engine.getProperty('voices')
        
        if 'male' in gender:
            engine.setProperty('voice', voices[0].id)
            speak("Voice changed to male.")
        elif 'female' in gender:
            engine.setProperty('voice', voices[1].id)
            speak("Voice changed to female.")
        else:
            speak("Sorry, I didn't understand. Keeping the default voice.")

def give_motivation():
    quotes = get_quotes(category='inspirational', count=1, random=True)  # Fetch random quote
    quote_text = quotes['data'][0]['quote']
    speak(quote_text)

def handle_query(query):

    if 'wikipedia' in query.lower():
        speak('searching wikipedia...')
        query = query.replace("wikipedia","")
        try:
            results = wikipedia.summary(query, sentences=3)
            speak(results)
        except wikipedia.exceptions.DisambiguationError as e:
            speak(f"There are multiple results for {query}, please be more specific.")
        except wikipedia.exceptions.HTTPTimeoutError:
            speak("I'm unable to access Wikipedia. Please check your internet connection.")
        except Exception as e:
            speak("Sorry, I couldn't find information on that.")

    elif 'translate' in query.lower():
        speak("What phrase would you like to translate?")
        phrase = takecommand()
        speak("Which language do you want to translate to?")
        language = takecommand()  
        translated_phrase = translate_text(phrase, language)
        speak(f"The translation is: {translated_phrase}")

    elif 'open youtube' in query.lower():
        speak('Opening YouTube...')
        webbrowser.open("youtube.com")

    elif 'calculate' in query.lower():
        voice_calculator()

    elif 'quotes' in query.lower():
        give_motivation()

    elif 'change your voice' in query.lower():
        change_voice()

    elif 'news' in query.lower():
        get_news()

    elif 'play' in query.lower():
        start_trivia()

    elif 'open google' in query.lower():
        speak('Opening Google...')
        webbrowser.open("google.com")

    elif 'search on google' in query.lower():
        speak("What should I search on Google?")
        cm = takecommand().lower()
        webbrowser.open(f"https://www.google.com/search?q={cm}")

    elif 'track me' in query.lower():
            speak("tracking you")
            track_motion()
    
    elif 'open instagram' in query.lower():
            speak('just wait a second sir...')
            url = "instagram.com"
            chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            webbrowser.get(chrome_path).open(url)

    elif 'play music' in query.lower():
        speak("Playing music")
        songs_dir = "D:\\music"
        if not os.path.exists(songs_dir):
            speak("The music directory was not found.")
        else:
            songs = os.listdir(songs_dir)
            if songs:
                os.startfile(os.path.join(songs_dir, songs[0]))
            else:
                speak("No songs found in the music directory.")
    
    elif 'set a reminder' in query.lower():
        set_reminder()

    elif 'shut down the system' in query.lower():
        os.system("shutdown /s /t 5")

    elif 'restart the system' in query.lower():
        os.system("shutdown /r /t 5")

    elif 'sleep the system' in query.lower():
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    elif 'the time' in query.lower():
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"{MASTER}, the time is {strTime}")
    
    elif 'current weather' in query.lower():
           check_weather()
            
    elif 'tell me a joke' in query.lower():
        joke = pyjokes.get_joke()
        speak(joke)

    elif 'nothing' in query.lower():
        speak("Okay, no problem.")
    
    elif 'hello' in query.lower():
        speak("hello, how you doin?")
    
    elif 'open file' in query.lower():
        speak("What is the file name you want to open?")
        file_name = takecommand()
        try:
            os.startfile(file_name)
            speak(f"Opening {file_name}...")
        except:
            speak("Sorry, I couldn't find that file.")
    
    elif 'rename file' in query.lower():
        speak("What file do you want to rename?")
        old_name = takecommand()
        speak("What should be the new name?")
        new_name = takecommand()
        try:
            os.rename(old_name, new_name)
            speak(f"File renamed to {new_name}")
        except:
            speak("Sorry, I couldn't rename the file.")
    
    elif 'move file' in query.lower():
        speak("What file would you like to move?")
        file_name = takecommand()
        speak("Where do you want to move it?")
        destination = takecommand()
        try:
            shutil.move(file_name, destination)
            speak(f"Moved {file_name} to {destination}.")
        except:
            speak("Sorry, I couldn't move the file.")
    
    elif 'delete file' in query.lower():
        speak("What file do you want to delete?")
        file_name = takecommand()
        try:
            os.remove(file_name)
            speak(f"File {file_name} deleted successfully.")
        except:
            speak("Sorry, I couldn't delete the file.")

    elif 'goodbye' in query.lower():
        speak("Going offline.")
        exit()

    else:
        try:
            results = wikipedia.summary(query, sentences = 3)
            speak(results)  
        except:
            speak("try, with other query")
            return 

def main():
    speak("Initializing Wolverine...")
    wishMe()
    while True:
        query = takecommand()
        check_reminders() 
        if query:
            handle_query(query)           
        #time.sleep(60)

main()

import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import time
import requests
import json
from AppOpener import run

dictionary = json.load(open('dictionary_compact.json'))

# weather
base_url_weather = "http://api.openweathermap.org/data/2.5/weather?appid="
weather_api = open("api_key.txt", "r").read()
city = ""

#news
base_url_news = "https://newsapi.org/v2/top-headlines?country=in&apiKey="
news_api=open("news_api_key.txt","r").read()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 190)


# coverts string into speech
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# wishes the user
def wishme():
    hour = datetime.datetime.now().hour
    if 0 <= hour <= 12:
        print("Good morning Boss!waiting for your command")
        speak("Good morning Boss!waiting for your command")
    elif 12 < hour <= 16:
        print("Good Afternoon Boss!waiting for your command")
        speak("Good afternoon Boss!waiting for your command")
    else:
        print("Good Evening Boss!waiting for your command")
        speak("Good evening Boss!waiting for your command")


# takes microphone i/p and returns string
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source, phrase_time_limit=5)
        r.pause_threshold = 0.5
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"Boss your command is:{query}\n")
    except:
        print("Sorry boss!can't get you")
        return "None"
    return query


def take_city():
    print("Enter the place:")
    city = input()
    return city

if __name__ == '__main__':
    wishme()
    while True:
        data = take_command().lower()
        if 'about' in data:
            speak("searching in wikipedia...")
            data.replace("about ", "")
            results = wikipedia.summary(data, sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)
            # exit()
        elif "search" in data:
            speak("searching")
            data = data.replace("search ", "")
            print(data)
            webbrowser.open(data)
            exit()
        elif "time" in data:
            data = datetime.datetime.now().strftime("%H:%M:%S")
            print(data)
            speak(data)
            # exit()
        elif "blog" in data:
            webbrowser.open("mobilebloggerstelugu.blogspot.com")
            exit()
        elif "open" in data:
            data = data.replace("open ", "")
            run(data)
            #time.sleep(4)
        elif "meaning" in data:
            data = data.replace(" meaning", "")
            try:
                if data in dictionary:
                    meaning = dictionary[data]
                    print(meaning)
                    speak(meaning)
                else:
                    raise WordNotFound
            except:
                # print("Can't understand,Try entering the word")
                # speak("Can't understand,Try entering the word")
                # if data in dictionary:
                #     meaning = dictionary[data]
                #     print(meaning)
                #     speak(meaning)
                # else:
                print("word doesn't exist")
        elif ("weather" in data) or ("climate" in data) or ("temperature" in data):
            print("Give the city name Boss!")
            city = take_command()
            url = base_url_weather + weather_api + "&q=" + city
            try:
                res = requests.get(url).json()
                print("place =", city)
                print("Temperature =", str(res["main"]["temp"] - 273) + "°C")
                print("Feels like =", str(res["main"]["feels_like"] - 273) + "°C")
                print("Humidity =", res["main"]["humidity"])
                print("Description =", res["weather"][0]["description"])
            except:
                print("can't find the place!")
        elif ("happening" in data) or ("latest" in data) or ("news" in data) or ("headlines" in data):
            url = base_url_news + news_api
            res=requests.get(url).json()
            for i in res["articles"]:
                print("Title =", i['title'])
                speak(i['title'])
                print("Description =", i['description'])
                time.sleep(10)
        elif "exit" in data:
            speak("Thank you Boss!")
            exit()

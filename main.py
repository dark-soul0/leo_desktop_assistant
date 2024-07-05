import datetime
import smtplib

import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install speechRecognition

from auth import faceauth
from gemini import gemini

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am leo Sir. Please tell me how may I help you")


def listen_for_wake_word():
    r = sr.Recognizer()
    r.energy_threshold = 300  # minimum audio energy to consider for recording
    r.dynamic_energy_threshold = True
    r.dynamic_energy_adjustment_damping = 0.15
    r.dynamic_energy_ratio = 1.5
    r.pause_threshold = 0.8  # seconds of non-speaking audio before a phrase is considered complete
    r.operation_timeout = None  # seconds after an internal operation (e.g., an API request) starts before it times out, or ``None`` for no timeout
    r.phrase_threshold = 0.3  # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
    r.non_speaking_duration = 0.5
    mic = sr.Microphone()

    while True:
        with mic as source:
            print("Listening for wake word...")
            r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = r.listen(source)  # Capture audio input

        try:
            print("Recognizing...")
            wake_word = r.recognize_google(audio, language='en-in')  # Perform recognition

            if "leo" in wake_word.lower():
                print(f"Wake word detected: {wake_word}\n")
                return wake_word.lower()  # Return wake word if recognized
            else:
                # Uncomment the line below for continuous listening without recursion
                # continue
                pass

        except sr.UnknownValueError:
            print("Could not understand the audio. Please try again.")
            return listen_for_wake_word()
        except sr.RequestError as e:
            print(f"Error fetching results from Google Speech Recognition service; {e}")
            return listen_for_wake_word()


def takeCommand():
    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        speak("Say that again please...")
        return "None"
    return query


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('sonu.samrat7668@gmail.com', 'Sk@Samrat1')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()


if __name__ == "__main__":
    wake = listen_for_wake_word()
    if "leo" in wake:
        # wishMe()
        userName = faceauth.recognize_faces()
        if userName:
            speak(f"hello {userName} how may i asssist you")
            while True:
                query = takeCommand().lower()
                if "open gemini" in query:
                    speak("openinig gemini what is your query.")
                    while True:
                        question = takeCommand()
                        print(question)
                        speak(f'{gemini(question)} whats your next query.')
                        if "exit" in query:
                            break

                elif "youtube" in query:
                    from scripts.youtube import *

                    speak("openning youtube")
                    youtube()
                    time.sleep(3)
                    speak("which song you want to listen")
                    song = takeCommand().lower()
                    if song == None:
                        # search_song(song)
                        speak("i didn't understand")
                        break
                    else:
                        try:
                            search_song(song)
                            time.sleep(7)
                            skip_ad()
                            yt = listen_for_wake_word()
                        except Exception as e:
                            print(e)
                            pass
                        if "leo" in yt.lower():
                            stop_song()
                            speak("how may i help you")
                            q = takeCommand()
                            if "next song" in q.lower():
                                play_next_song()
                            elif "search song" in q.lower():
                                speak("which song")
                                song = takeCommand().lower()
                                if song == None:
                                    speak("i didn't understand")
                                    break
                                else:
                                    search_song(song)

                            elif "pause" in q.lower():
                                stop_song()

                            elif "increase playback speed" in q.lower():
                                play_back_speed_i()

                            elif "decrease playback speed":
                                play_back_speed_d()
                            elif "exit" in q.lower():
                                break

                            else:
                                pass
                elif "exit" in query.lower():
                    speak(" okey have a good day")
                    break
        else:
            faceauth.Unknown_Face()

    else:
        pass

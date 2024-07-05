import pickle

import cv2 as cv
import face_recognition
import firebase_admin
import numpy as np
import pyttsx3
import speech_recognition as sr
from firebase_admin import credentials
from firebase_admin import firestore

from auth.encode import encode_and_upload_faces

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def listen_for_command():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for command...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        command = r.recognize_google(audio, language='en-in')
        print(f"User said: {command}\n")
        return command.lower()

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't understand that.")
        return ""


def Unknown_Face():
    cap = cv.VideoCapture(1)
    process_this_frame = True

    while True:
        ret, frame = cap.read()
        if process_this_frame:
            small_frame = cv.resize(frame, (0, 0), fx=0.5, fy=0.5)

            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
            face = face_recognition.face_encodings(rgb_small_frame)
            cv.imshow("test", small_frame)
            # cv.waitKey(0)
            if face:
                print("face detected..........")
                speak("Tell me your name Please")

                name = listen_for_command()
                if name:
                    success = cv.imwrite(f'{name}.jpg', frame)
                    if success:
                        encode_and_upload_faces()
                        print("saved successfully")
                        break
                    else:
                        print("some error occured")
                else:
                    Unknown_Face()
            else:
                print("no face......")
        if cv.waitKey(1) & 0xFF == ord('q'):
            print("you ch00se to exit.....")
            break
    cap.release()
    cv.destroyAllWindows()


def recognize_faces():
    options = {
        'databaseURL': "your database url",
        'storageBucket': "your storageBucket link"
    }

    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, name="leo assist", options=options)

    # Initialize Firestore database
    db = firestore.client(firebase_admin.get_app("leo assist"))
    # bucket = storage.bucket()
    # loading encode file
    print("loading encode file")
    file = open("Known_encodings.p", 'rb')
    Known_EncodingWithName = pickle.load(file)
    file.close()
    Known_encodings, userName = Known_EncodingWithName
    print("encode file loaded")

    cam = cv.VideoCapture(1)

    face_locations = []
    face_encodings = []
    face_names = []
    Process_this_frame = True

    while True:
        ret, frame = cam.read()
        if Process_this_frame:
            # resize the frame
            small_frame = cv.resize(frame, (0, 0), fx=0.5, fy=0.5)
            cv.imshow('face recogination', frame)

            # convert BGR to RGB
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

            face_currentFrame = face_recognition.face_locations(rgb_small_frame)
            encodeCurrentFrame = face_recognition.face_encodings(rgb_small_frame, face_currentFrame)

            for encodeFace, faceLoc in zip(encodeCurrentFrame, face_currentFrame):
                matches = face_recognition.compare_faces(Known_encodings, encodeFace)
                faceDis = face_recognition.face_distance(Known_encodings, encodeFace)
                print(matches)
                print(faceDis)
                matchindex = np.argmin(faceDis)

                if matches[matchindex]:
                    speak(userName[matchindex])
                    return userName[matchindex]
                else:
                    speak("unknown face")
                    Unknown_Face()
                    recognize_faces()

        if cv.waitKey(1) & 0xFF == ord('q'):
            print("you ch00se to exit.....")
            break

    cam.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    recognize_faces()

import speech_recognition as sr
import pyttsx3
import pyaudio
import datetime




#Creating Instances of Class Recognizer() and Text-to-Speech engine init()
recognizer = sr.Recognizer()
engine = pyttsx3.init()

#Greet The User According to Current Time
def greet():
    hour = int(datetime.datetime.now().hour)
    if hour>0 and hour<12:
          speak("Good morning, sir. Ready to start your day?")
    elif hour>=12 and hour<18:
          speak("Good afternoon, sir. How can I be of assistance?")
    else:
          speak("Good evening, sir. How can I assist you tonight?")

#Listen For Wake word(Jarvis) and Take input in Form of Audio from Microphone
def listen_wake_word():
    #The loop ensures that your program keeps running and listening for the keyword “Jarvis”. Without the loop, the program would stop after processing the first command.
    while True:
        try:
            #Listen For Wake word(Jarvis) and Take input in Form of Audio from Microphone 
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                recognizer.pause_threshold = 1
                audio = recognizer.listen(source,timeout=5,phrase_time_limit=2)

            wake = recognizer.recognize_google(audio)
        
            if("jarvis" in wake.lower()):
                greet()
                break
        except sr.UnknownValueError:
                print("Sorry, I did not understand that.")
        except Exception as e:
                print(e) 
       

#Takes Command From the User
def take_command(timeout,phrase_time_limit):
    try:
     #Listen for command from user
        with sr.Microphone() as source:
            print("Give Command")
            audio = recognizer.listen(source,timeout,phrase_time_limit)
            print("Listening.Just a Moment...")
            command = recognizer.recognize_google(audio)
            return command
    except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
    except sr.RequestError as e:
            print(f"Could not request results; {e}")
    except Exception as e:
            print(e)
   

#Function to speak What is Passed as an argument
def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

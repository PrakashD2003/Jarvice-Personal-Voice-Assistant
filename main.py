import webbrowser
import subprocess
import spotifyplay_main
import whatsapp_and_mail_integration as whatsappNmail
import Utility
import openai_integration
import os
import sys
from gtts import gTTS
from playsound import playsound
import pywhatkit as kit
import time


# def Utility.speak(text):
#     tts = gTTS(text=text, lang='en')
#     output = os.path.join(os.getcwd(), "output.mp3")
#     tts.save(output)
#     playsound(output)
#     os.remove(output)

# Open app by taking there AUMID as input
def open_app(aumid):
    try:
        # Attempt to open the app using its AUMID
        subprocess.Popen(['explorer.exe', f'shell:AppsFolder\\{aumid}'])
        time.sleep(2)
    except FileNotFoundError:
        # Handle the case where the app is not found
        print(f"App with AUMID {aumid} is not installed on this system.")
    except Exception as e:
        # Handle any other exceptions
        print(f"An error occurred: {e}")

#Extract Query from Command
def extract_query(command):
    # Define keywords to look for
    keywords = ["search for", "find", "look up", "query","play"]
    extra_words = [" on ","youtube","google","jarvis"]
    # Convert the command to lowercase for case-insensitive matching
    command = command.lower()
    
    # Iterate over the keywords to find the query
    for keyword in keywords:
        if keyword in command:
            # Extract the part of the command after the keyword
            query = command.split(keyword, 1)[1].strip()
            #Replace the Extra Words From Query
            for words in extra_words:
                query = query.replace(words,"").strip()
            return query
    
    # Return None if no keyword is found
    return None
def process_command(command):
    try:
        command = command.lower().strip()
        if("jarvis" in command):
            if("open google" in command):
                Utility.speak("Of course, sir. Opening Google for you now. How may I assist you further?")
                webbrowser.open("http://google.com")
            elif("open youtube" in command):
                Utility.speak("Of course, sir. Opening Youtube for you now. How may I assist you further?")
                webbrowser.open("https://www.youtube.com/")
            elif("open whatsapp" in command):
                Utility.speak("Certainly, sir. Initiating WhatsApp for you now.")
                aumid_whatsapp = "5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"
                open_app(aumid_whatsapp)
                Utility.speak("Sir WhatsApp is now open. Would you like to send a message to anyone in particular?")
                choice = Utility.take_command(timeout=2,phrase_time_limit=3)
                if("yes" in choice.lower()):
                    whatsappNmail.send_whatsapp_message(contacts_file=r"D:\Programming\Projects-Repo\Jarvice(Personal Voice assistant)\contacts.csv")
                else:
                    Utility.speak("Okay, sir.")
            elif("open spotify" in command):
                Utility.speak("Of course, sir. Opening Spotify for you now. How may I assist you further?")
                aumid_spotify = "SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify"
                open_app(aumid_spotify)
            elif("open calendar" in command):
                Utility.speak("Certainly, sir. Opening your calendar now.")
                aumid_calendar = "microsoft.windowscommunicationsapps_8wekyb3d8bbwe!microsoft.windowslive.calendar"
                open_app(aumid_calendar)
            elif("open camera" in command):
                Utility.speak("Certainly, sir. Activating the camera for you now. Ready to capture your next moment?")
                aumid_camera = "Microsoft.WindowsCamera_8wekyb3d8bbwe!App"
                open_app(aumid_camera)
            elif("open netflix" in command):
                Utility.speak("Absolutely, sir. Netflix is now at your service. Ready to dive into your favorite shows and movies?")
                aumid_netflix = "4DF9E0F8.Netflix_mcm4njqhnhss8!Netflix.App"
                open_app(aumid_netflix)
            elif("open setting" in command):
                Utility.speak("Absolutely, sir. Settings are now at your disposal. Ready to fine-tune your preferences?")
                aumid_setting = "windows.immersivecontrolpanel_cw5n1h2txyewy!microsoft.windows.immersivecontrolpanel"
                open_app(aumid_setting)
            elif("weather" in command):
                Utility.speak("sure sir")
                aumid_weather = "Microsoft.BingWeather_8wekyb3d8bbwe!App"
                open_app(aumid_weather)
            elif("open calculator" in command):
                Utility.speak("Right away, sir. Activating the Calculator. How can I assist with your computations today?")
                aumid_calculator = "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App"
                open_app(aumid_calculator)
            elif("search" in command):
                Utility.speak("Certainly, sir. Initiating search protocol.")
                key = command.split(" ") 
                search_query = extract_query(command)
                if("google" in key):
                    Utility.speak("Directing you to Google search.")
                    webbrowser.open(f"https://www.google.com/search?q={search_query}")
                elif("youtube" in key):
                    Utility.speak("Navigating to YouTube search results.")
                    webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
            elif("play" in command):
                key = command.split(" ") 
                if("spotify" in key or "song" in key):
                    search_query = command.replace("play", "").replace("on","").replace("spotify","").replace("song","").strip()
                    song_name,artist_name = openai_integration.extract_song_and_artist(command)
                    if  song_name or artist_name:
                        Utility.speak("Certainly, sir. Playing your requested song on Spotify.")
                        spotifyplay_main.play_song(song_name,artist_name)
                    else:
                        Utility.speak("Certainly, sir. Playing your selected track on Spotify.")
                        spotifyplay_main.play_song(search_query)
                elif("youtube" in key):
                    search_query = extract_query(command)
                    Utility.speak(f"Right away, sir. Initiating YouTube playback for {search_query}. Enjoy your viewing experience.")
                    kit.playonyt(search_query)
            elif any(word in command for word in ["pause", "stop", "resume", "start"]) and any(word in command for word in ["music", "song"]):
                if any(word in command for word in ["pause", "stop"]):
                    spotifyplay_main.pause_playback()
                else:
                    spotifyplay_main.resume_playback()

            elif all(word in command for word in ["jarvis","rest"]):
                Utility.speak("Thank you, sir. I hope to see you again soon.")
                sys.exit()  
            elif ("shutdown" in command):
                Utility.speak("Very well, sir. Initiating system shutdown sequence. Your PC will power down in 10 seconds. Have a pleasant day")
                kit.shutdown(10)
            elif("send" in command and "message" in command):
                whatsappNmail.send_whatsapp_message(contacts_file=r"D:\Programming\Projects-Repo\Jarvice(Personal Voice assistant)\contacts.csv")
            elif "send" in command and any(word in command for word in ["email","mail","gmail"]):
                whatsappNmail.send_mail()
            else:
                response = openai_integration.get_openai_response(command)
                Utility.speak(response)
        else:
            print("\"Jarvis\" was not found in command." )
    except Exception as e:
        print(f"Error:{e}")
            

        
        
if __name__=="__main__":
    Utility.speak("Initializing Jarvis")
    Utility.listen_wake_word()
    while True:
        command = Utility.take_command(timeout=2,phrase_time_limit=8)
        process_command(command)
       
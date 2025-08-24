import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import subprocess
import time
import Utility

#Spotify API Credentials
client_id = os.getenv('spotify_client_id')
client_secret = os.getenv('spotify_client_secret')
redirect_uri = 'http://localhost:8888/callback'


#Scope For Controlling Playback
scope = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'

# Authenticate With Spotify( creating an instance of the Spotify class from the spotipy library. 
#                            This instance, sp, is used to interact with the Spotify Web API)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))


def is_spotify_running():
    #Checks If Spotify Is Running
    try:
        output = subprocess.check_output("tasklist",shell=True).decode()
        return("spotify.exe" in output.lower())
    except Exception as e:
        print(f"An error occurred while checking if Spotify is running: {e}")
        return False

def start_spotify():
    try:
        # Start Spotify
        subprocess.Popen(['explorer.exe', f'shell:AppsFolder\\{"SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify"}'])
        print("Starting Spotify...")
          # Wait for Spotify to be ready
        time.sleep(5)  # Adjust the sleep time if necessary
    except Exception as e:
        print(f"An error occurred while starting Spotify: {e}")


def play_song(song_name,artist_name=None):
    try:

        if not is_spotify_running():
            start_spotify()
          
       # Construct the search query
        query = f'track:{song_name}'
        if artist_name:
            query += f' artist:{artist_name}'
       
        #Search For The Song
        results = sp.search(q=query,limit=1,type="track") #function reeturn a Dictionary and store it to 'results'
    
        if(results["tracks"]["items"]):
            track = results["tracks"]["items"][0]
            track_uri = track["uri"]
            #Get The Usr's Device
            devices = sp.devices()
            if (devices['devices']):
                devices_id = devices['devices'][0]['id']
                #Starts The Playback On The First Available Device
                sp.start_playback(device_id=devices_id,uris=[track_uri])
                print(f"Playing {track['name']} by {track['artists'][0]['name']}")
            else:
                Utility.speak("No active devices found.")
        else:
            Utility.speak("Song not found.")
    except spotipy.exceptions.SpotifyException as e:
        if 'PREMIUM_REQUIRED' in str(e):
            Utility.speak("Error: Spotify Premium account required.")
            # Clear the token cache to force re-authentication
            if 'PREMIUM_REQUIRED' in str(e):
                if os.path.exists('.cache'):
                    os.remove('.cache')                  
        else:
            Utility.speak(f"An error occurred: {e}")
#Pauses the Playback
def pause_playback():
    sp.pause_playback()

#Resumes the Playback
def resume_playback():
    sp.start_playback()
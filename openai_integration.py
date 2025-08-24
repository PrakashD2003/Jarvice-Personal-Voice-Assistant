# openai_integration.py
import openai
import os

openai.api_key = os.getenv('openai_api_key')
#Function For Answering Any Question
def get_openai_response(command):
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=f"You are a virtual assistant like Alexa and Google Assistant so answer users questions and perform task they are giving you in a way that IRONMAN JARVIS would respond. {command}",
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
#Function to Extract Song Name and Artist Name From Command Using Open AI API
def extract_song_and_artist(command):
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=f"Extract the song name and artist name from the following command and return just song name and artist name respectively if artist name is not give return N/A for artist name: '{command}'",
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
        )
        text = response.choices[0].text.strip()
        # Assuming the response format is "Song name: [song] Artist name: [artist]"
        parts = text.lower().split("artist name:")
        song_name = parts[0].replace("song name:", "").strip() if len(parts) > 0 else ""
        artist_name = parts[1].replace("n/a","").strip() if len(parts) > 1 else ""
        print(song_name,artist_name)
        return song_name, artist_name
    except Exception as e:
        print(f"An error occurred: {e}")

    
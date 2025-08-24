# Jarvice-Personal-Voice-Assistant 🤖🎙️

---

Jarvice (stylised as **JARVIS**) is a Python-based personal voice assistant inspired by Marvel’s Iron Man. It can listen for a wake word, interpret spoken commands, and perform actions such as opening Windows apps, searching the web, playing music on Spotify or YouTube, sending WhatsApp messages or e-mails, and answering general questions using the OpenAI API. It targets Windows and uses speech recognition, text-to-speech, and third-party APIs to provide a hands-free, conversational interface. ✨

## Key Features ✨

* 🎙️ **Wake word + greeting** – listens for “Jarvis”, greets based on time, then awaits commands.
* 🚀 **Open applications** – launches Google, YouTube, WhatsApp Desktop, Spotify, Calendar, Camera, Netflix, Settings, Weather, and Calculator using their AUMIDs.
* 🔎 **Web & YouTube search** – extracts queries from speech and opens the right results page (Google or YouTube).
* 🎵 **Media playback**

  * 🎧 Understands “play \<song> (by \<artist>) on Spotify”; extracts song/artist with OpenAI and plays via Spotipy.
  * ▶️ Plays YouTube videos via `pywhatkit`.
  * ⏯️ Supports pause/resume of Spotify playback.
* 💬📧 **Messaging & e-mail**

  * 🟢 Sends WhatsApp messages using a CSV contacts file (`pywhatkit.sendwhatmsg`), scheduling at the next minute.
  * ✉️ Sends e-mails via Gmail SMTP after asking for recipient, subject, and body; credentials come from environment variables.
* 🧠 **General Q\&A** – for other prompts, generates a Jarvis-style response with OpenAI.
* 📴 **Exit & shutdown** – “Jarvis rest” exits; “Jarvis shutdown” powers off the PC after a 10-second warning.

## Project Structure 🗂️

* [`main.py`](https://github.com/PrakashD2003/Jarvice-Personal-Voice-Assistant/blob/8dbb6bc20c2d1c9031b4ca08fad2db941e1317d8/main.py) – entry point; listens for the wake word, parses speech, and delegates actions (launching apps, searching, media).
* [`Utility.py`](https://github.com/PrakashD2003/Jarvice-Personal-Voice-Assistant/blob/8dbb6bc20c2d1c9031b4ca08fad2db941e1317d8/Utility.py) – helpers for greeting, listening to mic audio, speech-to-text, and text-to-speech.
* [`openai_integration.py`](https://github.com/PrakashD2003/Jarvice-Personal-Voice-Assistant/blob/8dbb6bc20c2d1c9031b4ca08fad2db941e1317d8/openai_integration.py) – wraps OpenAI to:

  * 💬 answer general questions in a Jarvis tone, and
  * 🎼 extract song and artist names from free-form commands.
* [`whatsapp_and_mail_integration.py`](https://github.com/PrakashD2003/Jarvice-Personal-Voice-Assistant/blob/8dbb6bc20c2d1c9031b4ca08fad2db941e1317d8/whatsapp_and_mail_integration.py) – reads contacts CSV, sends WhatsApp messages, validates e-mail addresses, and sends e-mails via SMTP.
* [`spotifyplay_main.py`](https://github.com/PrakashD2003/Jarvice-Personal-Voice-Assistant/blob/8dbb6bc20c2d1c9031b4ca08fad2db941e1317d8/spotifyplay_main.py) – authenticates with Spotify (Spotipy), ensures the app is running, and plays/pauses/resumes tracks.

## Requirements 📦

Python **3.8+** and these major packages (install individually; no `requirements.txt` bundled):

* 🎤 `SpeechRecognition`, `pyaudio` – microphone capture & speech recognition
* 🗣️ `pyttsx3` – offline TTS used by [`Utility.speak()`](https://github.com/PrakashD2003/Jarvice-Personal-Voice-Assistant/blob/8dbb6bc20c2d1c9031b4ca08fad2db941e1317d8/Utility.py#L63-L67)
* 🌐 `gTTS`, `playsound` – alternative TTS routine (currently commented in [`main.py`](https://github.com/PrakashD2003/Jarvice-Personal-Voice-Assistant/blob/8dbb6bc20c2d1c9031b4ca08fad2db941e1317d8/main.py#L14-L20))
* ▶️ `pywhatkit` – WhatsApp messages, shutdown, YouTube play
* 🎧 `spotipy` – Spotify Web API integration ([`spotifyplay_main.py`](https://github.com/PrakashD2003/Jarvice-Personal-Voice-Assistant/blob/8dbb6bc20c2d1c9031b4ca08fad2db941e1317d8/spotifyplay_main.py))
* 🤖 `openai` – AI responses & music metadata extraction ([`openai_integration.py`](https://github.com/PrakashD2003/Jarvice-Personal-Voice-Assistant/blob/8dbb6bc20c2d1c9031b4ca08fad2db941e1317d8/openai_integration.py))
* 🧰 Built-ins: `smtplib`, `email.mime`, `datetime`, `subprocess`, `os`

> ⚠️ Windows users may need a prebuilt **PyAudio** wheel; some systems require installing PortAudio.

## Environment Variables 🔐

Set these before running:

* 🔑 `openai_api_key` – OpenAI API key for answers & extracting song info ([`openai_integration.py`](https://github.com/PrakashD2003/Jarvice-Personal-Voice-Assistant/blob/8dbb6bc20c2d1c9031b4ca08fad2db941e1317d8/openai_integration.py#L4))
* 🎼 `spotify_client_id`, `spotify_client_secret` – Spotify credentials (register an app, set redirect URI to `http://localhost:8888/callback`; Spotify **Premium** required for playback) ([`spotifyplay_main.py`](https://github.com/PrakashD2003/Jarvice-Personal-Voice-Assistant/blob/8dbb6bc20c2d1c9031b4ca08fad2db941e1317d8/spotifyplay_main.py#L7-L22))
* 📧 `Email_ID`, `Email_Password_Jarvis` – Gmail address & password (for 2FA accounts, use an **App Password**) ([`whatsapp_and_mail_integration.py`](https://github.com/PrakashD2003/Jarvice-Personal-Voice-Assistant/blob/8dbb6bc20c2d1c9031b4ca08fad2db941e1317d8/whatsapp_and_mail_integration.py#L92-L97))

## Installation & Running 🛠️🚀

```bash
# 1) Clone
git clone https://github.com/PrakashD2003/Jarvice-Personal-Voice-Assistant.git
cd Jarvice-Personal-Voice-Assistant

# 2) (Optional) venv
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

# 3) Install deps
pip install SpeechRecognition pyaudio pyttsx3 gtts playsound pywhatkit spotipy openai
```

Set environment variables (examples):

```bash
# PowerShell
$env:openai_api_key="sk-..."
$env:spotify_client_id="your-client-id"
$env:spotify_client_secret="your-client-secret"
$env:Email_ID="your-email@gmail.com"
$env:Email_Password_Jarvis="your-app-password"
```

```bash
# Bash
export openai_api_key="sk-..."
export spotify_client_id="your-client-id"
export spotify_client_secret="your-client-secret"
export Email_ID="your-email@gmail.com"
export Email_Password_Jarvis="your-app-password"
```

📇 Prepare a contacts CSV (optional, for WhatsApp). Each row should be:
`name,phone_number_in_international_format`

▶️ Run the assistant:

```bash
python main.py
```

(See [`main.py`](https://github.com/PrakashD2003/Jarvice-Personal-Voice-Assistant/blob/8dbb6bc20c2d1c9031b4ca08fad2db941e1317d8/main.py))

## Usage Examples 💡

* 🖥️ “**Jarvis, open Google**” – opens `google.com`
* 🎬 “**Jarvis, search for cats on YouTube**” – opens YouTube results for *cats*
* 🎶 “**Jarvis, play Blinding Lights by The Weeknd on Spotify**” – extracts song & artist and plays via Spotipy ([`openai_integration.py`](https://github.com/PrakashD2003/Jarvice-Personal-Voice-Assistant/blob/8dbb6bc20c2d1c9031b4ca08fad2db941e1317d8/openai_integration.py), [`spotifyplay_main.py`](https://github.com/PrakashD2003/Jarvice-Personal-Voice-Assistant/blob/8dbb6bc20c2d1c9031b4ca08fad2db941e1317d8/spotifyplay_main.py))
* 📲 “**Jarvis, send a message**” – asks whom and what to send, then sends a WhatsApp message ([`whatsapp_and_mail_integration.py`](https://github.com/PrakashD2003/Jarvice-Personal-Voice-Assistant/blob/8dbb6bc20c2d1c9031b4ca08fad2db941e1317d8/whatsapp_and_mail_integration.py))
* ✉️ “**Jarvis, send an email**” – collects recipient, subject, body, then sends via Gmail ([`whatsapp_and_mail_integration.py`](https://github.com/PrakashD2003/Jarvice-Personal-Voice-Assistant/blob/8dbb6bc20c2d1c9031b4ca08fad2db941e1317d8/whatsapp_and_mail_integration.py))
* 😴 “**Jarvis, rest**” – exits gracefully ([`main.py`](https://github.com/PrakashD2003/Jarvice-Personal-Voice-Assistant/blob/8dbb6bc20c2d1c9031b4ca08fad2db941e1317d8/main.py))

## Notes 📝

* 🪟 **Platform** – Focused on **Windows**; uses AUMIDs (`explorer.exe shell:AppsFolder\...`) to open UWP apps. For macOS/Linux, adapt the `open_app` logic in [`main.py`](https://github.com/PrakashD2003/Jarvice-Personal-Voice-Assistant/blob/8dbb6bc20c2d1c9031b4ca08fad2db941e1317d8/main.py#L21-L33).
* 📁 **Contacts file** – The example path is hard-coded in [`main.py`](https://github.com/PrakashD2003/Jarvice-Personal-Voice-Assistant/blob/8dbb6bc20c2d1c9031b4ca08fad2db941e1317d8/main.py#L70-L73,L139-L141) for demonstration; change it to your CSV path or extend the code to load dynamically.
* 🔒 **Secrets** – Never commit keys/passwords. Prefer environment variables (or a secrets manager).

## Contributing 🤝

Issues and PRs are welcome—bug fixes, features, cross-platform improvements, a `requirements.txt`, and better NLP are great places to help.

---

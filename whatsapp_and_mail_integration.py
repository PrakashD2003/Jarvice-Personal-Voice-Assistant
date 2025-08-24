# For Whatsapp
import csv
import pywhatkit as kit
import datetime
import Utility
# For Email 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import os

# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

# def get_google_contacts(credentials_file):
#     SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']
#     credentials = service_account.Credentials.from_service_account_file(
#         credentials_file, scopes=SCOPES)

#     service = build('people', 'v1', credentials=credentials)

#     try:
#         results = service.people().connections().list(
#             resourceName='people/me',
#             pageSize=100,
#             personFields='names,emailAddresses').execute()
#         connections = results.get('connections', [])

#         print(f"Raw API response: {results}")
#         print(f"Total connections found: {len(connections)}")

#         contacts = []
#         for person in connections:
#             names = person.get('names', [])
#             if names:
#                 name = names[0].get('displayName')
#                 contacts.append(name)
#         return contacts
#     except HttpError as err:
#         print(f"An error occurred: {err}")
#         return []

# # Example usage
# contacts = get_google_contacts(r"D:\Programming\API\serious-case-431010-q3-7670f23f8a72.json")
# print(contacts)

#Takes a CSV File Path and Convert its Content into a Dictionary
def csv_to_dict(filename):
    with open(filename, mode='r') as csvfile:
        reader = csv.reader(csvfile)
        csv_dict = {rows[0].lower(): rows[1].lower() for rows in reader}
    return csv_dict

#Sends WhatsApp Message to the Specified Person
def send_whatsapp_message(contacts_file):
    try:
        Utility.speak("To whom shall I send a message, sir?")
        contact = Utility.take_command(timeout=2,phrase_time_limit=4)
        contacts = csv_to_dict(filename=contacts_file)#Contact File Path
        if contact:
            Utility.speak("What would you like the message to say, sir?")
            message = Utility.take_command(timeout=2,phrase_time_limit=8)
            if message:
                contact_number = contacts.get(contact.lower().strip(), None)
                if contact_number:
                    # Send message at the next minute
                    now = datetime.datetime.now()
                    hour = now.hour
                    minute = now.minute + 1
                    Utility.speak("Absolutely, sir. Your message is being sent.")
                    kit.sendwhatmsg(contact_number, message, hour, minute,tab_close=True,close_time=2)
                    Utility.speak(f"Message sent to {contact}")
                else:
                    Utility.speak("I'm afraid I don't have that contact, sir.")
    except FileNotFoundError:
        Utility.speak("I'm sorry, sir. The contacts file could not be found.")
    except Exception as e:
        Utility.speak(f"An error occurred, sir: {str(e)}. Please try again.")

# Sends Email to specified Email address
def send_mail():
    """
    Sends an email from the sender's email address to the specified receiver's email address.

    This function prompts the user for the receiver's email, subject, and body of the email 
    through voice commands. It then constructs the email and sends it using the SMTP protocol.
    
    If an error occurs during the process, it will print the error message.
    """
    try:
        sender_email = os.getenv('Email_ID')
        password = os.getenv('Email_Password_Jarvis')
        
        if not sender_email or not password:
            raise ValueError("Sender email or password not set in environment variables.")
        
        receiver_email = get_receiver_email()
        subject = get_email_subject()
        body = get_email_body()

        send_email_via_smtp(sender_email, receiver_email, subject, body, password)
        Utility.speak("Email successfully sent, sir. Is there anything else you need assistance with?")
    except Exception as e:
        logging.error(f"Error: {e}")
        Utility.speak("An error occurred while sending the email. Please try again later.")

# Gets receivers email address from user
def get_receiver_email():

    while True:
        Utility.speak("To whom shall I send a mail, sir?")
        receiver_email = Utility.take_command(timeout=5, phrase_time_limit=10)
        
        # Process the input
        receiver_email = receiver_email.lower()
        receiver_email = receiver_email.replace(" dot ", ".")
        receiver_email = receiver_email.replace(" dot", ".")
        receiver_email = receiver_email.replace("dot ", ".")
        receiver_email = receiver_email.replace(" at the rate ", "@")
        receiver_email = receiver_email.replace(" attherate ", "@")
        receiver_email = receiver_email.replace(" at ", "@")
        receiver_email = receiver_email.replace(" ", "")
        receiver_email = receiver_email.strip()
        
        print(receiver_email)
        
        if validate_email(receiver_email):
            return receiver_email
        else:
            Utility.speak("Invalid email address provided. Please try again.")

# Gets subject of email from user
def get_email_subject():
    Utility.speak("What would you like the subject of the email to be?")
    return Utility.take_command(timeout=5, phrase_time_limit=10)

# Gets body of email from user
def get_email_body():
    Utility.speak("What message would you like to include in the email?")
    return Utility.take_command(timeout=10, phrase_time_limit=20)

# Validates the receivers email if it is correct or not
def validate_email(email):
    import re
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# Sends email via SMTP
def send_email_via_smtp(sender_email, receiver_email, subject, body, password):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
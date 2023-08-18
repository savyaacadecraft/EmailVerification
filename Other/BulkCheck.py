
from email.mime.text import MIMEText
from time import sleep
import sys
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.multipart import MIMEMultipart
import os
import time


def verifying2(Emails, id_num):
    subject = "Test email"
    message_text = "This is a test email."

    # Set up the Gmail API
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    # Load credentials
    creds = None
    if os.path.exists(f'Credentials\cred{id_num}.json'):
        creds = Credentials.from_authorized_user_file(
            f'Credentials\cred{id_num}.json', SCOPES)

    # Create message object
    msg = MIMEMultipart()
    msg['to'] = ', '.join(Emails)
    msg['subject'] = subject

    # Create text part
    text_part = MIMEText(message_text, 'plain')
    msg.attach(text_part)

    try:
        service = build('gmail', 'v1', credentials=creds)
        raw_msg = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')
        send_message = service.users().messages().send(userId='me', body={'raw': raw_msg}).execute()
        print(f"Mail sent to {Emails}")
    except HttpError as error:
        print(F'Error while Sending Email: {error}')
        send_message = None
        return False


    sleep(0.1)
    
    knkt = receive(id_num)
    return knkt

def receive(id_num):
    # Request the last 10 messages

    # Set up the Gmail API
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    # Load the credentials
    creds = None
    if os.path.exists(f'Credentials\\cred{id_num}.json'):
        creds = Credentials.from_authorized_user_file(f'Credentials\\cred{id_num}.json', SCOPES)

    # Build the Gmail API client
    service = build('gmail', 'v1', credentials=creds)
    # Retrieve the last 10 emails
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    messages = results.get('messages', [])

    # Process and print the emails
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        payload = msg['payload']
        headers = payload['headers']

        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
                print('Subject:', subject)
            elif header['name'] == 'From':
                sender = header['value']
                print('From:', sender)

        if 'parts' in payload:
            parts = payload['parts']
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    text = base64.urlsafe_b64decode(data).decode('utf-8')
                    print('Body:', text)
                    break

        print('---')

emaols = ["Priyamtomar0wresd12@gmail.com","priyamtomsdfar1123123133@gmail.com"]
receive(9)
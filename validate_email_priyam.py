
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

ID_COUNTER = dict()

def verifying2(recipient_email, id_num):
    to = recipient_email
    subject = "Test email"
    message_text = "This is a test email."

    # Set up the Gmail API
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    # Load credentials
    creds = None
    if os.path.exists(f'Credentials/cred{id_num}.json'):
        creds = Credentials.from_authorized_user_file(
            f'Credentials/cred{id_num}.json', SCOPES)

    # Create message object
    msg = MIMEMultipart()
    msg['to'] = to
    msg['subject'] = subject

    # Create text part
    text_part = MIMEText(message_text, 'plain')
    msg.attach(text_part)

    try:
        service = build('gmail', 'v1', credentials=creds)
        raw_msg = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')
        send_message = service.users().messages().send(userId='me', body={'raw': raw_msg}).execute()

    except HttpError as error:
        send_message = None
        return False
    
    sleep(0.1)
    return receive(recipient_email, 11, id_num)

def receive(recipient_email, count, id_num):
    sleep(1)

    if count == 0:
        current_time = time.time()
        # Convert the current time to a human-readable format
        formatted_time = time.strftime('%H:%M:%S', time.localtime(current_time))
        print(f"{recipient_email}: EXIST {formatted_time}\n")
        return True
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    # Load the credentials
    creds = None
    if os.path.exists(f'Credentials/cred{id_num}.json'):
        creds = Credentials.from_authorized_user_file(f'Credentials/cred{id_num}.json', SCOPES)

    # Build the Gmail API client
    service = build('gmail', 'v1', credentials=creds)

    # Recursive function to extract the message body from a payload
    def get_message_body(payload):
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    body = part['body']
                    data = body.get('data', '')
                    if data:
                        return base64.urlsafe_b64decode(data).decode('utf-8')
                elif part['mimeType'] == 'multipart/alternative':
                    return get_message_body(part)
                elif part['mimeType'] == 'multipart/mixed':
                    return get_message_body(part)
                else:
                    return get_message_body(part)
        else:
            body = payload['body']
            data = body.get('data', '')
            if data:
                return base64.urlsafe_b64decode(data).decode('utf-8')
    # Fetch the latest message
    try:
        response = service.users().messages().list(userId='me', q='is:inbox', maxResults=1).execute()
        message = None
        if 'messages' in response:
            message = response['messages'][0]
            msg = service.users().messages().get(
                userId='me', id=message['id']).execute()
            payload = msg['payload']
            content = get_message_body(payload)
            mnEmail = recipient_email

            if content.splitlines()[0:1][0] == "" or content.splitlines()[0:1][0] == "\n" or content.splitlines()[0:1][0] == " ":
                pass
            else:
                print(content.splitlines()[0:1][0])

            if "You have reached a limit for sending mail" in content:
                # print("You have reached a limit for sending mail. Your message was not sent.")
                raise Exception("You have reached a limit for sending mail. Your message was not sent.")
            
            if mnEmail in content:
                current_time = time.time()
                # Convert the current time to a human-readable format
                formatted_time = time.strftime('%H:%M:%S', time.localtime(current_time))
                print(f'{mnEmail} == Not EXIST {formatted_time}\n')
                return False
            
            else:

                return receive(recipient_email, count-1, id_num)
            
    except HttpError as error:
        print('An error occurred: %s' % error)

def getVars(line):
    with open('patterns.txt', 'r') as f:
        return f.readlines()[line].removesuffix('\n')

def PatternCheck(name, domain, idnum):

    f_name = name.split(" ")[0]
    l_name = name.split(" ")[1]

    if "//" in domain:
        domain = f'{".".join(" ".join(domain.split("//")[1:]).replace("/","").replace("www.","").split(".")[0:2])}'
    else:
        domain = f'{domain.replace("www.","")}'

    
    for i in range(16):
        try:
            ptrn = getVars(i).replace('firstname', f_name).replace('lastname', l_name).replace('firstinitial', f_name[0]).replace('lastinitial', l_name[0]).lower()

            email = ptrn+"@"+domain

            if idnum not in ID_COUNTER.keys(): ID_COUNTER[idnum] = 1
            else: ID_COUNTER[idnum] += 1

            if verifying2(email, idnum) == True:
                return (getVars(i),email, ID_COUNTER[idnum])
        except Exception as e:
            print('[validate email ({})] :::: '.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            raise Exception("Refresh problem")
    return None,None, ID_COUNTER[idnum]


# def BulkCheckForBulkCsv():
#     for i in range(10):
#         with open("bulk.csv", 'r') as f:
#             email = f.readlines()[i].replace(" ", "").replace("\n", "")
#             verifying2(email, 2)
#             f.close()


if __name__ == "__main__":
    for i in range(17, 31):
        # i is idnum from 14 to 30
        try:
            verifying2("savyarex2205@gmail.com",i)
            input("Enter: ")
        except Exception as E:
            print("Exception: ", E)
        
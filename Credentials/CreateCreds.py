from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle


def VerifySecreat(id_num):
    # Define the scopes for the Gmail API
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
              "https://www.googleapis.com/auth/gmail.compose",
              'https://www.googleapis.com/auth/gmail.send']

    # Define the path to the credentials file
    creds_file_path = f'Credentials\cred{id_num}.json'

    # Create a flow object to authorize the user
    flow = InstalledAppFlow.from_client_secrets_file(
        creds_file_path, scopes=SCOPES)

    # Start the authorization flow and open a local server to handle the
    # OAuth2 callback
    creds = flow.run_local_server(port=0)

    creds_json = creds.to_json()
    with open(f'Credentials\cred{id_num}.json', 'w') as f:
        f.write(creds_json)

i=30
while i <= 33:
    VerifySecreat(i)
    i+=1
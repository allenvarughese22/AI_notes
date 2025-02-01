import os
import csv
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_emails(max_results=100):
    """Fetch emails and save subjects/snippets to a CSV file."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Re-authenticate if token is missing or invalid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the new token
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])
    
    if not messages:
        print("No messages found.")
    else:
        # Create a CSV file to save subjects and snippets
        with open('emails_to_label.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(['email_id', 'subject', 'snippet', 'label'])
            
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
                headers = msg['payload']['headers']
                # Extract subject and snippet
                subject = next(
                    (header['value'] for header in headers if header['name'] == 'Subject'),
                    "No Subject"
                )
                snippet = msg.get('snippet', 'No Snippet')
                email_id = message['id']
                # Write to CSV (label column is empty for you to fill)
                writer.writerow([email_id, subject, snippet, ''])
        print(f"Saved {len(messages)} emails to emails_to_label.csv")

if __name__ == '__main__':
    get_emails(max_results=100)  # Fetch 100 emails
    
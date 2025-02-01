import os
import joblib
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Load the trained model and vectorizer
model = joblib.load('spam_classifier_retrained.pkl')
vectorizer = joblib.load('vectorizer_retrained.pkl')

# Gmail API setup
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def classify_real_emails(max_results=10):
    """Fetch and classify real emails from your Gmail inbox."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        print("Re-authenticate to refresh the token.")
        return
    
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])
    
    if not messages:
        print("No emails found.")
    else:
        print("Email Classifications:")
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
            headers = msg['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
            # Classify the subject
            features = vectorizer.transform([subject])
            prediction = model.predict(features)
            label = "SPAM" if prediction[0] == 1 else "HAM"
            print(f"Subject: {subject}\nClassification: {label}\n")

if __name__ == '__main__':
    classify_real_emails(max_results=10)  # Classify 10 emails
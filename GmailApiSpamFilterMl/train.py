import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load labeled data
df = pd.read_csv('emails_to_label.csv')

# Preprocess text data
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
X = vectorizer.fit_transform(df['subject'])  # Use subject for training
y = df['label'].map({'spam': 1, 'ham': 0})

# Train the model
model = LogisticRegression()
model.fit(X, y)

# Save the model and vectorizer for future use
import joblib
joblib.dump(model, 'spam_classifier.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
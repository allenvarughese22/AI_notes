import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Load the new training split
train_df = pd.read_csv('training_data.csv')

# Preprocess text data (retrain the vectorizer on the training split)
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
X_train = vectorizer.fit_transform(train_df['subject'])  # Fit on training data only
y_train = train_df['label'].map({'spam': 1, 'ham': 0})

# Train the model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save the new model and vectorizer
joblib.dump(model, 'spam_classifier_retrained.pkl')
joblib.dump(vectorizer, 'vectorizer_retrained.pkl')
print("Model retrained and saved!")
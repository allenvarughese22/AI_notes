import pandas as pd
import joblib
from sklearn.metrics import classification_report

# Load retrained model and vectorizer
model = joblib.load('spam_classifier_retrained.pkl')
vectorizer = joblib.load('vectorizer_retrained.pkl')

# Load validation data
val_df = pd.read_csv('validation_data.csv')

# Preprocess validation data
X_val = vectorizer.transform(val_df['subject'])
y_val = val_df['label'].map({'spam': 1, 'ham': 0})

# Evaluate
y_pred = model.predict(X_val)
print("Validation Report:")
print(classification_report(y_val, y_pred))
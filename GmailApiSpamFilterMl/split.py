import pandas as pd
from sklearn.model_selection import train_test_split

# Load your CSV dataset
df = pd.read_csv('emails_to_label.csv')

# Split into training (80%) and validation (20%)
train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)

# Save the splits to new files
train_df.to_csv('training_data.csv', index=False)
val_df.to_csv('validation_data.csv', index=False)

print(f"Training samples: {len(train_df)}")
print(f"Validation samples: {len(val_df)}")
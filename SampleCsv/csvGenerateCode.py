import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta

# Install required package
# pip install faker pandas numpy

fake = Faker()

# Generate 1000 rows of data
np.random.seed(42)
num_rows = 1000

# Create date range
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)

data = {
    "Date": [fake.date_between(start_date=start_date, end_date=end_date) for _ in range(num_rows)],
    "Product": np.random.choice(
        ["Product A", "Product B", "Product C", "Product D", "Product E"], 
        size=num_rows,
        p=[0.3, 0.25, 0.2, 0.15, 0.1]  # Uneven distribution
    ),
    "Category": np.random.choice(
        ["Electronics", "Home Goods", "Clothing", "Books", "Toys"], 
        num_rows
    ),
    "Total Amount": np.round(np.random.gamma(5, 20, num_rows) + 50, 2),
    "Quantity": np.random.randint(1, 15, num_rows)
}

# Create DataFrame
df = pd.DataFrame(data)

# Add some missing values (5% of each column)
for col in ["Product", "Category", "Total Amount"]:
    df.loc[df.sample(frac=0.05, random_state=42).index, col] = np.nan

# Add duplicate rows (3% duplicates)
duplicates = df.sample(frac=0.03, random_state=42)
df = pd.concat([df, duplicates])

# Save to CSV
df.to_csv("sales_data.csv", index=False)
print("Sample dataset generated as 'sales_data.csv'")
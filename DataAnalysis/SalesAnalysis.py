import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
import os

plt.style.use('ggplot')

def load_data(file_path):
    """Load and inspect initial data"""
    df = pd.read_csv(file_path, parse_dates=['Date'], dayfirst=True)
    print("✅ Data loaded successfully")
    print(f"📅 Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
    print(f"📊 Dataset shape: {df.shape}")
    return df

def clean_data(df):
    """Data cleaning pipeline"""
    print("\n🧹 Data Cleaning Report:")
    print("Missing values before cleaning:")
    print(df.isna().sum())
    
    # Handle missing values
    df_clean = df.dropna(subset=['Total Amount', 'Product'])
    df_clean['Category'] = df_clean['Category'].fillna('Unknown')
    
    # Remove duplicates
    df_clean = df_clean.drop_duplicates()
    
    # Convert data types
    df_clean['Total Amount'] = df_clean['Total Amount'].astype(float)
    df_clean['Quantity'] = df_clean['Quantity'].astype(int)
    
    print("\nMissing values after cleaning:")
    print(df_clean.isna().sum())
    print(f"New dataset shape: {df_clean.shape}")
    return df_clean

def analyze_data(df):
    """Perform comprehensive analysis"""
    print("\n🔍 Data Analysis Results:")
    
    # Basic statistics
    print("\n📈 Basic Statistics:")
    print(df[['Total Amount', 'Quantity']].describe().round(2))
    
    # Monthly sales analysis with proper ordering
    df['Month'] = df['Date'].dt.month_name()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_sales = df.groupby('Month')['Total Amount'].agg(['sum', 'count']).rename(
        columns={'sum': 'Total Sales', 'count': 'Transactions'}).reindex(month_order)
    
    # Product performance
    product_stats = df.groupby('Product').agg({
        'Total Amount': ['sum', 'mean'],
        'Quantity': 'sum'
    }).sort_values(('Total Amount', 'sum'), ascending=False)
    
    # Category analysis
    category_stats = df.groupby('Category').agg({
        'Total Amount': 'sum',
        'Quantity': 'mean'
    }).sort_values('Total Amount', ascending=False)
    
    print("\n💰 Top Performing Products:")
    print(product_stats.head())
    
    print("\n🏷️ Category Performance:")
    print(category_stats.head())
    
    return monthly_sales, product_stats, category_stats

def visualize_data(monthly_sales, product_stats, category_stats):
    """Create professional visualizations"""
    
    # Formatting helper
    def currency(x, pos):
        return f'${x:,.0f}'
    
    formatter = FuncFormatter(currency)
    
    # Monthly Sales Trend
    plt.figure(figsize=(14, 7))
    ax = monthly_sales['Total Sales'].plot(kind='line', marker='o', color='tab:blue')
    plt.title('Monthly Sales Trend 2023', fontsize=14)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Total Sales', fontsize=12)
    ax.yaxis.set_major_formatter(formatter)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('monthly_sales_trend.png')
    plt.show()
    
    # Product Performance
    plt.figure(figsize=(12, 6))
    ax = product_stats['Total Amount']['sum'].head(5).plot(kind='bar', color='forestgreen')
    plt.title('Top 5 Products by Total Sales', fontsize=14)
    plt.xlabel('Product', fontsize=12)
    plt.ylabel('Total Sales', fontsize=12)
    ax.yaxis.set_major_formatter(formatter)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('top_products_sales.png')
    plt.show()
    
    # Category Distribution
    plt.figure(figsize=(10, 8))
    category_stats['Total Amount'].plot(kind='pie', autopct='%1.1f%%', 
                                      colors=['gold', 'lightcoral', 'lightskyblue', 'lightgreen', 'violet'])
    plt.title('Sales Distribution by Category', fontsize=14)
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('category_distribution.png')
    plt.show()

def main():
    DATA_DIR = r'I:\AI_blog\DataAnalysis'
    FILE_NAME = 'sales_data.csv'
    file_path = os.path.join(DATA_DIR, FILE_NAME)
    # file_path = 'sales_data.csv'  # Keep in same directory
    
    # Data pipeline
    df = load_data(file_path)
    df_clean = clean_data(df)
    monthly_sales, product_stats, category_stats = analyze_data(df_clean)
    visualize_data(monthly_sales, product_stats, category_stats)
    
    # Save cleaned data
    df_clean.to_csv('cleaned_sales_data.csv', index=False)
    print("\n💾 Cleaned data saved to 'cleaned_sales_data.csv'")

if __name__ == "__main__":
    main()
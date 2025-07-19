import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns # Often used with matplotlib for enhanced visuals

# --- 1. Generate a Sample CSV File ---
# In a real scenario, you would replace this with pd.read_csv('your_file.csv')
data = {
    'Product_Category': np.random.choice(['Electronics', 'Apparel', 'Home Goods', 'Books', 'Food'], 100),
    'Sales_Amount': np.random.randint(100, 1000, 100),
    'Customer_Rating': np.random.uniform(2.0, 5.0, 100).round(1),
    'Units_Sold': np.random.randint(1, 50, 100),
    'Region': np.random.choice(['North', 'South', 'East', 'West'], 100),
    'Order_Date': pd.to_datetime(pd.date_range(start='2023-01-01', periods=100, freq='D'))
}
df = pd.DataFrame(data)

# Save to a CSV file (optional, but good for demonstration)
csv_file_path = 'sample_sales_data.csv'
df.to_csv(csv_file_path, index=False)
print(f"Sample CSV '{csv_file_path}' created successfully.\n")

# --- 2. Load the CSV File using Pandas ---
try:
    df_loaded = pd.read_csv(csv_file_path)
    print("CSV file loaded successfully. First 5 rows:\n")
    print(df_loaded.head())
    print("\nData Info:\n")
    df_loaded.info()
except FileNotFoundError:
    print(f"Error: The file '{csv_file_path}' was not found.")
    exit()

# --- 3. Perform Basic Data Analysis Tasks ---

print("\n--- Basic Data Analysis ---")

# Calculate the average of a selected column (e.g., 'Sales_Amount')
average_sales = df_loaded['Sales_Amount'].mean()
print(f"\nAverage Sales Amount: ${average_sales:.2f}")

# Descriptive statistics for numerical columns
print("\nDescriptive Statistics for Numerical Columns:\n")
print(df_loaded.describe())

# Value counts for categorical columns
print("\nValue Counts for 'Product_Category':\n")
print(df_loaded['Product_Category'].value_counts())

print("\nValue Counts for 'Region':\n")
print(df_loaded['Region'].value_counts())

# Group by 'Product_Category' and calculate sum of 'Sales_Amount'
sales_by_category = df_loaded.groupby('Product_Category')['Sales_Amount'].sum().sort_values(ascending=False)
print("\nTotal Sales by Product Category:\n")
print(sales_by_category)

# --- 4. Create Visualizations using Matplotlib and Seaborn ---

print("\n--- Data Visualizations ---")

# Set a style for better aesthetics
plt.style.use('seaborn-v0_8-darkgrid')

# Figure 1: Bar Chart - Total Sales by Product Category
plt.figure(figsize=(10, 6))
sales_by_category.plot(kind='bar', color=sns.color_palette("viridis", len(sales_by_category)))
plt.title('Total Sales Amount by Product Category', fontsize=16)
plt.xlabel('Product Category', fontsize=12)
plt.ylabel('Total Sales Amount ($)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Figure 2: Scatter Plot - Sales Amount vs. Customer Rating
plt.figure(figsize=(10, 6))
plt.scatter(df_loaded['Customer_Rating'], df_loaded['Sales_Amount'],
            alpha=0.7, color='purple', edgecolors='w', linewidth=0.5)
plt.title('Sales Amount vs. Customer Rating', fontsize=16)
plt.xlabel('Customer Rating (1-5)', fontsize=12)
plt.ylabel('Sales Amount ($)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# Figure 3: Heatmap - Correlation Matrix of Numerical Columns
plt.figure(figsize=(8, 7))
# Select only numerical columns for correlation
numerical_df = df_loaded.select_dtypes(include=np.number)
correlation_matrix = numerical_df.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Correlation Matrix of Numerical Features', fontsize=16)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()

# Figure 4: Distribution of Customer Ratings (Histogram)
plt.figure(figsize=(8, 6))
sns.histplot(df_loaded['Customer_Rating'], bins=10, kde=True, color='skyblue', edgecolor='black')
plt.title('Distribution of Customer Ratings', fontsize=16)
plt.xlabel('Customer Rating', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Figure 5: Box Plot - Sales Amount by Region
plt.figure(figsize=(10, 6))
sns.boxplot(x='Region', y='Sales_Amount', data=df_loaded, palette='pastel')
plt.title('Sales Amount Distribution by Region', fontsize=16)
plt.xlabel('Region', fontsize=12)
plt.ylabel('Sales Amount ($)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

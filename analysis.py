import pandas as pd
import os

print("--- Starting Data Cleaning ---")

# Check if file exists
if not os.path.exists('metadata.csv'):
    print("ERROR: metadata.csv not found. Did you run the wget command?")
    exit()

# 1. Load Data (Smart Loading)
# We use 'nrows=20000' to only take the first 20,000 rows.
# This ignores the rest of the 1.2GB file so your computer doesn't freeze.
print("Loading dataset (sampling first 20,000 rows)...")
df = pd.read_csv('metadata.csv', low_memory=False, nrows=20000)

# 2. Clean Data
print("Cleaning data...")
df_clean = df.dropna(subset=['title', 'publish_time', 'journal'])

# Convert dates
df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'], errors='coerce')
df_clean['publish_year'] = df_clean['publish_time'].dt.year

# Filter for modern papers only
df_clean = df_clean[df_clean['publish_year'] > 2000]

# Fill empty abstracts
df_clean['abstract'] = df_clean['abstract'].fillna("No Abstract Available")

# 3. Save Data
print("Saving cleaned mini-dataset...")
df_clean.to_csv('cleaned_metadata.csv', index=False)
print("SUCCESS: 'cleaned_metadata.csv' has been created!")
import pandas as pd
import numpy as np

# Create the dataset
data = {
    'City': ['City A', 'City B', 'City C', 'City D', 'City E'] * 10,
    'AQI': np.random.randint(50, 200, 50),
    'Temperature': np.random.randint(15, 35, 50),
    'Humidity': np.random.randint(40, 80, 50),
    'Date': pd.date_range(start='2024-01-01', periods=50, freq='D').tolist() * 1
}

# Function to classify AQI
def classify_aqi(aqi):
    if aqi <= 50:
        return 'Good'
    elif aqi <= 100:
        return 'Moderate'
    elif aqi <= 150:
        return 'Unhealthy for Sensitive Groups'
    elif aqi <= 200:
        return 'Unhealthy'
    else:
        return 'Very Unhealthy'

# Add AQI classification
df = pd.DataFrame(data)
df['AQI Classification'] = df['AQI'].apply(classify_aqi)

# Save to Excel
file_path = "AQI_Dataset.xlsx"
df.to_excel(file_path, index=False)
print(f"Dataset saved as {file_path}")

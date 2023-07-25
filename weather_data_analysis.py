import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

API_KEY = "5ac3473587856d05d696ba5626cfd409"
API_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
CITY_ID = "5128581"  # New York, US

def fetch_weather_data(city_id):
    params = {
        'id': city_id,
        'appid': API_KEY
    }
    response = requests.get(API_ENDPOINT, params=params)
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return {}
    return response.json()

def clean_data(raw_data):
    weather_data = []
    for entry in raw_data.get('list', []):
        weather_data.append({
            'time': entry['dt'],
            'temperature': entry['main']['temp'] - 273.15,  # Kelvin to Celsius
            'humidity': entry['main']['humidity']
        })
    if not weather_data:
        print("No weather data available.")
        return pd.DataFrame()
    df = pd.DataFrame(weather_data)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

def plot_temperature_trends(df):
    if df.empty:
        print("No data available for plotting.")
        return
    plt.figure(figsize=(15, 7))
    sns.lineplot(data=df, x='time', y='temperature')
    plt.title('Temperature Trends')
    plt.ylabel('Temperature (°C)')
    plt.xlabel('Time')
    plt.grid(True)
    plt.show()

def main():
    raw_data = fetch_weather_data(CITY_ID)
    df = clean_data(raw_data)
    plot_temperature_trends(df)

if __name__ == '__main__':
    main()

## Real-Time Weather Information & Data Logger
A Python application that fetches real-time weather data from OpenWeatherMap API, displays weather information for user-specified cities, and logs all responses with timestamps to both SQLite database and text files.

# Features
- **Real-time Weather Data**: Fetches current weather information using OpenWeatherMap API

- **Multi-city Support**: Input multiple cities to get weather data

- **Comprehensive Display**: Shows temperature, humidity, weather conditions and wind speed

- **Object-Oriented Design**: Clean, modular code using OOP principles

## Project Structure

WEATHER
|___pycache___
├── config.py
├── data_logger.py
├── main.py
├── weather_api.py
└── weather.db

## Data Storage & Logging

- **SQLite Database**: All API responses are automatically logged with timestamps

- **Persistent Storage**: Data remains available between sessions

- **Structured Logging**: Each entry includes:

- Timestamp of request

- City name searched

Complete API response data

## User Experience
- **Interactive CLI**: Easy-to-use command-line interface

- **Input Validation**: Handles invalid city names gracefully

- **Continuous Operation**: Run multiple queries without restarting

- **Clear Display**: Formatted, readable weather information
## Error Handling
- Invalid city names

- Network connectivity issues

- API rate limiting

- Database connection problems

- Invalid user inputs

## Requirements

- Python 3.6+
- `requests` library

## Installation

1. Clone or download the project files
2. Install required dependencies:
   ```bash
   pip install requests
   ```

3. Get an API key from [OpenWeatherMap](https://openweathermap.org/api)
   - Sign up for a free account
   - Generate an API key in your dashboard

## Database Schema

The application uses SQLite with the following table structure:

```sql
CREATE TABLE logs (
    id INTEGER PRIMARY KEY,
    city TEXT,
    temp REAL,
    humidity INTEGER,
    condition TEXT,
    wind speed REAL,
    timestamp TEXT
)
```

 **Data basa** :
Example of output
```sql
Main Menu:

1. Check weather
2. View history
3. Exit
Enter your choice (1-3): 1
Enter city name: Guntur
Getting weather data for Guntur...
=== Weather in Guntur ===
Temperature: 20.88 °C
Humidity: 80%
I
Wind Speed: 2.23 m/s
Conditions: broken clouds
Data saved successfully!

Main Menu:

1. Check weather
2. View history
3. Exit
Enter your choice (1-3): 1
Enter city name: Tenali
Getting weather data for Tenali...
Weather in Thenali
Temperature: 22.72 °C
Humidity: 75%
Wind Speed: 2.86 m/s
Conditions: broken clouds
Data saved successfully
```
 **Final output** :
```sql
Main Menu:

1. Check weather
2. View history
3. Exit
Enter your choice (1-3): 2

=== Recent Weather Searches ===

Ponnuru: 22.21°C, 83.0% humidity, 2.4 m/s wind
Condition: overcast clouds
Time: 2025-11-27 22:48:11

london: 13.08°C, 90.0% humidity, 5.66 m/s wind
Condition: overcast clouds
Time: 2025-11-27 22:47:48

Vinukonda: 20.21°C, 86.0% humidity, 1.2 m/s wind
Condition: broken clouds
Time: 2025-11-27 22:37:55

Tenali: 22.72°C, 75.0% humidity, 2.86 m/s wind
Condition: broken clouds
Time: 2025-11-27 22:22:06

Guntur: 20.88°C, 80.0% humidity, 2.23 m/s wind
Condition: broken clouds
Time: 2025-11-27 22:21:45

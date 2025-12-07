## Real-Time Weather Information & Data Logger
A Python application that fetches real-time weather data from OpenWeatherMap API, displays weather information for user-specified cities, and logs all responses with timestamps to both SQLite database and text files.

## Project Structure

WEATHER
├── config.py
├── file_logger.py
├── main.py
├── menu_system.py
├── validators.py
├── weather_api.py
├──weather_log.txt
└── weather_data.db


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
  

   
# Features
- **Real-time Weather Data**: Fetches current weather information using OpenWeatherMap API

- **Multi-city Support**: Input multiple cities to get weather data

- **Comprehensive Display**: Shows temperature, humidity, weather conditions and wind speed

- **Object-Oriented Design**: Clean, modular code using OOP principles



## Data Storage & Logging

- **SQLite Database**: All API responses are automatically logged with timestamps

- **Persistent Storage**: Data remains available between sessions

- **Structured Logging**: Each entry includes:

- Timestamp of request

- City name searched

Complete API response data



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




 **Data basa** :
 output
```
REAL-TIME WEATHER DATA LOGGER

MAIN OPERATIONS MENU

A. CHECK CURRENT WEATHER
B. VIEW ALL WEATHER LOGS
C. VIEW RECENT LOGS (LAST 10)
D. SEARCH LOGS BY CITY NAME
E. MANAGE DATA STORAGE
F. SYSTEM SETTINGS
Enter city name (or 'BACK' to return): guntur

Fetching weather data for guntur...
---------------------------------------------------
CURRENT WEATHER REPORT
---------------------------------------------------
City:         Guntur
Temperature:  20.9 C
Humidity:     84 %
Pressure:     1017 hPa
Wind Speed:   1.59 m/s
Condition:    Broken Clouds
Report Time:  2025-12-07 21:59:57
---------------------------------------------------

SUCCESS: Data logged to both database and file.
Options:
1. Check another city
2. Return to main menu
Select option (1 or 2): 1

Enter city name (or 'BACK' to return): ponnur

Fetching weather data for ponnur...

---------------------------------------------------
CURRENT WEATHER REPORT
---------------------------------------------------
City:         Ponnur, IN
Temperature:  22.8 C
Humidity:     84 %
Pressure:     1017 hPa
Wind Speed:   1.66 m/s
Condition:    Overcast Clouds
Report Time:  2025-12-07 22:00:05

 REAL-TIME WEATHER DATA LOGGER
---------------------------------------------------

ALL WEATHER LOGS
---------------------------------------------------

No.  City                 Country    Temp(C)    Humidity(%)  Condition            Time
---------------------------------------------------
1    Tenali              IN         22.7       85           overcast clouds      2025-12-07 16:30:12
2    Ponnur               IN         22.8       84           overcast clouds      2025-12-07 16:30:05
3    London               GB         14.3       90           overcast clouds      2025-12-07 16:29:09
4    Guntur               IN         20.9       84           broken clouds        2025-12-07 16:26:07
Total records in database: 4

---------------------------------------------------
MAIN OPERATIONS MENU
---------------------------------------------------
A. CHECK CURRENT WEATHER
B. VIEW ALL WEATHER LOGS
C. VIEW RECENT LOGS (LAST 10)
D. SEARCH LOGS BY CITY NAME
E. MANAGE DATA STORAGE
F. SYSTEM SETTINGS
X. EXIT APPLICATION

Select option (A-X): X

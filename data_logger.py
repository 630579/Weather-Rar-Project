import sqlite3
from datetime import datetime

class DataLogger:
    def __init__(self):
        self.conn = sqlite3.connect('weather.db')
        self.setup_database()
        
    def setup_database(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT,
                temperature REAL,
                humidity REAL,
                condition TEXT,
                wind_speed REAL,
                timestamp TEXT
            )
        ''')
        self.conn.commit()
        
    def save_weather(self, city, data):
        try:
            self.conn.execute('''
                INSERT INTO weather_data (city, temperature, humidity, condition, wind_speed, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                city,
                data['main']['temp'],
                data['main']['humidity'],
                data['weather'][0]['description'],
                data['wind']['speed'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
        
    def get_recent_data(self, limit=10):
        try:
            cursor = self.conn.execute('SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT ?', (limit,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving data: {e}")
            return []
        
    def get_all_cities(self):
        try:
            cursor = self.conn.execute('SELECT DISTINCT city FROM weather_data')
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error retrieving cities: {e}")
            return []
    
    def close(self):
        if self.conn:
            self.conn.close()
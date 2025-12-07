import requests
import sqlite3
import os
from datetime import datetime
from typing import Dict, Optional, List, Tuple

class WeatherApplication:
    
    def __init__(self):
        
        self.default_api_key = "aa00015428549d15927ba90d925622dc"
        self.api_key = None
        self.db_name = "weather_data.db"
        self.log_file = "weather_log.txt"
        self._initialize_database()
        self._initialize_log_file()
    
    def _initialize_database(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weather_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT NOT NULL,
                    country TEXT,
                    temperature REAL,
                    humidity INTEGER,
                    weather_condition TEXT,
                    wind_speed REAL,
                    pressure INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            print("Database initialized successfully.")
            
        except sqlite3.Error as e:
            print(f"Database Error: {e}")
    
    def _initialize_log_file(self):
        try:
            if not os.path.exists(self.log_file):
                with open(self.log_file, 'w', encoding='utf-8') as f:
                    f.write("-" * 50 + "\n")
                    f.write("WEATHER DATA LOG - Real-Time Weather Information System\n")
                    f.write("-" * 50 + "\n\n")
        except IOError as e:
            print(f"File Error: {e}")
    
    def display_header(self):
        print("\n" + "-" * 50)
        print("       REAL-TIME WEATHER DATA LOGGER")
        print("-" * 50)
    
    def display_menu(self):
        print("\n" + "-" * 50)
        print("MAIN OPERATIONS MENU")
        print("-" * 50)
        print("A. CHECK CURRENT WEATHER")
        print("B. VIEW ALL WEATHER LOGS")
        print("C. VIEW RECENT LOGS (LAST 10)")
        print("D. SEARCH LOGS BY CITY NAME")
        print("E. MANAGE DATA STORAGE")
        print("F. SYSTEM SETTINGS")
        print("X. EXIT APPLICATION")
        print("-" * 50)
    
    def get_api_key(self):
        print("\n" + "-" * 50)
        print("WEATHER INFORMATION SYSTEM SETUP")
        print("-" * 50)
        print("\nUsing default API key for OpenWeatherMap")
        print("You can also use your own API key")
        print("Get one for free at: https://openweathermap.org/api")
        print("-" * 50)
        
        
        api_key = os.environ.get('OPENWEATHER_API_KEY')
        if api_key:
            self.api_key = api_key
            print("\nUsing API key from environment variable.")
            return
        
       
        print(f"\nUsing default API key: {self.default_api_key[:8]}...")
        self.api_key = self.default_api_key
        os.environ['OPENWEATHER_API_KEY'] = self.default_api_key
    
    def fetch_weather_data(self, city_name: str) -> Optional[Dict]:
        try:
            params = {
                'q': city_name,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(
                "http://api.openweathermap.org/data/2.5/weather",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.ConnectionError:
            print("ERROR: Unable to connect to the internet.")
            print("Please check your internet connection.")
            return None
            
        except requests.exceptions.Timeout:
            print("ERROR: Request timed out.")
            print("The server took too long to respond.")
            return None
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"ERROR: City '{city_name}' not found.")
                print("Please check the city name and try again.")
            elif e.response.status_code == 401:
                print("ERROR: Invalid API key.")
                print("Please check your API key.")
            elif e.response.status_code == 429:
                print("ERROR: Too many requests.")
                print("Please wait a few minutes before trying again.")
            else:
                print(f"ERROR {e.response.status_code}: {str(e)}")
            return None
            
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return None
    
    def process_weather_data(self, raw_data: Dict) -> Optional[Dict]:
        try:
            result = {
                'city': raw_data.get('name', 'Unknown'),
                'country': raw_data.get('sys', {}).get('country', 'Unknown'),
                'temperature': raw_data['main'].get('temp'),
                'humidity': raw_data['main'].get('humidity'),
                'pressure': raw_data['main'].get('pressure'),
                'weather': raw_data['weather'][0].get('description', 'Unknown') 
                          if raw_data.get('weather') else 'Unknown',
                'wind_speed': raw_data.get('wind', {}).get('speed', 0),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return result
            
        except (KeyError, IndexError):
            print("ERROR: Invalid data received from API.")
            return None
    
    def display_weather_report(self, weather_info: Dict):
        print("\n" + "-" * 50)
        print("CURRENT WEATHER REPORT")
        print("-" * 50)
        print(f"City:         {weather_info['city']}, {weather_info['country']}")
        print(f"Temperature:  {weather_info['temperature']:.1f} C")
        print(f"Humidity:     {weather_info['humidity']} %")
        print(f"Pressure:     {weather_info['pressure']} hPa")
        print(f"Wind Speed:   {weather_info['wind_speed']} m/s")       
        print(f"Condition:    {weather_info['weather'].title()}")
        print(f"Report Time:  {weather_info['timestamp']}")
        print("=" * 60)
    
    def log_to_database(self, weather_info: Dict) -> bool:
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO weather_logs 
                (city, country, temperature, humidity, weather_condition, wind_speed, pressure)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                weather_info['city'],
                weather_info['country'],
                weather_info['temperature'],
                weather_info['humidity'],
                weather_info['weather'],
                weather_info['wind_speed'],
                weather_info['pressure']
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error as e:
            print(f"Database Error: {e}")
            return False
    
    def log_to_file(self, weather_info: Dict) -> bool:
        try:
            log_entry = (
                f"[{weather_info['timestamp']}] "
                f"City: {weather_info['city']}, "
                f"Country: {weather_info['country']}, "
                f"Temperature: {weather_info['temperature']:.1f}C, "
                f"Humidity: {weather_info['humidity']}%, "
                f"Pressure: {weather_info['pressure']} hPa, "
                f"Wind Speed: {weather_info['wind_speed']} m/s, "
                f"Condition: {weather_info['weather']}\n"
            )
            
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            
            return True
            
        except IOError as e:
            print(f"File Error: {e}")
            return False
    
    def check_current_weather(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.display_header()
        
        print("\n" + "-" * 50)
        print("CHECK CURRENT WEATHER")
        print("-" * 50)
        
        while True:
            city = input("\nEnter city name (or 'BACK' to return): ").strip()
            
            if city.upper() == 'BACK':
                break
                
            if not city:
                print("ERROR: City name cannot be empty.")
                continue
            
            print(f"\nFetching weather data for {city}...")
            
            # Fetch data
            raw_data = self.fetch_weather_data(city)
            if not raw_data:
                continue

            weather_info = self.process_weather_data(raw_data)
            if not weather_info:
                continue
            
            self.display_weather_report(weather_info)
            
            
            db_success = self.log_to_database(weather_info)
            file_success = self.log_to_file(weather_info)
            
            if db_success and file_success:
                print("\nSUCCESS: Data logged to both database and file.")
            elif db_success:
                print("\nSUCCESS: Data logged to database.")
            elif file_success:
                print("\nSUCCESS: Data logged to file.")
            else:
                print("\nERROR: Failed to log data.")
            
            print("\n" + "-" * 50)
            print("Options:")
            print("1. Check another city")
            print("2. Return to main menu")
            print("-" * 50)
            
            choice = input("\nSelect option (1 or 2): ").strip()
            if choice == '2':
                break
    
    def get_all_logs(self) -> List[Tuple]:
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT city, country, temperature, humidity, weather_condition, timestamp
                FROM weather_logs 
                ORDER BY timestamp DESC
            ''')
            
            logs = cursor.fetchall()
            conn.close()
            
            return logs
            
        except sqlite3.Error as e:
            print(f"Database Error: {e}")
            return []
    
    def view_all_logs(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.display_header()
        
        print("\n" + "-" * 40)
        print("ALL WEATHER LOGS")
        print("-" * 40)
        
        logs = self.get_all_logs()
        
        if not logs:
            print("\nNo weather logs found in database.")
            input("\nPress Enter to continue...")
            return
        
        print(f"\n{'No.':<4} {'City':<20} {'Country':<10} {'Temp(C)':<10} {'Humidity(%)':<12} {'Condition':<20} {'Time'}")
        print("-" * 40)
        
        for i, log in enumerate(logs, 1):
            city, country, temp, humidity, condition, timestamp = log
            
           
            condition_display = condition[:18] + '...' if len(condition) > 18 else condition
            
            print(f"{i:<4} {city:<20} {country:<10} {temp:<10.1f} {humidity:<12} {condition_display:<20} {timestamp}")
        
        print("-" * 40)
        print(f"Total records in database: {len(logs)}")
        
        input("\nPress Enter to continue...")
    
    def view_recent_logs(self):

        os.system('cls' if os.name == 'nt' else 'clear')
        self.display_header()
        
        print("\n" + "-" * 40)
        print("RECENT WEATHER LOGS (LAST 10)")
        print("-" * 40)
        
        logs = self.get_all_logs()[:10] 
        
        if not logs:
            print("\nNo logs found in database.")
            input("\nPress Enter to continue...")
            return
        
        print(f"\n{'No.':<4} {'City':<20} {'Country':<10} {'Temp(C)':<10} {'Humidity(%)':<12} {'Condition':<20} {'Time'}")
        print("-" * 40)
        
        for i, log in enumerate(logs, 1):
            city, country, temp, humidity, condition, timestamp = log
            
            
            condition_display = condition[:18] + '...' if len(condition) > 18 else condition
            
            print(f"{i:<4} {city:<20} {country:<10} {temp:<10.1f} {humidity:<12} {condition_display:<20} {timestamp}")
        
        print("-" * 40)
        
        try:
            if os.path.exists(self.log_file):
                file_size = os.path.getsize(self.log_file) / 1024
                print(f"Log file size: {file_size:.2f} KB")
        except OSError:
            pass
        
        input("\nPress Enter to continue...")
    
    def search_logs(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.display_header()
        
        print("\n" + "-" * 50)
        print("SEARCH WEATHER LOGS")
        print("-" * 50)
        
        search_term = input("\nEnter city name to search: ").strip().lower()
        
        if not search_term:
            print("ERROR: Search term cannot be empty.")
            input("\nPress Enter to continue...")
            return
        
        logs = self.get_all_logs()
        results = []
        
        for log in logs:
            city, country, temp, humidity, condition, timestamp = log
            if search_term in city.lower():
                results.append(log)
        
        if not results:
            print(f"\nNo logs found for '{search_term}'.")
            input("\nPress Enter to continue...")
            return
        
        print(f"\nSEARCH RESULTS FOR '{search_term.upper()}'")
        print("-" * 40)
        print(f"{'No.':<4} {'City':<20} {'Country':<10} {'Temp(C)':<10} {'Humidity(%)':<12} {'Condition':<20} {'Time'}")
        print("-" * 40)
        
        for i, log in enumerate(results, 1):
            city, country, temp, humidity, condition, timestamp = log
            condition_display = condition[:18] + '...' if len(condition) > 18 else condition
            
            print(f"{i:<4} {city:<20} {country:<10} {temp:<10.1f} {humidity:<12} {condition_display:<20} {timestamp}")
        
        print("-" * 40)
        print(f"Found {len(results)} matching record(s)")
        
        input("\nPress Enter to continue...")
    
    def manage_data_storage(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.display_header()
            
            print("\n" + "-" * 50)
            print("DATA STORAGE MANAGEMENT")
            print("-" * 50)
            print("1. Clear all database logs")
            print("2. Clear log file")
            print("3. View storage information")
            print("4. Back to main menu")
            print("-" * 50)
            
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == "1":
                self.clear_database_logs()
            elif choice == "2":
                self.clear_log_file()
            elif choice == "3":
                self.view_storage_info()
            elif choice == "4":
                break
            else:
                print("\nInvalid choice. Please enter 1-4.")
                input("Press Enter to continue...")
    
    def clear_database_logs(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.display_header()
        
        print("\n" + "-" * 50)
        print("CLEAR DATABASE LOGS")
        print("-" * 50)
        
        confirm = input("\nAre you sure you want to clear ALL database logs? (yes/no): ").strip().lower()
        
        if confirm != 'yes':
            print("\nOperation cancelled.")
            input("\nPress Enter to continue...")
            return
        
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM weather_logs')
            conn.commit()
            conn.close()
            
            print("\nSUCCESS: All database logs cleared successfully.")
            
        except Exception as e:
            print(f"\nERROR: Failed to clear database logs: {e}")
        
        input("\nPress Enter to continue...")
    
    def clear_log_file(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.display_header()
        
        print("\n" + "-" * 50)
        print("CLEAR LOG FILE")
        print("-" * 0)
        
        confirm = input("\nAre you sure you want to clear the log file? (yes/no): ").strip().lower()
        
        if confirm != 'yes':
            print("\nOperation cancelled.")
            input("\nPress Enter to continue...")
            return
        
        try:
            self._initialize_log_file()
            print("\nSUCCESS: Log file cleared successfully.")
            
        except Exception as e:
            print(f"\nERROR: Failed to clear log file: {e}")
        
        input("\nPress Enter to continue...")
    
    def view_storage_info(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.display_header()
        
        print("\n" + "-" * 50)
        print("STORAGE INFORMATION")
        print("-" * 50)
        
        
        logs = self.get_all_logs()
        print(f"\nDatabase Records: {len(logs)}")
        
        
        try:
            if os.path.exists(self.log_file):
                file_size = os.path.getsize(self.log_file)
                print(f"Log File Size:    {file_size} bytes ({file_size/1024:.2f} KB)")
            else:
                print(f"Log File Status:  Not found")
        except OSError:
            print(f"Log File Status:  Error reading file")
        
        print("\n" + "-" * 50)
        
        input("\nPress Enter to continue...")
    
    def system_settings(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.display_header()
            
            print("\n" + "-" * 50)
            print("SYSTEM SETTINGS")
            print("-" * 50)
            print("1. Change API key")
            print("2. Test API connection")
            print("3. View application info")
            print("4. Back to main menu")
            print("-" * 50)
            
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == "1":
                self.change_api_key()
            elif choice == "2":
                self.test_api_connection()
            elif choice == "3":
                self.view_application_info()
            elif choice == "4":
                break
            else:
                print("\nInvalid choice. Please enter 1-4.")
                input("Press Enter to continue...")
    
    def change_api_key(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.display_header()
        
        print("\n" + "-" * 50)
        print("CHANGE API KEY")
        print("-" * 50)
        
        new_key = input("\nEnter new API key: ").strip()
        
        if not new_key:
            print("\nERROR: API key cannot be empty.")
            input("\nPress Enter to continue...")
            return
        
        old_key = self.api_key
        self.api_key = new_key
        os.environ['OPENWEATHER_API_KEY'] = new_key
        
       
        print("\nTesting new API key...")
        test_result = self.fetch_weather_data("London")
        
        if test_result:
            print("\nSUCCESS: New API key is working.")
        else:
            print("\nERROR: New API key failed. Reverting to old key.")
            self.api_key = old_key
            os.environ['OPENWEATHER_API_KEY'] = old_key
        
        input("\nPress Enter to continue...")
    
    def test_api_connection(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.display_header()
        
        print("\n" + "-" * 50)
        print("API CONNECTION TEST")
        print("-" * 50)
        
        print("\nTesting connection to OpenWeatherMap API...")
        
        test_city = "London"
        result = self.fetch_weather_data(test_city)
        
        if result:
            print("\nSUCCESS: API connection is working.")
            print(f"Tested with city: {test_city}")
        else:
            print("\nERROR: API connection failed.")
            print("Please check your API key and internet connection.")
        
        input("\nPress Enter to continue...")
    
    def view_application_info(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.display_header()
        
        print("\n" + "-" * 50)
        print("APPLICATION INFORMATION")
        print("=" * 50)
        
        print("\nWeather Information System v1.0")
        print("Real-Time Weather Data Logger")
        print("\nFeatures:")
        print("- Fetch current weather for any city")
        print("- Store data in SQLite database")
        print("- Log data to text file")
        print("- View and search weather history")
        print("- Manage data storage")
        print("\nAPI Provider: OpenWeatherMap")
        print("Data Units: Metric (Celsius)")
        print("\n" + "-" * 50)
        
        input("\nPress Enter to continue...")
    
    def run(self):
      
        self.get_api_key()
        
      
        os.system('cls' if os.name == 'nt' else 'clear')
        self.display_header()
        
        print("\nTesting API connection...")
        test_result = self.fetch_weather_data("London")
        
        if not test_result:
            print("\nERROR: Failed to connect with the provided API key.")
            print("Please check your API key and try again.")
            input("\nPress Enter to exit...")
            return
        
        print("\nSUCCESS: API connection established!")
        input("\nPress Enter to start the application...")
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.display_header()
            self.display_menu()
            
            try:
                choice = input("\nSelect option (A-X): ").strip().upper()
                
                if choice == 'A':
                    self.check_current_weather()
                elif choice == 'B':
                    self.view_all_logs()
                elif choice == 'C':
                    self.view_recent_logs()
                elif choice == 'D':
                    self.search_logs()
                elif choice == 'E':
                    self.manage_data_storage()
                elif choice == 'F':
                    self.system_settings()
                elif choice == 'X':
                    print("\n" + "-" * 50)
                    print("Thank you for using Weather Information System")
                    print("Application terminated")
                    print("-" * 50)
                    break
                else:
                    print("\nInvalid selection. Please enter A, B, C, D, E, F, or X.")
                    input("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\nApplication interrupted by user.")
                break
            except Exception as e:
                print(f"\nError: {e}")
                input("Press Enter to continue...")


def main():
    try:
        try:                       
            import requests
        except ImportError:
            print("ERROR: 'requests' library is not installed.")
            print("Please install it using: pip install requests")
            return
        app = WeatherApplication()
        app.run()
        
    except KeyboardInterrupt:
        print("\n\nApplication terminated by user.")
    except Exception as e:
        print(f"\nFatal Error: {e}")
        print("\nPlease check your setup and try again.")


if __name__ == "__main__":

    main()

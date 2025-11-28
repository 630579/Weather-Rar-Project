from weather_api import WeatherAPI
from data_logger import DataLogger

class WeatherApp:
    def __init__(self):
        self.weather_api = WeatherAPI()
        self.data_logger = DataLogger()
        
    def display_weather(self, data):
        print(f"\n=== Weather in {data['name']} ===")
        print(f"Temperature: {data['main']['temp']} °C")
        print(f"Humidity: {data['main']['humidity']} %")
        print(f"Wind Speed: {data['wind']['speed']} m/s")
        print(f"Conditions: {data['weather'][0]['description']}")
        print("=" * 40)
        
    def check_weather(self):
        city = input("Enter city name: ").strip()   # enter details to check weather
        
        if not city:
            print("Error: Please enter a city name!")
            return
            
        print(f"Getting weather data for {city}...")
        data = self.weather_api.get_weather(city)
        
        if data:
            self.display_weather(data)                      #data saved
            if self.data_logger.save_weather(city, data):
                print("Data saved successfully!")
            else:
                print("Error: Failed to save data!")
        else:
            print("Error: City not found or API issue!")
            
    def show_history(self):
        data = self.data_logger.get_recent_data()
        print("\n=== Recent Weather Searches ===")
        
        if not data:
            print("No data found!")
            return
            
        for item in data:
            print(f"{item[1]}: {item[2]}°C, {item[3]}% humidity, {item[5]} m/s wind")
            print(f"Condition: {item[4]}")
            print(f"Time: {item[6]}")
            print()
            
    def run(self):
        print("=== Weather Information App ===")
        
        # api key is entered 
        if self.weather_api.api_key == "aa00015428549d15927ba90d925622dc":
            print("Please configure your API key in config.py")
            print("Get free API key from: https://openweathermap.org/api")
            print("Using default key - some features may not work properly")
            
        while True:
            print("\nMain Menu:")
            print("1. Check weather")
            print("2. View history")
            print("3. Exit")
            
            choice = input("Enter your choice (1-3): ").strip()
            if choice == "1":
                self.check_weather()
            elif choice == "2":
                self.show_history()
            elif choice == "3":
                print("Thank you! Good bye!")
                self.data_logger.close()
                break
            else:
                print("Invalid choice! Please enter 1, 2, or 3.")

if __name__ == "__main__":
    app = WeatherApp()
    app.run()
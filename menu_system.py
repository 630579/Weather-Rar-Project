import os
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SCREEN_WIDTH, DATE_FORMAT, DISPLAY_DATE_FORMAT, MENU_OPTIONS


class MenuSystem:
    """Handles all user interface operations"""
    
    @staticmethod
    def clear_screen() -> None:
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def display_header(title: str = "WEATHER INFORMATION SYSTEM") -> None:
        """
        Display application header
        
        Args:
            title (str): Header title
        """
        print("\n" + "=" * SCREEN_WIDTH)
        print(f"{title:^{SCREEN_WIDTH}}")
        print("=" * SCREEN_WIDTH)
    
    @staticmethod
    def display_main_menu() -> None:
        """Display main menu options"""
        MenuSystem.display_header("MAIN OPERATIONS MENU")
        
        print("\n" + "-" * SCREEN_WIDTH)
        print("SELECT AN OPTION:")
        print("-" * SCREEN_WIDTH)
        
        for key, value in MENU_OPTIONS.items():
            print(f"  {key}. {value}")
        
        print("-" * SCREEN_WIDTH)
    
    @staticmethod
    def display_weather_info(weather_info: dict) -> None:
        """
        Display weather information in formatted output
        
        Args:
            weather_info (dict): Weather information to display
        """
        if not weather_info:
            print("\nNo weather information available to display.")
            return
        
        print("\n" + "=" * 60)
        print("CURRENT WEATHER REPORT")
        print("=" * 60)
        print(f"Location:        {weather_info.get('city', 'N/A')}, {weather_info.get('country', 'N/A')}")
        print(f"Temperature:     {weather_info.get('temperature', 'N/A'):.1f}°C")
        print(f"Humidity:        {weather_info.get('humidity', 'N/A')}%")
        print(f"Pressure:        {weather_info.get('pressure', 'N/A')} hPa")
        print(f"Weather:         {weather_info.get('weather_description', 'N/A').title()}")
        print(f"Wind Speed:      {weather_info.get('wind_speed', 'N/A')} m/s")
    
    @staticmethod
    def display_logs(logs: list, title: str = "WEATHER LOGS") -> None:
        """
        Display weather logs in formatted table
        
        Args:
            logs (list): List of log records
            title (str): Table title
        """
        if not logs:
            print("\nNo logs available.")
            return
        
        print(f"\n{'='*90}")
        print(f"{title:^90}")
        print(f"{'='*90}")
        print(f"{'No.':<4} {'Date/Time':<20} {'City':<20} {'Temp(°C)':<10} {'Humidity(%)':<12} {'Condition':<20}")
        print(f"{'-'*90}")
        
        for i, log in enumerate(logs, 1):
            city, country, temp, humidity, condition, timestamp = log
            try:
                dt = datetime.strptime(timestamp, DATE_FORMAT)
                display_time = dt.strftime(DISPLAY_DATE_FORMAT)
            except:
                display_time = timestamp[:16]
            if country and country != 'Unknown':
                location = f"{city}, {country}"
            else:
                location = city
            if len(location) > 19:
                location = location[:16] + "..."
            condition_display = condition[:17] + "..." if len(condition) > 17 else condition
            
            print(f"{i:<4} {display_time:<20} {location:<20} {temp:<10.1f} {humidity:<12} {condition_display:<20}")
        
        print(f"{'='*90}")
        print(f"Total Records: {len(logs)}")
    
    @staticmethod
    def display_message(message: str, msg_type: str = "INFO") -> None:
        """
        Display formatted message
        
        Args:
            message (str): Message to display
            msg_type (str): Type of message (INFO, SUCCESS, ERROR, WARNING)
        """
        symbols = {
            "INFO": "[i]",
            "SUCCESS": "[✓]",
            "ERROR": "[✗]",
            "WARNING": "[!]"
        }
        
        symbol = symbols.get(msg_type.upper(), "[i]")
        print(f"\n{symbol} {message}")
    
    @staticmethod
    def display_submenu(options: dict, title: str = "SUB-MENU") -> None:
        """
        Display submenu with options
        
        Args:
            options (dict): Dictionary of options {key: description}
            title (str): Submenu title
        """
        MenuSystem.display_header(title)
        
        print("\n" + "-" * SCREEN_WIDTH)
        print("SELECT AN OPTION:")
        print("-" * SCREEN_WIDTH)
        
        for key, value in options.items():
            print(f"  {key}. {value}")
        
        print("-" * SCREEN_WIDTH)
    
    @staticmethod
    def get_user_input(prompt: str) -> str:
        """
        Get input from user with prompt
        
        Args:
            prompt (str): Input prompt
            
        Returns:
            str: User input
        """
        return input(f"\n{prompt}: ").strip()
    
    @staticmethod
    def get_confirmation(prompt: str) -> bool:
        """
        Get confirmation from user
        
        Args:
            prompt (str): Confirmation prompt
            
        Returns:
            bool: True if confirmed, False otherwise
        """
        response = input(f"\n{prompt} (yes/no): ").strip().lower()
        return response in ['yes', 'y']
    
    @staticmethod
    def display_exit_message() -> None:
        """Display exit message"""
        MenuSystem.display_header("APPLICATION TERMINATED")
        print("\nThank you for using Weather Information System.")
        print("Goodbye!")
import os
from typing import Dict
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import LOG_FILE_NAME, DATE_FORMAT


class FileLogger:
    """Handles file-based logging of weather data"""
    
    def __init__(self, filename: str = LOG_FILE_NAME):
        """
        Initialize FileLogger
        
        Args:
            filename (str): Log file name
        """
        self.filename = filename
        self._ensure_data_directory()
        self._initialize_log_file()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        data_dir = os.path.dirname(self.filename)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def _initialize_log_file(self):
        """Create log file with header if it doesn't exist"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("WEATHER DATA LOG - Real-Time Weather Information System\n")
                f.write("=" * 80 + "\n")
                f.write("Created: " + datetime.now().strftime(DATE_FORMAT) + "\n")
                f.write("\n")
    
    def log_weather_data(self, weather_info: Dict) -> bool:
        """
        Log weather data to text file
        
        Args:
            weather_info (Dict): Weather information to log
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            timestamp = datetime.now().strftime(DATE_FORMAT)
            
            log_entry = f"""
[{timestamp}] Weather Report for {weather_info.get('city', 'Unknown')}, {weather_info.get('country', 'Unknown')}
    Temperature:     {weather_info.get('temperature', 'N/A'):.1f}°C
    Humidity:        {weather_info.get('humidity', 'N/A')}%
    Pressure:        {weather_info.get('pressure', 'N/A')} hPa
    Weather:         {weather_info.get('weather_description', 'N/A')}
    Wind Speed:      {weather_info.get('wind_speed', 'N/A')} m/s
{'='*80}
"""
            
            with open(self.filename, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            
            return True
            
        except IOError as e:
            print(f"File Logging Error: {str(e)}")
            return False
    
    def get_log_file_size(self) -> int:
        """
        Get size of log file in bytes
        
        Returns:
            int: File size in bytes, -1 if error
        """
        try:
            if os.path.exists(self.filename):
                return os.path.getsize(self.filename)
            return 0
        except OSError:
            return -1
    
    def clear_log_file(self) -> bool:
        """
        Clear log file contents
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self._initialize_log_file()
            return True
        except IOError as e:
            print(f"File Clear Error: {str(e)}")
            return False
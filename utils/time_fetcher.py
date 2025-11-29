"""
دریافت زمان و تاریخ از اینترنت
"""
import urllib.request
import urllib.error
import json
from datetime import datetime
from typing import Optional, Tuple

class TimeFetcher:
    """دریافت زمان از اینترنت"""
    
    # چند API مختلف برای دریافت زمان
    TIME_APIS = [
        "http://worldtimeapi.org/api/timezone/Asia/Tehran",
        "http://worldtimeapi.org/api/ip",
        "https://timeapi.io/api/Time/current/zone?timeZone=Asia/Tehran",
    ]
    
    @staticmethod
    def fetch_time_from_internet() -> Optional[Tuple[datetime, str]]:
        """
        دریافت زمان از اینترنت
        Returns: (datetime object, timezone) or None if failed
        """
        for api_url in TimeFetcher.TIME_APIS:
            try:
                with urllib.request.urlopen(api_url, timeout=5) as response:
                    data = json.loads(response.read().decode())
                    
                    # پردازش پاسخ از worldtimeapi.org
                    if 'datetime' in data:
                        dt_str = data['datetime']
                        timezone = data.get('timezone', 'UTC')
                        # تبدیل به datetime
                        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
                        return dt, timezone
                    
                    # پردازش پاسخ از timeapi.io
                    elif 'dateTime' in data:
                        dt_str = data['dateTime']
                        timezone = data.get('timeZone', 'UTC')
                        dt = datetime.fromisoformat(dt_str)
                        return dt, timezone
                        
            except (urllib.error.URLError, urllib.error.HTTPError, 
                    json.JSONDecodeError, ValueError, KeyError, TimeoutError) as e:
                continue
        
        return None
    
    @staticmethod
    def get_local_time() -> datetime:
        """دریافت زمان محلی سیستم"""
        return datetime.now()
    
    @staticmethod
    def format_datetime(dt: datetime, date_format: str = "%Y-%m-%d", 
                       time_format: str = "%H:%M:%S") -> Tuple[str, str]:
        """
        فرمت کردن تاریخ و زمان
        Returns: (date_string, time_string)
        """
        date_str = dt.strftime(date_format)
        time_str = dt.strftime(time_format)
        return date_str, time_str


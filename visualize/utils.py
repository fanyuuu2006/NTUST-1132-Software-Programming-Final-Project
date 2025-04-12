import pandas as pd
from datetime import datetime

def convert_timestamp(timestamp: int) -> str:
    """將時間戳轉換為 HH:MM"""
    return datetime.fromtimestamp(timestamp).strftime('%H:%M')

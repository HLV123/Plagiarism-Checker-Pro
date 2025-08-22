# config.py
"""
Cấu hình API và các thông số cho plagiarism checker
"""

# API Configuration
API_KEY = ""
SEARCH_ENGINE_ID = ""
BASE_URL = "https://www.googleapis.com/customsearch/v1"

# Plagiarism Settings
SIMILARITY_THRESHOLD = 0.6  # 60% để coi là đạo văn
MAX_REQUESTS_PER_DAY = 100
REQUEST_DELAY = 1  # Giây delay giữa các requests

# Text Processing Settings
MIN_SENTENCE_WORDS = 5
MAX_SENTENCE_WORDS = 20
MAX_RESULTS_PER_SEARCH = 3

# Risk Levels
RISK_LEVELS = {
    'HIGH': 30,    # > 30% = HIGH RISK
    'MEDIUM': 15,  # 15-30% = MEDIUM RISK
    'LOW': 0       # < 15% = LOW RISK
}

# Colors for GUI
COLORS = {
    'HIGH': '#ff4444',      # Red
    'MEDIUM': '#ffaa00',    # Orange  
    'LOW': '#44ff44',       # Green
    'PRIMARY': '#2196F3',   # Blue
    'SECONDARY': '#757575', # Gray
    'BACKGROUND': '#f5f5f5',
    'WHITE': '#ffffff'
}
# api.py
"""
Xử lý API calls với Google Custom Search
"""

import requests
import time
from typing import List, Dict
from config import API_KEY, SEARCH_ENGINE_ID, BASE_URL, REQUEST_DELAY, MAX_RESULTS_PER_SEARCH

class GoogleSearchAPI:
    def __init__(self):
        self.api_key = API_KEY
        self.search_engine_id = SEARCH_ENGINE_ID
        self.base_url = BASE_URL
        self.requests_made = 0
        
    def test_connection(self) -> bool:
        """Test API connection"""
        try:
            result = self.search("python programming", max_results=1)
            return len(result) > 0
        except:
            return False
    
    def search(self, query: str, max_results: int = MAX_RESULTS_PER_SEARCH) -> List[Dict]:
        """
        Tìm kiếm với Google Custom Search API
        """
        if not query or len(query.strip()) < 3:
            return []
            
        params = {
            'key': self.api_key,
            'cx': self.search_engine_id,
            'q': f'"{query.strip()}"',
            'num': min(max_results, 10),
            'safe': 'medium',
            'lr': 'lang_en'
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=15)
            self.requests_made += 1
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for item in data.get('items', []):
                    results.append({
                        'title': item.get('title', ''),
                        'link': item.get('link', ''),
                        'snippet': item.get('snippet', ''),
                        'display_link': item.get('displayLink', '')
                    })
                
                # Add delay to avoid rate limiting
                time.sleep(REQUEST_DELAY)
                return results
                
            elif response.status_code == 403:
                print("❌ API Error: Quota exceeded or invalid key")
                return []
            else:
                print(f"❌ API Error: {response.status_code}")
                return []
                
        except requests.RequestException as e:
            print(f"❌ Network error: {e}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return []
    
    def get_requests_made(self) -> int:
        """Lấy số requests đã sử dụng"""
        return self.requests_made
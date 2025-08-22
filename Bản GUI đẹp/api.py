import requests
import time
import json
from typing import List, Dict, Optional
from config import *

class GoogleSearchAPI:
    def __init__(self):
        self.api_key = API_KEY
        self.search_engine_id = SEARCH_ENGINE_ID
        self.base_url = BASE_URL
        self.requests_made = 0
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PlagiarismChecker/1.0 (Educational Purpose)'
        })
        
    def test_connection(self) -> bool:
        try:
            result = self.search("python programming test", max_results=1)
            return len(result) > 0
        except Exception:
            return False
    
    def search(self, query: str, max_results: int = MAX_RESULTS_PER_SEARCH) -> List[Dict]:
        if not query or len(query.strip()) < 4:
            return []
            
        query_cleaned = self._clean_query(query.strip())
        
        params = {
            'key': self.api_key,
            'cx': self.search_engine_id,
            'q': f'"{query_cleaned}"',
            'num': min(max_results, 10),
            'safe': 'active',
            'lr': 'lang_en',
            'gl': 'us',
            'hl': 'en',
            'filter': '1'
        }
        
        try:
            response = self.session.get(
                self.base_url, 
                params=params, 
                timeout=20
            )
            self.requests_made += 1
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for item in data.get('items', []):
                    snippet = item.get('snippet', '').strip()
                    if len(snippet) > 10:
                        results.append({
                            'title': item.get('title', '').strip(),
                            'link': item.get('link', '').strip(),
                            'snippet': snippet,
                            'display_link': item.get('displayLink', '').strip(),
                            'formatted_url': item.get('formattedUrl', '').strip()
                        })
                
                time.sleep(REQUEST_DELAY)
                return results[:max_results]
                
            elif response.status_code == 403:
                raise Exception("API quota exceeded or invalid credentials")
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded")
            else:
                raise Exception(f"API request failed with status {response.status_code}")
                
        except requests.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("Invalid response format from API")
        except Exception as e:
            raise Exception(f"Search failed: {str(e)}")
    
    def _clean_query(self, query: str) -> str:
        import re
        query = re.sub(r'[^\w\s\-\.]', ' ', query)
        query = re.sub(r'\s+', ' ', query)
        return query.strip()
    
    def get_requests_made(self) -> int:
        return self.requests_made
    
    def get_remaining_requests(self) -> int:
        return max(0, MAX_REQUESTS_PER_DAY - self.requests_made)
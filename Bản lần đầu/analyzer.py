# analyzer.py
"""
Phân tích văn bản và tính toán độ tương đồng
"""

import re
from difflib import SequenceMatcher
from typing import List, Dict
from config import MIN_SENTENCE_WORDS, MAX_SENTENCE_WORDS, SIMILARITY_THRESHOLD

class TextAnalyzer:
    def __init__(self):
        self.similarity_threshold = SIMILARITY_THRESHOLD
    
    def extract_sentences(self, text: str) -> List[str]:
        """
        Tách văn bản thành các câu
        """
        # Clean text
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Split by sentence endings
        sentences = re.split(r'[.!?]+', text)
        
        # Filter sentences by word count
        filtered_sentences = []
        for sentence in sentences:
            words = sentence.strip().split()
            if MIN_SENTENCE_WORDS <= len(words) <= MAX_SENTENCE_WORDS:
                filtered_sentences.append(sentence.strip())
        
        return filtered_sentences
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Tính độ tương đồng giữa hai văn bản
        """
        if not text1 or not text2:
            return 0.0
        
        # Normalize texts
        text1 = re.sub(r'\s+', ' ', text1.lower().strip())
        text2 = re.sub(r'\s+', ' ', text2.lower().strip())
        
        # Method 1: Sequence similarity
        seq_similarity = SequenceMatcher(None, text1, text2).ratio()
        
        # Method 2: Word overlap
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            word_similarity = 0
        else:
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            word_similarity = len(intersection) / len(union) if union else 0
        
        # Method 3: Exact substring match
        substring_similarity = 0
        if text1 in text2 or text2 in text1:
            substring_similarity = 0.9
        
        # Weighted combination
        final_similarity = (seq_similarity * 0.4 + 
                          word_similarity * 0.4 + 
                          substring_similarity * 0.2)
        
        return final_similarity
    
    def analyze_sentence(self, sentence: str, search_results: List[Dict]) -> Dict:
        """
        Phân tích một câu với kết quả tìm kiếm
        """
        best_match = {
            'sentence': sentence,
            'similarity': 0.0,
            'source': None,
            'source_title': '',
            'matched_text': '',
            'is_plagiarism': False,
            'confidence': 'low'
        }
        
        for result in search_results:
            similarity = self.calculate_similarity(sentence, result['snippet'])
            
            if similarity > best_match['similarity']:
                confidence = self._get_confidence_level(similarity)
                
                best_match = {
                    'sentence': sentence,
                    'similarity': similarity,
                    'source': result['link'],
                    'source_title': result['title'],
                    'matched_text': result['snippet'],
                    'is_plagiarism': similarity > self.similarity_threshold,
                    'confidence': confidence
                }
        
        return best_match
    
    def _get_confidence_level(self, similarity: float) -> str:
        """
        Xác định mức độ tin cậy dựa trên similarity score
        """
        if similarity > 0.8:
            return 'high'
        elif similarity > 0.6:
            return 'medium'
        else:
            return 'low'
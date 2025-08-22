import re
import string
from difflib import SequenceMatcher
from typing import List, Dict, Tuple, Set
from collections import Counter
from config import *

class TextAnalyzer:
    def __init__(self):
        self.similarity_threshold = SIMILARITY_THRESHOLD
        self.stop_words = self._load_stop_words()
        
    def _load_stop_words(self) -> Set[str]:
        common_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those',
            'it', 'he', 'she', 'they', 'we', 'you', 'i', 'me', 'him', 'her',
            'them', 'us', 'my', 'your', 'his', 'her', 'its', 'our', 'their'
        }
        return common_words
    
    def extract_sentences(self, text: str) -> List[str]:
        text = self._clean_text(text)
        
        sentence_patterns = [
            r'[.!?]+\s+(?=[A-Z])',
            r'[.!?]+$',
            r'\n\s*\n',
            r';\s+(?=[A-Z])'
        ]
        
        sentences = [text]
        for pattern in sentence_patterns:
            new_sentences = []
            for sentence in sentences:
                parts = re.split(pattern, sentence)
                new_sentences.extend([p.strip() for p in parts if p.strip()])
            sentences = new_sentences
        
        filtered_sentences = []
        for sentence in sentences:
            words = self._extract_words(sentence)
            if MIN_SENTENCE_WORDS <= len(words) <= MAX_SENTENCE_WORDS:
                if self._is_meaningful_sentence(sentence, words):
                    filtered_sentences.append(sentence.strip())
        
        return filtered_sentences
    
    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\.\!\?\;\:\,\-\'\"]', ' ', text)
        return text.strip()
    
    def _extract_words(self, text: str) -> List[str]:
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        return [w for w in words if len(w) > 2 and w not in self.stop_words]
    
    def _is_meaningful_sentence(self, sentence: str, words: List[str]) -> bool:
        if len(words) < 3:
            return False
        if len(sentence) < 20:
            return False
        return True
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        if not text1 or not text2:
            return 0.0
        
        text1_clean = self._normalize_text(text1)
        text2_clean = self._normalize_text(text2)
        
        if not text1_clean or not text2_clean:
            return 0.0
        
        sequence_sim = self._sequence_similarity(text1_clean, text2_clean)
        semantic_sim = self._semantic_similarity(text1_clean, text2_clean)
        structural_sim = self._structural_similarity(text1_clean, text2_clean)
        lexical_sim = self._lexical_similarity(text1_clean, text2_clean)
        
        weights = [0.3, 0.3, 0.2, 0.2]
        similarities = [sequence_sim, semantic_sim, structural_sim, lexical_sim]
        
        final_similarity = sum(w * s for w, s in zip(weights, similarities))
        
        return min(1.0, max(0.0, final_similarity))
    
    def _normalize_text(self, text: str) -> str:
        text = text.lower().strip()
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def _sequence_similarity(self, text1: str, text2: str) -> float:
        return SequenceMatcher(None, text1, text2).ratio()
    
    def _semantic_similarity(self, text1: str, text2: str) -> float:
        words1 = set(self._extract_words(text1))
        words2 = set(self._extract_words(text2))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        jaccard_sim = len(intersection) / len(union) if union else 0
        
        overlap_ratio = len(intersection) / min(len(words1), len(words2))
        
        return (jaccard_sim + overlap_ratio) / 2
    
    def _structural_similarity(self, text1: str, text2: str) -> float:
        len1, len2 = len(text1), len(text2)
        if len1 == 0 or len2 == 0:
            return 0.0
        
        length_sim = 1 - abs(len1 - len2) / max(len1, len2)
        
        words1, words2 = text1.split(), text2.split()
        word_count_sim = 1 - abs(len(words1) - len(words2)) / max(len(words1), len(words2))
        
        return (length_sim + word_count_sim) / 2
    
    def _lexical_similarity(self, text1: str, text2: str) -> float:
        words1 = text1.split()
        words2 = text2.split()
        
        if not words1 or not words2:
            return 0.0
        
        counter1 = Counter(words1)
        counter2 = Counter(words2)
        
        all_words = set(words1 + words2)
        cosine_sim = sum(counter1[word] * counter2[word] for word in all_words)
        
        norm1 = sum(count * count for count in counter1.values()) ** 0.5
        norm2 = sum(count * count for count in counter2.values()) ** 0.5
        
        if norm1 * norm2 == 0:
            return 0.0
        
        return cosine_sim / (norm1 * norm2)
    
    def analyze_sentence(self, sentence: str, search_results: List[Dict]) -> Dict:
        best_match = {
            'sentence': sentence,
            'similarity': 0.0,
            'source': None,
            'source_title': '',
            'source_domain': '',
            'matched_text': '',
            'is_plagiarism': False,
            'confidence_level': 'very_low',
            'risk_score': 0
        }
        
        for result in search_results:
            similarity = self.calculate_similarity(sentence, result['snippet'])
            
            if similarity > best_match['similarity']:
                confidence = self._calculate_confidence(similarity)
                risk_score = self._calculate_risk_score(similarity)
                
                best_match = {
                    'sentence': sentence,
                    'similarity': similarity,
                    'source': result['link'],
                    'source_title': result['title'],
                    'source_domain': result['display_link'],
                    'matched_text': result['snippet'],
                    'is_plagiarism': similarity > self.similarity_threshold,
                    'confidence_level': confidence,
                    'risk_score': risk_score
                }
        
        return best_match
    
    def _calculate_confidence(self, similarity: float) -> str:
        if similarity >= 0.9:
            return 'very_high'
        elif similarity >= 0.8:
            return 'high'
        elif similarity >= 0.7:
            return 'medium_high'
        elif similarity >= 0.6:
            return 'medium'
        elif similarity >= 0.4:
            return 'medium_low'
        elif similarity >= 0.2:
            return 'low'
        else:
            return 'very_low'
    
    def _calculate_risk_score(self, similarity: float) -> int:
        return int(similarity * 100)
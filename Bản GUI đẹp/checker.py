import time
from typing import Dict, List, Callable, Optional
from collections import defaultdict
from urllib.parse import urlparse
from api import GoogleSearchAPI
from analyzer import TextAnalyzer
from config import *

class PlagiarismChecker:
    def __init__(self):
        self.api = GoogleSearchAPI()
        self.analyzer = TextAnalyzer()
        self.last_check_time = None
        
    def test_connection(self) -> bool:
        try:
            return self.api.test_connection()
        except Exception:
            return False
    
    def check_text(self, text: str, progress_callback: Optional[Callable] = None) -> Dict:
        self.last_check_time = time.time()
        
        if not text or len(text.strip()) < 10:
            return self._generate_empty_report("Text too short")
        
        try:
            sentences = self.analyzer.extract_sentences(text)
            
            if not sentences:
                return self._generate_empty_report("No valid sentences found")
            
            results = []
            total_sentences = len(sentences)
            
            for i, sentence in enumerate(sentences):
                if progress_callback:
                    progress_callback(i + 1, total_sentences, sentence)
                
                try:
                    search_results = self.api.search(sentence)
                    analysis = self.analyzer.analyze_sentence(sentence, search_results)
                    results.append(analysis)
                    
                except Exception as e:
                    error_result = {
                        'sentence': sentence,
                        'similarity': 0.0,
                        'source': None,
                        'source_title': '',
                        'source_domain': '',
                        'matched_text': '',
                        'is_plagiarism': False,
                        'confidence_level': 'error',
                        'risk_score': 0,
                        'error': str(e)
                    }
                    results.append(error_result)
            
            return self._generate_comprehensive_report(results, text)
            
        except Exception as e:
            return self._generate_error_report(str(e))
    
    def _generate_comprehensive_report(self, results: List[Dict], original_text: str) -> Dict:
        total_sentences = len(results)
        valid_results = [r for r in results if 'error' not in r]
        error_count = total_sentences - len(valid_results)
        
        if not valid_results:
            return self._generate_empty_report("No valid analysis results")
        
        plagiarized_sentences = [r for r in valid_results if r['is_plagiarism']]
        high_risk_sentences = [r for r in valid_results if r['risk_score'] >= 70]
        medium_risk_sentences = [r for r in valid_results if 50 <= r['risk_score'] < 70]
        
        plagiarism_percentage = (len(plagiarized_sentences) / total_sentences) * 100
        avg_similarity = sum(r['similarity'] for r in valid_results) / len(valid_results) * 100
        max_similarity = max((r['similarity'] for r in valid_results), default=0) * 100
        
        risk_level = self._determine_risk_level(plagiarism_percentage)
        overall_score = self._calculate_overall_score(valid_results)
        
        source_analysis = self._analyze_sources(plagiarized_sentences)
        confidence_distribution = self._analyze_confidence_distribution(valid_results)
        
        recommendations = self._generate_smart_recommendations(
            plagiarism_percentage, risk_level, source_analysis, valid_results
        )
        
        processing_time = time.time() - self.last_check_time if self.last_check_time else 0
        
        return {
            'summary': {
                'total_sentences': total_sentences,
                'analyzed_sentences': len(valid_results),
                'error_count': error_count,
                'plagiarized_sentences': len(plagiarized_sentences),
                'high_risk_sentences': len(high_risk_sentences),
                'medium_risk_sentences': len(medium_risk_sentences),
                'plagiarism_percentage': round(plagiarism_percentage, 2),
                'average_similarity': round(avg_similarity, 2),
                'maximum_similarity': round(max_similarity, 2),
                'risk_level': risk_level,
                'overall_score': overall_score,
                'api_requests_used': self.api.get_requests_made(),
                'api_requests_remaining': self.api.get_remaining_requests(),
                'processing_time': round(processing_time, 2)
            },
            'detailed_results': valid_results,
            'source_analysis': source_analysis,
            'confidence_distribution': confidence_distribution,
            'recommendations': recommendations,
            'metadata': {
                'original_text': original_text,
                'text_length': len(original_text),
                'word_count': len(original_text.split()),
                'character_count': len(original_text.replace(' ', '')),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'checker_version': '2.0'
            }
        }
    
    def _determine_risk_level(self, percentage: float) -> str:
        if percentage >= RISK_LEVELS['CRITICAL']:
            return 'CRITICAL'
        elif percentage >= RISK_LEVELS['HIGH']:
            return 'HIGH'
        elif percentage >= RISK_LEVELS['MEDIUM']:
            return 'MEDIUM'
        elif percentage >= RISK_LEVELS['LOW']:
            return 'LOW'
        else:
            return 'SAFE'
    
    def _calculate_overall_score(self, results: List[Dict]) -> int:
        if not results:
            return 0
        
        total_risk = sum(r['risk_score'] for r in results)
        avg_risk = total_risk / len(results)
        overall_score = max(0, 100 - int(avg_risk))
        
        return overall_score
    
    def _analyze_sources(self, plagiarized_results: List[Dict]) -> Dict:
        domain_count = defaultdict(int)
        source_details = defaultdict(list)
        
        for result in plagiarized_results:
            if result['source']:
                domain = self._extract_domain(result['source'])
                domain_count[domain] += 1
                source_details[domain].append({
                    'title': result['source_title'],
                    'url': result['source'],
                    'similarity': result['similarity'],
                    'sentence': result['sentence'][:100] + '...'
                })
        
        top_sources = sorted(domain_count.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_unique_sources': len(domain_count),
            'top_sources': top_sources,
            'source_details': dict(source_details),
            'most_problematic_domain': top_sources[0][0] if top_sources else None
        }
    
    def _analyze_confidence_distribution(self, results: List[Dict]) -> Dict:
        confidence_counts = defaultdict(int)
        for result in results:
            confidence_counts[result['confidence_level']] += 1
        
        return dict(confidence_counts)
    
    def _generate_smart_recommendations(self, percentage: float, risk_level: str, 
                                      source_analysis: Dict, results: List[Dict]) -> List[str]:
        recommendations = []
        
        if risk_level == 'CRITICAL':
            recommendations.extend([
                "🚨 CRITICAL: Immediate action required - text contains severe plagiarism",
                "📝 Complete rewrite necessary - current content is not acceptable",
                "🔍 Review all flagged sentences and create original content",
                "📚 Ensure proper citation for all referenced materials",
                "⚖️ Consider legal implications of current plagiarism level"
            ])
        elif risk_level == 'HIGH':
            recommendations.extend([
                "⚠️ HIGH RISK: Significant plagiarism detected - major revisions needed",
                "✏️ Rewrite all sentences with similarity > 70%",
                "📖 Add proper citations and references",
                "🔄 Use paraphrasing tools and techniques",
                "👥 Consider peer review before submission"
            ])
        elif risk_level == 'MEDIUM':
            recommendations.extend([
                "⚡ MEDIUM RISK: Some plagiarism detected - revisions recommended",
                "📝 Focus on rewriting high-similarity sentences",
                "📑 Add citations where appropriate",
                "🔍 Double-check suspicious content",
                "💡 Enhance with personal insights and analysis"
            ])
        elif risk_level == 'LOW':
            recommendations.extend([
                "✅ LOW RISK: Minor issues detected - small improvements needed",
                "🔍 Review flagged sentences for improvement",
                "📋 Add citations for referenced facts",
                "💭 Consider adding more original thoughts"
            ])
        else:
            recommendations.append("🎉 EXCELLENT: High originality - content appears to be original")
        
        if source_analysis['total_unique_sources'] > 3:
            recommendations.append(f"📊 Multiple sources detected ({source_analysis['total_unique_sources']}) - ensure proper attribution")
        
        high_similarity_count = len([r for r in results if r['similarity'] > 0.8])
        if high_similarity_count > 0:
            recommendations.append(f"🎯 {high_similarity_count} sentences need immediate attention (>80% similarity)")
        
        return recommendations
    
    def _extract_domain(self, url: str) -> str:
        try:
            parsed = urlparse(url)
            domain = parsed.netloc
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
        except Exception:
            return url
    
    def _generate_empty_report(self, reason: str = "No content to analyze") -> Dict:
        return {
            'summary': {
                'total_sentences': 0,
                'analyzed_sentences': 0,
                'error_count': 0,
                'plagiarized_sentences': 0,
                'high_risk_sentences': 0,
                'medium_risk_sentences': 0,
                'plagiarism_percentage': 0.0,
                'average_similarity': 0.0,
                'maximum_similarity': 0.0,
                'risk_level': 'SAFE',
                'overall_score': 100,
                'api_requests_used': self.api.get_requests_made(),
                'api_requests_remaining': self.api.get_remaining_requests(),
                'processing_time': 0.0
            },
            'detailed_results': [],
            'source_analysis': {
                'total_unique_sources': 0,
                'top_sources': [],
                'source_details': {},
                'most_problematic_domain': None
            },
            'confidence_distribution': {},
            'recommendations': [f"ℹ️ {reason}"],
            'metadata': {
                'original_text': '',
                'text_length': 0,
                'word_count': 0,
                'character_count': 0,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'checker_version': '2.0'
            }
        }
    
    def _generate_error_report(self, error_message: str) -> Dict:
        report = self._generate_empty_report(f"Error: {error_message}")
        report['summary']['error_count'] = 1
        return report
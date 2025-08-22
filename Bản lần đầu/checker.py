# checker.py
"""
Main plagiarism checker logic
"""

from typing import Dict, List
from api import GoogleSearchAPI
from analyzer import TextAnalyzer
from config import RISK_LEVELS

class PlagiarismChecker:
    def __init__(self):
        self.api = GoogleSearchAPI()
        self.analyzer = TextAnalyzer()
        
    def test_connection(self) -> bool:
        """Test API connection"""
        return self.api.test_connection()
    
    def check_text(self, text: str, progress_callback=None) -> Dict:
        """
        Kiểm tra đạo văn cho văn bản
        """
        # Extract sentences
        sentences = self.analyzer.extract_sentences(text)
        
        if not sentences:
            return self._generate_empty_report()
        
        results = []
        total_sentences = len(sentences)
        
        # Check each sentence
        for i, sentence in enumerate(sentences):
            if progress_callback:
                progress_callback(i + 1, total_sentences, sentence)
            
            # Search online
            search_results = self.api.search(sentence)
            
            # Analyze results
            analysis = self.analyzer.analyze_sentence(sentence, search_results)
            results.append(analysis)
        
        # Generate report
        return self._generate_report(results, text)
    
    def _generate_report(self, results: List[Dict], original_text: str) -> Dict:
        """
        Tạo báo cáo từ kết quả phân tích
        """
        total_sentences = len(results)
        plagiarized_sentences = sum(1 for r in results if r['is_plagiarism'])
        
        if total_sentences == 0:
            return self._generate_empty_report()
        
        # Calculate percentages
        plagiarism_percentage = (plagiarized_sentences / total_sentences) * 100
        avg_similarity = sum(r['similarity'] for r in results) / total_sentences * 100
        
        # Determine risk level
        risk_level = self._get_risk_level(plagiarism_percentage)
        
        # Find top sources
        sources = {}
        for result in results:
            if result['is_plagiarism'] and result['source']:
                domain = self._extract_domain(result['source'])
                sources[domain] = sources.get(domain, 0) + 1
        
        top_sources = sorted(sources.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            'summary': {
                'total_sentences': total_sentences,
                'plagiarized_sentences': plagiarized_sentences,
                'plagiarism_percentage': round(plagiarism_percentage, 1),
                'average_similarity': round(avg_similarity, 1),
                'risk_level': risk_level,
                'requests_used': self.api.get_requests_made()
            },
            'detailed_results': results,
            'top_sources': top_sources,
            'recommendations': self._get_recommendations(plagiarism_percentage),
            'original_text': original_text
        }
    
    def _generate_empty_report(self) -> Dict:
        """
        Tạo báo cáo rỗng
        """
        return {
            'summary': {
                'total_sentences': 0,
                'plagiarized_sentences': 0,
                'plagiarism_percentage': 0,
                'average_similarity': 0,
                'risk_level': 'LOW',
                'requests_used': self.api.get_requests_made()
            },
            'detailed_results': [],
            'top_sources': [],
            'recommendations': ["Văn bản quá ngắn hoặc không có câu phù hợp để kiểm tra."],
            'original_text': ''
        }
    
    def _get_risk_level(self, percentage: float) -> str:
        """
        Xác định mức độ rủi ro
        """
        if percentage > RISK_LEVELS['HIGH']:
            return 'HIGH'
        elif percentage > RISK_LEVELS['MEDIUM']:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _extract_domain(self, url: str) -> str:
        """
        Trích xuất domain từ URL
        """
        try:
            return url.split('/')[2]
        except:
            return url
    
    def _get_recommendations(self, percentage: float) -> List[str]:
        """
        Đưa ra khuyến nghị
        """
        recommendations = []
        
        if percentage > 30:
            recommendations.extend([
                "❌ Tỷ lệ đạo văn rất cao! Cần viết lại hoàn toàn",
                "📝 Paraphrase các đoạn văn có vấn đề",
                "💡 Thêm nhiều ý kiến cá nhân và phân tích",
                "📚 Trích dẫn đúng cách các nguồn tham khảo"
            ])
        elif percentage > 15:
            recommendations.extend([
                "⚠️ Tỷ lệ đạo văn ở mức trung bình",
                "✏️ Viết lại các câu có độ tương đồng cao",
                "📖 Thêm citation cho thông tin tham khảo",
                "🔄 Sử dụng từ đồng nghĩa và cấu trúc câu khác"
            ])
        elif percentage > 5:
            recommendations.extend([
                "✅ Tỷ lệ đạo văn ở mức thấp",
                "🔍 Kiểm tra lại vài câu có độ tương đồng cao",
                "📝 Thêm citation nếu cần"
            ])
        else:
            recommendations.append("🎉 Tuyệt vời! Văn bản có tính nguyên gốc cao")
        
        return recommendations
from transformers import pipeline

class SentimentAnalyzer:
    """Metinlerden zero-shot sınıflandırma ile duygu durumunu tespit eder."""
    
    def __init__(self):
        """Duygu analizi modelini yükler."""
        # HuggingFace üzerinden çok dilli modeli yükle
        self.analyzer = pipeline(
            "zero-shot-classification", 
            model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"
        )
        
    def get_emotion(self, text):
        """Metni analiz edip en uygun Spotify duygu anahtarını döner."""
        # Hedef Türkçe duygu etiketleri
        candidate_labels = [
            'mutlu', 'üzgün', 'enerjik', 'sakin', 'romantik', 
            'odaklanmış', 'eğlenmiş', 'uykulu', 'nostaljik', 'öfkeli', 'özgüvenli'
        ]
        
        # Sınıflandırma tahmini
        result = self.analyzer(
            text, 
            candidate_labels=candidate_labels, 
            hypothesis_template="Bu metin {} hissi veriyor."
        )
        
        # En yüksek skorlu etiketi seç
        best_label = result['labels'][0]
        
        # Türkçe etiketleri İngilizce Spotify kategorilerine eşle
        mapping = {
            'mutlu': 'happy',
            'üzgün': 'sad',
            'enerjik': 'energetic',
            'sakin': 'calm',
            'romantik': 'romantic',
            'odaklanmış': 'focus',
            'eğlenmiş': 'party',
            'uykulu': 'sleep',
            'nostaljik': 'nostalgic',
            'öfkeli': 'angry',
            'özgüvenli': 'confident'
        }
        
        return mapping.get(best_label, 'happy')

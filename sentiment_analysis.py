from transformers import pipeline

class SentimentAnalyzer:
    """
    Kullanıcı metinlerini analiz ederek duygu durumlarını tespit eden sınıf.
    Zero-Shot Classification modelini kullanarak metnin bağlamını anlar.
    """
    
    def __init__(self):
        """
        Duygu analizi modelini (mDeBERTa-v3-base-mnli-xnli) yükler.
        Bu model çok dilli desteğe sahiptir ve sıfır-atış (zero-shot) sınıflandırma yapabilir.
        """
        # Model yükleme işlemi (HuggingFace üzerinden)
        self.analyzer = pipeline(
            "zero-shot-classification", 
            model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"
        )
        
    def get_emotion(self, text):
        """
        Verilen metni analiz eder ve en uygun Spotify duygu kategorisini döndürür.
        
        Args:
            text (str): Kullanıcının girdiği ruh hali açıklaması.
            
        Returns:
            str: Spotify için uygun olan duygu anahtarı (örn: 'happy', 'sad').
        """
        # Analiz edilecek hedef etiketler (Türkçe)
        candidate_labels = [
            'mutlu', 'üzgün', 'enerjik', 'sakin', 'romantik', 
            'odaklanmış', 'eğlenmiş', 'uykulu', 'nostaljik', 'öfkeli', 'özgüvenli'
        ]
        
        # Zero-shot sınıflandırma tahmini
        result = self.analyzer(
            text, 
            candidate_labels=candidate_labels, 
            hypothesis_template="Bu metin {} hissi veriyor."
        )
        
        # En yüksek güven skoruna sahip etiketi seç
        best_label = result['labels'][0]
        
        # Türkçe etiketleri Spotify API sorgularında kullanılacak İngilizce karşılıklarına eşle
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

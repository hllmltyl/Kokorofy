from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self):
        # Klasik sentiment yerine çok daha zeki olan Multi-lingual Zero-Shot Classification modeline geçiyoruz.
        # Bu model herhangi bir kelime dizisi listesine ihtiyaç duymadan cümlenin bağlamını (anlamını) kavrar
        # ve verdiğimiz etiketler (mutlu, üzgün vb.) arasında en mantıklı olanı seçer.
        self.analyzer = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")
        
    def get_emotion(self, text):
        """
        Metni okur ve bağlamı anlayarak en uygun Spotify duygu kategorisini döner.
        """
        # Yalnizca Türkçe candidate listesini kullanıyoruz:
        
        # Spotify Mood/Genre sistemine paralel çok daha geniş kapsamlı duygu yelpazesi:
        candidate_labels = ['mutlu', 'üzgün', 'enerjik', 'sakin', 'romantik', 'odaklanmış', 'eğlenmiş', 'uykulu', 'nostaljik', 'öfkeli', 'özgüvenli']
        
        result = self.analyzer(text, candidate_labels=candidate_labels, hypothesis_template="Bu metin {} hissi veriyor.")
        
        # En yüksek ihtimalli sonucu al
        best_label = result['labels'][0]
        
        # Seçilen Türkçe etiketi İngilizce Spotify kategorisine çevir
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

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import random
from dotenv import load_dotenv

# .env dosyasındaki ortam değişkenlerini yükle
load_dotenv()

class SpotifyClient:
    """
    Spotify Web API ile etkileşime geçen istemci sınıfı.
    Şarkı arama ve öneri işlemlerini yürütür.
    """
    
    def __init__(self):
        """
        Spotify API kimlik bilgilerini yükler ve istemciyi doğrular.
        """
        client_id = os.getenv("SPOTIPY_CLIENT_ID")
        client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        
        if not client_id or not client_secret:
            raise ValueError("Spotify API anahtarları eksik. Lütfen .env dosyasını kontrol edin.")
            
        # İstemci kimlik bilgileri ile kimlik doğrulama yöneticisini başlat
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        
    def get_recommendations_for_emotion(self, emotion):
        """
        Belirlenen duygu durumuna göre Spotify üzerinden şarkı önerileri getirir.
        
        Args:
            emotion (str): Analiz sonucunda gelen duygu anahtarı (örn: 'happy', 'energetic').
            
        Returns:
            list: Şarkı bilgilerini içeren sözlük listesi.
        """
        limit = 5
        market = 'TR'
        
        # Duygu durumlarına göre özelleştirilmiş arama sorguları havuzu
        tag_queries = {
            'happy': ['happy pop', 'feel good', 'happy hits', 'neşeli'],
            'energetic': ['workout', 'energetic dance', 'gym hype', 'upbeat'],
            'sad': ['sad acoustic', 'melancholy', 'sad piano', 'hüzünlü'],
            'calm': ['chill ambient', 'peaceful', 'relaxing', 'sakin'],
            'romantic': ['romantic love', 'aşk şarkıları', 'love songs'],
            'focus': ['lofi beats', 'focus piano', 'study music', 'odaklanma'],
            'party': ['party hits', 'club dance', 'eğlence pop'],
            'sleep': ['sleep ambient', 'deep sleep', 'relaxing sleep'],
            'nostalgic': ['70s 80s 90s hits', 'nostalji', 'retro pop'],
            'angry': ['heavy metal', 'hard rock', 'angry rock', 'öfke'],
            'confident': ['badass hype', 'confident pop', 'boss vibe']
        }
        
        # Duygu anahtarına göre sorgu listesini al, yoksa 'pop' varsayılanını kullan
        pool = tag_queries.get(emotion, ['pop'])
        # Listeden rastgele bir sorgu seçerek çeşitlilik sağla
        selected_query = random.choice(pool)
        
        tracks = []
        try:
            # Arama sonuçlarında çeşitliliği artırmak için rastgele bir başlangıç noktası (offset) seç
            offset_val = random.randint(0, 80)
            
            # Spotify üzerinde arama yap
            search_results = self.sp.search(q=selected_query, type='track', limit=limit, offset=offset_val, market=market)
            
            for track in search_results['tracks']['items']:
                if not track: continue
                
                # Albüm kapağı URL'sini al
                cover_url = track['album']['images'][0]['url'] if track['album']['images'] else None
                
                # Gerekli bilgileri sözlük formatında listeye ekle
                tracks.append({
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'cover_url': cover_url,
                    'spotify_url': track['external_urls']['spotify']
                })
                
            return tracks
            
        except Exception as e:
            # Hata durumunda konsola yazdır ve boş liste dön
            print(f"Spotify API hatası: {e}")
            return []

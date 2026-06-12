import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import random
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()

class SpotifyClient:
    """Spotify Web API istemcisi. Şarkı arama ve öneri işlemlerini yapar."""
    
    def __init__(self):
        """Spotify API kimlik bilgilerini doğrular."""
        client_id = os.getenv("SPOTIPY_CLIENT_ID")
        client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        
        if not client_id or not client_secret:
            raise ValueError("Spotify API anahtarları eksik. .env dosyasını kontrol edin.")
            
        # API kimlik doğrulaması
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        
    def get_recommendations_for_emotion(self, emotion):
        """Duygu durumuna göre Spotify'dan şarkı önerileri getirir."""
        limit = 5
        market = 'TR'
        
        # Duygu durumlarına göre arama kelimeleri
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
        
        # Duyguya göre sorgu havuzunu seç, yoksa varsayılan 'pop'
        pool = tag_queries.get(emotion, ['pop'])
        # Rastgele arama kelimesi seç
        selected_query = random.choice(pool)
        
        tracks = []
        try:
            # Çeşitlilik için rastgele offset değeri belirle
            offset_val = random.randint(0, 80)
            
            # Spotify'da arama yap
            search_results = self.sp.search(q=selected_query, type='track', limit=limit, offset=offset_val, market=market)
            
            for track in search_results['tracks']['items']:
                if not track: continue
                
                # Albüm kapağı URL'sini al
                cover_url = track['album']['images'][0]['url'] if track['album']['images'] else None
                
                # Parça bilgilerini listeye ekle
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

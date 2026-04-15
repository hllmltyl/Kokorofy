import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()

class SpotifyClient:
    def __init__(self):
        client_id = os.getenv("SPOTIPY_CLIENT_ID")
        client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        
        if not client_id or not client_secret:
            raise ValueError("Spotify API anahtarları eksik. Lütfen .env dosyasını kontrol edin.")
            
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        
    def get_recommendations_for_emotion(self, emotion):
        """
        Duygu durumuna göre 5 adet şarkı önerisi getirir.
        Seed parametrelerini ve audio features parametrelerini ayarlar.
        """
        limit = 5
        market = 'TR'
        
        import random
        
        # Seçilen Spotify etiketleri (dinamik arama kelimeleri)
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
        
        pool = tag_queries.get(emotion, ['pop'])
        # Ortaya karışık ve geniş bir sorgu havuzu için bir tag seç
        selected_query = random.choice(pool)
        
        tracks = []
        try:
            # Püf nokta: Spotify API kısıtlamalarından dolayı "offset"i rastgele belirleyerek 
            # hep aynı listelerin veya şarkıların gelmesini engelliyoruz!
            offset_val = random.randint(0, 80)
            
            search_results = self.sp.search(q=selected_query, type='track', limit=limit, offset=offset_val, market=market)
            
            for track in search_results['tracks']['items']:
                if not track: continue
                # Kapak fotoğrafı, URL gibi özellikleri seç
                cover_url = track['album']['images'][0]['url'] if track['album']['images'] else None
                tracks.append({
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'cover_url': cover_url,
                    'spotify_url': track['external_urls']['spotify']
                })
                
            return tracks
            
        except Exception as e:
            print(f"Spotify API hatası: {e}")
            return []

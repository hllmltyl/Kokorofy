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
        
        # Çok daha yüksek kaliteli ve isabetli şarkı önerileri için elle seçilmiş (Curated) popüler şarkı havuzu
        curated_tracks = {
            'happy': [
                "Tarkan Şımarık", "Kenan Doğulu Çakkıdı", "Gülşen Bangır Bangır", "Athena Yaşamak Var Ya", "Sertab Erener Rengarenk",
                "Pharrell Williams Happy", "Dua Lipa Levitating", "Justin Timberlake Can't Stop The Feeling", "Coldplay Viva La Vida", "Avicii Wake Me Up",
                "Mark Ronson Uptown Funk", "Katy Perry Roar", "Edis Benim Ol", "Yalın Zalim"
            ],
            'energetic': [
                "maNga Bir Kadın Çizeceksin", "Mor ve Ötesi Cambaz", "Duman Senden Daha Güzel", "Teoman Renkli Rüyalar Oteli", "Edis Çok Çok",
                "Eminem Lose Yourself", "Survivor Eye of the Tiger", "The Weeknd Blinding Lights", "Tiesto The Business", "Skrillex Bangarang",
                "David Guetta Titanium", "Athena 12 Dev Adam", "Ezhel Felaket", "Ceza Suspus"
            ],
            'sad': [
                "Müslüm Gürses Affet", "Ahmet Kaya Kum Gibi", "Sezen Aksu Küçüğüm", "Teoman Gemiler", "Cem Adrian Kül", "Sertab Erener Olsun",
                "Adele Someone Like You", "Billie Eilish when the party's over", "Coldplay Fix You", "Tom Odell Another Love", "Sam Smith Stay With Me",
                "Sagopa Kajmer Galiba", "Model Değmesin Ellerimiz", "Emre Aydın Hoşçakal"
            ],
            'calm': [
                "Pinhani Hele Bi Gel", "Bülent Ortaçgil Sensiz Olmaz", "Fikret Kızılok Gönül", "Yüzyüzeyken Konuşuruz Dinle Beni Bi", "Kaan Tangöze Bekle Dedi Gitti",
                "Ed Sheeran Perfect", "John Legend All of Me", "Norah Jones Don't Know Why", "Enya Orinoco Flow", "Hans Zimmer Time",
                "Canozan Toprak Yağmura", "Mabel Matiz Öyle Kolaysa", "Sıla Yan Benimle"
            ],
            'romantic': [
                "Sezen Aksu Seni Yerler", "Kenan Doğulu Aşkkolik", "Yalın Küçüğüm", "Bora Duran Sana Doğru", "Mustafa Ceceli Hastalıkta Sağlıkta",
                "Ed Sheeran Thinking Out Loud", "Bruno Mars Just The Way You Are", "John Legend All Of Me", "Whitney Houston I Will Always Love You", "Celine Dion My Heart Will Go On"
            ],
            'focus': [
                "Lofi Girl lo fi beats", "Hans Zimmer Interstellar", "Ludovico Einaudi Nuvole Bianche", "Yiruma River Flows in You", "Fazıl Say Alla Turca Jazz",
                "Chillhop Music jazzy hip hop", "Kavinsky Nightcall", "Daft Punk Rammot"
            ],
            'party': [
                "Demet Akalın Çalkala", "Serdar Ortaç Dansöz", "Tarkan Kuzu Kuzu", "Gülşen Yurtta Aşk Cihanda Aşk", "Hande Yener Romeo",
                "Pitbull Timber", "Rihanna Don't Stop The Music", "LMFAO Party Rock Anthem", "David Guetta Memories", "Don Omar Danza Kuduro"
            ],
            'sleep': [
                "Max Richter On the Nature of Daylight", "Chopin Nocturne op.9 No.2", "Evgeny Grinko Valse", "C418 Sweden", "Brian Eno Apollo",
                "Erik Satie Gymnopedie", "Debussy Clair de Lune"
            ],
            'nostalgic': [
                "Ajda Pekkan Bambaşka Biri", "Barış Manço Gülpembe", "Cem Karaca Resimdeki Gözyaşları", "Erkin Koray Şaşkın", "Nilüfer Ta Uzak Yollardan",
                "Queen Bohemian Rhapsody", "ABBA Dancing Queen", "Michael Jackson Billie Jean", "The Beatles Hey Jude", "Oasis Wonderwall"
            ],
            'angry': [
                "Şebnem Ferah Mayın Tarlası", "Athena Kime Ne", "Pentagram Gündüz Gece", "Kurban Yalan", "Hayko Cepkin Fırtınam",
                "Rage Against The Machine Killing In the Name", "Slipknot Duality", "Eminem Till I Collapse", "Linkin Park Numb", "System Of A Down Chop Suey!"
            ],
            'confident': [
                "Zeynep Bastık Uslanmıyor Bu", "Hey! Douglas Vay", "Ezhel Geceler", "Sefo Bilmem Mi", "Murat Boz Janti",
                "Beyonce Crazy In Love", "Dua Lipa Don't Start Now", "Kendrick Lamar HUMBLE.", "Kanye West Stronger", "Ariana Grande 7 rings"
            ]
        }
        
        import random
        # Duyguya uygun özel havuzdan rastgele 5 şarkı metni seç
        pool = curated_tracks.get(emotion, curated_tracks['happy'])
        selected_queries = random.sample(pool, min(limit, len(pool)))
        
        tracks = []
        try:
            for query in selected_queries:
                # Her şarkıyı tam ismiyle aratıp garantili ve bilinen ilk global hit sonucunu çekiyoruz
                search_results = self.sp.search(q=query, type='track', limit=1, market=market)
                
                track_items = search_results['tracks']['items']
                if not track_items:
                    continue
                    
                track = track_items[0]
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
            return tracks # Hata alsa bile bulabildiği harika şarkıları dönmeye devam etsin

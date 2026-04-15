import streamlit as st
from sentiment_analysis import SentimentAnalyzer
from spotify_client import SpotifyClient

st.set_page_config(page_title="Kokorofy - Müzik Önerici", page_icon="🎵", layout="centered")

win98_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400;500;600;700&display=swap');

/* Teal desktop background */
.stApp {
    background-color: #008080 !important;
    font-family: 'Pixelify Sans', 'MS Sans Serif', Tahoma, sans-serif !important;
    background-image: none !important;
}

/* Remove default header */
header[data-testid="stHeader"] {
    display: none;
}

/* The Main Window */
.block-container {
    background-color: #c0c0c0 !important;
    border-top: 2px solid #ffffff !important;
    border-left: 2px solid #ffffff !important;
    border-right: 2px solid #000000 !important;
    border-bottom: 2px solid #000000 !important;
    box-shadow: inset -1px -1px #808080, inset 1px 1px #dfdfdf !important;
    padding: 3px !important;
    margin-top: 2rem !important;
    margin-bottom: 2rem !important;
    max-width: 600px !important;
    color: #000000 !important;
}

/* Base text */
h1, h2, h3, p, span, div, label, li {
    font-family: inherit !important;
    color: #000000 !important;
    letter-spacing: normal !important;
}

h1 { font-size: 1.5rem !important; }
h2 { font-size: 1.2rem !important; }
h3 { font-size: 1.1rem !important; }

/* Title Bar simulated */
.win98-title-bar {
    background: linear-gradient(90deg, #000080 0%, #1084d0 100%);
    padding: 2px 3px 2px 3px;
    color: #ffffff;
    font-weight: bold;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}
.win98-title-bar span {
    color: #ffffff !important;
    font-size: 14px;
}
.win98-title-buttons {
    display: flex;
    gap: 2px;
}
.win98-title-btn {
    background: #c0c0c0;
    border-top: 1px solid #fff;
    border-left: 1px solid #fff;
    border-right: 1px solid #000;
    border-bottom: 1px solid #000;
    box-shadow: inset -1px -1px #808080, inset 1px 1px #dfdfdf;
    font-weight: bold;
    width: 16px;
    height: 14px;
    font-size: 10px;
    line-height: 10px;
    padding: 0;
    text-align: center;
    color: #000 !important;
    display: inline-block;
}

/* Text Area */
.stTextArea textarea {
    background-color: #ffffff !important;
    border-top: 2px solid #808080 !important;
    border-left: 2px solid #808080 !important;
    border-bottom: 2px solid #ffffff !important;
    border-right: 2px solid #ffffff !important;
    border-radius: 0 !important;
    box-shadow: inset 1px 1px #000000, inset -1px -1px #dfdfdf !important;
    color: black !important;
}
.stTextArea textarea:focus {
    outline: none !important;
    box-shadow: inset 1px 1px #000000, inset -1px -1px #dfdfdf !important;
}

/* Button */
.stButton>button {
    background-color: #c0c0c0 !important;
    border-top: 2px solid #ffffff !important;
    border-left: 2px solid #ffffff !important;
    border-right: 2px solid #000000 !important;
    border-bottom: 2px solid #000000 !important;
    box-shadow: inset -1px -1px #808080, inset 1px 1px #dfdfdf !important;
    border-radius: 0 !important;
    color: black !important;
    padding: 4px 15px !important;
    min-height: 0 !important;
    line-height: normal !important;
    margin-top: 5px;
}
.stButton>button:active {
    border-top: 2px solid #000000 !important;
    border-left: 2px solid #000000 !important;
    border-right: 2px solid #ffffff !important;
    border-bottom: 2px solid #ffffff !important;
    box-shadow: inset 1px 1px #808080, inset -1px -1px #dfdfdf !important;
    padding: 5px 14px 3px 16px !important; /* Visual inset shift */
}

/* Spinner / Info block replacements */
.stAlert {
    background-color: #c0c0c0 !important;
    border-top: 2px solid #ffffff !important;
    border-left: 2px solid #ffffff !important;
    border-right: 2px solid #000000 !important;
    border-bottom: 2px solid #000000 !important;
    box-shadow: inset -1px -1px #808080, inset 1px 1px #dfdfdf !important;
    color: black !important;
    border-radius: 0 !important;
    padding: 10px !important;
}

/* Inner frame for content to look like a Win98 sub-window */
.win98-inner-frame {
    border-top: 2px solid #808080;
    border-left: 2px solid #808080;
    border-bottom: 2px solid #ffffff;
    border-right: 2px solid #ffffff;
    box-shadow: inset 1px 1px #000000, inset -1px -1px #dfdfdf;
    padding: 15px;
    background-color: #c0c0c0;
    margin-bottom: 10px;
}

/* Song card images */
.stImage img {
    border-top: 2px solid #808080 !important;
    border-left: 2px solid #808080 !important;
    border-bottom: 2px solid #ffffff !important;
    border-right: 2px solid #ffffff !important;
    box-shadow: inset 1px 1px #000, inset -1px -1px #dfdfdf !important;
}

/* Links */
a {
    color: #0000ff !important;
    text-decoration: underline !important;
}

/* Separators */
hr {
    border: none !important;
    border-top: 2px solid #808080 !important;
    border-bottom: 2px solid #ffffff !important;
    margin: 15px 0 !important;
}

/* Hide Streamlit elements */
.st-emotion-cache-1jo8hni, .st-emotion-cache-1wtvtyf { display: none; }
</style>
"""

st.markdown(win98_css, unsafe_allow_html=True)

# Custom Win98 Title Bar
st.markdown("""
<div class="win98-title-bar">
    <span>🎶 Kokorofy.exe</span>
    <div class="win98-title-buttons">
        <div class="win98-title-btn">_</div>
        <div class="win98-title-btn">[]</div>
        <div class="win98-title-btn">X</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Inner content wrapped in Markdown for visual structure where possible
# However, Streamlit components will break HTML flow. We will just use standard Streamlit components which are styled globally.


# Modelleri önbellekte tut, her yenilemede tekrar yüklenmesin
@st.cache_resource
def load_sentiment_analyzer():
    return SentimentAnalyzer()

@st.cache_resource
def load_spotify_client():
    return SpotifyClient()

st.markdown("Kokorofy Ruh Hali Algılama Sihirbazı'na Hoş Geldiniz.")
st.markdown("Lütfen mevcut ruh halinizi tarif ediniz. Cihazınız sizin için Müzik CD'lerini tarayacaktır.")
st.markdown("---")

with st.spinner("Sürücüler yükleniyor..."):
    analyzer = load_sentiment_analyzer()
    spotify = load_spotify_client()

user_input = st.text_area("Mevcut Durumunuz:", placeholder="C:\> Bugün harika hissediyorum!")

if st.button("Müzik Bul"):
    if not user_input.strip():
        st.warning("HATA: Girdi bulunamadı. Lütfen boş bırakmayın.")
    else:
        with st.spinner("NLP Motoru Çalışıyor..."):
            emotion = analyzer.get_emotion(user_input)
            
        emotion_tr = {
            'happy': 'Mutlu 😃',
            'energetic': 'Enerjik ⚡',
            'sad': 'Üzgün 😔',
            'calm': 'Sakin 🧘‍♂️',
            'romantic': 'Romantik ❤️',
            'focus': 'Odaklanmış 🧠',
            'party': 'Eğlenmiş / Kopuyo 🥳',
            'sleep': 'Uykulu 😴',
            'nostalgic': 'Nostaljik 📻',
            'angry': 'Öfkeli 😠',
            'confident': 'Özgüvenli 😎'
        }
            
        st.success(f"Analiz Tamamlandı! Tespit Edilen Değer: {emotion_tr.get(emotion, emotion).upper()}")
        
        with st.spinner("Ağ üzerinden Spotify Sunucularına Bağlanılıyor..."):
            recommendations = spotify.get_recommendations_for_emotion(emotion)
            
        if recommendations:
            st.markdown("### Bulunan Medya Dosyaları:")
            st.markdown("---")
            
            for track in recommendations:
                col1, col2 = st.columns([1, 3])
                with col1:
                    if track['cover_url']:
                        st.image(track['cover_url'], use_container_width=True)
                    else:
                        st.write("Resim Yok")
                with col2:
                    st.markdown(f"**Disket Adı:** {track['name']}")
                    st.markdown(f"**Sanatçı:** {track['artist']}")
                    st.markdown(f"[CD'yi Yürüt (Spotify)]({track['spotify_url']})")
                st.markdown("---")
        else:
            st.error("Ağ Hatası: Parçalar getirilirken bir sorun oluştu.")

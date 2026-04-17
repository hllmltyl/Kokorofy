# 🎶 Kokorofy: Duygu Temelli Müzik Önerici

Kokorofy, kullanıcıların ruh hallerini doğal dil işleme (NLP) teknikleri kullanarak analiz eden ve bu analize dayanarak Spotify üzerinden kişiselleştirilmiş müzik önerileri sunan retro (Windows 98) temalı bir web uygulamasıdır.

## 🚀 Özellikler

- **Gelişmiş Duygu Analizi:** HuggingFace üzerindeki `mDeBERTa-v3-base-mnli-xnli` Zero-Shot Classification modelini kullanarak, metnin bağlamını derinlemesine kavrar.
- **Dinamik Spotify Entegrasyonu:** Analiz edilen duyguya göre Spotify API üzerinden gerçek zamanlı parça sorgulaması yapar.
- **Nostaljik Tasarım:** Windows 98 estetiğini modernize eden bir kullanıcı arayüzü sunar.
- **Geniş Duygu Yelpazesi:** 11 farklı ruh hali kategorisi (Mutlu, Üzgün, Enerjik, Sakin, Romantik, Odaklanmış, Eğlenmiş, Uykulu, Nostaljik, Öfkeli, Özgüvenli) desteklenir.
- **Akıllı Arama:** Spotify API'sinde arama yaparken rastgele 'offset' kullanarak her seferinde farklı şarkılar önerir.

## 🛠️ Teknolojiler

- **Arayüz:** [Streamlit](https://streamlit.io/)
- **Yapay Zeka / NLP:** [HuggingFace Transformers](https://huggingface.co/docs/transformers/index)
- **Müzik API:** [Spotipy](https://spotipy.readthedocs.io/) (Spotify Web API istemcisi)
- **Dil:** Python 3.x

## 📦 Kurulum

1. **Projeyi Klonlayın:**
   ```bash
   git clone https://github.com/kullanici/Kokorofy.git
   cd Kokorofy
   ```

2. **Gerekli Kütüphaneleri Yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Spotify API Anahtarlarını Alın:**
   - [Spotify for Developers](https://developer.spotify.com/) adresine gidin.
   - Yeni bir uygulama oluşturun ve `Client ID` ile `Client Secret` bilgilerini alın.

4. **Ortam Değişkenlerini Ayarlayın:**
   Proje dizininde `.env` adında bir dosya oluşturun ve bilgilerinizi ekleyin:
   ```env
   SPOTIPY_CLIENT_ID='your_client_id_here'
   SPOTIPY_CLIENT_SECRET='your_client_secret_here'
   ```

## 🎮 Kullanım

Uygulamayı başlatmak için terminale şu komutu yazın:
```bash
streamlit run app.py
```

Açılan pencerede "Mevcut Durumunuz" kısmına o anki hislerinizi yazın (örneğin: "Bugün çok enerjik hissediyorum, dünyayı fethedebilirim!") ve **Müzik Bul** butonuna tıklayın.

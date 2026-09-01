import os
import requests
from bs4 import BeautifulSoup
from google import genai

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def haberleri_getir():
    url = "https://news.google.com/rss/search?q=Beylikdüzü+haber&hl=tr&gl=TR&ceid=TR:tr"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="xml")
    
    ilk_haber = soup.find_all('item')[0]
    baslik = ilk_haber.title.text
    link = ilk_haber.link.text
    
    return f"Başlık: {baslik}\nLink: {link}"

def haberi_formatla(ham_haber):
    prompt = f"""
    Sen 'Beylikdüzü Radar' adlı tarafsız bir Instagram haber sayfasının editörüsün.
    Aşağıdaki haberi incele ve Instagram Hikayesi'nde paylaşmak için 3 kısa, çarpıcı cümle ile özetle.
    Haber metni haricinde hiçbir ek yorum veya giriş/çıkış cümlesi kullanma.
    
    Ham Haber: {ham_haber}
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

def telegrama_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mesaj
    }
    requests.post(url, data=payload)

if __name__ == "__main__":
    try:
        ham_veri = haberleri_getir()
        ig_metni = haberi_formatla(ham_veri)
        son_mesaj = f"🚨 YENİ BEYLİKDÜZÜ HABERİ!\n\n{ig_metni}\n\n(Doğrudan şablona yapıştırabilirsin)"
        telegrama_gonder(son_mesaj)
    except Exception as e:
        print(f"Hata: {e}")

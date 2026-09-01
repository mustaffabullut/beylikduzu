import os
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def haberleri_getir():
    # 'when:1d' filtresi sayesinde sadece son 24 saat içinde çıkan haberler çekilir
    url = "https://news.google.com/rss/search?q=Beylikdüzü+when:1d&hl=tr&gl=TR&ceid=TR:tr"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="xml")
    
    haberler = soup.find_all('item')
    if not haberler:
        return None
        
    ilk_haber = haberler[0]
    baslik = ilk_haber.title.text
    link = ilk_haber.link.text
    
    return f"🚨 YENİ BEYLİKDÜZÜ HABERİ!\n\n📌 {baslik}\n\n🔗 {link}"

def telegrama_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mesaj
    }
    requests.post(url, data=payload)

if __name__ == "__main__":
    try:
        haber_mesaji = haberleri_getir()
        if haber_mesaji:
            telegrama_gonder(haber_mesaji)
            print("Haber başarıyla Telegram'a gönderildi!")
        else:
            print("Şu an yeni haber bulunamadı.")
    except Exception as e:
        print(f"Hata: {e}")

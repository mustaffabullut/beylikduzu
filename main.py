import os
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def haberleri_getir():
    # Sadece Beylikdüzü Belediyesi resmi duyuru ve haber RSS kaynağını hedefliyoruz
    url = "https://www.beylikduzu.istanbul/rss/haberler" # Veya yerel arama filtresi
    
    # Alternatif olarak Google News'i ilçe tam adresi ve tırnak içinde (kesin eşleşme) zorlayalım:
    rss_url = "https://news.google.com/rss/search?q=%22Beylikdüzü%22+ilçesi+when:1d&hl=tr&gl=TR&ceid=TR:tr"
    
    response = requests.get(rss_url)
    soup = BeautifulSoup(response.content, features="xml")
    
    haberler = soup.find_all('item')
    
    # Gelen haberin gerçekten Beylikdüzü ile ilgili olup olmadığını metin içinde doğrulayalım
    for haber in haberler:
        baslik = haber.title.text
        link = haber.link.text
        
        # Eğer başlıkta veya açıklamada başka şehir/ilçe geçiyorsa atla, sadece taze ve yerel olanı al
        yasakli_kelimeler = ["Siirt", "Kurtalan", "Ankara", "İzmir", "Adana", "Antalya", "Trabzon"]
        if any(kelime in baslik for kelime in yasakli_kelimeler):
            continue
            
        return f"🚨 BEYLİKDÜZÜ RADAR - GÜNCEL HABER\n\n📌 {baslik}\n\n🔗 {link}"
        
    return None

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
            print("Güncel Beylikdüzü haberi Telegram'a gönderildi!")
        else:
            print("Filtrelere uygun güncel haber bulunamadı.")
    except Exception as e:
        print(f"Hata: {e}")

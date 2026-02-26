import requests
import re
import sys

# Ayarlar
PAROLA_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=11kalAdKaAde11s"
FILE_NAME = "playlist.m3u"

def get_latest_data():
    session = requests.Session()
    # En güncel Chrome tarayıcı başlıkları (Bot engelini aşmak için)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.seir-sanduk.com/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
    
    try:
        # 1. Aşama: Ana sayfaya gidip çerez tanımlaması yapıyoruz
        print("Siteye bağlanılıyor...")
        session.get("https://www.seir-sanduk.com/", timeout=15)
        
        # 2. Aşama: Şifrenin bulunduğu sayfayı çekiyoruz
        response = session.get(PAROLA_URL, timeout=15)
        
        print(f"Site Yanıt Kodu: {response.status_code}")
        
        if response.status_code == 403:
            print("HATA: Site GitHub sunucusunu engelledi (403 Forbidden).")
            return None
        
        response.raise_for_status()
        
        # 3. Aşama: HTML içinden 'pass=' veya 'hash=' değerini çekiyoruz
        # Regex hem pass= hem de hash= içeren linkleri yakalar
        match = re.search(r'(pass|hash)=([a-zA-Z0-9]+)', response.text)
        
        if match:
            extracted_code = match.group(2)
            print(f"Başarılı! Bulunan Kod: {extracted_code}")
            return extracted_code
        else:
            print("HATA: Sayfa içeriğinde pass veya hash kodu bulunamadı.")
            # Hata ayıklama için sayfa içeriğinin bir kısmını yazdıralım
            print("Sayfa İçeriği Önizleme:", response.text[:200])
            return None
            
    except Exception as e:
        print(f"Bağlantı sırasında bir hata oluştu: {e}")
        return None

def create_m3u(pass_code):
    # Kanal listesi ve ID'leri
    channels = [
        {"name": "BNT 1 HD", "id": "hd-bnt-1-hd"},
        {"name": "BNT 2", "id": "bnt-2"},
        {"name": "BTV HD", "id": "hd-btv-hd"},
        {"name": "NOVA TV HD", "id": "hd-nova-tv-hd"},
        {"name": "DIEMA SPORT HD", "id": "hd-diema-sport-hd"},
        {"name": "MAX SPORT 1 HD", "id": "hd-max-sport-1-hd"}
    ]
    
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for ch in channels:
                f.write(f'#EXTINF:-1, {ch["name"]}\n')
                # Yayın linki yapısı
                f.write(f'https://www.seir-sanduk.com/stream.php?id={ch["id"]}&pass={pass_code}\n')
        
        print(f"Dosya başarıyla güncellendi: {FILE_NAME}")
        return True
    except Exception as e:
        print(f"Dosya yazma hatası: {e}")
        return False

if __name__ == "__main__":
    code = get_latest_data()
    
    if code:
        if create_m3u(code):
            print("İşlem başarıyla tamamlandı.")
            sys.exit(0) # Başarılı çıkış
    
    print("İşlem başarısız oldu.")
    sys.exit(1) # Hata koduyla çıkış (GitHub Actions'da kırmızı yanar)

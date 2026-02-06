import requests
import re
import sys

# Ayarlar
PAROLA_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
FILE_NAME = "playlist.m3u"

def get_latest_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.seir-sanduk.com/'
    }
    
    try:
        session = requests.Session()
        response = session.get(PAROLA_URL, headers=headers, timeout=15)
        response.raise_for_status()
        
        # HTML içinden pass parametresini bul (Örn: pass=11kal...)
        pass_match = re.search(r'pass=([a-zA-Z0-9]+)', response.text)
        
        if pass_match:
            return pass_match.group(1)
        else:
            print("Hata: Sayfa içinde 'pass' kodu bulunamadı.")
            return None
            
    except Exception as e:
        print(f"Bağlantı Hatası: {e}")
        return None

def create_m3u(pass_code):
    channels = [
        {"name": "BNT 1 HD", "id": "hd-bnt-1-hd"},
        {"name": "BNT 2", "id": "bnt-2"},
        {"name": "BTV HD", "id": "hd-btv-hd"},
        {"name": "NOVA TV HD", "id": "hd-nova-tv-hd"},
        {"name": "DIEMA SPORT HD", "id": "hd-diema-sport-hd"},
        {"name": "DIEMA SPORT 2 HD", "id": "hd-diema-sport-2-hd"},
        {"name": "MAX SPORT 1 HD", "id": "hd-max-sport-1-hd"}
    ]
    
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for ch in channels:
                # Seir-Sanduk direkt m3u8 link yapısı
                f.write(f'#EXTINF:-1 tvg-id="{ch["id"]}", {ch["name"]}\n')
                f.write(f'https://www.seir-sanduk.com/?id={ch["id"]}&pass={pass_code}\n')
        print(f"M3U dosyası başarıyla oluşturuldu: {FILE_NAME}")
        return True
    except Exception as e:
        print(f"Dosya yazma hatası: {e}")
        return False

if __name__ == "__main__":
    code = get_latest_data()
    if code:
        if create_m3u(code):
            sys.exit(0) # Başarılı çıkış
    sys.exit(1) # Hatalı çıkış (GitHub Action bunu fark eder)

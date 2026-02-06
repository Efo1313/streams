import requests
import re
import sys

# Ayarlar
PAROLA_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
FILE_NAME = "playlist.m3u"

def get_latest_data():
    session = requests.Session()
    # Gerçek bir tarayıcı (Chrome) gibi görünmek için gerekli başlıklar
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'https://www.seir-sanduk.com/',
        'Upgrade-Insecure-Requests': '1'
    })
    
    try:
        # Önce ana sayfaya gidip çerez alıyoruz
        session.get("https://www.seir-sanduk.com/", timeout=15)
        
        # Şimdi parola linkine gidiyoruz
        response = session.get(PAROLA_URL, timeout=15)
        
        # Eğer hala 403 alıyorsak içeriği kontrol et
        if response.status_code == 403:
            print("Hata 403: GitHub IP'si engellenmiş olabilir.")
            return None
            
        response.raise_for_status()
        
        # HTML içinden pass parametresini bul
        pass_match = re.search(r'pass=([a-zA-Z0-9]+)', response.text)
        
        if pass_match:
            return pass_match.group(1)
        else:
            # Bazı durumlarda pass link içinde hash olarak geçer
            hash_match = re.search(r'hash=([a-zA-Z0-9]+)', response.text)
            return hash_match.group(1) if hash_match else None
            
    except Exception as e:
        print(f"Hata detayı: {e}")
        return None

def create_m3u(pass_code):
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
                # M3U oynatıcılarda çalışması için tam URL yapısı
                f.write(f'https://www.seir-sanduk.com/?id={ch["id"]}&pass={pass_code}\n')
        print(f"Liste güncellendi. Yeni kod: {pass_code}")
        return True
    except Exception as e:
        print(f"Yazma hatası: {e}")
        return False

if __name__ == "__main__":
    code = get_latest_data()
    if code:
        if create_m3u(code):
            sys.exit(0)
    sys.exit(1)

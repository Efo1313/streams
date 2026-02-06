import requests
import re

# Ayarlar
PAROLA_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
CHANNELS = [
    {"name": "BNT 1 HD", "id": "hd-bnt-1-hd"},
    {"name": "BTV HD", "id": "hd-btv-hd"},
    {"name": "NOVA TV HD", "id": "hd-nova-tv-hd"}
]

def get_pass():
    session = requests.Session()
    response = session.get(PAROLA_URL)
    # Sayfa içindeki pass kodunu bulur
    match = re.search(r'pass=([a-zA-Z0-9]+)', response.text)
    return match.group(1) if match else None

current_pass = get_pass()

if current_pass:
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in CHANNELS:
            f.write(f'#EXTINF:-1, {ch["name"]}\n')
            f.write(f'https://www.seir-sanduk.com/?id={ch["id"]}&pass={current_pass}\n')
    print("Liste başarıyla güncellendi!")

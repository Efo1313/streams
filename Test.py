from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def yayini_derinden_kaz(url):
    options = webdriver.ChromeOptions()
    # Bazı siteler headless (görünmez) modu engeller, o yüzden normal açıyoruz
    # İstersen '--headless' ekleyebilirsin.
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        time.sleep(10) # Sayfanın tam yüklenmesi için süre ver

        # 1. Yöntem: Sayfadaki tüm iframe'leri tara
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"Toplam {len(iframes)} adet çerçeve bulundu. İçlerine bakılıyor...")

        for index, iframe in enumerate(iframes):
            try:
                driver.switch_to.frame(iframe)
                # İçeride video veya kaynak linki var mı?
                source = driver.page_source
                if ".m3u8" in source or "googlevideo" in source:
                    print(f"✅ {index}. iframe içinde yayın verisi bulundu!")
                    # Buradaki linki yakalamak için network loglarına bakmak en iyisi
                driver.switch_to.default_content() # Ana sayfaya geri dön
            except:
                continue

        # 2. Yöntem: Network Loglarını (Ağ trafiğini) süz
        print("\n--- Ağ trafiği kontrol ediliyor ---")
        logs = driver.execute_script("return window.performance.getEntries();")
        for entry in logs:
            link = entry['name']
            if ".m3u8" in link or "videoplayback" in link:
                print(f"🚀 Bulunan Canlı Yayın Linki: \n{link}\n")
                
    finally:
        print("İşlem tamamlandı. Tarayıcıyı kapatmak için bir tuşa bas...")
        # driver.quit() # Hemen kapanmasın diye yorum satırı yaptım

yayin_url = "https://famelack.com/external?url=famelack.com"
yayini_derinden_kaz(yayin_url)

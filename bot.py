import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Samsung Modelleri Listesi
URL = "https://www.gsmarena.com/samsung-phones-9.php" 
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def verileri_cek():
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        cihazlar = []
        
        # Sayfadaki telefonları buluyoruz
        liste = soup.find('div', {'class': 'makers'}).find_all('li')
        
        for item in liste:
            isim = item.find('span').text
            link = "https://www.gsmarena.com/" + item.find('a')['href']
            resim = item.find('img')['src']
            cihazlar.append({"Cihaz": isim, "Link": link, "Resim": resim})
        
        return pd.DataFrame(cihazlar)
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return pd.DataFrame()

# Dosya adı
dosya_adi = "telefonlar.csv"

# Yeni verileri çek
yeni_df = verileri_cek()

if not yeni_df.empty:
    if os.path.exists(dosya_adi):
        eski_df = pd.read_csv(dosya_adi)
        # Sadece listede olmayan GERÇEKTEN YENİ cihazları bul
        yeni_eklenenler = yeni_df[~yeni_df['Cihaz'].isin(eski_df['Cihaz'])]
        # Yeni cihazları EN ÜSTE koy, eskileri altına ekle
        son_liste = pd.concat([yeni_eklenenler, eski_df], ignore_index=True)
    else:
        son_liste = yeni_df

    # Kaydet
    son_liste.to_csv(dosya_adi, index=False)
    print("İşlem Başarılı! Yeni cihazlar en üste eklendi.")
else:
    print("Veri çekilemedi.")

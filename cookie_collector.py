import requests
from bs4 import BeautifulSoup

# Kullanıcıdan anahtar kelime ve ülke kodu al
keyword = input("Anahtar kelime: ")
country = input("Ülke kodu (ör: tr, us, de): ")

# Google arama URL'si (ülkeye göre domain)
google_domains = {
    'tr': 'https://www.google.com.tr/search',
    'us': 'https://www.google.com/search',
    'de': 'https://www.google.de/search',
    # Gerekirse daha fazla ülke eklenebilir
}

google_url = google_domains.get(country, 'https://www.google.com/search')

params = {'q': keyword}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Google'da arama yap
response = requests.get(google_url, params=params, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# İlk organik sonucu bul
first_result = soup.find('a', href=True)
if not first_result:
    print("Sonuç bulunamadı.")
    exit()

first_url = first_result['href']
print(f"İlk sonuç: {first_url}")

# İlk sonuca istek gönder ve çerezleri topla
session = requests.Session()
result_response = session.get(first_url, headers=headers, allow_redirects=True)

print("\nToplanan çerezler:")
for cookie in session.cookies:
    print(f"{cookie.name} = {cookie.value}")
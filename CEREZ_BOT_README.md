# 🍪 Çerez Toplama Botu

Girdiğiniz kelime ve ülkeye göre web sitelerindeki çerezleri hızlıca tarayan masaüstü uygulaması.

## ✨ Özellikler

- 🔍 **Hızlı Tarama**: Anahtar kelime ve ülke bazlı çerez taraması
- 📊 **Detaylı Analiz**: Çerez güvenlik ayarları, boyut ve sona erme bilgileri
- 💾 **Dışa Aktarma**: Sonuçları JSON formatında kaydetme
- 🎨 **Modern Arayüz**: Kullanıcı dostu Tkinter GUI
- 🌍 **Çoklu Ülke**: 12 farklı ülke desteği
- ⚡ **Gerçek Zamanlı**: İlerleme çubuğu ile canlı durum takibi

## 🚀 Kurulum

### Gereksinimler
- Python 3.7 veya üzeri
- tkinter (çoğu Python kurulumunda hazır gelir)

### Adım 1: Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### Adım 2: Programı Çalıştırın
```bash
python cerez_bot.py
```

## 📱 Kullanım

1. **Programı başlatın**
   ```bash
   python cerez_bot.py
   ```

2. **Anahtar kelime girin**
   - Örnek: shopping, news, social, gaming

3. **Ülke seçin**
   - 12 farklı ülke seçeneği mevcut
   - TR, US, GB, DE, FR, IT, ES, RU, CN, JP, BR, IN

4. **"Taramayı Başlat" butonuna tıklayın**
   - İlerleme çubuğu tarama durumunu gösterir
   - Sonuçlar otomatik olarak tabloda görüntülenir

5. **Sonuçları inceleyin**
   - Çerez isimleri
   - Domain bilgileri
   - Değer önizlemeleri
   - Güvenlik ayarları (Secure, HttpOnly)
   - Boyut bilgileri

6. **Sonuçları dışa aktarın** (isteğe bağlı)
   - "Dışa Aktar" butonuna tıklayın
   - JSON dosyası olarak kaydedin

## 🔧 Özellikler

### Tarama Bilgileri
- **Çerez Analizi**: Name, Value, Domain, Path, Security flags
- **Güvenlik Kontrolleri**: Secure, HttpOnly, SameSite değerleri
- **Meta Veriler**: Boyut, sona erme tarihi, oluşturulma zamanı

### Dışa Aktarma
Sonuçlar şu bilgilerle JSON formatında kaydedilir:
```json
{
  "keyword": "shopping",
  "country": "TR",
  "country_name": "Türkiye",
  "scan_date": "2025-01-24 23:15:30",
  "total_cookies": 8,
  "cookies": [...],
  "summary": {
    "total_cookies": 8,
    "secure_cookies": 5,
    "http_only_cookies": 3,
    "total_size": 456
  }
}
```

## 🎯 Desteklenen Ülkeler

| Kod | Ülke |
|-----|------|
| TR  | Türkiye |
| US  | Amerika |
| GB  | İngiltere |
| DE  | Almanya |
| FR  | Fransa |
| IT  | İtalya |
| ES  | İspanya |
| RU  | Rusya |
| CN  | Çin |
| JP  | Japonya |
| BR  | Brezilya |
| IN  | Hindistan |

## 🛠️ Teknik Detaylar

- **Dil**: Python 3
- **GUI Framework**: Tkinter
- **Çerez Simülasyonu**: Gerçekçi örnek veriler
- **Thread Güvenliği**: Asenkron tarama işlemi
- **Veri Formatı**: JSON export desteği

## 📋 Sistem Gereksinimleri

- **İşletim Sistemi**: Windows, macOS, Linux
- **Python**: 3.7+
- **RAM**: 100MB
- **Disk Alanı**: 10MB

## 🔒 Güvenlik

Bu uygulama eğitim amaçlıdır ve simülasyon verisi kullanır. Gerçek çerez verisi toplamaz.

## 📞 Destek

Herhangi bir sorun yaşarsanız:
1. Python versiyonunuzu kontrol edin: `python --version`
2. Gerekli paketlerin yüklü olduğundan emin olun: `pip list`
3. Programı terminal/komut satırından çalıştırarak hata mesajlarını görün

## 🎉 Hızlı Başlangıç

```bash
# Projeyi indirin
# Terminal/komut satırını açın
# Proje klasörüne gidin

# Bağımlılıkları yükleyin
pip install requests

# Programı çalıştırın
python cerez_bot.py
```

**Hepsi bu kadar!** Program açılacak ve çerez taramaya başlayabilirsiniz. 🚀
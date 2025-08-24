# 🚀 Perakende Stok Optimizasyonu ve Talep Tahmini

Facebook Prophet modeli ile satış tahminleri yapan ve ABC analizi ile stok optimizasyonu sağlayan Streamlit uygulaması.

## 🌟 Canlı Demo
**[Uygulamayı Deneyin](https://kaanbostan-tahmin-similasyonu.streamlit.app/)**

## ✨ Ana Özellikler
- **ABC Analizi** - Ürünleri gelire göre A, B, C kategorilerine ayırır
- **Satış Tahmini** - Prophet modeli ile gelecek satış tahminleri
- **Stok Optimizasyonu** - Güvenlik stoğu ve EOQ hesaplamaları
- **Görselleştirmeler** - İnteraktif grafikler ve dashboard

## 📋 Nasıl Kullanılır?

### 1. Veri Hazırlama
Verileriniz şu formatta olmalı:
```csv
date,product,sales
2024-01-01,Ürün A,100
2024-01-02,Ürün A,120
2024-01-01,Ürün B,80
```

**Önemli:** 
- Tarih formatı: YYYY-MM-DD
- Sütun adları tam olarak: `date`, `product`, `sales`
- En az 10-15 satır veri olması önerilir
- **Her ürün için en az 2 farklı tarihte veri olmalı** (grafiklerin çıkması için)
- Aynı ürünün birden fazla gündeki satış verisi gerekli

### 2. Veri Yükleme
- **CSV Yükleme:** Hazırladığınız CSV dosyasını yükleyin
- **Manuel Giriş:** Arayüzde direkt veri girin

### 3. Sonuçları İnceleme
- **ABC Analizi:** Hangi ürünler en çok gelir getiriyor?
- **Tahmin Grafikleri:** Gelecek satışlar nasıl olacak?
- **Stok Önerileri:** Ne kadar stok tutmalısınız?

## 🛠️ Teknolojiler
- **Python** - Streamlit, Pandas, Prophet
- **Görselleştirme** - Plotly charts
- **Model** - Facebook Prophet (zaman serisi tahmini)

## 💡 Kimler Kullanabilir?
- **Perakende mağaza sahipleri** - Stok planlaması
- **E-ticaret işletmeleri** - Talep tahmini
- **KOBİ'ler** - Envanter yönetimi
- **Öğrenciler** - Veri analizi projesi

## ⚡ Hızlı Başlangıç
1. Uygulamayı açın: [Link](https://kaanbostan-tahmin-similasyonu.streamlit.app/)
2. CSV dosyanızı yükleyin veya örnek veri girin
3. Sonuçları inceleyin ve kararlarınızı alın

## 📞 İletişim
- **Geliştirici:** Fatih Kaan Bostan
- **E-posta:** kaan.kbostan@gmail.com
- **GitHub:** [kaanbostan](https://github.com/kaanbostan)

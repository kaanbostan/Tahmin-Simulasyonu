# 🚀 Perakende Stok Optimizasyonu ve Talep Tahmini

Bu proje, perakende satış verilerinizi kullanarak ABC analizi, satış tahmini (Prophet modeli ile) ve stok optimizasyonu yapmanıza olanak sağlar.  
Streamlit tabanlı interaktif bir web uygulamasıdır.

---

## Özellikler

- CSV veya manuel veri girişi ile kolay kullanım  
- ABC analizine göre ürün önceliklendirme  
- Facebook Prophet kullanarak ürün bazlı satış tahminleri  
- Tahmin sonuçlarının grafiklerle görselleştirilmesi  
- Güvenlik stoğu ve ekonomik sipariş miktarı (EOQ) hesaplamaları  
- Ürün performans metrikleri ve günlük satış heatmap  

---

## Kullanım

1. Verilerinizi yükleyin veya manuel girin (date, product, sales sütunları gereklidir).  
2. ABC analizi ile ürünlerinizi kategorilere ayırın.  
3. İlgili ürünü seçip, geleceğe yönelik satış tahminleri oluşturun.  
4. Tahminlere göre stok önerilerini ve EOQ hesaplamalarını görüntüleyin.  

---

## Önemli Notlar ve Bilinen Sınırlamalar

- **Tedarik Süresi (Lead Time):**  
  Mevcut stok önerileri hesaplamasında, tedarik süresi sabit veya kullanıcı tarafından girilmiyor. Bu nedenle, önerilen minimum stok seviyesi gerçek tedarik süresine göre yeterli veya fazla olabilir.  
  Gelecekte bu parametrenin kullanıcı tarafından girilmesi veya ürün bazlı yönetilmesi planlanmaktadır.  

- **Tahmin Modeli:**  
  Prophet modeli veri kalitesine bağlıdır. Eksik günler veya çok düşük veri sayısı tahmin doğruluğunu etkileyebilir.  
  Eksik günlerin veri setine dahil edilip, sıfır ile doldurulması önerilir.

- **Stok Hesaplama:**  
  Güvenlik stoğu ve minimum stok seviyesi, istatistiksel varsayımlara dayanır ve iş süreçlerine göre özelleştirilebilir.  

---

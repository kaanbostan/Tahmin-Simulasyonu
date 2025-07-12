import streamlit as st
import pandas as pd
from prophet import Prophet
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Perakende Stok Optimizasyonu", layout="wide")

st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
            padding: 20px 40px 40px 40px;
        }
        .header {
            color: #0a4b78;
            font-weight: 700;
            font-size: 42px;
            margin-bottom: 20px;
        }
        .subheader {
            color: #1373e6;
            font-weight: 600;
            font-size: 24px;
            margin-bottom: 20px;
            margin-top: 30px;
        }
        .section-box {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 8px 20px rgb(0 0 0 / 0.12);
            margin-bottom: 30px;
        }
        .footer {
            font-size: 12px;
            color: #777;
            text-align: center;
            margin-top: 50px;
        }
        .plot-container {
            margin-bottom: 30px;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
            text-align: center;
        }
        .abc-a { background: #28a745; color: white; padding: 5px 10px; border-radius: 5px; }
        .abc-b { background: #ffc107; color: black; padding: 5px 10px; border-radius: 5px; }
        .abc-c { background: #dc3545; color: white; padding: 5px 10px; border-radius: 5px; }
        .spacer {
            margin-top: 40px;
            margin-bottom: 40px;
        }
        .section-divider {
            border-top: 2px solid #e0e6ed;
            margin: 40px 0;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">🚀 Perakende Stok Optimizasyonu ve Talep Tahmini</div>', unsafe_allow_html=True)

# Veri girişi
with st.container():
    st.markdown('<div class="subheader">1. 📊 Satış Verilerinizi Yükleyin veya Girin</div>', unsafe_allow_html=True)
    upload_option = st.radio("", ("CSV Dosyası Yükle", "Manuel Veri Girişi"), label_visibility="collapsed")

    if upload_option == "CSV Dosyası Yükle":
        uploaded_file = st.file_uploader("CSV dosyanızı yükleyin (date, product, sales sütunları olmalı)", type=["csv"])
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file, parse_dates=['date'])
            st.success("✅ Dosya başarıyla yüklendi!")
            st.dataframe(data.head())
        else:
            data = None

    else:
        st.markdown("### Manuel Veri Girişi")
        rows = st.number_input("Kaç satır veri gireceksiniz?", min_value=1, max_value=100, value=10)
        
        manual_data = []
        st.markdown("**Veri Girişi:**")
        
        for i in range(rows):
            cols = st.columns([2, 3, 2])
            
            with cols[0]:
                date = st.date_input(f"📅 Tarih {i+1}", key=f"date_{i}")
            
            with cols[1]:
                product = st.text_input(f"🏷️ Ürün Adı {i+1}", 
                                       placeholder="Ürün adını yazın...", 
                                       key=f"product_{i}")
            
            with cols[2]:
                sales = st.number_input(f"💰 Satış Miktarı {i+1}", 
                                       min_value=0, 
                                       value=0, 
                                       key=f"sales_{i}")
            
            if product:  # Sadece ürün adı girilmişse listeye ekle
                manual_data.append({
                    'date': pd.to_datetime(date), 
                    'product': product, 
                    'sales': sales
                })
        
        if manual_data:
            data = pd.DataFrame(manual_data)
            st.markdown("### 📋 Girilen Veriler:")
            st.dataframe(data, use_container_width=True)
        else:
            data = None

# Bölüm ayırıcı
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ABC Analizi ve Çoklu Ürün Karşılaştırması
if data is not None and not data.empty:
    st.markdown('<div class="subheader">2. 🎯 ABC Analizi ve Ürün Performansı</div>', unsafe_allow_html=True)
    
    # ABC Analizi
    abc_data = data.groupby('product')['sales'].agg(['sum', 'count', 'mean']).reset_index()
    abc_data.columns = ['product', 'total_sales', 'frequency', 'avg_sales']
    abc_data['revenue'] = abc_data['total_sales'] * abc_data['avg_sales']
    abc_data = abc_data.sort_values('revenue', ascending=False)
    
    # ABC kategorileri
    abc_data['cumulative_revenue'] = abc_data['revenue'].cumsum()
    abc_data['cumulative_percent'] = (abc_data['cumulative_revenue'] / abc_data['revenue'].sum()) * 100
    
    def assign_abc_category(cum_percent):
        if cum_percent <= 80:
            return 'A'
        elif cum_percent <= 95:
            return 'B'
        else:
            return 'C'
    
    abc_data['ABC_Category'] = abc_data['cumulative_percent'].apply(assign_abc_category)
    
    # ABC Analizi Sonuçları
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("📈 ABC Analizi Sonuçları")
        for _, row in abc_data.iterrows():
            category = row['ABC_Category']
            css_class = f"abc-{category.lower()}"
            st.markdown(f"""
            <div style="margin: 15px 0; padding: 15px; background: #f8f9fa; border-radius: 8px;">
                <strong>{row['product']}</strong> 
                <span class="{css_class}">{category}</span><br>
                <small>Toplam Satış: {row['total_sales']:.0f} | Gelir: {row['revenue']:.0f} TL</small>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("🥧 ABC Kategori Dağılımı")
        
        # Modern Plotly pie chart - legend'ı tamamen kaldır
        fig_abc = px.pie(abc_data, values='revenue', names='product', 
                        title="Ürün Gelir Dağılımı",
                        color='ABC_Category',
                        color_discrete_map={'A': '#28a745', 'B': '#ffc107', 'C': '#dc3545'},
                        template='plotly_white')
        
        fig_abc.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            textfont_size=12,
            marker=dict(line=dict(color='white', width=2))
        )
        
        fig_abc.update_layout(
            height=400,
            font=dict(size=12),
            showlegend=False,  # Legend'ı tamamen kaldır
            margin=dict(l=20, r=20, t=60, b=20)  # Margin'ları optimize et
        )
        
        st.plotly_chart(fig_abc, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Bölüm ayırıcı
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Çoklu Ürün Karşılaştırması
    st.markdown('<div class="subheader">3. 📊 Çoklu Ürün Karşılaştırması</div>', unsafe_allow_html=True)
    
    # Zaman serisi karşılaştırması - Ana referans grafik
    daily_sales = data.groupby(['date', 'product'])['sales'].sum().reset_index()
    
    fig_comparison = px.line(daily_sales, x='date', y='sales', color='product',
                           title='📈 Ürün Satış Trendleri',
                           labels={'sales': 'Satış Miktarı', 'date': 'Tarih'},
                           template='plotly_white')
    
    fig_comparison.update_traces(
        line=dict(width=3),
        marker=dict(size=6)
    )
    
    fig_comparison.update_layout(
        height=450,
        font=dict(size=12),
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        title_font_size=16,
        xaxis_title_font_size=14,
        yaxis_title_font_size=14,
        margin=dict(l=50, r=50, t=80, b=80)
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    
    # Performans metrikleri
    st.subheader("🏆 Ürün Performans Metrikleri")
    
    metrics_cols = st.columns(len(abc_data))
    for i, (_, row) in enumerate(abc_data.iterrows()):
        with metrics_cols[i]:
            st.markdown(f"""
            <div class="metric-card">
                <h4>{row['product']}</h4>
                <p>Kategori: <strong>{row['ABC_Category']}</strong></p>
                <p>Toplam Satış: <strong>{row['total_sales']:.0f}</strong></p>
                <p>Ortalama: <strong>{row['avg_sales']:.1f}</strong></p>
            </div>
            """, unsafe_allow_html=True)

# Bölüm ayırıcı
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Tekil Ürün Analizi
with st.container():
    if data is not None and not data.empty:
        st.markdown('<div class="subheader">4. 🔍 Detaylı Ürün Analizi ve Tahmin</div>', unsafe_allow_html=True)
        
        product_list = data['product'].dropna().unique()
        if len(product_list) == 0:
            st.warning("⚠️ Veride ürün bilgisi bulunamadı.")
        else:
            selected_product = st.selectbox("🎯 Tahmin için ürün seçin:", product_list)

            product_data = data[data['product'].str.lower() == selected_product.lower()]
            df = product_data.rename(columns={"date": "ds", "sales": "y"})[['ds', 'y']]
            df['ds'] = pd.to_datetime(df['ds'])

            df = df.groupby('ds').agg({'y':'sum'}).reset_index()
            df = df.set_index('ds').asfreq('D').reset_index()

            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.write(f"**{selected_product}** ürününe ait temizlenmiş veri (eksik günler NaN):")
            st.dataframe(df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            if df['y'].dropna().shape[0] < 2:
                st.error("❌ Yeterli veri yok. En az 2 geçerli satış günü olmalı.")
            else:
                model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
                model.fit(df)

                days_to_forecast = st.slider("📅 Kaç gün sonrası için tahmin yapılsın?", 7, 60, 30)

                future = model.make_future_dataframe(periods=days_to_forecast)
                forecast = model.predict(future)

                st.markdown('<div class="section-box">', unsafe_allow_html=True)
                st.write("📊 Tahmin sonuçları (son günler):")
                st.dataframe(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(days_to_forecast), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

                # 1. Ana tahmin grafiği - Plotly versiyonu
                st.markdown('<div class="plot-container">', unsafe_allow_html=True)
                st.subheader("🔮 Satış Tahmini")
                
                fig_forecast = go.Figure()
                
                # Belirsizlik aralığı
                fig_forecast.add_trace(go.Scatter(
                    x=forecast['ds'],
                    y=forecast['yhat_upper'],
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False,
                    name='Üst Sınır'
                ))
                
                fig_forecast.add_trace(go.Scatter(
                    x=forecast['ds'],
                    y=forecast['yhat_lower'],
                    mode='lines',
                    line=dict(width=0),
                    fill='tonexty',
                    fillcolor='rgba(68, 68, 68, 0.2)',
                    name='Belirsizlik Aralığı'
                ))
                
                # Tahmin çizgisi
                fig_forecast.add_trace(go.Scatter(
                    x=forecast['ds'],
                    y=forecast['yhat'],
                    mode='lines',
                    name='Tahmin',
                    line=dict(color='#1f77b4', width=3)
                ))
                
                # Gerçek veriler
                df_clean = df.dropna()
                if not df_clean.empty:
                    fig_forecast.add_trace(go.Scatter(
                        x=df_clean['ds'],
                        y=df_clean['y'],
                        mode='markers',
                        name='Gerçek Veri',
                        marker=dict(color='#ff7f0e', size=8)
                    ))
                
                fig_forecast.update_layout(
                    title=f'🔮 {selected_product} Ürünü için Satış Tahmini',
                    xaxis_title='Tarih',
                    yaxis_title='Satış Miktarı',
                    height=450,
                    template='plotly_white',
                    hovermode='x unified',
                    legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
                    margin=dict(l=50, r=50, t=80, b=80)
                )
                
                st.plotly_chart(fig_forecast, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

                # 2. Bileşenler grafiği - Plotly subplots (daha fazla boşluk)
                st.markdown('<div class="plot-container">', unsafe_allow_html=True)
                st.subheader("🧩 Zaman Serisi Bileşenleri")
                
                # Subplot oluştur - vertical_spacing artırıldı
                fig_components = make_subplots(
                    rows=3, cols=1,
                    subplot_titles=['📈 Genel Trend', '📅 Haftalık Sezonallik', '🔄 Yıllık Sezonallik'],
                    vertical_spacing=0.15  # 0.08'den 0.15'e çıkarıldı
                )
                
                # Trend
                fig_components.add_trace(
                    go.Scatter(x=forecast['ds'], y=forecast['trend'], 
                              mode='lines', name='Trend', line=dict(color='#2E86AB', width=3)),
                    row=1, col=1
                )
                
                # Haftalık sezonallik
                fig_components.add_trace(
                    go.Scatter(x=forecast['ds'], y=forecast['weekly'], 
                              mode='lines', name='Haftalık', line=dict(color='#A23B72', width=3)),
                    row=2, col=1
                )
                
                # Yıllık sezonallik
                if 'yearly' in forecast.columns:
                    fig_components.add_trace(
                        go.Scatter(x=forecast['ds'], y=forecast['yearly'], 
                                  mode='lines', name='Yıllık', line=dict(color='#F18F01', width=3)),
                        row=3, col=1
                    )
                
                fig_components.update_layout(
                    height=700,  # Yükseklik artırıldı
                    template='plotly_white',
                    showlegend=False,
                    title_text="🧩 Zaman Serisi Bileşenleri",
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                
                st.plotly_chart(fig_components, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

                # --- Burada "Tahmin Belirsizliği ve Doğruluk" ile "Trend ve Mevsimsellik Analizi" kaldırıldı ---

                # Bölüm ayırıcı
                st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

                # Stok önerileri
                st.subheader("📦 Stok Önerileri")
                last_period = forecast[-days_to_forecast:]
                average_demand = last_period['yhat'].mean()
                std_demand = last_period['yhat'].std()
                safety_stock = 1.65 * std_demand
                min_stock_level = average_demand + safety_stock

                # ABC kategorisi bilgisi
                product_abc = abc_data[abc_data['product'] == selected_product]['ABC_Category'].iloc[0]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    **📊 Temel Stok Metrikleri:**
                    - **ABC Kategorisi:** `{product_abc}`
                    - **Ortalama günlük tahmini talep:** `{average_demand:.2f}`
                    - **Talep standart sapması:** `{std_demand:.2f}`
                    - **Güvenlik stoğu (95% güven):** `{safety_stock:.2f}`
                    - **Önerilen minimum stok seviyesi:** `{min_stock_level:.2f}`
                    """)
                
                with col2:
                    # ABC kategorisine göre öneriler
                    if product_abc == 'A':
                        st.markdown("""
                        **🎯 A Kategorisi Önerileri:**
                        - Yüksek öncelikli ürün
                        - Sık sık stok kontrolü yapın
                        - Güvenlik stoğunu artırın
                        - Tedarikçi ilişkilerini güçlendirin
                        """)
                    elif product_abc == 'B':
                        st.markdown("""
                        **⚖️ B Kategorisi Önerileri:**
                        - Orta öncelikli ürün
                        - Düzenli stok kontrolü
                        - Standart güvenlik stoğu
                        - Maliyet-fayda dengesini koruyun
                        """)
                    else:
                        st.markdown("""
                        **📉 C Kategorisi Önerileri:**
                        - Düşük öncelikli ürün
                        - Minimal stok tutun
                        - Maliyet odaklı yaklaşım
                        - Gözden geçirme sıklığını azaltın
                        """)

                # Bölüm ayırıcı
                st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

                st.subheader("💰 Ekonomik Sipariş Miktarı (EOQ) Hesaplama")
                
                st.markdown('<div class="section-box">', unsafe_allow_html=True)
                col_eoq1, col_eoq2 = st.columns(2)
                
                with col_eoq1:
                    order_cost = st.number_input("Sipariş Başına Maliyet (TL)", min_value=0.0, value=50.0, step=10.0)
                with col_eoq2:
                    holding_cost = st.number_input("Yıllık Stok Tutma Maliyeti (TL/ürün)", min_value=0.0, value=2.0, step=0.5)

                demand_per_year = average_demand * 365

                if order_cost > 0 and holding_cost > 0:
                    optimal_order_qty = (2 * demand_per_year * order_cost / holding_cost) ** 0.5
                    reorder_frequency = demand_per_year / optimal_order_qty
                    
                    st.markdown(f"""
                    **📈 EOQ Analizi:**
                    - **Yıllık tahmini talep:** `{demand_per_year:.2f}`
                    - **Optimal Sipariş Miktarı (EOQ):** `{optimal_order_qty:.2f}`
                    - **Yıllık optimal sipariş sayısı:** `{reorder_frequency:.1f}`
                    - **Sipariş aralığı:** `{365/reorder_frequency:.0f} gün`
                    """)
                
                st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("ℹ️ Lütfen önce veri yükleyin veya manuel veri girin.")

# Bölüm ayırıcı
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Özet Dashboard
if data is not None and not data.empty:
    st.markdown('<div class="subheader">5. 📊 Genel Özet Dashboard</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_products = data['product'].nunique()
        st.metric("🏷️ Toplam Ürün Sayısı", total_products)
    
    with col2:
        total_sales = data['sales'].sum()
        st.metric("💰 Toplam Satış", f"{total_sales:,.0f}")
    
    with col3:
        avg_daily_sales = data.groupby('date')['sales'].sum().mean()
        st.metric("📅 Ortalama Günlük Satış", f"{avg_daily_sales:.1f}")
    
    with col4:
        a_category_count = len(abc_data[abc_data['ABC_Category'] == 'A'])
        st.metric("🎯 A Kategorisi Ürün", a_category_count)
    
    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    
    # Heatmap - Ürün x Günlük Satış (Plotly versiyonu)
    st.subheader("🔥 Ürün x Günlük Satış Heatmap")
    pivot_data = data.pivot_table(values='sales', index='product', columns='date', aggfunc='sum', fill_value=0)
    
    fig_heatmap = px.imshow(pivot_data, 
                           title="📈 Ürün x Günlük Satış Heatmap",
                           labels=dict(x="Tarih", y="Ürün", color="Satış"),
                           aspect="auto",
                           color_continuous_scale='Viridis',
                           template='plotly_white')
    
    fig_heatmap.update_layout(
        height=350,
        font=dict(size=11),
        title_font_size=16
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)
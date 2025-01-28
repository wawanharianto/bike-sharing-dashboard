import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

# Memperbaiki path file sesuai dengan struktur folder
hour_data = pd.read_csv("data/hour.csv")  # File berada di folder 'data'
day_data = pd.read_csv("data/day.csv")  # File berada di folder 'data'

# Fungsi untuk memuat data dan memeriksa apakah data sudah dimuat dengan benar
def load_data():
    return hour_data, day_data

# Mengatur judul halaman dan layout
st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide", page_icon="🚲")

# Menampilkan judul dashboard
st.markdown("""
<style>
    .main-title {
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>Dashboard Penyewaan Sepeda 🚴</div>", unsafe_allow_html=True)

# --- Penjelasan Proyek ---
st.sidebar.header("📖 Tentang Proyek")
st.sidebar.write("""
    Proyek ini bertujuan untuk menganalisis dan memvisualisasikan data penyewaan sepeda berdasarkan waktu, musim, dan cuaca. 
    Dengan menggunakan data historis penyewaan sepeda, kita dapat memahami tren dan faktor-faktor yang mempengaruhi jumlah penyewaan sepeda.
""")

# Menampilkan informasi dasar tentang data
st.sidebar.header("📊 Informasi Data")
st.sidebar.write(f"Total data pada hour: {len(hour_data)}")
st.sidebar.write(f"Total data pada day: {len(day_data)}")

# Menampilkan contoh data
if st.sidebar.checkbox("👀 Tampilkan contoh data"):
    st.write("**Contoh Data Hour**", hour_data.head())
    st.write("**Contoh Data Day**", day_data.head())

# --- Menambahkan Kolom rental_group berdasarkan jam ---
# Membuat kelompok waktu berdasarkan jam (misal: pagi, siang, sore, malam)
def create_rental_group(hour):
    if 6 <= hour < 12:
        return 'Pagi'
    elif 12 <= hour < 18:
        return 'Siang'
    elif 18 <= hour < 24:
        return 'Sore'
    else:
        return 'Malam'

# Menambahkan kolom rental_group ke dataset hour_data
hour_data['rental_group'] = hour_data['hr'].apply(create_rental_group)

# --- Statistik Utama ---
st.markdown("### 📌 Statistik Utama")
stats1, stats2, stats3 = st.columns(3)
with stats1:
    st.metric("Total Penyewaan", int(hour_data['cnt'].sum()))
with stats2:
    st.metric("Rata-rata Penyewaan", round(hour_data['cnt'].mean(), 2))
with stats3:
    st.metric("Jumlah Hari", day_data['dteday'].nunique())

# --- Bagian 1: Analisis Time Series ---
st.header("📈 Analisis Time Series")

# Mengubah kolom tanggal menjadi format datetime
hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])
day_data['dteday'] = pd.to_datetime(day_data['dteday'])

# Menampilkan jumlah penyewaan sepeda per hari
st.subheader("Jumlah Penyewaan Sepeda per Hari")
day_data_grouped = day_data.groupby('dteday')['cnt'].sum()
st.line_chart(day_data_grouped)

# Menampilkan jumlah penyewaan sepeda per jam
st.subheader("Jumlah Penyewaan Sepeda per Jam")
hour_data_grouped = hour_data.groupby('dteday')['cnt'].sum()
st.line_chart(hour_data_grouped)

# --- Bagian 2: Distribusi Penyewaan ---
st.header("📊 Distribusi Penyewaan Sepeda")

# Penyewaan per kelompok waktu
st.subheader("Penyewaan per Kelompok Waktu")
grouped_data = hour_data.groupby('rental_group')['cnt'].sum()
sns.set(style="whitegrid")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=grouped_data.index, y=grouped_data.values, ax=ax, palette="coolwarm")
ax.set_title("Jumlah Penyewaan Berdasarkan Kelompok Waktu")
ax.set_xlabel("Kelompok Waktu")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# --- Bagian 3: Analisis Korelasi ---
st.header("🔗 Analisis Korelasi")

# Heatmap korelasi untuk fitur numerik
st.subheader("Heatmap Korelasi")
corr_data = hour_data[['temp', 'atemp', 'hum', 'windspeed', 'cnt']].corr()
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(corr_data, annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Korelasi Antar Fitur")
st.pyplot(fig)

# --- Bagian 4: Analisis Kelompok Penyewaan ---
st.header("🌍 Analisis Kelompok Penyewaan")

# Menampilkan penyewaan sepeda berdasarkan musim
st.subheader("Penyewaan Sepeda Berdasarkan Musim")
season_grouped = hour_data.groupby('season')['cnt'].sum()
sns.set(style="whitegrid")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=season_grouped.index, y=season_grouped.values, ax=ax, palette="coolwarm")
ax.set_title("Jumlah Penyewaan Berdasarkan Musim")
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# --- Bagian 5: Visualisasi Peta ---
st.header("🗺️ Analisis Geografis")

# Membuat data lokasi contoh untuk visualisasi (gantilah dengan data sebenarnya)
sample_location = {
    'lat': 40.7128,  # Latitude contoh (New York City)
    'lon': -74.0060  # Longitude contoh (New York City)
}

# Membuat peta
st.subheader("Peta Lokasi Penyewaan")
m = folium.Map(location=[sample_location['lat'], sample_location['lon']], zoom_start=12)

# Menambahkan marker cluster untuk beberapa lokasi (contoh)
marker_cluster = MarkerCluster().add_to(m)
folium.Marker([sample_location['lat'], sample_location['lon']], popup="Lokasi Penyewaan Sepeda").add_to(marker_cluster)

# Menampilkan peta di Streamlit
st.write("Peta Lokasi Penyewaan")
folium_static(m)

# --- Bagian 6: Filter ---
st.sidebar.header("🎛️ Filter Data")

# Filter berdasarkan musim
season_filter = st.sidebar.multiselect("Pilih Musim", options=hour_data['season'].unique())
if season_filter:
    filtered_data = hour_data[hour_data['season'].isin(season_filter)]
else:
    filtered_data = hour_data

# Filter berdasarkan bulan
month_filter = st.sidebar.multiselect("Pilih Bulan", options=hour_data['mnth'].unique())
if month_filter:
    filtered_data = filtered_data[filtered_data['mnth'].isin(month_filter)]

# Menampilkan data yang telah difilter
st.subheader("Data yang Diperbarui")
st.write(filtered_data)

# --- Bagian 7: Hasil Analisis dan Saran ---
st.header("📝 Hasil Analisis dan Saran")

st.subheader("Hasil Analisis")
st.write("""
1. **Kelompok Waktu Paling Populer:** Penyewaan sepeda tertinggi terjadi pada kelompok waktu pagi dan siang hari.
2. **Musim dengan Penyewaan Tertinggi:** Musim tertentu, seperti musim panas, memiliki jumlah penyewaan yang lebih tinggi dibandingkan musim lainnya.
3. **Faktor yang Mempengaruhi Penyewaan:** Korelasi menunjukkan bahwa suhu (temp) memiliki pengaruh yang cukup besar terhadap jumlah penyewaan sepeda.
""")

st.subheader("Saran")
st.write("""
1. **Optimalisasi Sumber Daya:** Tambahkan lebih banyak sepeda selama kelompok waktu populer (pagi dan siang) untuk memenuhi permintaan.
2. **Perawatan Sepeda:** Fokus pada musim dengan penyewaan tertinggi untuk memastikan ketersediaan sepeda yang memadai.
3. **Promosi:** Adakan promosi pada musim dengan penyewaan yang rendah, seperti musim dingin atau musim hujan, untuk menarik lebih banyak pelanggan.
4. **Peningkatan Pengalaman Pelanggan:** Pertimbangkan untuk menambahkan lokasi parkir tambahan di area yang sering digunakan berdasarkan analisis data lokasi.
5. **Pemantauan Faktor Cuaca:** Karena suhu memengaruhi penyewaan, siapkan strategi untuk hari-hari dengan suhu ekstrem seperti diskon atau layanan tambahan.
""")

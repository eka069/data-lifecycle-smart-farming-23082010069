import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Smart Farming", layout="wide")

st.title("🌾 Monitoring Pertanian Pintar (Smart Farming)")
st.write("Aplikasi ini memantau kondisi lahan berdasarkan data sensor secara real-time.")

# 2. Fungsi Load Data
# Pastikan jalur file ini benar saat di-upload ke GitHub
@st.cache_data
def load_data():
    # Sesuaikan path jika nanti di-deploy di Streamlit Cloud
    df = pd.read_csv('outputs/cleaned_data.csv')
    return df

df = load_data()

# 3. Visualisasi 1: Matriks Ringkasan (Metric)
# Mengambil data terakhir yang masuk ke sensor
st.subheader("📊 Status Sensor Terkini")
latest = df.iloc[-1]
col1, col2, col3 = st.columns(3)

col1.metric("Suhu Lingkungan", f"{latest['temp']} °C")
col2.metric("Kelembaban Udara", f"{latest['humidity']} %")
col3.metric("Kelembaban Tanah (MOI)", f"{latest['MOI']} %")

st.divider()

# 4. Visualisasi 2 & 3: Grafik Tren & Korelasi
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📈 Tren Nilai Sensor")
    # Menampilkan grafik garis untuk 100 data terakhir
    st.line_chart(df[['temp', 'humidity', 'MOI']].tail(100))

with col_right:
    st.subheader("🔥 Korelasi Antar Sensor")
    fig, ax = plt.subplots()
    sns.heatmap(df[['temp', 'humidity', 'MOI']].corr(), annot=True, cmap='YlGnBu', ax=ax)
    st.pyplot(fig)

# 5. Visualisasi 4: Sistem Peringatan (Decision Support)
st.divider()
st.subheader("🚨 Sistem Peringatan Dini")

# Algoritma Keputusan
if latest['MOI'] < 30:
    st.error(f"KONDISI KRITIS: Kelembaban tanah hanya {latest['MOI']}%. Pompa air harus segera dinyalakan!")
elif 30 <= latest['MOI'] <= 60:
    st.warning("KONDISI WASPADA: Tanah mulai kering. Pantau jadwal penyiraman.")
else:
    st.success("KONDISI OPTIMAL: Kelembaban tanah cukup. Tanaman dalam keadaan sehat.")
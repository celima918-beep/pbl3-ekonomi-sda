import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Dashboard Ekonomi SDA - FEB UNISBA", layout="wide")

# --- BAGIAN LOGO LOKAL ---
nama_file_logo = "logo_unisba.png" 

# Custom CSS untuk Estetika Profesional
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stMetric { 
        background-color: #ffffff;
        padding: 15px; 
        border-radius: 10px; 
        border-top: 4px solid #1a3a5f; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); 
    }
    .explanation-box { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #28a745; 
        margin: 15px 0px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        color: #333333;
        font-size: 14px;
        line-height: 1.6;
    }
    .identity-card {
        background-color: #1a3a5f;
        padding: 20px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
    }
    .param-card {
        background-color: #eef2f6;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #d1d9e0;
        margin-bottom: 20px;
    }
    h1, h2, h3 { color: #1a3a5f; }
    .footer {
        text-align: center;
        padding: 30px;
        color: #777;
        font-size: 0.85em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA UTAMA ---
data_historis = {
    'Tahun': [2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'Produksi (q)': [81100000, 86300000, 83300000, 78800000, 71900000, 77800000, 74700000],
    'Harga Batu Bara (P)': [58.4, 56.1, 47.6, 67.4, 121.0, 81.3, 71.8]
}
df_h = pd.DataFrame(data_historis)

tahun_proyeksi = [2025, 2026, 2027, 2028, 2029, 2030, 2031]
mc_presisi = [13.71, 15.50, 18.20, 22.00, 28.00, 38.00, 55.00] 

# --- 3. SIDEBAR (KONTROL SIMULASI) ---
with st.sidebar:
    if os.path.exists(nama_file_logo):
        st.image(nama_file_logo, width=100)
    st.markdown("### ⚙️ Kontrol Simulasi")
    
    harga_input = st.slider("Harga Batu Bara (P0) $", 40.0, 150.0, 71.8)
    r_rate = st.slider("Tingkat Diskonto (r)", 0.01, 0.20, 0.05)
    pajak_gp = st.slider("Pajak Karbon Future ($)", 0, 100, 20)
    
    st.divider()
    st.caption("Fakultas Ekonomi dan Bisnis\nUniversitas Islam Bandung")

# --- 4. PERHITUNGAN DINAMIS ---
mc_awal = 13.71
muc_awal_dinamis = harga_input - mc_awal 

# LOGIKA DINAMIS: Green Paradox & Supply Rush
# Pajak karbon di masa depan memicu ekstraksi lebih cepat di masa kini
stok_awal = 544714167.87
laju_ekstraksi_normal = 75000000 
efek_pajak = (pajak_gp / 50) * 15000000 # Semakin tinggi pajak, semakin besar supply rush
faktor_r = (r_rate / 0.05)

ekstraksi_dinamis = (laju_ekstraksi_normal + efek_pajak) * faktor_r

stok_plot = []
curr_stok = stok_awal
for t in range(len(tahun_proyeksi)):
    stok_plot.append(max(0, curr_stok))
    curr_stok -= ekstraksi_dinamis

# Perhitungan MUC Hotelling dengan r
t_idx = np.arange(len(tahun_proyeksi))
muc_t = muc_awal_dinamis * np.exp(r_rate * t_idx)
p_t = np.array(mc_presisi) + muc_t

# --- 5. HEADER ---
col_l, col_j = st.columns([1, 6])
with col_l:
    if os.path.exists(nama_file_logo):
        st.image(nama_file_logo, width=120)
with col_j:
    st.markdown("<h1 style='margin-bottom: 0;'>Analisis Intertemporal Sumber Daya Batu Bara</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top: 0; color: #555; font-weight: normal;'>PT Bumi Resources Tbk</h3>", unsafe_allow_html=True)

# --- 6. PANEL ANGGOTA KELOMPOK ---
st.markdown(f"""
<div class="identity-card">
    <table style="width:100%; border:none; color:white;">
        <tr>
            <td style="width:65%; vertical-align: top;">
                <span style='font-size: 0.9em; opacity: 0.8;'>ANGGOTA KELOMPOK:</span><br>
                <div style='margin-top: 5px; line-height: 1.4;'>
                1. Ina Rani Amelia (10090224002)<br>
                2. Nayla Dwi Safitri (10090224007)<br>
                3. Celi Maulidi Aprilia (10090224027)
                </div>
            </td>
            <td style="width:35%; vertical-align: top; text-align: right; border-left: 1px solid rgba(255,255,255,0.2); padding-left: 20px;">
                <span style='font-size: 0.9em; opacity: 0.8;'>DOSEN PENGAMPU:</span><br>
                <div style='margin-top: 5px; font-size: 1.1em;'><b>Yuhka Sundaya, S.E., M.Si.</b></div>
            </td>
        </tr>
    </table>
</div>
""", unsafe_allow_html=True)

# --- 7. PARAMETER DASAR ---
st.subheader("📍 Parameter Dasar Analisis (T=0)")
c_p1, c_p2, c_p3, c_p4 = st.columns(4)
with c_p1:
    st.markdown(f"<div class='param-card'><b>Harga Dasar (P0):</b><br>${harga_input:.2f}</div>", unsafe_allow_html=True)
with c_p2:
    st.markdown(f"<div class='param-card'><b>MUC Awal (λ0):</b><br>${muc_awal_dinamis:.2f}</div>", unsafe_allow_html=True)
with c_p3:
    st.markdown(f"<div class='param-card'><b>Tingkat Diskonto (r):</b><br>{r_rate*100:.0f}%</div>", unsafe_allow_html=True)
with c_p4:
    st.markdown(f"<div class='param-card'><b>Pajak Karbon:</b><br>${pajak_gp}</div>", unsafe_allow_html=True)

# --- 8. BAGIAN UTAMA ---
tab_hist, tab_hotelling, tab_green = st.tabs(["📊 Data Historis", "📈 Model Hotelling", "🌿 Analisis Green Paradox"])

with tab_hist:
    col1, col2 = st.columns([2, 3])
    with col1:
        st.write("**Historis Produksi & Harga**")
        st.dataframe(df_h, use_container_width=True)
    with col2:
        fig_h, ax_h = plt.subplots(figsize=(8, 4.5), facecolor='#f4f7f9')
        ax_h.plot(df_h['Tahun'], df_h['Harga Batu Bara (P)'], marker='o', color='#1a3a5f', label='Harga')
        ax_h.set_ylabel("Harga ($)")
        ax_h.set_title("Trend Harga Historis")
        st.pyplot(fig_h)

with tab_hotelling:
    st.write("**Proyeksi Harga & Rente Kelangkaan**")
    df_res = pd.DataFrame({'Tahun': tahun_proyeksi, 'MUC': muc_t, 'Harga': p_t})
    st.dataframe(df_res.style.format('{:,.2f}'), use_container_width=True)
    
    fig_ht, ax_ht = plt.subplots(figsize=(10, 4))
    ax_ht.plot(tahun_proyeksi, p_t, label='Harga Proyeksi (P)', color='green', marker='s')
    ax_ht.plot(tahun_proyeksi, muc_t, label='MUC (λ)', color='blue', linestyle='--')
    ax_ht.set_title("Keseimbangan Hotelling")
    ax_ht.legend()
    st.pyplot(fig_ht)

# --- BAGIAN IV: REVISI GREEN PARADOX ---
with tab_green:
    st.header("Analisis Dampak Green Paradox")
    
    st.markdown(f"""
    <div class="explanation-box">
    <b>Mekanisme Alat Analisis:</b><br>
    Ketika variabel <b>Pajak Karbon (${pajak_gp})</b> dinaikkan, produsen melihat ancaman biaya di masa depan. 
    Hal ini memicu <i>Supply Rush</i>, di mana stok cadangan akan dikuras lebih cepat di tahun-tahun awal. 
    Secara simultan, <b>MUC</b> akan merespons tingkat diskonto <b>({r_rate*100:.0f}%)</b> untuk menentukan 
    apakah lebih menguntungkan menjual batu bara sekarang atau membiarkannya di dalam tanah.
    </div>
    """, unsafe_allow_html=True)
    
    # Grafik Korelasi Green Paradox
    fig_gp, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), facecolor='#f4f7f9')
    
    # Subplot 1: Sisa Stok vs Pajak Karbon
    ax1.fill_between(tahun_proyeksi, stok_plot, color='green', alpha=0.2)
    ax1.plot(tahun_proyeksi, stok_plot, color='green', marker='o', linewidth=2)
    ax1.set_title("Penurunan Stok (Supply Rush Efek)", fontweight='bold')
    ax1.set_ylabel("Volume Cadangan (Ton)")
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # Subplot 2: Hubungan MUC & r dalam Konteks Pajak
    ax2.plot(tahun_proyeksi, muc_t, color='#1a3a5f', marker='^', label='MUC (Pertumbuhan r)')
    ax2.set_title("Respon MUC terhadap Suku Bunga", fontweight='bold')
    ax2.set_ylabel("Nilai Kelangkaan ($)")
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    st.pyplot(fig_gp)
    
    # Alert System
    if pajak_gp > 40:
        st.error(f"🚨 **Peringatan Green Paradox:** Pajak sebesar ${pajak_gp} terlalu agresif! Produsen mempercepat ekstraksi, stok cadangan habis di bawah tahun 2031.")
    else:
        st.success("✅ **Stabilitas Ekstraksi:** Tekanan regulasi masih dapat dikompensasi oleh cadangan fisik.")

st.divider()
st.markdown("<div class='footer'>Dashboard Analisis Ekonomi SDA | PBL 3 | FEB UNISBA | 2026</div>", unsafe_allow_html=True)

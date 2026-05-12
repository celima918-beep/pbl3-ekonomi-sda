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

# LOGIKA DINAMIS GREEN PARADOX
# Pajak karbon masa depan memicu ekstraksi lebih besar di masa sekarang
stok_awal = 544714167.87
laju_ekstraksi_base = 75000000 

# Rumus Supply Rush: Pajak dan r meningkatkan kecepatan ekstraksi
efek_supply_rush = (pajak_gp / 100) * 20000000 # Bonus ekstraksi karena takut pajak
faktor_ekstraksi = (r_rate / 0.05) * (harga_input / 71.8)
total_ekstraksi_tahunan = (laju_ekstraksi_base + efek_supply_rush) * faktor_ekstraksi

stok_gp = []
curr_stok = stok_awal
for t in range(len(tahun_proyeksi)):
    stok_gp.append(max(0, curr_stok))
    curr_stok -= total_ekstraksi_tahunan

# Perhitungan MUC & Harga Proyeksi
t_idx = np.arange(len(tahun_proyeksi))
muc_t = muc_awal_dinamis * np.exp(r_rate * t_idx)
# Harga proyeksi memasukkan ekspektasi pajak di masa depan
p_t = np.array(mc_presisi) + muc_t + (pajak_gp * (t_idx / max(t_idx)))

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

# --- 7. TABS UTAMA ---
tabs = st.tabs(["📊 Tinjauan Data", "📈 Analisis Hotelling", "🌿 Simulasi Green Paradox"])

with tabs[0]:
    st.subheader("Data Historis & Stok Saat Ini")
    c1, c2 = st.columns([2, 3])
    with c1:
        st.dataframe(df_h, use_container_width=True)
    with c2:
        fig_h, ax_h = plt.subplots(figsize=(8, 4))
        ax_h.plot(df_h['Tahun'], df_h['Harga Batu Bara (P)'], marker='o', color='#1a3a5f')
        ax_h.set_title("Trend Harga Historis")
        st.pyplot(fig_h)

with tabs[1]:
    st.subheader("Model Optimasi Intertemporal")
    df_hot = pd.DataFrame({'Tahun': tahun_proyeksi, 'MUC (λ)': muc_t, 'P Proyeksi': p_t})
    st.dataframe(df_hot.style.format('{:,.2f}'), use_container_width=True)
    
    fig_ht, ax_ht = plt.subplots(figsize=(10, 4))
    ax_ht.plot(tahun_proyeksi, p_t, label='Harga Proyeksi', color='green', marker='s')
    ax_ht.plot(tahun_proyeksi, muc_t, label='MUC (Rente)', color='blue', linestyle='--')
    ax_ht.legend()
    st.pyplot(fig_ht)

# --- BAGIAN IV REVISI: GREEN PARADOX CORRELATION ---
with tabs[2]:
    st.header("Analisis Korelasi Green Paradox")
    
    st.markdown(f"""
    <div class='explanation-box'>
    <b>Alat Analisis Korelasi:</b><br>
    Grafik di bawah ini menunjukkan bagaimana <b>Pajak Karbon (${pajak_gp})</b> berinteraksi dengan 
    <b>Tingkat Bunga ({r_rate*100:.0f}%)</b>. Secara teori, ekspektasi pajak di masa depan akan menyebabkan 
    produsen melakukan <i>Supply Rush</i> (ekstraksi besar-besaran sekarang), yang mempercepat habisnya <b>Stok Cadangan</b> 
    dan meningkatkan <b>MUC</b> secara prematur.
    </div>
    """, unsafe_allow_html=True)

    # Pembuatan Grafik Korelasi Multi-Variabel
    fig_gp, ax1 = plt.subplots(figsize=(12, 6), facecolor='#f4f7f9')

    # Sumbu Kiri: Jumlah Stok
    ax1.set_xlabel('Tahun Proyeksi')
    ax1.set_ylabel('Sisa Stok Cadangan (Ton)', color='green')
    ax1.bar(tahun_proyeksi, stok_gp, color='green', alpha=0.3, label='Sisa Stok (Supply Rush)')
    ax1.tick_params(axis='y', labelcolor='green')

    # Sumbu Kanan: MUC dan Harga
    ax2 = ax1.twinx()
    ax2.set_ylabel('Nilai Moneter ($)', color='#1a3a5f')
    ax2.plot(tahun_proyeksi, muc_t, color='blue', marker='o', label='MUC (λ)')
    ax2.plot(tahun_proyeksi, p_t, color='red', marker='x', label='Harga (P) + Efek Pajak')
    ax2.tick_params(axis='y', labelcolor='#1a3a5f')

    plt.title("Korelasi Intertemporal: Stok vs MUC vs Harga (Efek Green Paradox)", fontweight='bold')
    fig_gp.tight_layout()
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    
    st.pyplot(fig_gp)

    # Indikator Status Analisis
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("Laju Ekstraksi Tahunan", f"{total_ekstraksi_tahunan/1000000:.2f} Juta Ton", 
                  delta=f"{(efek_supply_rush/1000000):.2f} Juta (Efek Pajak)")
    with col_stat2:
        if pajak_gp > 40:
            st.warning("🚨 **Supply Rush Terdeteksi:** Eksploitasi dipercepat akibat beban pajak tinggi.")
        else:
            st.success("✅ **Laju Normal:** Kebijakan karbon belum memicu pengurasan radikal.")

st.divider()
st.markdown("<div class='footer'>Dashboard Analisis Ekonomi SDA | FEB UNISBA | 2026</div>", unsafe_allow_html=True)

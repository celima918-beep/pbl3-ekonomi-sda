import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# --- 1. KONFIGURASI HALAMAN ---
# Menggunakan layout="centered" seringkali lebih stabil untuk tampilan mobile
st.set_page_config(page_title="Dashboard Ekonomi SDA - FEB UNISBA", layout="wide")

# --- BAGIAN LOGO LOKAL ---
nama_file_logo = "logo_unisba.png" 

# Custom CSS Mobile Friendly
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stMetric { 
        background-color: #ffffff;
        padding: 10px; 
        border-radius: 10px; 
        border-top: 4px solid #1a3a5f; 
    }
    .explanation-box { 
        background-color: #ffffff; 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 5px solid #28a745; 
        margin: 10px 0px;
        font-size: 13px;
    }
    .identity-card {
        background-color: #1a3a5f;
        padding: 15px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
        font-size: 13px;
    }
    .param-card {
        background-color: #eef2f6;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #d1d9e0;
        margin-bottom: 10px;
        text-align: center;
        color: #1a3a5f;
        font-size: 12px;
    }
    h1 { font-size: 22px !important; color: #1a3a5f; }
    h2 { font-size: 18px !important; color: #1a3a5f; }
    h3 { font-size: 16px !important; color: #1a3a5f; }
    .footer {
        text-align: center;
        padding: 20px;
        color: #777;
        font-size: 11px;
    }
    /* Sembunyikan gambar logo di mobile jika terlalu besar */
    @media (max-width: 600px) {
        .identity-card table, .identity-card tr, .identity-card td {
            display: block;
            width: 100% !important;
            text-align: left !important;
            border-left: none !important;
            padding-left: 0 !important;
        }
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
df_h['Tahun'] = df_h['Tahun'].astype(str)

tahun_proyeksi = [2025, 2026, 2027, 2028, 2029, 2030, 2031]
mc_presisi = [13.71, 15.50, 18.20, 22.00, 28.00, 38.00, 55.00] 

# --- 3. SIDEBAR ---
with st.sidebar:
    if os.path.exists(nama_file_logo):
        st.image(nama_file_logo, width=80)
    st.markdown("### ⚙️ Kontrol")
    harga_input = st.slider("Harga (P0) $", 40.0, 150.0, 71.8)
    r_rate = st.slider("Diskonto (r)", 0.01, 0.20, 0.05)
    muc_manual = st.slider("MUC Awal (λ0) $", 0.0, 100.0, float(harga_input - 13.71))
    pajak_gp = st.slider("Pajak Karbon ($)", 0, 100, 20)

# --- 4. PERHITUNGAN ---
stok_awal = 544714167.87
efek_supply_rush = (pajak_gp / 100) * 20000000 
faktor_ekstraksi = (r_rate / 0.05) * (harga_input / 71.8)
total_ekstraksi_tahunan = (75000000 + efek_supply_rush) * faktor_ekstraksi

stok_gp = []
curr_stok = stok_awal
for t in range(len(tahun_proyeksi)):
    stok_gp.append(max(0, curr_stok))
    curr_stok -= total_ekstraksi_tahunan

t_idx = np.arange(len(tahun_proyeksi))
muc_t = muc_manual * np.exp(r_rate * t_idx)
p_t = np.array(mc_presisi) + muc_t + (pajak_gp * (t_idx / 6))

# --- 5. HEADER ---
col_head1, col_head2 = st.columns([1, 4])
with col_head1:
    if os.path.exists(nama_file_logo):
        st.image(nama_file_logo, width=80)
with col_head2:
    st.markdown("<h1 style='margin:0;'>Dashboard Ekonomi SDA</h1>", unsafe_allow_html=True)
    st.caption("PT Bumi Resources Tbk | FEB UNISBA")

# --- 6. PANEL ANGGOTA (Mobile Optimized) ---
st.markdown(f"""
<div class="identity-card">
    <b>KELOMPOK PBL 3:</b><br>
    1. Ina Rani Amelia (002)<br>
    2. Nayla Dwi Safitri (007)<br>
    3. Celi Maulidi Aprilia (027)<br>
    <hr style="opacity:0.2; margin:10px 0;">
    <b>DOSEN:</b> Yuhka Sundaya, S.E., M.Si.
</div>
""", unsafe_allow_html=True)

# --- PANEL PARAMETER DASAR ---
st.markdown("### 📍 Parameter Utama")
c_p1, c_p2 = st.columns(2) # Pecah jadi 2 kolom agar tidak terlalu sempit di HP
with c_p1:
    st.markdown(f"<div class='param-card'><b>Harga (P0):</b><br>${harga_input:.2f}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='param-card'><b>MUC (λ0):</b><br>${muc_manual:.2f}</div>", unsafe_allow_html=True)
with c_p2:
    st.markdown(f"<div class='param-card'><b>MC0:</b><br>$13.71</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='param-card'><b>Bunga (r):</b><br>{r_rate*100:.0f}%</div>", unsafe_allow_html=True)

# --- 7. TABS UTAMA ---
tabs = st.tabs(["📊 Data", "📈 Hotelling", "🏛️ Pasar", "📦 Stok", "🌿 Green Paradox"])

with tabs[0]:
    st.markdown("### Data Historis")
    st.dataframe(df_h, use_container_width=True)
    fig_h, ax_h = plt.subplots(figsize=(6, 3))
    ax_h.plot(df_h['Tahun'], df_h['Harga Batu Bara (P)'], marker='o', color='#1a3a5f')
    st.pyplot(fig_h)

with tabs[1]:
    st.markdown("### Proyeksi Hotelling")
    df_res = pd.DataFrame({'Tahun': [str(t) for t in tahun_proyeksi], 'MUC': muc_t, 'Harga': p_t})
    st.dataframe(df_res.style.format({'MUC': '{:,.2f}', 'Harga': '{:,.2f}'}), use_container_width=True)
    fig_ht, ax_ht = plt.subplots(figsize=(6, 3))
    ax_ht.plot(tahun_proyeksi, p_t, label='Harga', color='green')
    ax_ht.plot(tahun_proyeksi, muc_t, label='MUC', color='blue', linestyle='--')
    ax_ht.legend(fontsize='small')
    st.pyplot(fig_ht)

with tabs[2]:
    st.markdown("### Struktur Pasar")
    st.caption("Klik grafik untuk memperbesar")
    st.line_chart(muc_t)

with tabs[3]:
    st.markdown("### Simulasi Stok")
    fig_stok, ax_stok = plt.subplots(figsize=(6, 3))
    ax_stok.bar([str(t) for t in tahun_proyeksi], stok_gp, color='#28a745')
    st.pyplot(fig_stok)
    st.dataframe(pd.DataFrame({'Tahun': tahun_proyeksi, 'Sisa Stok': stok_gp}), use_container_width=True)

with tabs[4]:
    st.markdown("### Green Paradox")
    st.markdown(f"<div class='explanation-box'>Pajak Karbon Future: <b>${pajak_gp}</b> memicu percepatan ekstraksi.</div>", unsafe_allow_html=True)
    fig_gp, ax1 = plt.subplots(figsize=(7, 4))
    ax1.bar([str(t) for t in tahun_proyeksi], stok_gp, color='gray', alpha=0.2)
    ax2 = ax1.twinx()
    ax2.plot([str(t) for t in tahun_proyeksi], muc_t, color='blue', marker='o')
    ax2.plot([str(t) for t in tahun_proyeksi], p_t, color='red', marker='x')
    st.pyplot(fig_gp)

st.markdown("<div class='footer'>Dashboard PBL 3 | FEB UNISBA | 2026</div>", unsafe_allow_html=True)

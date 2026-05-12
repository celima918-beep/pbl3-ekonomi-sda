import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Dashboard Ekonomi SDA - FEB UNISBA", layout="wide")

# --- BAGIAN LOGO LOKAL ---
nama_file_logo = "logo_unisba.png" 

# Custom CSS
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
        border-left: 5px solid #2d5a88; 
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

# LOGIKA DINAMIS UNTUK STOK (Ekstraksi bereaksi terhadap r dan P)
stok_awal = 544714167.87
laju_ekstraksi_dasar = 80000000 # Rata-rata produksi tahunan

# Faktor percepatan: jika r naik atau P naik, ekstraksi bertambah
faktor_akselerasi = (r_rate / 0.05) * (harga_input / 71.8)
ekstraksi_tahunan = laju_ekstraksi_dasar * faktor_akselerasi

stok_dinamis = []
current_stok = stok_awal
for t in range(len(tahun_proyeksi)):
    stok_dinamis.append(max(0, current_stok))
    current_stok -= ekstraksi_tahunan

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
    st.markdown(f"<div class='param-card'><b>Biaya Marginal (MC0):</b><br>${mc_awal}</div>", unsafe_allow_html=True)
with c_p3:
    st.markdown(f"<div class='param-card'><b>MUC Awal (λ0):</b><br>${muc_awal_dinamis:.2f}</div>", unsafe_allow_html=True)
with c_p4:
    st.markdown(f"<div class='param-card'><b>Suku Bunga (r):</b><br>{r_rate*100:.0f}%</div>", unsafe_allow_html=True)

# --- 8. BAGIAN I: DATA HISTORIS & CADANGAN DINAMIS ---
st.divider()
st.header("I. Tinjauan Data Historis & Cadangan")
tab1, tab2 = st.tabs(["📊 Tabel & Grafik Harga", "📉 Proyeksi Deplesi Stok (Dinamis)"])

with tab1:
    c1, c2 = st.columns([2, 3])
    with c1: 
        st.write("**Data Historis 2018-2024**")
        st.dataframe(df_h, use_container_width=True)
    with c2:
        fig_h, ax_h = plt.subplots(figsize=(8, 4.2), facecolor='#f4f7f9')
        ax_h.plot(df_h['Tahun'], df_h['Harga Batu Bara (P)'], marker='o', color='#1a3a5f', linewidth=2.5)
        ax_h.set_title("Fluktuasi Harga Pasar", fontsize=10, fontweight='bold')
        ax_h.set_xlabel("Tahun"); ax_h.set_ylabel("Harga ($/Ton)")
        st.pyplot(fig_h)

with tab2:
    c3, c4 = st.columns([2, 3])
    df_s = pd.DataFrame({'Tahun': tahun_proyeksi, 'Sisa Stok': stok_dinamis})
    with c3: 
        st.write("**Estimasi Sisa Cadangan (Responsif terhadap Parameter)**")
        st.dataframe(df_s.style.format({'Sisa Stok': '{:,.0f}'}), use_container_width=True)
    with c4:
        fig_s, ax_s = plt.subplots(figsize=(8, 4.2), facecolor='#f4f7f9')
        ax_s.bar(df_s['Tahun'], df_s['Sisa Stok'], color='#2d5a88', alpha=0.8)
        ax_s.set_title("Laju Penurunan Stok Fisik", fontsize=10, fontweight='bold')
        ax_s.set_xlabel("Tahun Proyeksi"); ax_s.set_ylabel("Volume (Ton)")
        st.pyplot(fig_s)
        st.info("💡 Grafik di atas akan turun lebih curam jika Harga atau Suku Bunga dinaikkan (Supply Rush).")

# --- 9. BAGIAN II: ANALISIS HOTTELLING ---
st.divider()
st.header("II. Model Alokasi Intertemporal (Hotelling)")

t_idx = np.arange(0, len(tahun_proyeksi))
muc_t = muc_awal_dinamis * np.exp(r_rate * t_idx)
p_t = np.array(mc_presisi) + muc_t

df_est = pd.DataFrame({
    'Tahun': tahun_proyeksi,
    'MC (Biaya)': mc_presisi,
    'MUC (Kelangkaan)': muc_t,
    'Harga Proyeksi': p_t
})

st.dataframe(df_est.style.format('{:,.2f}'), use_container_width=True)

cg1, cg2 = st.columns(2)
with cg1:
    fig_p, ax_p = plt.subplots(figsize=(6, 4), facecolor='#f4f7f9')
    ax_p.plot(tahun_proyeksi, p_t, label='Harga Proyeksi', color='#1e7e34', linewidth=2)
    ax_p.plot(tahun_proyeksi, mc_presisi, label='Biaya (MC)', color='#bd2130', linestyle='--')
    ax_p.set_title("Keseimbangan Harga & Biaya", fontweight='bold')
    ax_p.set_xlabel("Tahun"); ax_p.set_ylabel("Nilai ($)")
    ax_p.legend(); st.pyplot(fig_p)

with cg2:
    fig_m, ax_m = plt.subplots(figsize=(6, 4), facecolor='#f4f7f9')
    ax_m.fill_between(tahun_proyeksi, muc_t, color='#1a3a5f', alpha=0.1)
    ax_m.plot(tahun_proyeksi, muc_t, color='#1a3a5f', marker='o')
    ax_m.set_title("Pertumbuhan Rente Kelangkaan (MUC)", fontweight='bold')
    ax_m.set_xlabel("Tahun"); ax_m.set_ylabel("MUC ($)")
    st.pyplot(fig_m)

# --- 10. BAGIAN III: STRUKTUR PASAR ---
st.divider()
st.header("III. Perbandingan Strategi Struktur Pasar")
sp1, sp2, sp3 = st.columns(3)

with sp1:
    st.markdown("🔍 **Persaingan Sempurna**")
    st.line_chart(muc_t)
    st.caption("MUC tumbuh proporsional dengan r.")
with sp2:
    st.markdown("🔒 **Monopoli**")
    muc_m = muc_awal_dinamis * 1.4 * np.exp((r_rate/2) * t_idx)
    st.line_chart(muc_m)
    st.caption("Produksi ditahan untuk harga tinggi.")
with sp3:
    st.markdown("🤝 **Oligopoli**")
    muc_o = muc_awal_dinamis * 1.1 * np.exp((r_rate/1.2) * t_idx)
    st.line_chart(muc_o)
    st.caption("Interaksi strategis produsen.")

# --- 11. BAGIAN IV: GREEN PARADOX ---
st.divider()
st.header("IV. Simulasi Dampak Green Paradox")
cgp1, cgp2 = st.columns([2, 1])
with cgp1:
    st.markdown(f"<div class='explanation-box'><b>Analisis Pajak Karbon (${pajak_gp}):</b><br>Regulasi masa depan memicu <i>Supply Rush</i> atau percepatan ekstraksi hari ini untuk menghindari beban biaya pajak nantinya.</div>", unsafe_allow_html=True)
with cgp2:
    if pajak_gp > 35: st.warning("⚠️ Potensi Supply Rush Tinggi")
    else: st.success("✅ Dampak Regulasi Stabil")

st.divider()
st.markdown("<div class='footer'>Dashboard Analisis Ekonomi SDA | PBL 3 | FEB UNISBA | 2026</div>", unsafe_allow_html=True)

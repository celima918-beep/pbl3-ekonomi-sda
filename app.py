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
        text-align: center;
        color: #1a3a5f;
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
df_h['Tahun'] = df_h['Tahun'].astype(str)

tahun_proyeksi = [2025, 2026, 2027, 2028, 2029, 2030, 2031]
mc_presisi = [13.71, 15.50, 18.20, 22.00, 28.00, 38.00, 55.00] 

# --- 3. SIDEBAR (KONTROL SIMULASI) ---
with st.sidebar:
    if os.path.exists(nama_file_logo):
        st.image(nama_file_logo, width=100)
    st.markdown("### ⚙️ Kontrol Simulasi")
    
    harga_input = st.slider("Harga Batu Bara (P0) $", 40.0, 150.0, 71.8)
    r_rate = st.slider("Tingkat Diskonto (r)", 0.01, 0.20, 0.05)
    
    mc_awal_konst = 13.71
    default_muc = harga_input - mc_awal_konst
    muc_manual = st.slider("MUC Awal (λ0) $", 0.0, 100.0, float(default_muc))
    
    pajak_gp = st.slider("Pajak Karbon Future ($)", 0, 100, 20)
    
    st.divider()
    st.caption("FEB UNISBA | Ekonomi SDA")

# --- 4. PERHITUNGAN DINAMIS ---
stok_awal = 544714167.87
laju_ekstraksi_base = 75000000 
efek_supply_rush = (pajak_gp / 100) * 20000000 
faktor_ekstraksi = (r_rate / 0.05) * (harga_input / 71.8)
total_ekstraksi_tahunan = (laju_ekstraksi_base + efek_supply_rush) * faktor_ekstraksi

stok_gp = []
curr_stok = stok_awal
for t in range(len(tahun_proyeksi)):
    stok_gp.append(max(0, curr_stok))
    curr_stok -= total_ekstraksi_tahunan

t_idx = np.arange(len(tahun_proyeksi))
muc_t = muc_manual * np.exp(r_rate * t_idx)
p_t = np.array(mc_presisi) + muc_t + (pajak_gp * (t_idx / max(t_idx)))

# --- 5. HEADER ---
col_l, col_j = st.columns([1, 6])
with col_l:
    if os.path.exists(nama_file_logo):
        st.image(nama_file_logo, width=120)
with col_j:
    st.markdown("<h1 style='margin-bottom: 0;'>Analisis Intertemporal Sumber Daya Batu Bara</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top: 0; color: #555; font-weight: normal;'>PT Bumi Resources Tbk</h3>", unsafe_allow_html=True)

# --- 6. PANEL ANGGOTA ---
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

# --- PANEL PARAMETER DASAR (KEMBALI) ---
st.subheader("📍 Parameter Dasar Analisis (T=0)")
c_p1, c_p2, c_p3, c_p4 = st.columns(4)
with c_p1:
    st.markdown(f"<div class='param-card'><b>Harga Pasar (P0):</b><br>${harga_input:.2f}</div>", unsafe_allow_html=True)
with c_p2:
    st.markdown(f"<div class='param-card'><b>Biaya Marginal (MC0):</b><br>${mc_awal_konst}</div>", unsafe_allow_html=True)
with c_p3:
    st.markdown(f"<div class='param-card'><b>MUC Awal (λ0):</b><br>${muc_manual:.2f}</div>", unsafe_allow_html=True)
with c_p4:
    st.markdown(f"<div class='param-card'><b>Suku Bunga (r):</b><br>{r_rate*100:.0f}%</div>", unsafe_allow_html=True)

# --- 7. TABS UTAMA ---
tabs = st.tabs(["📊 Data & Cadangan", "📈 Analisis Hotelling", "🏛️ Struktur Pasar", "📦 Simulasi Stok", "🌿 Green Paradox"])

with tabs[0]:
    st.subheader("Data Historis Produksi & Harga")
    c_h1, c_h2 = st.columns([2, 3])
    with c_h1:
        st.dataframe(df_h, use_container_width=True)
    with c_h2:
        fig_h, ax_h = plt.subplots(figsize=(8, 4))
        ax_h.plot(df_h['Tahun'], df_h['Harga Batu Bara (P)'], marker='o', color='#1a3a5f')
        ax_h.set_title("Tren Harga Historis (2018-2024)")
        st.pyplot(fig_h)

with tabs[1]:
    st.subheader("Model Optimasi Hotelling")
    col_hot1, col_hot2 = st.columns([2, 3])
    with col_hot1:
        st.write("**Tabel Proyeksi Harga & MUC**")
        df_res = pd.DataFrame({
            'Tahun': [str(t) for t in tahun_proyeksi], 
            'MUC ($)': muc_t, 
            'Harga ($)': p_t
        })
        st.dataframe(df_res.style.format({'MUC ($)': '{:,.2f}', 'Harga ($)': '{:,.2f}'}), use_container_width=True)
    with col_hot2:
        fig_ht, ax_ht = plt.subplots(figsize=(10, 5))
        ax_ht.plot(tahun_proyeksi, p_t, label='Harga Proyeksi', color='green', marker='s')
        ax_ht.plot(tahun_proyeksi, muc_t, label='MUC (Rente Kelangkaan)', color='blue', linestyle='--')
        ax_ht.set_title("Keseimbangan Nilai Intertemporal")
        ax_ht.legend()
        st.pyplot(fig_ht)

with tabs[2]:
    st.header("Analisis Struktur Pasar")
    col_sp1, col_sp2, col_sp3 = st.columns(3)
    muc_ps = muc_t 
    muc_mono = muc_manual * 1.5 * np.exp((r_rate * 0.7) * t_idx)
    muc_oligo = muc_manual * 1.2 * np.exp((r_rate * 0.9) * t_idx)
    with col_sp1:
        st.markdown("### 🔍 Persaingan Sempurna")
        st.line_chart(muc_ps)
    with col_sp2:
        st.markdown("### 🔒 Monopoli")
        st.line_chart(muc_mono)
    with col_sp3:
        st.markdown("### 🤝 Oligopoli")
        st.line_chart(muc_oligo)

with tabs[3]:
    st.header("Simulasi Deplesi Stok Cadangan")
    st.markdown("<div class='explanation-box'>Visualisasi laju deplesi stok cadangan fisik batu bara.</div>", unsafe_allow_html=True)
    
    col_st1, col_st2 = st.columns([3, 2])
    with col_st1:
        fig_stok, ax_stok = plt.subplots(figsize=(10, 5))
        ax_stok.bar([str(t) for t in tahun_proyeksi], stok_gp, color='#28a745', alpha=0.7)
        ax_stok.set_title("Proyeksi Sisa Cadangan (Ton)")
        ax_stok.set_ylabel("Ton")
        st.pyplot(fig_stok)
    
    with col_st2:
        st.write("**Data Stok Per Tahun**")
        df_stok_only = pd.DataFrame({
            'Tahun': [str(t) for t in tahun_proyeksi],
            'Sisa Stok (Ton)': stok_gp
        })
        st.dataframe(df_stok_only.style.format({'Sisa Stok (Ton)': '{:,.0f}'}), use_container_width=True)

with tabs[4]:
    st.header("Analisis Green Paradox")
    st.markdown(f"""<div class='explanation-box'><b>Analisis:</b> Pajak karbon sebesar <b>${pajak_gp}</b> memicu percepatan ekstraksi (Supply Rush) 
    sebelum kebijakan berlaku penuh untuk menghindari hilangnya rente di masa depan.</div>""", unsafe_allow_html=True)

    fig_gp, ax1 = plt.subplots(figsize=(12, 6), facecolor='#f4f7f9')
    ax1.bar([str(t) for t in tahun_proyeksi], stok_gp, color='gray', alpha=0.2, label='Deplesi Stok')
    ax1.set_ylabel('Volume Cadangan (Ton)', color='gray')
    
    ax2 = ax1.twinx()
    ax2.plot([str(t) for t in tahun_proyeksi], muc_t, color='blue', marker='o', label='MUC (λ)')
    ax2.plot([str(t) for t in tahun_proyeksi], p_t, color='red', marker='x', label='Harga Proyeksi')
    ax2.set_ylabel('Nilai Moneter ($)', color='#1a3a5f')
    
    plt.title("Korelasi Stok vs Nilai Moneter (Efek Green Paradox)", fontweight='bold')
    ax1.legend(loc='upper left'); ax2.legend(loc='upper right')
    st.pyplot(fig_gp)

st.divider()
st.markdown("<div class='footer'>Dashboard Analisis Ekonomi SDA | PBL 3 | FEB UNISBA | 2026</div>", unsafe_allow_html=True)

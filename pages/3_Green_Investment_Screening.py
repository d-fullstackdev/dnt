"""
CELIOS — Tahap 3: Skrining Taksonomi & Green Investment List
Menerapkan Graphic 1 Workflow dan Kriteria Skrining 3-Gate
Sesuai Dokumen Metodologi Riset CELIOS (brief-20260831_Methodological Approach.md).
"""

import streamlit as st
import os
import sys
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.components.sidebar import render_sidebar
from src.utils.styling import get_danantara_css

st.set_page_config(
    page_title="CELIOS — Skrining Taksonomi & Green List",
    page_icon="assets/celios_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar()
st.markdown(get_danantara_css(), unsafe_allow_html=True)

# ─── DATA LOADING (FINAL GREEN LIST) ──────────────────────────────────────────
FINAL_LIST_PATH = PROJECT_ROOT / "data" / "processed" / "green_investment_list.csv"

if FINAL_LIST_PATH.exists():
    df_green_list = pd.read_csv(FINAL_LIST_PATH)
else:
    # Kerangka Schema Kosong Green Investment List
    columns_green_list = [
        "project_id",
        "project_name",
        "soe_champion",
        "sector",
        "capacity",
        "investment_capex",
        "gate1_negative_filter",
        "gate2_tkbi_alignment",
        "gate3_norfund_additionality",
        "qualification_status",
        "danantara_role"
    ]
    df_green_list = pd.DataFrame(columns=columns_green_list)

total_qualified = len(df_green_list)

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown('<div class="org-badge">CELIOS — CENTER OF ECONOMIC AND LAW STUDIES</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Skrining Taksonomi & Green Investment List</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Tahap 3: Uji 3-Gate (Negative List, TKBI v3 / ASEAN v4, Norfund Additionality) & Pembentukan Portofolio Final Danantara</div>',
    unsafe_allow_html=True
)

# ─── DROPDOWN METODOLOGI (ACCORDION EXPANDER) ─────────────────────────────────
with st.expander("Metodologi Skrining: Graphic 1 Workflow, Kriteria Eksklusi & Prinsip Norfund Additionality", expanded=True):
    st.markdown("""
    **Alur Kerja Resmi Graphic 1** (<code>brief-20260831_Methodological Approach.md</code> baris 37–60):<br>
    
    1. <strong>Create Inventory:</strong> Memetakan seluruh inventaris proyek hijau BUMN (sejak 2020) dan proyek yang dikonfirmasi Danantara (sejak 2025).<br>
    2. <strong>Sort into Six Sectors:</strong> Mengelompokkan aktivitas ke dalam 6 sektor utama (Energy, Agriculture, Downstream industries, Housing, Infrastructure, Manufacturing).<br>
    3. <strong>Screen Projects using Universally Agreed Principles (Uji 3-Gate):</strong><br>
       * <strong>Gate 1 (Negative Filter / Eksklusi Mutlak):</strong> Proyek geothermal (kecuali untuk penghentian unit fosil), tenaga nuklir, dan coal repurposing / "green coal" <em>langsung dieliminasi secara otomatis</em>.<br>
       * <strong>Gate 2 (Kepatuhan Taksonomi Hijau):</strong> Uji keselarasan teknis dengan Taksonomi Keuangan Berkelanjutan Indonesia (TKBI Versi 3) dan ASEAN Taxonomy for Sustainable Finance (Versi 4), serta komitmen NDC 2030, Net Zero, FOLU Net Sink 2030, dan JETP.<br>
       * <strong>Gate 3 (Prinsip Norfund Additionality):</strong> Memastikan modal negara Danantara menghasilkan transformasi publik dan ekonomi yang tidak dapat diwujudkan oleh mekanisme pasar biasa (mencegah Danantara sekadar menjadi alokator aset pada proyek yang sudah bankable).<br>
    4. <strong>Compare with Danantara's Existing Portfolio:</strong> Menguji keselarasan dengan mandat investasi dan portofolio Danantara 2025.<br>
    5. <strong>Build Green Investment List:</strong> Menghasilkan daftar final proyek hijau kredibel yang direkomendasikan untuk pendanaan strategis.
    """, unsafe_allow_html=True)

# ─── STATUS BANNER ────────────────────────────────────────────────────────────
st.markdown("""
<div class="note-box">
<strong>Status Pengerjaan: Menunggu Hasil Ekstraksi Proyek (Tahap 2)</strong><br>
Penyaringan 3-Gate dan pembentukan daftar final Green Investment List akan dieksekusi segera setelah database 13 atribut inventaris proyek pada Tahap 2 selesai diekstrak dari korpus dokumen bukti.
</div>
""", unsafe_allow_html=True)

# ─── HERO METRIC CARDS (SKELETON) ─────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Lolos Gate 1: Negative Filter</div>
        <div class="metric-value">0 Proyek</div>
        <div class="metric-desc">Eksklusi Batu Bara, Geothermal, Nuklir</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Lolos Gate 2: TKBI v3 / ASEAN v4</div>
        <div class="metric-value">0 Proyek</div>
        <div class="metric-desc">Kesesuaian Taksonomi Berkelanjutan</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Lolos Gate 3: Norfund Additionality</div>
        <div class="metric-value">0 Proyek</div>
        <div class="metric-desc">Uji Peran Modal Katalis Danantara</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Final Green Investment List</div>
        <div class="metric-value">{total_qualified:,} Proyek</div>
        <div class="metric-desc">Proyek Hijau Siap Portofolio Danantara</div>
    </div>
    """, unsafe_allow_html=True)

# ─── VISUALISASI ALUR KERJA GRAPHIC 1 ─────────────────────────────────────────
st.markdown('<div class="section-header">Visualisasi Alur Keputusan Metodologi (Graphic 1 Workflow)</div>', unsafe_allow_html=True)

flow_col1, flow_col2, flow_col3, flow_col4, flow_col5 = st.columns(5)

with flow_col1:
    st.markdown("""
    <div class="metric-card" style="text-align: left; padding: 1rem;">
        <div style="font-size: 0.72rem; color: #66BB6A; font-weight: 700;">LANGKAH 1</div>
        <div style="font-weight: 700; color: #ECEFF1; font-size: 0.88rem; margin: 4px 0;">Create Inventory</div>
        <div style="font-size: 0.75rem; color: #9E9E9E;">Inventaris Proyek BUMN 2020+ & Danantara 2025+</div>
    </div>
    """, unsafe_allow_html=True)

with flow_col2:
    st.markdown("""
    <div class="metric-card" style="text-align: left; padding: 1rem;">
        <div style="font-size: 0.72rem; color: #66BB6A; font-weight: 700;">LANGKAH 2</div>
        <div style="font-weight: 700; color: #ECEFF1; font-size: 0.88rem; margin: 4px 0;">Sort Six Sectors</div>
        <div style="font-size: 0.75rem; color: #9E9E9E;">Energy, Agri, Downstream, Housing, Infra, Mfg</div>
    </div>
    """, unsafe_allow_html=True)

with flow_col3:
    st.markdown("""
    <div class="metric-card" style="text-align: left; padding: 1rem;">
        <div style="font-size: 0.72rem; color: #66BB6A; font-weight: 700;">LANGKAH 3</div>
        <div style="font-weight: 700; color: #ECEFF1; font-size: 0.88rem; margin: 4px 0;">Screening 3-Gate</div>
        <div style="font-size: 0.75rem; color: #9E9E9E;">Negative Filter, TKBI v3, Norfund Additionality</div>
    </div>
    """, unsafe_allow_html=True)

with flow_col4:
    st.markdown("""
    <div class="metric-card" style="text-align: left; padding: 1rem;">
        <div style="font-size: 0.72rem; color: #66BB6A; font-weight: 700;">LANGKAH 4</div>
        <div style="font-weight: 700; color: #ECEFF1; font-size: 0.88rem; margin: 4px 0;">Compare Danantara</div>
        <div style="font-size: 0.75rem; color: #9E9E9E;">Kesesuaian Portofolio Eksisting Danantara</div>
    </div>
    """, unsafe_allow_html=True)

with flow_col5:
    st.markdown("""
    <div class="metric-card" style="text-align: left; padding: 1rem; border-color: #2E7D32;">
        <div style="font-size: 0.72rem; color: #66BB6A; font-weight: 700;">LANGKAH 5</div>
        <div style="font-weight: 700; color: #66BB6A; font-size: 0.88rem; margin: 4px 0;">Green Investment List</div>
        <div style="font-size: 0.75rem; color: #ECEFF1;">Daftar Final Proyek Hijau Terkualifikasi</div>
    </div>
    """, unsafe_allow_html=True)

# ─── TABEL FINAL GREEN INVESTMENT LIST ────────────────────────────────────────
st.markdown('<div class="section-header">Daftar Final Green Investment List Terkualifikasi</div>', unsafe_allow_html=True)

if df_green_list.empty:
    st.info("Tabel Green Investment List final akan otomatis terpopulasi setelah seluruh proyek melalui gerbang skrining Taksonomi Hijau dan Additionality.")
    st.dataframe(
        df_green_list,
        use_container_width=True,
        column_config={
            "project_id": st.column_config.TextColumn("ID Proyek", width="small"),
            "project_name": st.column_config.TextColumn("Nama Proyek Hijau", width="large"),
            "soe_champion": st.column_config.TextColumn("BUMN Pelaksana", width="medium"),
            "sector": st.column_config.TextColumn("Sektor", width="small"),
            "capacity": st.column_config.TextColumn("Kapasitas", width="small"),
            "investment_capex": st.column_config.TextColumn("Nilai Capex", width="medium"),
            "gate1_negative_filter": st.column_config.TextColumn("Gate 1: Negative Filter", width="medium"),
            "gate2_tkbi_alignment": st.column_config.TextColumn("Gate 2: TKBI Alignment", width="medium"),
            "gate3_norfund_additionality": st.column_config.TextColumn("Gate 3: Norfund Additionality", width="medium"),
            "qualification_status": st.column_config.TextColumn("Status Kelayakan", width="small"),
            "danantara_role": st.column_config.TextColumn("Rekomendasi Peran Danantara", width="large")
        },
        hide_index=True
    )
else:
    st.dataframe(df_green_list, use_container_width=True, hide_index=True)

"""
CELIOS — Tahap 2: ETL & Ekstraksi 13 Atribut Proyek
Sesuai Dokumen Metodologi Riset CELIOS (brief-20260831_Methodological Approach.md)
Bagian 'Inventory of Green Projects' (13 Kolom Informasi Proyek).
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
    page_title="CELIOS — ETL & Ekstraksi 13 Atribut",
    page_icon="assets/celios_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar()
st.markdown(get_danantara_css(), unsafe_allow_html=True)

# ─── DATA LOADING (PROCESSED INVENTORY) ─────────────────────────────────────────
INVENTORY_PATH = PROJECT_ROOT / "data" / "processed" / "green_projects_inventory.csv"
HTML_DIR = PROJECT_ROOT / "data" / "raw" / "evidence_dorking" / "html"

total_html_files = len(os.listdir(HTML_DIR)) if HTML_DIR.exists() else 0

if INVENTORY_PATH.exists():
    df_inventory = pd.read_csv(INVENTORY_PATH)
else:
    # Kerangka Schema Kosong (13 Kolom Verbatim dari Brief CELIOS)
    columns_13 = [
        "project_name",
        "soe_name",
        "subsidiary_or_spv",
        "sector",
        "project_status",
        "location",
        "capacity_denomination",
        "investment_amount_currency",
        "funding_source",
        "partners",
        "emission_reduction_target",
        "environment_social_risks",
        "announcement_or_latest_date"
    ]
    df_inventory = pd.DataFrame(columns=columns_13)

total_extracted = len(df_inventory)

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown('<div class="org-badge">CELIOS — CENTER OF ECONOMIC AND LAW STUDIES</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">ETL & Ekstraksi 13 Atribut Proyek</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Tahap 2: Transformasi Teks Berita ke Database Inventaris Proyek BUMN (Graphic 1: Create Inventory of Green Projects)</div>',
    unsafe_allow_html=True
)

# ─── DROPDOWN METODOLOGI (ACCORDION EXPANDER) ─────────────────────────────────
with st.expander("Metodologi Ekstraksi: Standar 13 Atribut Proyek Sesuai Brief Riset CELIOS", expanded=True):
    st.markdown("""
    **Rujukan Verbatim Dokumen Riset CELIOS** (<code>brief-20260831_Methodological Approach.md</code> baris 64–80):<br>
    <em>"Writers scrape publicly available data on green projects by Indonesian state-owned enterprises (SOEs) to extract information, including:</em><br>
    1. <strong>Project name:</strong> Nama resmi proyek dekarbonisasi / energi terbarukan.<br>
    2. <strong>The name of the SOE:</strong> Nama induk BUMN (PLN, Pertamina, MIND ID, Semen Indonesia, dll.).<br>
    3. <strong>The name of the SOE subsidiary or SPV:</strong> Nama anak perusahaan operasional atau SPV proyek.<br>
    4. <strong>Sector:</strong> Klasifikasi ke dalam 6 sektor utama (Energy, Agriculture, Downstream industries, Housing, Infrastructure, Manufacturing).<br>
    5. <strong>Project status:</strong> Status tahapan proyek (planning, studies, MoU, LoI, tender, construction, commissioning, operations).<br>
    6. <strong>Location:</strong> Lokasi geografis (Provinsi / Kabupaten / Wilayah Proyek).<br>
    7. <strong>Capacity, including its denomination:</strong> Besaran kapasitas teknis (misal: 145 MWac, 88 ton/bulan).<br>
    8. <strong>Investment amount, including its currency:</strong> Nilai capex proyek (misal: USD 1,2 Miliar, Rp 1,7 Triliun).<br>
    9. <strong>Funding source:</strong> Sumber pendanaan (APBN, obligasi hijau, JETP, sindikasi perbankan, ekuitas BUMN).<br>
    10. <strong>Partners:</strong> Mitra konsorsium domestik dan global.<br>
    11. <strong>Emission reduction target:</strong> Estimasi reduksi emisi gas rumah kaca (tCO2e/tahun).<br>
    12. <strong>Environment and social risks:</strong> Analisis potensi risiko lingkungan, hak masyarakat adat, dan tata kelola.<br>
    13. <strong>Announcement date / latest update date:</strong> Tanggal publikasi pengumuman atau pembaruan terakhir.
    """, unsafe_allow_html=True)

# ─── STATUS BANNER ────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="note-box">
<strong>Status Pengerjaan: Menunggu Eksekusi ETL (Phase 2)</strong><br>
Sebanyak <strong>{total_html_files:,} berkas HTML mentah</strong> di <code>data/raw/evidence_dorking/html/</code> telah siap di disk lokal. Script ETL (ekstraksi Markdown bersih + Information Extraction) akan memproses seluruh berkas teks untuk mengekstrak dan mempopulasikan 13 atribut di bawah ini ke dalam database inventaris.
</div>
""", unsafe_allow_html=True)

# ─── HERO METRIC CARDS (SKELETON) ─────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Proyek Terekstrak</div>
        <div class="metric-value">{total_extracted:,} Proyek</div>
        <div class="metric-desc">Status: Standby Eksekusi ETL</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Total Nilai Investasi (Capex)</div>
        <div class="metric-value">USD 0.0 M</div>
        <div class="metric-desc">Menunggu Agregasi Nilai Investasi</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Total Kapasitas Teridentifikasi</div>
        <div class="metric-value">0 MW</div>
        <div class="metric-desc">Menunggu Ekstraksi Kapasitas</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Klasifikasi Sektor</div>
        <div class="metric-value">6 Sektor</div>
        <div class="metric-desc">Energy, Agri, Downstream, Housing, Infra, Mfg</div>
    </div>
    """, unsafe_allow_html=True)

# ─── SKEMA TABEL INVENTARIS PROYEK ────────────────────────────────────────────
st.markdown('<div class="section-header">Skema Database Inventaris Proyek (13 Kolom Terverifikasi)</div>', unsafe_allow_html=True)

if df_inventory.empty:
    st.info("Tabel inventaris proyek siap dipopulasikan saat eksekusi Langkah 4 / Phase 2 (ETL) dijalankan.")
    
    # Tampilkan representasi struktur tabel kosong / contoh schema
    st.dataframe(
        df_inventory,
        use_container_width=True,
        column_config={
            "project_name": st.column_config.TextColumn("1. Nama Proyek", width="medium"),
            "soe_name": st.column_config.TextColumn("2. BUMN Induk", width="small"),
            "subsidiary_or_spv": st.column_config.TextColumn("3. Anak Perusahaan / SPV", width="medium"),
            "sector": st.column_config.TextColumn("4. Sektor (6 Sektor)", width="small"),
            "project_status": st.column_config.TextColumn("5. Status Proyek", width="small"),
            "location": st.column_config.TextColumn("6. Lokasi", width="small"),
            "capacity_denomination": st.column_config.TextColumn("7. Kapasitas & Satuan", width="small"),
            "investment_amount_currency": st.column_config.TextColumn("8. Nilai Investasi (Capex)", width="medium"),
            "funding_source": st.column_config.TextColumn("9. Sumber Pendanaan", width="medium"),
            "partners": st.column_config.TextColumn("10. Mitra Kerja", width="medium"),
            "emission_reduction_target": st.column_config.TextColumn("11. Target Reduksi Emisi", width="small"),
            "environment_social_risks": st.column_config.TextColumn("12. Risiko Lingkungan & Sosial", width="large"),
            "announcement_or_latest_date": st.column_config.TextColumn("13. Tanggal Publikasi", width="small")
        },
        hide_index=True
    )
else:
    st.dataframe(df_inventory, use_container_width=True, hide_index=True)

"""
CELIOS — Danantara Monitor (Track A: 2025 Onward)
Pemantauan Regulasi Resmi & Media Kredibel Terkait Danantara
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
    page_title="CELIOS — Track A: Danantara Monitor",
    page_icon="assets/celios_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar()
st.markdown(get_danantara_css(), unsafe_allow_html=True)

# ─── DATA LOADING ─────────────────────────────────────────────────────────────
MANIFEST_PATH = PROJECT_ROOT / "data" / "raw" / "evidence_dorking" / "master_urls_manifest.csv"
BOARD_PATH = PROJECT_ROOT / "data" / "processed" / "danantara_board_structure.csv"
SPV_PATH = PROJECT_ROOT / "data" / "processed" / "danantara_spv_clean.csv"

df_manifest = pd.read_csv(MANIFEST_PATH)
df_track_a = df_manifest[df_manifest["track"] == "TRACK_A_DANANTARA_MONITOR"].copy()
df_board = pd.read_csv(BOARD_PATH) if BOARD_PATH.exists() else pd.DataFrame()
df_spv = pd.read_csv(SPV_PATH) if SPV_PATH.exists() else pd.DataFrame()

total_track_a = len(df_track_a)
total_pub = df_track_a["publisher"].nunique()

st.markdown('<div class="page-title">Danantara Monitor (Track A)</div>', unsafe_allow_html=True)
st.markdown(f'<div class="page-subtitle">Pemantauan Regulasi Resmi dan Media Kredibel Terkait Danantara ({total_track_a:,} Artikel Terverifikasi)</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="note-box">
<strong>Fokus Pemantauan Track A (Tahun 2025 ke atas)</strong><br>
Sesuai rumusan verbatim dokumen metodologi riset Celios: <em>"and all projects confirmed by Danantara Indonesia since its launch in 2025."</em><br>
Fokus pada seluruh proyek, kesepakatan investasi, dan arah kebijakan yang dikonfirmasi langsung oleh Danantara sejak peluncuran resminya pada tahun 2025. Data dikurasi dari portal resmi pemerintah (jdih.setneg.go.id, peraturan.bpk.go.id), dan media arus utama nasional dan global.
</div>
""", unsafe_allow_html=True)

# ─── METRIC CARDS ─────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Artikel Terverifikasi</div>
        <div class="metric-value">{total_track_a:,}</div>
        <div class="metric-desc">Rentang Waktu: Tahun 2025 ke atas</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Target Aset Konsolidasi</div>
        <div class="metric-value">USD 600 Miliar</div>
        <div class="metric-desc">7 BUMN Tahap 1 + INA</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">SPV Resmi Terverifikasi</div>
        <div class="metric-value">9 Entitas</div>
        <div class="metric-desc">Wisma Danantara (Gatot Subroto)</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Media & Portal Regulator</div>
        <div class="metric-value">{total_pub}</div>
        <div class="metric-desc">Setneg, Kompas, CNBC, Bloomberg, dll.</div>
    </div>
    """, unsafe_allow_html=True)

# ─── TABS KONTEN TRACK A ──────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "Feed Berita & Regulasi",
    "Struktur Dewan & Pimpinan",
    "SPV Resmi Wisma Danantara",
    "7 BUMN Konsolidasi Tahap 1"
])

with tab1:
    st.markdown('<div class="section-header">Feed Berita dan Regulasi Terverifikasi</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns([1.5, 2])
    with c1:
        top_pubs = ["Semua Publisher"] + sorted(df_track_a["publisher"].dropna().unique().tolist())
        sel_p = st.selectbox("Filter Media / Publisher:", top_pubs, key="track_a_pub")
    with c2:
        search_kw = st.text_input("Cari Judul / Kata Kunci:", "", key="track_a_kw")
        
    df_filtered = df_track_a.copy()
    if sel_p != "Semua Publisher":
        df_filtered = df_filtered[df_filtered["publisher"] == sel_p]
    if search_kw.strip():
        q = search_kw.lower()
        df_filtered = df_filtered[
            df_filtered["title"].str.lower().str.contains(q, na=False) |
            df_filtered["publisher"].str.lower().str.contains(q, na=False)
        ]
        
    st.markdown(f"Menampilkan **{len(df_filtered):,}** artikel bukti:")
    
    st.dataframe(
        df_filtered[["evidence_id", "published_at", "publisher", "title", "url"]].head(100),
        use_container_width=True,
        column_config={
            "evidence_id": st.column_config.TextColumn("ID", width="small"),
            "published_at": st.column_config.TextColumn("Tanggal", width="small"),
            "publisher": st.column_config.TextColumn("Publisher", width="medium"),
            "title": st.column_config.TextColumn("Judul Berita", width="large"),
            "url": st.column_config.LinkColumn("Link Sumber", display_text="Buka Berita")
        },
        hide_index=True
    )

with tab2:
    st.markdown('<div class="section-header">Struktur Kepemimpinan BPI Danantara</div>', unsafe_allow_html=True)
    if not df_board.empty:
        st.dataframe(
            df_board,
            use_container_width=True,
            column_config={
                "position_tier": st.column_config.TextColumn("Tingkat", width="small"),
                "position_title": st.column_config.TextColumn("Jabatan", width="medium"),
                "name": st.column_config.TextColumn("Nama Pejabat", width="medium"),
                "appointed_date": st.column_config.TextColumn("Tanggal Pelantikan", width="small"),
                "legal_basis": st.column_config.TextColumn("Dasar Hukum", width="medium"),
                "background": st.column_config.TextColumn("Latar Belakang Karir", width="large"),
                "role_focus": st.column_config.TextColumn("Fokus Tugas", width="large"),
            },
            hide_index=True
        )
    else:
        st.info("Dataset struktur dewan BPI Danantara sedang dikompilasi.")

with tab3:
    st.markdown('<div class="section-header">9 Special Purpose Vehicles (SPV) Resmi Wisma Danantara</div>', unsafe_allow_html=True)
    st.markdown("""
    Berdasarkan data domisili hukum di Menara Mandiri / Wisma Danantara (Jl. Jend. Gatot Subroto Kav. 36-38, Jakarta Selatan), teridentifikasi 9 SPV yang menjadi organ operasional Danantara:
    """)
    if not df_spv.empty:
        st.dataframe(
            df_spv,
            use_container_width=True,
            column_config={
                "company_name": st.column_config.TextColumn("Nama SPV / Perusahaan", width="large"),
                "holding_group": st.column_config.TextColumn("Holding Induk", width="medium"),
                "domicile_address": st.column_config.TextColumn("Alamat Domisili", width="large"),
                "source": st.column_config.TextColumn("Sumber Legalitas", width="medium"),
                "verification_status": st.column_config.TextColumn("Status Verifikasi", width="medium"),
            },
            hide_index=True
        )

with tab4:
    st.markdown('<div class="section-header">7 BUMN Raksasa Konsolidasi Tahap Awal (USD 600 Miliar AUM)</div>', unsafe_allow_html=True)
    bumn_stage1 = [
        {"BUMN": "PT Bank Mandiri (Persero) Tbk", "Sektor": "Perbankan & Jasa Keuangan", "Aset Konsolidasi": "Rp 2.174 Triliun", "Peran Strategis": "Pembiayaan korporasi & sindikasi investasi"},
        {"BUMN": "PT Bank Rakyat Indonesia (Persero) Tbk", "Sektor": "Perbankan Mikro & UMKM", "Aset Konsolidasi": "Rp 1.965 Triliun", "Peran Strategis": "Inklusi keuangan & pendanaan rantai pasok lokal"},
        {"BUMN": "PT Perusahaan Listrik Negara (Persero)", "Sektor": "Ketenagalistrikan & Transisi Energi", "Aset Konsolidasi": "Rp 1.692 Triliun", "Peran Strategis": "Transisi EBT, transmisi hijau, pensiun PLTU"},
        {"BUMN": "PT Pertamina (Persero)", "Sektor": "Energi, Migas & Petrokimia", "Aset Konsolidasi": "Rp 1.412 Triliun", "Peran Strategis": "Dekarbonisasi kilang, biofuel, hidrogen, panas bumi"},
        {"BUMN": "PT Bank Negara Indonesia (Persero) Tbk", "Sektor": "Perbankan & Valas Global", "Aset Konsolidasi": "Rp 1.087 Triliun", "Peran Strategis": "Sindikasi investasi global & green bond internasional"},
        {"BUMN": "PT Telkom Indonesia (Persero) Tbk", "Sektor": "Telekomunikasi & Infrastruktur Digital", "Aset Konsolidasi": "Rp 287 Triliun", "Peran Strategis": "Green data center & digitalisasi rantai pasok"},
        {"BUMN": "MIND ID (Mining Industry Indonesia)", "Sektor": "Pertambangan & Mineral Kritis", "Aset Konsolidasi": "Rp 259 Triliun", "Peran Strategis": "Hilirisasi nikel/tembaga & rantai pasok baterai EV"}
    ]
    df_stage1 = pd.DataFrame(bumn_stage1)
    st.dataframe(df_stage1, use_container_width=True, hide_index=True)

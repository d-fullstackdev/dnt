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
    page_title="CELIOS — Danantara Monitor",
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
STAGE1_PATH = PROJECT_ROOT / "data" / "processed" / "danantara_stage1_bumn.csv"
LOG_PATH = PROJECT_ROOT / "data" / "raw" / "evidence_dorking" / "html_download_log.csv"

df_manifest = pd.read_csv(MANIFEST_PATH)
df_track_a = df_manifest[df_manifest["track"] == "TRACK_A_DANANTARA_MONITOR"].copy()
df_board = pd.read_csv(BOARD_PATH) if BOARD_PATH.exists() else pd.DataFrame()
df_spv = pd.read_csv(SPV_PATH) if SPV_PATH.exists() else pd.DataFrame()
df_stage1 = pd.read_csv(STAGE1_PATH) if STAGE1_PATH.exists() else pd.DataFrame()
df_log = pd.read_csv(LOG_PATH) if LOG_PATH.exists() else pd.DataFrame()

# Pemetaan URL Langsung Penerbit
url_map = {}
if not df_log.empty:
    for _, r in df_log.iterrows():
        canon = str(r.get("canonical_url", "")).strip()
        if canon and "news.google.com" not in canon:
            url_map[str(r["evidence_id"])] = canon
df_track_a["direct_url"] = df_track_a["evidence_id"].map(url_map).fillna(df_track_a["url"])

total_track_a = len(df_track_a)
total_pub = df_track_a["publisher"].nunique()

st.markdown('<div class="org-badge">CELIOS — Center of Economic and Law Studies</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Danantara Monitor</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">Pemantauan Regulasi Resmi dan Media Kredibel Terkait Danantara ({total_track_a:,} Artikel Terverifikasi)</div>', unsafe_allow_html=True)

# ─── DROPDOWN METODOLOGI (ACCORDION EXPANDER) ─────────────────────────────────
with st.expander("Metodologi & Batasan Rentang Waktu Danantara (Tahun 2025 ke atas)", expanded=False):
    st.markdown("""
    **Rujukan Dokumen Metodologi Riset CELIOS** (`brief-20260831_Methodological Approach.md` baris 37):
    > *"and all projects confirmed by Danantara Indonesia since its launch in 2025."*
    
    * **Batasan Waktu:** Fokus pada seluruh proyek, kesepakatan investasi, dan arah kebijakan yang dikonfirmasi langsung oleh Danantara sejak peluncuran resminya pada tahun 2025.
    * **Sumber Validasi:** Data dikurasi dari portal resmi pemerintah (`jdih.setneg.go.id`, `peraturan.bpk.go.id`, `danantaraindonesia.co.id`), dan media arus utama nasional serta global.
    * **Akses Tautan:** Seluruh tautan artikel dapat dibuka langsung ke media penerbit tanpa redirect Google News.
    """)

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

# ─── BAGIAN 1: FEED BERITA & REGULASI (LANGSUNG TAMPIL) ───────────────────────
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
    df_filtered[["evidence_id", "published_at", "publisher", "title", "direct_url"]].head(100),
    use_container_width=True,
    column_config={
        "evidence_id": st.column_config.TextColumn("ID", width="small"),
        "published_at": st.column_config.TextColumn("Tanggal", width="small"),
        "publisher": st.column_config.TextColumn("Publisher", width="medium"),
        "title": st.column_config.TextColumn("Judul Berita", width="large"),
        "direct_url": st.column_config.LinkColumn("Tautan Langsung Media", display_text="Buka Sumber Langsung")
    },
    hide_index=True
)

# ─── BAGIAN 2: STRUKTUR DEWAN & PIMPINAN (LANGSUNG TAMPIL) ─────────────────────
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

# ─── BAGIAN 3: 9 SPV RESMI (LANGSUNG TAMPIL) ──────────────────────────────────
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

# ─── BAGIAN 4: 7 BUMN KONSOLIDASI (LANGSUNG TAMPIL) ───────────────────────────
st.markdown('<div class="section-header">7 BUMN Raksasa Konsolidasi Tahap Awal (USD 600 Miliar AUM)</div>', unsafe_allow_html=True)

st.markdown("""
Berikut adalah rincian kutipan verbatim teks asli dari rilis media dan dokumen publikasi resmi yang menjadi rujukan angka **USD 600 Miliar AUM**:

**1. Katadata Databoks (6 November 2024)**  
> *"Dengan sumbangan ini, Danantara diperkirakan memiliki **aset kelolaan awal Rp9,4 ribu triliun atau sekitar US$600 miliar**. Prabowo juga menargetkan aset kelolaan Danantara akan berkembang hingga **US$982 miliar**, dan menjadi SWF terbesar ke-4 di dunia."*  
🔗 [Buka Artikel Asli Katadata Databoks](https://databoks.katadata.co.id/keuangan/statistik/672ae5b1821f7/daftar-bumn-yang-sumbang-aset-untuk-dikelola-danantara)

**2. The Jakarta Post (19 November 2024)**  
> *"...aims to consolidate state assets initially valued at **around $600 billion (Rp 9.48 quadrillion)**, from seven of the country’s largest state-owned enterprises (SOEs)."*  
🔗 [Buka Artikel Asli The Jakarta Post](https://www.thejakartapost.com/opinion/2024/11/19/analysis-soes-superholding-danantara-launch-delayed-uncertainty-looms)

**3. CNBC Indonesia (7 November 2024)**  
> *"Selain tujuh BUMN jumbo itu, Danantara juga akan menaungi Indonesia Investment Authority (INA)... Dengan demikian total asset under management (AUM) Danantara akan menjadi **Rp9.049 triliun atau sekitar US$571,6 miliar**."*  
🔗 [Buka Artikel Asli CNBC Indonesia](https://www.cnbcindonesia.com/market/20241107084846-17-586318/diumumkan-prabowo-ini-daftar-7-bumn-jumbo-di-bawah-danantara)

**4. Detik Finance (Februari 2025)**  
> *"Danantara menaungi 7 BUMN jumbo pada tahap awal yakni Bank Mandiri, BRI, BNI, PLN, Pertamina, Telkom Indonesia, dan MIND ID."*  
🔗 [Buka Artikel Asli Detik Finance](https://finance.detik.com/berita-ekonomi-bisnis/d-7792821/resmi-diluncurkan-danantara-kelola-7-bumn-ini-di-tahap-awal)

---
""")

if not df_stage1.empty:
    cols_to_show = ["bumn", "sektor", "aset_label", "peran_strategis", "sumber_resmi", "direct_url"]
    st.dataframe(
        df_stage1[cols_to_show],
        use_container_width=True,
        column_config={
            "bumn": st.column_config.TextColumn("BUMN", width="medium"),
            "sektor": st.column_config.TextColumn("Sektor", width="medium"),
            "aset_label": st.column_config.TextColumn("Aset Konsolidasi", width="small"),
            "peran_strategis": st.column_config.TextColumn("Peran Strategis", width="large"),
            "sumber_resmi": st.column_config.TextColumn("Dasar Verifikasi", width="medium"),
            "direct_url": st.column_config.LinkColumn("Tautan Sumber Asli", display_text="Buka Sumber Berita", width="medium"),
        },
        hide_index=True
    )
else:
    st.info("Dataset konsolidasi 7 BUMN tahap awal sedang dikompilasi.")

st.caption("CELIOS · Center of Economic and Law Studies · Danantara Project 2026")

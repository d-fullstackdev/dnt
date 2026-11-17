"""
CELIOS — Forensic Evidence Preservation & Audit Status
Penyimpanan Bukti Fisik HTML & Audit Eliminasi Batasan Waktu
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
    page_title="CELIOS — Forensic Evidence Status",
    page_icon="assets/celios_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar()
st.markdown(get_danantara_css(), unsafe_allow_html=True)

# ─── DATA LOADING ─────────────────────────────────────────────────────────────
MANIFEST_PATH = PROJECT_ROOT / "data" / "raw" / "evidence_dorking" / "master_urls_manifest.csv"
STAGE1_PATH = PROJECT_ROOT / "data" / "processed" / "danantara_stage1_bumn.csv"
LOG_PATH = PROJECT_ROOT / "data" / "raw" / "evidence_dorking" / "html_download_log.csv"
EXCLUDED_PATH = PROJECT_ROOT / "data" / "raw" / "evidence_dorking" / "urls_excluded_time_series.csv"
HTML_DIR = PROJECT_ROOT / "data" / "raw" / "evidence_dorking" / "html"

df_manifest = pd.read_csv(MANIFEST_PATH) if MANIFEST_PATH.exists() else pd.DataFrame()
df_stage1 = pd.read_csv(STAGE1_PATH) if STAGE1_PATH.exists() else pd.DataFrame()
df_log = pd.read_csv(LOG_PATH) if LOG_PATH.exists() else pd.DataFrame()
df_excluded = pd.read_csv(EXCLUDED_PATH) if EXCLUDED_PATH.exists() else pd.DataFrame()

total_manifest = len(df_manifest)
physical_files_count = len(os.listdir(HTML_DIR)) if HTML_DIR.exists() else 0
success_downloads = len(df_log[df_log["status"] == "SUCCESS"]) if not df_log.empty else 0
failed_downloads = len(df_log[df_log["status"] == "FAILED"]) if not df_log.empty else 0
total_excluded = len(df_excluded)

st.markdown('<div class="org-badge">CELIOS — CENTER OF ECONOMIC AND LAW STUDIES</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Bukti Forensik & HTML Fisik</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">Penyimpanan File Mentah HTML di Disk Lokal dan Verifikasi Batasan Waktu — {total_manifest:,} Target Bukti</div>', unsafe_allow_html=True)

# ─── DROPDOWN METODOLOGI (ACCORDION EXPANDER) ─────────────────────────────────
with st.expander("Standar Preservasi Forensik & Integritas Bukti Fisik", expanded=False):
    st.markdown(f"""
    **Standar Preservasi Forensik (Anti-Hardcoding & Zero Network Parsing)**<br>
    Sesuai prinsip integritas data penelitian:<br>
    1. **Bukti Fisik Utuh:** Setiap artikel yang dikurasi diunduh utuh sebagai berkas HTML di <code>data/raw/evidence_dorking/html/</code> sebelum ekstraksi teks dimulai.<br>
    2. **Audit Batasan Waktu:** Sebanyak <strong>{total_excluded} artikel</strong> yang terbit di luar batasan waktu resmi (Proyek BUMN sebelum 2020 atau Danantara sebelum 2025) secara transparan dikeluarkan ke log audit terpisah.<br>
    3. **Traceability 100%:** Setiap klaim pada dashboard dapat ditelusuri kembali ke berkas mentah HTML dan log unduhan aslinya.
    """, unsafe_allow_html=True)

# ─── METRIC CARDS ─────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Target Manifest Lolos</div>
        <div class="metric-value">{total_manifest:,}</div>
        <div class="metric-desc">Tervalidasi Batasan Rentang Waktu</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">File HTML Fisik di Disk</div>
        <div class="metric-value">{physical_files_count:,}</div>
        <div class="metric-desc">data/raw/evidence_dorking/html/</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Unduhan Terverifikasi</div>
        <div class="metric-value">{success_downloads:,}</div>
        <div class="metric-desc">HTTP 200 & Ukuran > 500 B</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Dieliminasi Batas Waktu</div>
        <div class="metric-value">{total_excluded}</div>
        <div class="metric-desc">Audit Out-of-Scope (Proyek BUMN <2020)</div>
    </div>
    """, unsafe_allow_html=True)

# ─── BAGIAN 1: AUDIT GROUND TRUTH & VERBATIM ASET DANANTARA (USD 600 MILIAR) ───
st.markdown('<div class="section-header">Ground Truth & Verbatim Konsolidasi 7 BUMN Danantara (USD 600 Miliar AUM)</div>', unsafe_allow_html=True)

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

# ─── BAGIAN 2: LOG AUDIT UNDUHAN HTML (LANGSUNG TAMPIL) ───────────────────────
st.markdown('<div class="section-header">Log Status Unduhan File Mentah HTML</div>', unsafe_allow_html=True)
if not df_log.empty:
    c_status, c_search = st.columns([1.5, 2])
    with c_status:
        status_opts = ["Semua Status"] + df_log["status"].dropna().unique().tolist()
        sel_stat = st.selectbox("Filter Status:", status_opts)
    with c_search:
        search_log = st.text_input("Cari ID Bukti / URL:", "")
        
    df_log_view = df_log.copy()
    if not df_manifest.empty:
        df_log_view = pd.merge(df_log_view, df_manifest[["evidence_id", "title", "publisher"]], on="evidence_id", how="left")
        
    if sel_stat != "Semua Status":
        df_log_view = df_log_view[df_log_view["status"] == sel_stat]
    if search_log.strip():
        ql = search_log.lower()
        search_filter = (
            df_log_view["evidence_id"].astype(str).str.lower().str.contains(ql, na=False) |
            df_log_view["canonical_url"].astype(str).str.lower().str.contains(ql, na=False)
        )
        if "publisher" in df_log_view.columns:
            search_filter = search_filter | df_log_view["publisher"].astype(str).str.lower().str.contains(ql, na=False)
        if "title" in df_log_view.columns:
            search_filter = search_filter | df_log_view["title"].astype(str).str.lower().str.contains(ql, na=False)
        df_log_view = df_log_view[search_filter]
        
    col_info, col_dl = st.columns([3, 1])
    with col_info:
        st.markdown(f"Menampilkan **{len(df_log_view):,}** catatan log:")
    with col_dl:
        failed_csv_path = PROJECT_ROOT / "data" / "raw" / "evidence_dorking" / "failed_download_manifest.csv"
        if failed_csv_path.exists():
            with open(failed_csv_path, "rb") as f_failed:
                st.download_button(
                    label="Unduh CSV Arsip Gagal",
                    data=f_failed.read(),
                    file_name="failed_download_manifest.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
    st.dataframe(
        df_log_view.tail(200),
        use_container_width=True,
        column_config={
            "evidence_id": st.column_config.TextColumn("ID Bukti", width="small"),
            "publisher": st.column_config.TextColumn("Media / Penerbit", width="medium"),
            "title": st.column_config.TextColumn("Judul Artikel", width="large"),
            "status": st.column_config.TextColumn("Status", width="small"),
            "status_code": st.column_config.NumberColumn("HTTP Code", width="small"),
            "file_size_bytes": st.column_config.NumberColumn("Ukuran (Bytes)", width="small"),
            "method": st.column_config.TextColumn("Metode Unduh", width="medium"),
            "canonical_url": st.column_config.LinkColumn("URL Kanonikal", display_text="Buka Sumber"),
            "downloaded_at": st.column_config.TextColumn("Waktu Unduh (UTC)", width="medium")
        },
        hide_index=True
    )
else:
    st.info("Log pengunduhan sedang diinisialisasi.")

# ─── BAGIAN 2: AUDIT ELIMINASI BATAS WAKTU (LANGSUNG TAMPIL) ──────────────────
st.markdown('<div class="section-header">Daftar Dokumen yang Dieliminasi Berdasarkan Batasan Waktu</div>', unsafe_allow_html=True)
st.markdown("""
Artikel di bawah ini dikeluarkan dari manifest utama karena tanggal publikasi berada di luar rentang resmi TOR:
""")
if not df_excluded.empty:
    st.dataframe(
        df_excluded[["evidence_id", "published_at", "track", "publisher", "title", "exclusion_rationale"]],
        use_container_width=True,
        column_config={
            "evidence_id": st.column_config.TextColumn("ID", width="small"),
            "published_at": st.column_config.TextColumn("Tanggal Terbit", width="small"),
            "track": st.column_config.TextColumn("Kategori", width="small"),
            "publisher": st.column_config.TextColumn("Sumber Media", width="medium"),
            "title": st.column_config.TextColumn("Judul Artikel", width="large"),
            "exclusion_rationale": st.column_config.TextColumn("Alasan Eliminasi Audit", width="large")
        },
        hide_index=True
    )

# ─── BAGIAN 3: ARSITEKTUR DOWNLOADER (LANGSUNG TAMPIL) ────────────────────────
st.markdown('<div class="section-header">Prinsip Kerja Multi-Tier Forensic Downloader</div>', unsafe_allow_html=True)
st.markdown("""
Sistem pengunduhan bukti fisik dirancang dengan 3 lapisan proteksi:

1. **Tingkat 1: Google News Token Decoding**
   URL sindikasi `news.google.com/rss/articles/...` dipulihkan ke URL kanonikal media asal menggunakan decoder protobuf dengan Chrome User-Agent dan retry backoff.

2. **Tingkat 2: TLS Impersonation (curl_cffi)**
   Mengakses portal media dan regulator menggunakan sidik jari TLS Chrome 124 untuk stabilitas koneksi pada situs media nasional.

3. **Tingkat 3: Puppeteer Stealth WAF Elevation**
   Jika portal tujuan menerapkan proteksi Cloudflare Turnstile ketat (seperti presidenri.go.id), proses dialihkan ke Headless Chrome dengan plugin Stealth.
""")

st.caption("CELIOS · Center of Economic and Law Studies · Danantara Project 2026")

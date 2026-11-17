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
LOG_PATH = PROJECT_ROOT / "data" / "raw" / "evidence_dorking" / "html_download_log.csv"
EXCLUDED_PATH = PROJECT_ROOT / "data" / "raw" / "evidence_dorking" / "urls_excluded_time_series.csv"
HTML_DIR = PROJECT_ROOT / "data" / "raw" / "evidence_dorking" / "html"

df_manifest = pd.read_csv(MANIFEST_PATH) if MANIFEST_PATH.exists() else pd.DataFrame()
df_log = pd.read_csv(LOG_PATH) if LOG_PATH.exists() else pd.DataFrame()
df_excluded = pd.read_csv(EXCLUDED_PATH) if EXCLUDED_PATH.exists() else pd.DataFrame()

total_manifest = len(df_manifest)
physical_files_count = len(os.listdir(HTML_DIR)) if HTML_DIR.exists() else 0
success_downloads = len(df_log[df_log["status"] == "SUCCESS"]) if not df_log.empty else 0
failed_downloads = len(df_log[df_log["status"] == "FAILED"]) if not df_log.empty else 0
total_excluded = len(df_excluded)

st.markdown('<div class="page-title">Forensic Evidence & Audit Status</div>', unsafe_allow_html=True)
st.markdown(f'<div class="page-subtitle">Penyimpanan File Mentah HTML di Disk Lokal dan Verifikasi Batasan Waktu — {total_manifest:,} Target Bukti</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="note-box">
<strong>Standar Preservasi Forensik (Anti-Hardcoding & Zero Network Parsing)</strong><br>
Sesuai prinsip integritas data penelitian:<br>
1. <strong>Bukti Fisik Utuh:</strong> Setiap artikel yang dikurasi diunduh utuh sebagai berkas HTML di <code>data/raw/evidence_dorking/html/</code> sebelum ekstraksi teks dimulai.<br>
2. <strong>Audit Batasan Waktu:</strong> Sebanyak <strong>{total_excluded} artikel</strong> yang terbit di luar batasan waktu resmi (Track B sebelum 2020 atau Track A sebelum 2025) secara transparan dikeluarkan ke log audit terpisah.<br>
3. <strong>Traceability 100%:</strong> Setiap klaim pada dashboard dapat ditelusuri kembali ke berkas mentah HTML dan log unduhan aslinya.
</div>
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
        <div class="metric-desc">Audit Out-of-Scope (Track B <2020)</div>
    </div>
    """, unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "Log Audit Unduhan HTML",
    "Audit Eliminasi Waktu (93 URL)",
    "Arsitektur Downloader"
])

with tab1:
    st.markdown('<div class="section-header">Log Status Unduhan File Mentah HTML</div>', unsafe_allow_html=True)
    if not df_log.empty:
        c_status, c_search = st.columns([1.5, 2])
        with c_status:
            status_opts = ["Semua Status"] + df_log["status"].dropna().unique().tolist()
            sel_stat = st.selectbox("Filter Status:", status_opts)
        with c_search:
            search_log = st.text_input("Cari ID Bukti / URL:", "")
            
        df_log_view = df_log.copy()
        if sel_stat != "Semua Status":
            df_log_view = df_log_view[df_log_view["status"] == sel_stat]
        if search_log.strip():
            ql = search_log.lower()
            df_log_view = df_log_view[
                df_log_view["evidence_id"].str.lower().str.contains(ql, na=False) |
                df_log_view["canonical_url"].str.lower().str.contains(ql, na=False)
            ]
            
        st.markdown(f"Menampilkan **{len(df_log_view):,}** catatan log:")
        st.dataframe(
            df_log_view.tail(150),
            use_container_width=True,
            column_config={
                "evidence_id": st.column_config.TextColumn("ID Bukti", width="small"),
                "status": st.column_config.TextColumn("Status", width="small"),
                "status_code": st.column_config.NumberColumn("HTTP Code", width="small"),
                "file_size_bytes": st.column_config.NumberColumn("Ukuran (Bytes)", width="small"),
                "method": st.column_config.TextColumn("Metode Unduh", width="medium"),
                "canonical_url": st.column_config.LinkColumn("URL Kanonikal", display_text="Buka URL"),
                "downloaded_at": st.column_config.TextColumn("Waktu Unduh (UTC)", width="medium")
            },
            hide_index=True
        )
    else:
        st.info("Log pengunduhan sedang diinisialisasi.")

with tab2:
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

with tab3:
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

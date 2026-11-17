"""
CELIOS — Tahap 1: Hasil Scrape & Metadata Bukti Publikasi
Menggabungkan Track A (Danantara Monitor >= 2025) dan Track B (Proyek Hijau BUMN >= 2020)
dalam satu kesatuan repositori bukti publikasi terverifikasi.
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
    page_title="CELIOS — Hasil Scrape & Metadata Bukti",
    page_icon="assets/celios_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar()
st.markdown(get_danantara_css(), unsafe_allow_html=True)

# ─── DATA LOADING ─────────────────────────────────────────────────────────────
MANIFEST_PATH = PROJECT_ROOT / "data" / "raw" / "evidence_dorking" / "master_urls_manifest.csv"
LOG_PATH = PROJECT_ROOT / "data" / "raw" / "evidence_dorking" / "html_download_log.csv"

df_manifest = pd.read_csv(MANIFEST_PATH) if MANIFEST_PATH.exists() else pd.DataFrame()
df_log = pd.read_csv(LOG_PATH) if LOG_PATH.exists() else pd.DataFrame()

# Pemetaan URL Langsung Penerbit (Decoded Canonical URL)
url_map = {}
if not df_log.empty:
    for _, r in df_log.iterrows():
        canon = str(r.get("canonical_url", "")).strip()
        if canon and "news.google.com" not in canon and canon != "nan":
            url_map[str(r["evidence_id"])] = canon

df_manifest["direct_url"] = df_manifest["evidence_id"].map(url_map).fillna(df_manifest["url"])
df_manifest["year"] = pd.to_datetime(df_manifest["published_at"], errors="coerce").dt.year.fillna(2025).astype(int)

# Label Tampilan Jalur Riset
track_labels = {
    "TRACK_A_DANANTARA_MONITOR": "Danantara Monitor (>= 2025)",
    "TRACK_B_GREEN_INVENTORY": "Proyek Hijau BUMN (>= 2020)"
}
df_manifest["track_display"] = df_manifest["track"].map(track_labels).fillna(df_manifest["track"])

total_all = len(df_manifest)
count_danantara = len(df_manifest[df_manifest["track"] == "TRACK_A_DANANTARA_MONITOR"])
count_green = len(df_manifest[df_manifest["track"] == "TRACK_B_GREEN_INVENTORY"])
total_publishers = df_manifest["publisher"].nunique()

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown('<div class="org-badge">CELIOS — CENTER OF ECONOMIC AND LAW STUDIES</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Hasil Scrape & Metadata Bukti</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="sub-title">Tahap 1: Korpus {total_all:,} Dokumen Bukti Publikasi Terverifikasi — Danantara Monitor ({count_danantara:,}) & Proyek Hijau BUMN ({count_green:,})</div>',
    unsafe_allow_html=True
)

# ─── DROPDOWN METODOLOGI (ACCORDION EXPANDER) ─────────────────────────────────
with st.expander("Metodologi Pengumpulan Bukti Publikasi & Batasan Rentang Waktu (Sesuai TOR CELIOS)", expanded=False):
    st.markdown(f"""
    **Landasan Metodologi Riset CELIOS** (<code>brief-20260831_Methodological Approach.md</code> baris 37):<br>
    <em>"creating an inventory of green projects announced by state-owned enterprises from 2020 onward and all projects confirmed by Danantara Indonesia since its launch in 2025."</em><br><br>
    
    Halaman ini menyajikan seluruh korpus dokumen publikasi yang menjadi bahan mentah riset, dipisahkan berdasarkan dua batasan rentang waktu resmi:<br>
    1. <strong>Danantara Monitor (Tahun 2025 ke atas — {count_danantara:,} Artikel):</strong> Seluruh regulasi resmi pemerintah (Setneg, BPK), portal Danantara, dan liputan media kredibel mengenai struktur kelembagaan, kepemilikan aset USD 600 miliar, 7 BUMN tahap awal, dan 9 entitas SPV di Wisma Danantara.<br>
    2. <strong>Proyek Hijau BUMN (Tahun 2020 ke atas — {count_green:,} Artikel):</strong> Pengumuman proyek rendah karbon dan transisi energi yang telah dideklarasikan oleh 9 grup BUMN champion lintas 15 kluster (Solar, Air, Angin, Bioenergi, Hidrogen, EV, Dekarbonisasi Industri, dll.).<br><br>
    Seluruh tautan pada tabel di bawah dapat dibuka langsung ke media asal tanpa melewati halaman blokir redirect Google News.
    """, unsafe_allow_html=True)

# ─── HERO METRIC CARDS ────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Bukti Publikasi</div>
        <div class="metric-value">{total_all:,}</div>
        <div class="metric-desc">Tervalidasi Batas Waktu TOR</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Danantara Monitor</div>
        <div class="metric-value">{count_danantara:,}</div>
        <div class="metric-desc">Publikasi Tahun 2025 ke atas</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Proyek Hijau BUMN</div>
        <div class="metric-value">{count_green:,}</div>
        <div class="metric-desc">Publikasi Tahun 2020 ke atas</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Sumber Media / Regulator</div>
        <div class="metric-value">{total_publishers}</div>
        <div class="metric-desc">Portal Resmi, Nasional & Global</div>
    </div>
    """, unsafe_allow_html=True)

# ─── FILTER MULTI-DIMENSI ─────────────────────────────────────────────────────
st.markdown('<div class="section-header">Eksplorasi Korpus Dokumen Bukti Publikasi</div>', unsafe_allow_html=True)

f_col1, f_col2, f_col3, f_col4 = st.columns([1.5, 1.2, 1.2, 2])

with f_col1:
    track_opts = [
        "Semua Jalur (1.754 Dokumen)",
        "Danantara Monitor (>= 2025)",
        "Proyek Hijau BUMN (>= 2020)"
    ]
    sel_track = st.selectbox("Pilih Jalur Riset:", track_opts)

with f_col2:
    all_clusters = ["Semua Kluster"] + sorted(df_manifest["cluster"].dropna().unique().tolist())
    sel_cluster = st.selectbox("Pilih Kluster Proyek:", all_clusters)

with f_col3:
    all_years = ["Semua Tahun"] + sorted(df_manifest["year"].dropna().unique().tolist(), reverse=True)
    sel_year = st.selectbox("Tahun Publikasi:", all_years)

with f_col4:
    search_q = st.text_input("Cari Judul / BUMN Target / Publisher:", "")

# Filter Dataframe
df_view = df_manifest.copy()

if sel_track == "Danantara Monitor (>= 2025)":
    df_view = df_view[df_view["track"] == "TRACK_A_DANANTARA_MONITOR"]
elif sel_track == "Proyek Hijau BUMN (>= 2020)":
    df_view = df_view[df_view["track"] == "TRACK_B_GREEN_INVENTORY"]

if sel_cluster != "Semua Kluster":
    df_view = df_view[df_view["cluster"] == sel_cluster]

if sel_year != "Semua Tahun":
    df_view = df_view[df_view["year"] == int(sel_year)]

if search_q.strip():
    ql = search_q.lower()
    df_view = df_view[
        df_view["title"].astype(str).str.lower().str.contains(ql, na=False) |
        df_view["target_soe"].astype(str).str.lower().str.contains(ql, na=False) |
        df_view["publisher"].astype(str).str.lower().str.contains(ql, na=False) |
        df_view["evidence_id"].astype(str).str.lower().str.contains(ql, na=False)
    ]

st.markdown(f"Menampilkan **{len(df_view):,}** dokumen bukti:")

display_cols = ["evidence_id", "published_at", "track_display", "cluster", "target_soe", "title", "publisher", "direct_url"]

st.dataframe(
    df_view[display_cols],
    use_container_width=True,
    column_config={
        "evidence_id": st.column_config.TextColumn("ID Bukti", width="small"),
        "published_at": st.column_config.TextColumn("Tanggal", width="small"),
        "track_display": st.column_config.TextColumn("Jalur Riset", width="medium"),
        "cluster": st.column_config.TextColumn("Kluster Proyek", width="small"),
        "target_soe": st.column_config.TextColumn("BUMN Target", width="medium"),
        "title": st.column_config.TextColumn("Judul Artikel Publikasi", width="large"),
        "publisher": st.column_config.TextColumn("Media / Sumber", width="small"),
        "direct_url": st.column_config.LinkColumn("Tautan Media", display_text="Buka Sumber Langsung")
    },
    hide_index=True
)

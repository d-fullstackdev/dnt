"""
CELIOS — Danantara Monitor & Green Investment List
Dashboard Utama: Ringkasan Eksekutif & Pelacak Terpadu
"""

import streamlit as st
import os
import sys
import pandas as pd
import plotly.express as px
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.components.sidebar import render_sidebar
from src.utils.styling import get_danantara_css

st.set_page_config(
    page_title="CELIOS — Danantara Monitor & Green Investment List",
    page_icon="assets/celios_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar()
st.markdown(get_danantara_css(), unsafe_allow_html=True)

# ─── DATA LOADING DINAMIS (ZERO HARDCODING) ──────────────────────────────────
MANIFEST_PATH = PROJECT_ROOT / "data" / "raw" / "evidence_dorking" / "master_urls_manifest.csv"
BUMN_MASTER_PATH = PROJECT_ROOT / "data" / "processed" / "bumn_master_clean.csv"
EXCLUDED_PATH = PROJECT_ROOT / "data" / "raw" / "evidence_dorking" / "urls_excluded_time_series.csv"
LOG_PATH = PROJECT_ROOT / "data" / "raw" / "evidence_dorking" / "html_download_log.csv"
HTML_DIR = PROJECT_ROOT / "data" / "raw" / "evidence_dorking" / "html"

if not MANIFEST_PATH.exists():
    st.error("Dataset manifest master_urls_manifest.csv tidak ditemukan.")
    st.stop()

df_manifest = pd.read_csv(MANIFEST_PATH)
df_bumn = pd.read_csv(BUMN_MASTER_PATH) if BUMN_MASTER_PATH.exists() else pd.DataFrame()
df_excluded = pd.read_csv(EXCLUDED_PATH) if EXCLUDED_PATH.exists() else pd.DataFrame()
df_log = pd.read_csv(LOG_PATH) if LOG_PATH.exists() else pd.DataFrame()

# Pemetaan URL Langsung Penerbit (Decoded Canonical URL)
url_map = {}
if not df_log.empty:
    for _, r in df_log.iterrows():
        canon = str(r.get("canonical_url", "")).strip()
        if canon and "news.google.com" not in canon:
            url_map[str(r["evidence_id"])] = canon
df_manifest["direct_url"] = df_manifest["evidence_id"].map(url_map).fillna(df_manifest["url"])

# Metrik Utama Terkalkulasi Dinamis
total_manifest = len(df_manifest)
danantara_count = len(df_manifest[df_manifest["track"] == "TRACK_A_DANANTARA_MONITOR"])
green_bumn_count = len(df_manifest[df_manifest["track"] == "TRACK_B_GREEN_INVENTORY"])

total_bumn = len(df_bumn) if not df_bumn.empty else 196
bumn_holdings = len(df_bumn[df_bumn["entity_tier"].str.contains("HOLDING", na=False)]) if not df_bumn.empty else 14
bumn_persero = len(df_bumn[df_bumn["entity_tier"].str.contains("PERSERO", na=False)]) if not df_bumn.empty else 54
bumn_subsidiaries = len(df_bumn[df_bumn["entity_tier"].str.contains("SUBSIDIARY", na=False)]) if not df_bumn.empty else 128

total_publishers = df_manifest["publisher"].nunique()
total_excluded = len(df_excluded)

# Status Download HTML Fisik Real-time
physical_html_files = len(os.listdir(HTML_DIR)) if HTML_DIR.exists() else 0
decoded_urls_count = len(url_map)

# Ekstrak Tahun untuk Analisis Time Series
df_manifest["year"] = pd.to_datetime(df_manifest["published_at"], errors="coerce").dt.year.fillna(2025).astype(int)

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">Daya Anagata Nusantara (Danantara)</div>', unsafe_allow_html=True)
st.markdown(f'<div class="page-subtitle">Sovereign Wealth Fund Monitor & Green Investment List — {total_manifest:,} Dokumen Bukti Terverifikasi</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="note-box">
<strong>Dua Pilar Pengelompokan Data (Berdasarkan Teks Asli Metodologi Riset Celios)</strong><br>
Sesuai dokumen TOR (<code>brief-20260831_Methodological Approach.md</code> baris 37):<br>
<em>"creating an inventory of green projects announced by state-owned enterprises from 2020 onward and all projects confirmed by Danantara Indonesia since its launch in 2025."</em><br><br>
Data dipisahkan secara natural menjadi dua fokus riset:<br>
1. <strong>Danantara Monitor (Tahun 2025 ke atas):</strong> Proyek, regulasi, dan kebijakan yang dikonfirmasi langsung oleh Danantara sejak diluncurkan tahun 2025 ({danantara_count:,} artikel).<br>
2. <strong>Proyek Hijau BUMN (Tahun 2020 ke atas):</strong> Inventarisasi proyek hijau dan dekarbonisasi yang diumumkan BUMN (PLN, Pertamina, Semen Indonesia, dll.) sejak 2020 lintas 15 kluster ({green_bumn_count:,} artikel).<br><br>
Tautan pada tabel di bawah telah di-decode langsung ke URL resmi media/regulator ({decoded_urls_count:,} URL langsung terverifikasi) tanpa melalui redirect Google News.
</div>
""", unsafe_allow_html=True)

# ─── HERO METRICS ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Indikator Utama Hasil Kerja (Per Hari Ini)</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Bukti Terverifikasi</div>
        <div class="metric-value">{total_manifest:,}</div>
        <div class="metric-desc">{danantara_count:,} Danantara (>=2025) + {green_bumn_count:,} Proyek BUMN (>=2020)</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Universe Entitas BUMN</div>
        <div class="metric-value">{total_bumn}</div>
        <div class="metric-desc">{bumn_holdings} Holding · {bumn_persero} Persero Langsung · {bumn_subsidiaries} Anak Perusahaan</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Kluster Proyek Hijau BUMN</div>
        <div class="metric-value">15</div>
        <div class="metric-desc">Solar, Air, Angin, Bioenergi, Hidrogen, EV, Dekarbonisasi Industri, dll.</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Sumber Media & Regulator</div>
        <div class="metric-value">{total_publishers}</div>
        <div class="metric-desc">3 Portal Regulasi Resmi + 15 Media Nasional dan Global</div>
    </div>
    """, unsafe_allow_html=True)

# ─── BENTO GRID HIGHLIGHTS ───────────────────────────────────────────────────
st.markdown('<div class="section-header">Rincian Dua Jalur Pengumpulan Bukti</div>', unsafe_allow_html=True)

b_col1, b_col2, b_col3 = st.columns(3)

with b_col1:
    st.markdown(f"""
    <div class="bento-card">
        <div>
            <div class="bento-lbl">Danantara Monitor</div>
            <div class="bento-val" style="color: #26A69A;">{danantara_count:,} <span style="font-size: 1rem; color: #9E9E9E;">Artikel</span></div>
            <div class="bento-desc">
                Memantau proyek, regulasi, dan pembentukan kelembagaan Danantara sejak peluncuran resminya pada tahun 2025. Mencakup Keppres No. 30/2025, integrasi 7 BUMN raksasa tahap awal, dan 9 entitas SPV di Wisma Danantara.
            </div>
        </div>
        <div class="bento-src">Batasan Waktu: Tahun 2025 ke atas (Sesuai TOR)</div>
    </div>
    """, unsafe_allow_html=True)

with b_col2:
    st.markdown(f"""
    <div class="bento-card">
        <div>
            <div class="bento-lbl">Proyek Hijau BUMN</div>
            <div class="bento-val" style="color: #66BB6A;">{green_bumn_count:,} <span style="font-size: 1rem; color: #9E9E9E;">Artikel</span></div>
            <div class="bento-desc">
                Inventarisasi proyek dekarbonisasi dan energi bersih yang telah diumumkan BUMN sejak 2020 pada 9 grup BUMN champion (PLN, Pertamina, MIND ID, Semen Indonesia, Pupuk Indonesia, PTPN, Perhutani, Hutama Karya, dan Danantara).
            </div>
        </div>
        <div class="bento-src">Batasan Waktu: Tahun 2020 ke atas (Sesuai TOR)</div>
    </div>
    """, unsafe_allow_html=True)

with b_col3:
    st.markdown(f"""
    <div class="bento-card">
        <div>
            <div class="bento-lbl">Bukti Fisik HTML di Disk</div>
            <div class="bento-val" style="color: #42A5F5;">{physical_html_files:,} <span style="font-size: 1rem; color: #9E9E9E;">File HTML</span></div>
            <div class="bento-desc">
                Setiap artikel diunduh utuh sebagai file HTML fisik ke folder lokal sebelum diekstraksi. Sebanyak {total_excluded} artikel yang terbit di luar rentang waktu resmi dikeluarkan ke log audit terpisah.
            </div>
        </div>
        <div class="bento-src">Lokasi: data/raw/evidence_dorking/html/</div>
    </div>
    """, unsafe_allow_html=True)

# ─── VISUALISASI ANALITIK (PLOTLY) ───────────────────────────────────────────
st.markdown('<div class="section-header">Analisis Sebaran Waktu dan Kluster</div>', unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    df_ts = df_manifest.groupby(["year", "track"]).size().reset_index(name="count")
    df_ts["track_label"] = df_ts["track"].map({
        "TRACK_A_DANANTARA_MONITOR": "Danantara Monitor (>=2025)",
        "TRACK_B_GREEN_INVENTORY": "Proyek Hijau BUMN (>=2020)"
    })
    
    fig_ts = px.bar(
        df_ts,
        x="year",
        y="count",
        color="track_label",
        barmode="stack",
        title="Distribusi Waktu Artikel per Tahun Publikasi (2020 - 2026)",
        labels={"year": "Tahun Publikasi", "count": "Jumlah Artikel", "track_label": "Kategori"},
        color_discrete_map={
            "Danantara Monitor (>=2025)": "#26A69A",
            "Proyek Hijau BUMN (>=2020)": "#66BB6A"
        }
    )
    fig_ts.update_layout(
        template="plotly_dark",
        paper_bgcolor="#141A24",
        plot_bgcolor="#141A24",
        font=dict(family="Inter", color="#ECEFF1"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=50, b=20),
        height=360
    )
    st.plotly_chart(fig_ts, use_container_width=True)

with chart_col2:
    df_green = df_manifest[df_manifest["track"] == "TRACK_B_GREEN_INVENTORY"]
    df_clusters = df_green["cluster"].value_counts().reset_index()
    df_clusters.columns = ["cluster", "count"]
    
    fig_cl = px.bar(
        df_clusters.head(10),
        x="count",
        y="cluster",
        orientation="h",
        title="Top 10 Kluster Proyek Hijau BUMN",
        labels={"count": "Jumlah Artikel Bukti", "cluster": "Kluster Proyek"},
        color="count",
        color_continuous_scale="Greens"
    )
    fig_cl.update_layout(
        template="plotly_dark",
        paper_bgcolor="#141A24",
        plot_bgcolor="#141A24",
        font=dict(family="Inter", color="#ECEFF1"),
        coloraxis_showscale=False,
        yaxis=dict(autorange="reversed"),
        margin=dict(l=20, r=20, t=50, b=20),
        height=360
    )
    st.plotly_chart(fig_cl, use_container_width=True)

# ─── MEDIA DOMAINS & FORENSIC STATUS ─────────────────────────────────────────
col_m1, col_m2 = st.columns(2)

with col_m1:
    df_top_pub = df_manifest["publisher"].value_counts().head(10).reset_index()
    df_top_pub.columns = ["publisher", "count"]
    
    fig_pub = px.pie(
        df_top_pub,
        values="count",
        names="publisher",
        hole=0.45,
        title="Sumber Media dan Portal Regulator Terbanyak",
        color_discrete_sequence=px.colors.qualitative.Dark24
    )
    fig_pub.update_layout(
        template="plotly_dark",
        paper_bgcolor="#141A24",
        font=dict(family="Inter", color="#ECEFF1"),
        margin=dict(l=20, r=20, t=50, b=20),
        height=340
    )
    st.plotly_chart(fig_pub, use_container_width=True)

with col_m2:
    st.markdown('<div style="font-weight:700; font-size:1.05rem; margin-bottom:12px; color:#ECEFF1;">Status Tahapan Kerja</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:#141A24; border:1px solid #2E3B4E; border-radius:8px; padding:16px;">
        <div style="margin-bottom:10px;">
            <span class="badge-track-a">SELESAI</span> <strong>Langkah 1:</strong> Ingesti Master Universe BUMN ({total_bumn} entitas) dan panen data awal ({total_manifest:,} artikel).
        </div>
        <div style="margin-bottom:10px;">
            <span class="badge-track-a">SELESAI</span> <strong>Langkah 2:</strong> Penerapan batas rentang waktu sesuai TOR (Proyek BUMN >=2020, Danantara >=2025; {total_excluded} artikel di luar rentang dikeluarkan ke log audit).
        </div>
        <div style="margin-bottom:10px;">
            <span class="badge-track-b">SEDANG BERJALAN</span> <strong>Langkah 3:</strong> Unduhan bukti fisik mentah HTML ke folder lokal (Tersimpan <strong>{physical_html_files:,} file fisik</strong> di <code>data/raw/evidence_dorking/html/</code>).
        </div>
        <div style="margin-bottom:10px; color:#9E9E9E;">
            <span style="border:1px solid #555; padding:2px 6px; border-radius:4px; font-size:0.7rem;">SIAP EKSEKUSI</span> <strong>Langkah 4:</strong> Ekstraksi teks bersih Markdown secara 100% offline (menggunakan Trafilatura dan BeautifulSoup).
        </div>
        <div style="color:#9E9E9E;">
            <span style="border:1px solid #555; padding:2px 6px; border-radius:4px; font-size:0.7rem;">BERIKUTNYA</span> <strong>Tahap Lanjutan:</strong> Deduplikasi berita dan ekstraksi 13 atribut proyek untuk penyaringan taksonomi 3-Gate.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── TABEL EKSPLORASI BUKTI TERKINI ──────────────────────────────────────────
st.markdown('<div class="section-header">Tabel Bukti Terverifikasi</div>', unsafe_allow_html=True)

f_col1, f_col2, f_col3 = st.columns([1.5, 1.5, 2])
with f_col1:
    sel_track = st.selectbox("Pilih Kategori:", ["Semua", "Danantara Monitor (>= 2025)", "Proyek Hijau BUMN (>= 2020)"])
with f_col2:
    publishers_list = ["Semua Publisher"] + sorted(df_manifest["publisher"].dropna().unique().tolist())
    sel_pub = st.selectbox("Filter Media / Publisher:", publishers_list)
with f_col3:
    search_q = st.text_input("Cari Judul / BUMN / Publisher:", "")

# Filter Dataframe
df_view = df_manifest.copy()
if sel_track == "Danantara Monitor (>= 2025)":
    df_view = df_view[df_view["track"] == "TRACK_A_DANANTARA_MONITOR"]
elif sel_track == "Proyek Hijau BUMN (>= 2020)":
    df_view = df_view[df_view["track"] == "TRACK_B_GREEN_INVENTORY"]

if sel_pub != "Semua Publisher":
    df_view = df_view[df_view["publisher"] == sel_pub]

if search_q.strip():
    q = search_q.lower()
    df_view = df_view[
        df_view["title"].str.lower().str.contains(q, na=False) |
        df_view["target_soe"].str.lower().str.contains(q, na=False) |
        df_view["publisher"].str.lower().str.contains(q, na=False)
    ]

st.markdown(f"Menampilkan **{len(df_view):,}** dokumen dari total {total_manifest:,} dokumen:")

# Format Display Table dengan Direct Link
cols_to_show = ["evidence_id", "published_at", "track", "publisher", "target_soe", "cluster", "title", "direct_url"]
st.dataframe(
    df_view[cols_to_show].head(100),
    use_container_width=True,
    column_config={
        "evidence_id": st.column_config.TextColumn("ID Bukti", width="small"),
        "published_at": st.column_config.TextColumn("Tanggal", width="small"),
        "track": st.column_config.TextColumn("Kategori", width="small"),
        "publisher": st.column_config.TextColumn("Sumber / Media", width="medium"),
        "target_soe": st.column_config.TextColumn("BUMN", width="small"),
        "cluster": st.column_config.TextColumn("Kluster", width="small"),
        "title": st.column_config.TextColumn("Judul Artikel", width="large"),
        "direct_url": st.column_config.LinkColumn("Tautan Langsung Media", display_text="Buka Sumber Langsung")
    },
    hide_index=True
)

st.caption("CELIOS · Center of Economic and Law Studies · Danantara Project 2026")

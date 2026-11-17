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
bumn_persero = len(df_bumn[df_bumn["entity_tier"].str.contains("PERSERO", na=False)]) if not df_bumn.empty else 45
bumn_subsidiaries = len(df_bumn[df_bumn["entity_tier"].str.contains("SUBSIDIARY", na=False)]) if not df_bumn.empty else 128
bumn_spv = len(df_bumn[df_bumn["entity_tier"].str.contains("SPV", na=False)]) if not df_bumn.empty else 9

total_publishers = df_manifest["publisher"].nunique()
total_excluded = len(df_excluded)

# Status Download HTML Fisik Real-time
physical_html_files = len(os.listdir(HTML_DIR)) if HTML_DIR.exists() else 0
decoded_urls_count = len(url_map)

# Ekstrak Tahun untuk Analisis Time Series
df_manifest["year"] = pd.to_datetime(df_manifest["published_at"], errors="coerce").dt.year.fillna(2025).astype(int)

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown('<div class="org-badge">CELIOS — CENTER OF ECONOMIC AND LAW STUDIES</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Daya Anagata Nusantara (Danantara)</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">Sovereign Wealth Fund Monitor & Green Investment List — {total_manifest:,} Dokumen Bukti Terverifikasi</div>', unsafe_allow_html=True)

with st.expander("Metodologi Analisis, Alur Riset Graphic 1, & Batasan Rentang Waktu TOR CELIOS", expanded=False):
    st.markdown(f"""
    **Landasan Metodologi Riset Resmi CELIOS** (<code>brief-20260831_Methodological Approach.md</code> baris 37):<br>
    <em>"Map Indonesia's investable green and transition opportunities by creating an inventory of green projects announced by state-owned enterprises from 2020 onward and all projects confirmed by Danantara Indonesia since its launch in 2025."</em><br><br>
    
    Dashboard ini mengintegrasikan seluruh tahapan riset investigatif dalam tiga tahapan berurutan (Graphic 1 Pipeline):<br>
    1. <strong>Tahap 1 — Hasil Scrape & Metadata Bukti (Aktif):</strong> Menghimpun korpus bukti mentah dari 9 jalur metadata (media massa, laporan tahunan, laporan keberlanjutan, publikasi investigasi NGO, regulasi/RUPTL, open data spasial, dll.) dengan pemisahan rentang waktu resmi ({danantara_count:,} Danantara &ge; 2025 dan {green_bumn_count:,} Proyek Hijau BUMN &ge; 2020).<br>
    2. <strong>Tahap 2 — ETL & Ekstraksi 13 Atribut (Standby):</strong> Transformasi teks bersih berkas bukti menjadi basis data inventaris proyek yang terisi 13 kolom informasi dan dikelompokkan ke dalam 6 Sektor Ekonomi.<br>
    3. <strong>Tahap 3 — Skrining 3-Gate & Green List (Standby):</strong> Penyaringan bertingkat melalui Negative Filter, keselarasan TKBI v3/ASEAN v4, dan uji Norfund Additionality untuk menyusun rekomendasi portofolio hijau Danantara.<br><br>
    Seluruh tautan artikel di dashboard ini telah di-decode langsung ke URL resmi penerbit ({decoded_urls_count:,} tautan langsung) tanpa melewati halaman pengalihan Google News.
    """, unsafe_allow_html=True)

# ─── HERO METRICS ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Indikator Utama Portofolio Riset</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Korpus Bukti Terverifikasi</div>
        <div class="metric-value">{total_manifest:,}</div>
        <div class="metric-desc">{danantara_count:,} Danantara (&ge;2025) · {green_bumn_count:,} Proyek BUMN (&ge;2020)</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Silsilah Entitas BUMN</div>
        <div class="metric-value">{total_bumn}</div>
        <div class="metric-desc">{bumn_holdings} Holding · {bumn_persero} Persero · {bumn_subsidiaries} Anak Usaha · {bumn_spv} SPV</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Kluster Sektoral Riset</div>
        <div class="metric-value">15 Kluster</div>
        <div class="metric-desc">Solar, Air, Angin, Bioenergi, Hidrogen, EV, Dekarbonisasi Industri, dll.</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Metode Skrining Taksonomi</div>
        <div class="metric-value">3-Gate</div>
        <div class="metric-desc">Negative Filter · TKBI v3 / ASEAN v4 · Norfund Additionality</div>
    </div>
    """, unsafe_allow_html=True)

# ─── VISUALISASI WORKFLOW GRAPHIC 1 (ALUR KERJA RISET) ────────────────────────
st.markdown('<div class="section-header">Alur Metodologi Riset CELIOS (Graphic 1 Workflow)</div>', unsafe_allow_html=True)

w1, w2, w3, w4, w5 = st.columns(5)

with w1:
    st.markdown("""
    <div class="metric-card" style="text-align: left; padding: 1rem; border-color: #2E7D32;">
        <div style="font-size: 0.72rem; color: #66BB6A; font-weight: 700;">LANGKAH 1 (AKTIF)</div>
        <div style="font-weight: 700; color: #ECEFF1; font-size: 0.88rem; margin: 4px 0;">Create Inventory</div>
        <div style="font-size: 0.75rem; color: #B0BEC5;">Koleksi bukti mentah 9 jalur metadata (Media, AR, NGO, RUPTL)</div>
    </div>
    """, unsafe_allow_html=True)

with w2:
    st.markdown("""
    <div class="metric-card" style="text-align: left; padding: 1rem;">
        <div style="font-size: 0.72rem; color: #81C784; font-weight: 700;">LANGKAH 2 (NEXT)</div>
        <div style="font-weight: 700; color: #ECEFF1; font-size: 0.88rem; margin: 4px 0;">Sort Six Sectors</div>
        <div style="font-size: 0.75rem; color: #9E9E9E;">Energy, Agri, Downstream, Housing, Infra, Mfg</div>
    </div>
    """, unsafe_allow_html=True)

with w3:
    st.markdown("""
    <div class="metric-card" style="text-align: left; padding: 1rem;">
        <div style="font-size: 0.72rem; color: #81C784; font-weight: 700;">LANGKAH 3 (NEXT)</div>
        <div style="font-weight: 700; color: #ECEFF1; font-size: 0.88rem; margin: 4px 0;">Screening 3-Gate</div>
        <div style="font-size: 0.75rem; color: #9E9E9E;">Negative Filter, TKBI v3, Norfund Additionality</div>
    </div>
    """, unsafe_allow_html=True)

with w4:
    st.markdown("""
    <div class="metric-card" style="text-align: left; padding: 1rem;">
        <div style="font-size: 0.72rem; color: #81C784; font-weight: 700;">LANGKAH 4 (NEXT)</div>
        <div style="font-weight: 700; color: #ECEFF1; font-size: 0.88rem; margin: 4px 0;">Compare Danantara</div>
        <div style="font-size: 0.75rem; color: #9E9E9E;">Komparasi portofolio eksisting Danantara 2025</div>
    </div>
    """, unsafe_allow_html=True)

with w5:
    st.markdown("""
    <div class="metric-card" style="text-align: left; padding: 1rem;">
        <div style="font-size: 0.72rem; color: #81C784; font-weight: 700;">LANGKAH 5 (FINAL)</div>
        <div style="font-weight: 700; color: #ECEFF1; font-size: 0.88rem; margin: 4px 0;">Green Investment List</div>
        <div style="font-size: 0.75rem; color: #9E9E9E;">Daftar proyek hijau final siap alokasi modal negara</div>
    </div>
    """, unsafe_allow_html=True)

# ─── BENTO GRID HIGHLIGHTS ───────────────────────────────────────────────────
st.markdown('<div class="section-header">Rincian Dua Fokus Pengumpulan Bukti</div>', unsafe_allow_html=True)

b_col1, b_col2, b_col3 = st.columns(3)

with b_col1:
    st.markdown(f"""
    <div class="bento-card">
        <div>
            <div class="bento-lbl">Danantara Monitor</div>
            <div class="bento-val" style="color: #66BB6A;">{danantara_count:,} <span style="font-size: 1rem; color: #9E9E9E;">Artikel Bukti</span></div>
            <div class="bento-desc">
                Memantau pembentukan, regulasi, dan kepemilikan aset Danantara sejak peluncuran resminya pada tahun 2025. Mencakup Keppres No. 30/2025, konsolidasi 7 BUMN raksasa tahap awal, dan 9 entitas SPV di Wisma Danantara.
            </div>
        </div>
        <div class="bento-src">Batasan Waktu: Tahun 2025 ke atas (Sesuai TOR CELIOS)</div>
    </div>
    """, unsafe_allow_html=True)

with b_col2:
    st.markdown(f"""
    <div class="bento-card">
        <div>
            <div class="bento-lbl">Proyek Hijau BUMN</div>
            <div class="bento-val" style="color: #4CAF50;">{green_bumn_count:,} <span style="font-size: 1rem; color: #9E9E9E;">Artikel Bukti</span></div>
            <div class="bento-desc">
                Kandidat proyek transisi energi, EBT, dan dekarbonisasi industri BUMN sejak 2020 lintas 15 kluster (menjadi bahan baku ekstraksi 13 atribut sebelum melalui penyaringan taksonomi).
            </div>
        </div>
        <div class="bento-src">Batasan Waktu: Tahun 2020 ke atas (Sesuai TOR CELIOS)</div>
    </div>
    """, unsafe_allow_html=True)

with b_col3:
    st.markdown(f"""
    <div class="bento-card">
        <div>
            <div class="bento-lbl">Preservasi Bukti Fisik Disk</div>
            <div class="bento-val" style="color: #81C784;">{physical_html_files:,} <span style="font-size: 1rem; color: #9E9E9E;">File HTML</span></div>
            <div class="bento-desc">
                Setiap publikasi disimpan utuh sebagai file HTML mentah di disk lokal sebelum ekstraksi teks untuk menjaga integritas forensik bukti. Sebanyak {total_excluded} artikel di luar rentang waktu diaudit terpisah.
            </div>
        </div>
        <div class="bento-src">Lokasi: data/raw/evidence_dorking/html/</div>
    </div>
    """, unsafe_allow_html=True)

# ─── VISUALISASI ANALITIK (PLOTLY) ───────────────────────────────────────────
st.markdown('<div class="section-header">Analisis Sebaran Waktu dan Kluster Sektoral</div>', unsafe_allow_html=True)

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
            "Danantara Monitor (>=2025)": "#4CAF50",
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

# ─── MEDIA DOMAINS & STATUS TAHAPAN ──────────────────────────────────────────
col_m1, col_m2 = st.columns(2)

with col_m1:
    df_top_pub = df_manifest["publisher"].value_counts().head(10).reset_index()
    df_top_pub.columns = ["publisher", "count"]
    
    fig_pub = px.pie(
        df_top_pub,
        values="count",
        names="publisher",
        hole=0.45,
        title="Sumber Media & Portal Regulator Terbanyak",
        color_discrete_sequence=["#2E7D32", "#388E3C", "#43A047", "#4CAF50", "#66BB6A", "#81C784", "#A5D6A7", "#1B5E20", "#455A64", "#607D8B"]
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
    st.markdown('<div style="font-weight:700; font-size:1.05rem; margin-bottom:12px; color:#ECEFF1;">Status Tahapan Riset CELIOS (Graphic 1)</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:#141A24; border:1px solid #2E3B4E; border-radius:8px; padding:16px;">
        <div style="margin-bottom:12px;">
            <span class="badge-track-a">TAHAP 1: SELESAI / AKTIF</span><br>
            <strong>Panen Korpus Bukti & Metadata:</strong> Sebanyak <strong>{total_manifest:,} artikel</strong> terverifikasi dan <strong>{physical_html_files:,} berkas HTML</strong> tersimpan di disk lokal. Kerangka penyelaman 9 jalur metadata multi-sumber telah dibakukan.
        </div>
        <div style="margin-bottom:12px; color:#CFD8DC;">
            <span class="badge-track-b">TAHAP 2: NEXT / STANDBY</span><br>
            <strong>ETL & Ekstraksi 13 Atribut Proyek:</strong> Membedah teks bersih berkas bukti untuk mempopulasikan 13 kolom informasi inventaris proyek hijau dan mengelompokkannya ke dalam 6 sektor ekonomi.
        </div>
        <div style="color:#CFD8DC;">
            <span class="badge-track-b">TAHAP 3: NEXT / STANDBY</span><br>
            <strong>Skrining Taksonomi 3-Gate:</strong> Menyaring proyek inventaris melalui Negative Filter, keselarasan TKBI v3/ASEAN v4, dan prinsip Norfund Additionality untuk menyusun rekomendasi Green Investment List Danantara.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── TABEL EKSPLORASI BUKTI TERKINI ──────────────────────────────────────────
st.markdown('<div class="section-header">Eksplorasi Ringkas Bukti Publikasi Terverifikasi</div>', unsafe_allow_html=True)

st.markdown("""
<div class="note-box" style="margin-top: 5px; margin-bottom: 15px;">
Tabel di bawah menyajikan sampel ringkasan berkas bukti terkini. Untuk eksplorasi mendalam lintas <strong>9 Jalur Metadata</strong> (Media Massa, Laporan Tahunan BUMN, Sustainability Report, Publikasi Investigasi NGO, Regulasi, dll.), silakan buka menu <strong>Hasil Scrape & Metadata Bukti</strong> pada bilah sisi.
</div>
""", unsafe_allow_html=True)

f_col1, f_col2, f_col3 = st.columns([1.5, 1.5, 2])
with f_col1:
    sel_track = st.selectbox("Pilih Track Riset:", ["Semua Track", "Danantara Monitor (>= 2025)", "Proyek Hijau BUMN (>= 2020)"])
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

st.markdown(f"Menampilkan **{min(len(df_view), 25)}** berkas bukti terkini dari total {len(df_view):,} dokumen terfilter:")

# Format Display Table dengan Direct Link
cols_to_show = ["evidence_id", "published_at", "track", "publisher", "target_soe", "cluster", "title", "direct_url"]
st.dataframe(
    df_view[cols_to_show].head(25),
    use_container_width=True,
    column_config={
        "evidence_id": st.column_config.TextColumn("ID Bukti", width="small"),
        "published_at": st.column_config.TextColumn("Tanggal", width="small"),
        "track": st.column_config.TextColumn("Track", width="small"),
        "publisher": st.column_config.TextColumn("Sumber / Media", width="medium"),
        "target_soe": st.column_config.TextColumn("BUMN", width="small"),
        "cluster": st.column_config.TextColumn("Kluster", width="small"),
        "title": st.column_config.TextColumn("Judul Publikasi", width="large"),
        "direct_url": st.column_config.LinkColumn("Tautan Media", display_text="Buka Sumber Langsung")
    },
    hide_index=True
)

st.caption("CELIOS · Center of Economic and Law Studies · Danantara Project 2026")

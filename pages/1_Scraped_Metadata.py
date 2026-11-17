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

source_options = [
    "Semua Sumber Metadata (1.754+)",
    "Media Massa & Berita Kredibel (1.754 Dokumen)",
    "Laporan Tahunan BUMN (Annual Report)",
    "Laporan Keberlanjutan (Sustainability Report)",
    "Publikasi NGO & Laporan Advokasi (WALHI, JATAM, KPA, dll)",
    "Regulasi & Dokumen Perencanaan (JDIH, RUPTL, JETP)",
    "Open Dataset Pemerintah & Industri (ESDM, MODI, GEM)",
    "Jurnal Ilmiah & Policy Paper",
    "Buku & Monograf Riset"
]

row1_col1, row1_col2, row1_col3 = st.columns([1.8, 1.2, 1.2])

with row1_col1:
    sel_source = st.selectbox("Jalur Metadata:", source_options, index=0)

with row1_col2:
    track_opts = [
        "Semua Track",
        "Danantara Monitor (>= 2025)",
        "Proyek Hijau BUMN (>= 2020)"
    ]
    sel_track = st.selectbox("Track Riset:", track_opts)

with row1_col3:
    all_clusters = ["Semua Kluster"] + sorted(df_manifest["cluster"].dropna().unique().tolist())
    sel_cluster = st.selectbox("Kluster Proyek:", all_clusters)

row2_col1, row2_col2 = st.columns([1.2, 3.0])

with row2_col1:
    all_years = ["Semua Tahun"] + sorted(df_manifest["year"].dropna().unique().tolist(), reverse=True)
    sel_year = st.selectbox("Tahun Publikasi:", all_years)

with row2_col2:
    search_q = st.text_input("Cari Judul / BUMN Target / Publisher / Kata Kunci:", "")

# ─── TAMPILAN DATA BERDASARKAN JALUR METADATA ──────────────────────────────────
is_media_active = sel_source in ["Semua Sumber Metadata (1.754+)", "Media Massa & Berita Kredibel (1.754 Dokumen)"]

if is_media_active:
    # Filter Dataframe Media
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

    st.markdown(f"Menampilkan **{len(df_view):,}** dokumen bukti media massa & rilis kredibel terverifikasi:")

    display_cols = ["evidence_id", "published_at", "track_display", "cluster", "target_soe", "title", "publisher", "direct_url"]

    st.dataframe(
        df_view[display_cols],
        use_container_width=True,
        column_config={
            "evidence_id": st.column_config.TextColumn("ID Bukti", width="small"),
            "published_at": st.column_config.TextColumn("Tanggal", width="small"),
            "track_display": st.column_config.TextColumn("Track Riset", width="medium"),
            "cluster": st.column_config.TextColumn("Kluster Proyek", width="small"),
            "target_soe": st.column_config.TextColumn("BUMN Target", width="medium"),
            "title": st.column_config.TextColumn("Judul Artikel Publikasi", width="large"),
            "publisher": st.column_config.TextColumn("Media / Sumber", width="small"),
            "direct_url": st.column_config.LinkColumn("Tautan Media", display_text="Buka Sumber Langsung")
        },
        hide_index=True
    )

else:
    # ─── KERANGKA STANDBY JALUR METADATA NON-MEDIA (PARADIGMA MULTI-SUMBER D3TLH) ───
    source_profiles = {
        "Laporan Tahunan BUMN (Annual Report)": {
            "peran": "Atribut 3 (Struktur Anak Usaha/SPV), Atribut 7 (Kapasitas Terpasang), Atribut 8 (Realisasi Capex / Alokasi Modal Bersih), Atribut 9 (Sumber Pendanaan Korporasi).",
            "target": "14 BUMN Holding di bawah Danantara (PLN, Pertamina, MIND ID, Semen Indonesia, BRI, Mandiri, BNI, Telkom, ASDP, InJourney, Bio Farma, Pupuk Indonesia, dll.).",
            "metodologi": "Annual Report diaudit oleh Kantor Akuntan Publik (KAP) terdaftar, memberikan angka investasi dan struktur kepemilikan saham legal yang mengikat.",
            "status": "Standby Ingestion (Target 14–28 Berkas Laporan Tahunan 2020–2024)"
        },
        "Laporan Keberlanjutan (Sustainability Report)": {
            "peran": "Atribut 11 (Target Reduksi Emisi Gas Rumah Kaca Scope 1, 2, 3), Atribut 12 (Identifikasi Awal Risiko ESG, Konsumsi Energi, Penggunaan Air, Pengelolaan Limbah B3).",
            "target": "Laporan Keberlanjutan berbasis GRI Standards / POJK 51 dari emiten dan anak usaha BUMN (PGAS, ANTM, PTBA, TINS, SMGR, TLKM, BBRI, BMRI, BBNI).",
            "metodologi": "Menyediakan baseline data dekarbonisasi korporasi dan komitmen net-zero roadmap per sektor industri.",
            "status": "Standby Ingestion (Target 20+ Berkas SR Terbitan 2021–2024)"
        },
        "Publikasi NGO & Laporan Advokasi (WALHI, JATAM, KPA, dll)": {
            "peran": "KRUSIAL UNTUK ATRIBUT 12 (Environment and Social Risks) — Melacak konflik agraria, pencemaran lingkungan, perampasan ruang hidup masyarakat adat, sengketa lahan, kriminalisasi warga, dan deforestasi.",
            "target": "WALHI Nasional & Eksekutif Daerah, JATAM (Jaringan Advokasi Tambang), Trend Asia, Auriga Nusantara, Konsorsium Pembaruan Agraria (KPA), Aliansi Masyarakat Adat Nusantara (AMAN), ICW, Publish What You Pay (PWYP) Indonesia.",
            "metodologi": "Persis seperti pada riset CELIOS 2 D3TLH, laporan investigasi independen masyarakat sipil menjadi 'counter-narrative' wajib untuk mengimbangi klaim sepihak greenwashing publikasi korporasi BUMN.",
            "status": "Standby Ingestion (Target 50–100 Laporan Investigasi & Policy Brief NGO)"
        },
        "Regulasi & Dokumen Perencanaan (JDIH, RUPTL, JETP)": {
            "peran": "Atribut 5 (Project Status: MoU, LoI, Tender, COD Schedule), Atribut 9 (Skema Pendanaan Multilateral / Pensiun Dini PLTU), Atribut 4 (Sektor Prioritas Nasional).",
            "target": "JDIH Setneg / Kemenkeu (Keppres/PP Pembentukan Danantara), RUPTL PLN 2021–2030 (Daftar Pembangkit EBT & Jadwal COD), Sekretariat JETP Indonesia (Dokumen CIPP JETP).",
            "metodologi": "Memberikan kepastian hukum dan target kuantitatif perencanaan transisi energi nasional.",
            "status": "Standby Ingestion (Target 10 Dokumen Induk Kebijakan & Regulasi)"
        },
        "Open Dataset Pemerintah & Industri (ESDM, MODI, GEM)": {
            "peran": "Atribut 6 (Lokasi Geografis & Koordinat Spasial Konsesi), Atribut 7 (Kapasitas Izin Usaha Pertambangan / Kelistrikan), Atribut 1 & 2 (Validasi Nama Entitas Berizin).",
            "target": "Minerba One Data Indonesia (MODI ESDM), Ditjen EBTKE Kementerian ESDM, Global Energy Monitor (GEM Coal & Renewable Trackers).",
            "metodologi": "Data tabular terbuka pemerintah dan pemetaan satelit global untuk verifikasi silang integritas data lapangan.",
            "status": "Standby Ingestion (Target 5 Dataset Tabular Spasial)"
        },
        "Jurnal Ilmiah & Policy Paper": {
            "peran": "Validasi metodologi valuasi ekonomi, elastisitas investasi hijau terhadap penciptaan lapangan kerja (green jobs), dan dampak fiskal pembentukan Danantara.",
            "target": "Jurnal terindeks SINTA 1–2 / Scopus, Publikasi LPEM FEB UI, CSIS Indonesia, IESR, dan Arsip Kertas Kebijakan CELIOS.",
            "metodologi": "Menjamin ketelitian akademis dan dasar kausalitas ilmiah dalam penyusunan rekomendasi kebijakan publik.",
            "status": "Standby Ingestion (Target 25 Paper Riset Kunci)"
        },
        "Buku & Monograf Riset": {
            "peran": "Kerangka komparasi tata kelola Sovereign Wealth Fund (SWF) global (Norfund Additionality, Temasek Model, Khazanah Nasional) dan sejarah ekonomi politik BUMN Indonesia.",
            "target": "Monograf tata kelola BUMN, studi transisi energi berkeadilan, literatur Santiago Principles untuk SWF.",
            "metodologi": "Landasan konseptual perumusan uji Gate 3 (Norfund Additionality) dan mitigasi risiko moral hazard Danantara.",
            "status": "Standby Ingestion (Target 10 Monograf Pilihan)"
        }
    }

    profile = source_profiles.get(sel_source, {
        "peran": "Mendukung pemenuhan 13 atribut inventaris proyek hijau CELIOS.",
        "target": "Lembaga riset dan repositori dokumen resmi.",
        "metodologi": "Verifikasi silang multi-sumber independen.",
        "status": "Standby Ingestion"
    })

    st.markdown(f"""
    <div class="note-box" style="margin-top: 10px; margin-bottom: 20px;">
        <div style="font-size: 1.05rem; font-weight: 700; color: #66BB6A; margin-bottom: 6px;">
            JALUR METADATA: {sel_source.upper()}
        </div>
        <div style="font-size: 0.88rem; color: #E0E0E0; line-height: 1.6;">
            <strong>Peran Metodologis dalam 13 Atribut CELIOS:</strong><br>{profile['peran']}<br><br>
            <strong>Target Lembaga / Repositori:</strong><br>{profile['target']}<br><br>
            <strong>Landasan Riset:</strong><br>{profile['metodologi']}<br><br>
            <strong>Status Pipeline:</strong> <span style="background: rgba(76, 175, 80, 0.2); color: #81C784; padding: 2px 8px; border-radius: 4px; font-weight: 600;">{profile['status']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"**Kerangka Skema Metadata Koleksi Dokumen ({sel_source}):**")

    # Kerangka DataFrame Kosong Standby untuk Jalur Ini
    cols_standby = [
        "doc_id",
        "institution_publisher",
        "document_title",
        "publication_year",
        "target_bumn_cluster",
        "key_focus_13_attributes",
        "repository_url_or_file",
        "ingestion_status"
    ]
    df_standby = pd.DataFrame(columns=cols_standby)

    st.dataframe(
        df_standby,
        use_container_width=True,
        column_config={
            "doc_id": st.column_config.TextColumn("ID Dokumen", width="small"),
            "institution_publisher": st.column_config.TextColumn("Lembaga / Penerbit", width="medium"),
            "document_title": st.column_config.TextColumn("Judul Dokumen / Laporan / Dataset", width="large"),
            "publication_year": st.column_config.TextColumn("Tahun", width="small"),
            "target_bumn_cluster": st.column_config.TextColumn("Target BUMN / Kluster", width="medium"),
            "key_focus_13_attributes": st.column_config.TextColumn("Fokus 13 Atribut CELIOS", width="medium"),
            "repository_url_or_file": st.column_config.TextColumn("Tautan Berkas / Repositori", width="medium"),
            "ingestion_status": st.column_config.TextColumn("Status Ingestion", width="small")
        },
        hide_index=True
    )
    st.caption("Kerangka tabel di atas akan terisi otomatis saat pipeline penyelaman dokumen multi-sumber diaktifkan.")

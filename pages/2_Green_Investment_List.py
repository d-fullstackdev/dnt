"""
CELIOS — Green Investment List (Track B: 2020 Onward)
Inventarisasi Portofolio & Proyek Transisi Hijau BUMN Lintas 15 Kluster
"""

import streamlit as st
import os
import sys
import pandas as pd
import plotly.express as px
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.components.sidebar import render_sidebar
from src.utils.styling import get_danantara_css

st.set_page_config(
    page_title="CELIOS — Track B: Green Investment List",
    page_icon="assets/celios_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar()
st.markdown(get_danantara_css(), unsafe_allow_html=True)

# ─── DATA LOADING ─────────────────────────────────────────────────────────────
MANIFEST_PATH = PROJECT_ROOT / "data" / "raw" / "evidence_dorking" / "master_urls_manifest.csv"
df_manifest = pd.read_csv(MANIFEST_PATH)
df_green = df_manifest[df_manifest["track"] == "TRACK_B_GREEN_INVENTORY"].copy()

total_green = len(df_green)
total_clusters = df_green["cluster"].nunique()
df_green["year"] = pd.to_datetime(df_green["published_at"], errors="coerce").dt.year.fillna(2023).astype(int)

st.markdown('<div class="page-title">Green Investment List (Track B)</div>', unsafe_allow_html=True)
st.markdown(f'<div class="page-subtitle">Inventarisasi Proyek Transisi Hijau BUMN Lintas 15 Kluster Metodologis ({total_green:,} Artikel Bukti Terverifikasi)</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="note-box">
<strong>Batasan Rentang Waktu Track B (Sesuai Dokumen Metodologi Riset CELIOS)</strong><br>
Berdasarkan arahan eksplisit Tim Riset CELIOS (Tabita Diela & Bhima Yudhistira):<br>
<em>"creating an inventory of green projects already announced by the Indonesian government and/or state-owned enterprises from 2020 onwards."</em><br>
Seluruh artikel bukti proyek hijau BUMN yang dikurasi dibatasi pada pengumuman sejak <strong>Tahun 2020 ke atas</strong> pada 9 BUMN champion (PLN, Pertamina, Semen Indonesia/SIG, Pupuk Indonesia, MIND ID, PTPN, Perhutani, Hutama Karya, dan Danantara).
</div>
""", unsafe_allow_html=True)

# ─── METRIC CARDS ─────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Bukti Proyek Hijau</div>
        <div class="metric-value">{total_green:,}</div>
        <div class="metric-desc">Rentang Waktu: 2020 – 2026 (≥ 2020)</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Kluster Proyek Terpantau</div>
        <div class="metric-value">{total_clusters}</div>
        <div class="metric-desc">15 Kluster Resmi SOW Riset Celios</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Grup BUMN Champion</div>
        <div class="metric-value">9 Grup</div>
        <div class="metric-desc">PLN, Pertamina, SIG, MIND ID, dll.</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Metode Skrining Taksonomi</div>
        <div class="metric-value">3-Gate</div>
        <div class="metric-desc">Negative List + TKBI v3 + Norfund</div>
    </div>
    """, unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📊 Distribusi 15 Kluster Hijau",
    "🔍 Eksplorasi Inventaris Bukti",
    "🛡️ Kerangka Skrining 3-Gate"
])

with tab1:
    st.markdown('<div class="section-header">Sebaran Dokumen Bukti per Kluster Proyek Hijau</div>', unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns([1.5, 1])
    with col_c1:
        df_cl_counts = df_green["cluster"].value_counts().reset_index()
        df_cl_counts.columns = ["Kluster", "Jumlah Bukti"]
        
        fig = px.bar(
            df_cl_counts,
            x="Jumlah Bukti",
            y="Kluster",
            orientation="h",
            color="Jumlah Bukti",
            color_continuous_scale="Teal",
            title="Jumlah Artikel Bukti per Kluster (Track B)"
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#141A24",
            plot_bgcolor="#141A24",
            font=dict(family="Inter", color="#ECEFF1"),
            yaxis=dict(autorange="reversed"),
            coloraxis_showscale=False,
            height=480,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col_c2:
        st.markdown('<div style="font-weight:700; color:#ECEFF1; margin-bottom:8px;">15 Kluster Metodologi Celios:</div>', unsafe_allow_html=True)
        clusters_desc = [
            ("1. Solar / PLTS", "PLTS terapung Cirata, rooftop solar pabrik Semen Indonesia/Pupuk."),
            ("2. Geothermal / PLTP", "Proyek panas bumi Pertamina Geothermal Energy (PGE) & PLN IP."),
            ("3. Hydro / PLTA", "PLTA pumped storage Cisokan, PLTM Batang Toru, Asahan."),
            ("4. Wind / PLTB", "PLTB Sidrap, Jeneponto, eksplorasi lepas pantai."),
            ("5. Bioenergy & Biomass", "Co-firing biomassa PLTU PLN, pelet kayu, bioetanol Pertamina."),
            ("6. Green Hydrogen & Ammonia", "Proyek hidrogen hijau PLN Muara Karang, Pupuk Indonesia green ammonia."),
            ("7. EV & Battery Ecosystem", "Indonesia Battery Corporation (IBC), ekosistem SPKLU PLN."),
            ("8. Smart Grid & Transmission", "Transmisi bawah laut Jawa-Sumatera, smart grid PLN."),
            ("9. Energy Efficiency", "Efisiensi energi industri pupuk, semen, dan kilang migas."),
            ("10. Industrial Decarbonization", "Green cement SIG, dekarbonisasi smelter MIND ID."),
            ("11. Waste to Energy (WtE)", "Pengolahan sampah RDF di Cilacap, WtE Bantargebang."),
            ("12. Nature-based Solutions (NBS)", "Konservasi hutan Perhutani, restorasi mangrove, kredit karbon."),
            ("13. Sustainable Agriculture", "Praktik sawit berkelanjutan PTPN, regenerasi tanah pangan."),
            ("14. Green Financing", "Penerbitan green bond Mandiri, BRI, BNI untuk transisi."),
            ("15. Carbon Capture (CCUS)", "Injeksi CO2 Sukowati Pertamina, CCS lapangan migas.")
        ]
        for name, desc in clusters_desc:
            st.markdown(f"• **{name}**: <span style='font-size:0.8rem; color:#9E9E9E;'>{desc}</span>", unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-header">Eksplorasi Dokumen Bukti Proyek Hijau</div>', unsafe_allow_html=True)
    
    f1, f2, f3 = st.columns([1.5, 1.5, 2])
    with f1:
        cluster_list = ["Semua Kluster"] + sorted(df_green["cluster"].dropna().unique().tolist())
        sel_cluster = st.selectbox("Pilih Kluster Hijau:", cluster_list)
    with f2:
        year_list = ["Semua Tahun"] + sorted(df_green["year"].dropna().unique().astype(str).tolist())
        sel_year = st.selectbox("Tahun Publikasi (≥ 2020):", year_list)
    with f3:
        search_g = st.text_input("Cari Proyek / Lokasi / BUMN (misal: cirata, cisokan, ibc, amonia):", "")
        
    df_g_view = df_green.copy()
    if sel_cluster != "Semua Kluster":
        df_g_view = df_g_view[df_g_view["cluster"] == sel_cluster]
    if sel_year != "Semua Tahun":
        df_g_view = df_g_view[df_g_view["year"].astype(str) == sel_year]
    if search_g.strip():
        q = search_g.lower()
        df_g_view = df_g_view[
            df_g_view["title"].str.lower().str.contains(q, na=False) |
            df_g_view["topic"].str.lower().str.contains(q, na=False) |
            df_g_view["bumn_target"].str.lower().str.contains(q, na=False)
        ]
        
    st.markdown(f"Menampilkan **{len(df_g_view):,}** dokumen bukti:")
    
    st.dataframe(
        df_g_view[["evidence_id", "published_at", "cluster", "bumn_target", "title", "publisher", "url"]].head(100),
        use_container_width=True,
        column_config={
            "evidence_id": st.column_config.TextColumn("ID Bukti", width="small"),
            "published_at": st.column_config.TextColumn("Tanggal", width="small"),
            "cluster": st.column_config.TextColumn("Kluster Proyek", width="medium"),
            "bumn_target": st.column_config.TextColumn("BUMN Target", width="small"),
            "title": st.column_config.TextColumn("Judul Bukti Pengumuman Proyek", width="large"),
            "publisher": st.column_config.TextColumn("Media / Sumber", width="small"),
            "url": st.column_config.LinkColumn("Tautan Asli", display_text="Buka Sumber")
        },
        hide_index=True
    )

with tab3:
    st.markdown('<div class="section-header">Proses Skrining 3-Gate Sesuai Metodologi Celios</div>', unsafe_allow_html=True)
    st.markdown("""
    Setelah tahap ekstraksi teks bersih (Phase 2), inventaris proyek hijau akan disaring secara deterministik melalui **3 Gerbang (3-Gate Screening)**:
    """)
    
    g1, g2, g3 = st.columns(3)
    with g1:
        st.markdown("""
        <div class="bento-card">
            <div>
                <div class="bento-lbl" style="color:#EF5350;">Gate 1 · Negative Filter</div>
                <div class="bento-val" style="font-size:1.4rem; color:#EF5350;">Exclusion List</div>
                <div class="bento-desc">
                    Mengeliminasi proyek yang bertentangan dengan prinsip keberlanjutan: proyek batu bara baru, captive coal power plant (PLTU captive industri), deforestasi primer, dan pelanggaran AMDAL berat.
                </div>
            </div>
            <div class="bento-src">Standar: EIB Exclusion & Celios Negative Screen</div>
        </div>
        """, unsafe_allow_html=True)
        
    with g2:
        st.markdown("""
        <div class="bento-card">
            <div>
                <div class="bento-lbl" style="color:#FFA726;">Gate 2 · Taksonomi Teknis</div>
                <div class="bento-val" style="font-size:1.4rem; color:#FFA726;">TKBI v3 / ASEAN</div>
                <div class="bento-desc">
                    Pengujian teknis batas ambang emisi (thresholds): klasifikasi Hijau (Green), Transisi (Amber), atau Merah (Red) berdasarkan Taksonomi Keuangan Berkelanjutan Indonesia (TKBI v3) dan ASEAN Taxonomy v4.
                </div>
            </div>
            <div class="bento-src">Standar: OJK TKBI 2024 & ASEAN Taxonomy v4</div>
        </div>
        """, unsafe_allow_html=True)
        
    with g3:
        st.markdown("""
        <div class="bento-card">
            <div>
                <div class="bento-lbl" style="color:#66BB6A;">Gate 3 · Adisionalitas</div>
                <div class="bento-val" style="font-size:1.4rem; color:#66BB6A;">Norfund Standard</div>
                <div class="bento-desc">
                    Menguji apakah proyek memberikan adisionalitas riil (finansial dan lingkungan) yang tidak akan terjadi tanpa intervensi pembiayaan transisi energi berkelanjutan, serta kelayakan komersial jangka panjang.
                </div>
            </div>
            <div class="bento-src">Standar: Norfund Climate Investment Fund</div>
        </div>
        """, unsafe_allow_html=True)

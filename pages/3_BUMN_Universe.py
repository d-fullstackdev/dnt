"""
CELIOS — Universe BUMN & Anak Usaha Ekosistem Danantara
Taksonomi Yuridis & Audit Forensik 196 Entitas (Holding, BUMN Persero, Anak Usaha, dan SPV)
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
    page_title="CELIOS — Universe BUMN Ekosistem Danantara",
    page_icon="assets/celios_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar()
st.markdown(get_danantara_css(), unsafe_allow_html=True)

# ─── DATA LOADING ─────────────────────────────────────────────────────────────
BUMN_MASTER_PATH = PROJECT_ROOT / "data" / "processed" / "bumn_master_clean.csv"
HOLDINGS_PATH = PROJECT_ROOT / "data" / "processed" / "bumn_holdings_clean.csv"
PERSERO_PATH = PROJECT_ROOT / "data" / "processed" / "bumn_legal_persero_clean.csv"
SUBSIDIARIES_PATH = PROJECT_ROOT / "data" / "processed" / "bumn_subsidiaries_clean.csv"
SPV_PATH = PROJECT_ROOT / "data" / "processed" / "danantara_spv_clean.csv"
EXCLUDED_ENTITIES_PATH = PROJECT_ROOT / "data" / "processed" / "danantara_unrelated_companies_excluded.csv"

df_bumn = pd.read_csv(BUMN_MASTER_PATH) if BUMN_MASTER_PATH.exists() else pd.DataFrame()
df_holdings = pd.read_csv(HOLDINGS_PATH) if HOLDINGS_PATH.exists() else pd.DataFrame()
df_persero = pd.read_csv(PERSERO_PATH) if PERSERO_PATH.exists() else pd.DataFrame()
df_subs = pd.read_csv(SUBSIDIARIES_PATH) if SUBSIDIARIES_PATH.exists() else pd.DataFrame()
df_spv = pd.read_csv(SPV_PATH) if SPV_PATH.exists() else pd.DataFrame()
df_excluded_ent = pd.read_csv(EXCLUDED_ENTITIES_PATH) if EXCLUDED_ENTITIES_PATH.exists() else pd.DataFrame()

total_bumn = len(df_bumn)
total_holdings = len(df_bumn[df_bumn["entity_tier"].str.contains("HOLDING", na=False)]) if not df_bumn.empty else 14
total_persero = len(df_bumn[df_bumn["entity_tier"].str.contains("PERSERO", na=False)]) if not df_bumn.empty else 45
total_subs = len(df_bumn[df_bumn["entity_tier"].str.contains("SUBSIDIARY", na=False)]) if not df_bumn.empty else 128
total_spvs = len(df_bumn[df_bumn["entity_tier"].str.contains("SPV", na=False)]) if not df_bumn.empty else 9
total_excluded_pt = len(df_excluded_ent)
total_pilot = len(df_bumn[df_bumn["is_danantara_stage1_pilot"] == True]) if ("is_danantara_stage1_pilot" in df_bumn.columns and not df_bumn.empty) else 18
total_green_priority = len(df_bumn[df_bumn["is_priority_for_green_screening"] == True]) if ("is_priority_for_green_screening" in df_bumn.columns and not df_bumn.empty) else 117

st.markdown('<div class="page-title">Universe BUMN & Anak Usaha Ekosistem Danantara</div>', unsafe_allow_html=True)
st.markdown(f'<div class="page-subtitle">Taksonomi Yuridis dan Pemetaan Kepemilikan {total_bumn} Entitas (14 Holding · 45 BUMN Persero · 128 Anak Usaha · 9 SPV)</div>', unsafe_allow_html=True)

# ─── DROPDOWN METODOLOGI (ACCORDION EXPANDER) ─────────────────────────────────
with st.expander("Catatan Metodologi: Audit Yuridis & Rekonstruksi Ekosistem Danantara", expanded=False):
    st.markdown(f"""
    **Integritas Metodologi & Batasan Yuridis (Sesuai Pedoman Riset CELIOS):**<br>
    Berdasarkan Undang-Undang No. 19/2003 tentang BUMN dan Putusan Mahkamah Konstitusi No. 01/PHP.PRES/XVII/2019, anak perusahaan BUMN berbadan hukum perseroan terbatas (PT) privat dan secara yuridis bukan BUMN mandiri karena sahamnya tidak dimiliki langsung oleh Negara melalui APBN. Selain itu, pada tahap peluncuran resmi awal (2024–2025), konsolidasi BPI Danantara berfokus pada <strong>7 BUMN Raksasa (Pilot Cohort)</strong> ditambah INA.<br><br>
    Untuk menjaga reproduktifitas data ilmiah dan mencegah tumpang tindih data, master universe direkonstruksi ke dalam 4 lapisan legal terverifikasi:<br>
    1. <strong>Holding BUMN Induk ({total_holdings} Entitas):</strong> Induk konglomerasi BUMN sektoral (MIND ID, Pertamina, PLN, PTPN III, Semen Indonesia, dll.).<br>
    2. <strong>BUMN Persero Langsung ({total_persero} Entitas):</strong> BUMN berstatus persero/perum mandiri dengan kepemilikan Saham Seri A Dwiwarna milik Negara RI.<br>
    3. <strong>Anak & Afiliasi BUMN ({total_subs} Entitas):</strong> Entitas operasional yang dimiliki mayoritas oleh holding/persero BUMN (seperti PT KINRA, PT Petrokimia Gresik, dll.).<br>
    4. <strong>Entitas SPV Terindikasi ({total_spvs} PT):</strong> 9 perseroan yang tercatat beralamat di Wisma Danantara Jl. Gatot Subroto dan PT Denera. <em>(Catatan: Berstatus terindikasi basis alamat, menunggu validasi nomor SK/AHU Kemenkumham)</em>.<br>
    5. <strong>Eliminasi Swasta Kebetulan ({total_excluded_pt} PT):</strong> Perusahaan swasta murni pihak ketiga yang memiliki nama "Danantara" di daerah telah diverifikasi dan dikeluarkan dari database.
    """, unsafe_allow_html=True)

# ─── METRIC CARDS ─────────────────────────────────────────────────────────────
m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Master Universe</div>
        <div class="metric-value">{total_bumn}</div>
        <div class="metric-desc">Semua Entitas Ekosistem</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Holding BUMN Induk</div>
        <div class="metric-value">{total_holdings}</div>
        <div class="metric-desc">Grup Pengendali Sektoral</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Persero Langsung</div>
        <div class="metric-value">{total_persero}</div>
        <div class="metric-desc">Saham Seri A Dwiwarna</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Anak Perusahaan</div>
        <div class="metric-value">{total_subs}</div>
        <div class="metric-desc">Badan Hukum PT Privat</div>
    </div>
    """, unsafe_allow_html=True)

with m5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">SPV Terindikasi</div>
        <div class="metric-value">{total_spvs}</div>
        <div class="metric-desc">Basis Wisma Danantara</div>
    </div>
    """, unsafe_allow_html=True)

# ─── BAGIAN 1: EKSPLORASI MASTER UNIVERSE (LANGSUNG TAMPIL) ───────────────────
st.markdown('<div class="section-header">Pencarian dan Filter Master Universe</div>', unsafe_allow_html=True)

col_f1, col_f2, col_f3 = st.columns([1.5, 1.2, 2])
with col_f1:
    tier_opts = ["Semua Tingkat"] + sorted(df_bumn["entity_tier"].dropna().unique().tolist())
    sel_tier = st.selectbox("Filter Tingkat Yuridis:", tier_opts)
with col_f2:
    filter_opts = ["Semua Kategori", f"Prioritas Hijau ({total_green_priority})", "Pilot Cohort Tahap 1 Danantara"]
    sel_filter = st.selectbox("Filter Kategori Strategis:", filter_opts)
with col_f3:
    search_bumn = st.text_input("Cari Nama BUMN / Parent Holding / Sektor:", "")
    
df_view_bumn = df_bumn.copy()
if sel_tier != "Semua Tingkat":
    df_view_bumn = df_view_bumn[df_view_bumn["entity_tier"] == sel_tier]

if sel_filter.startswith("Prioritas Hijau"):
    df_view_bumn = df_view_bumn[df_view_bumn["is_priority_for_green_screening"] == True]
elif sel_filter == "Pilot Cohort Tahap 1 Danantara":
    df_view_bumn = df_view_bumn[df_view_bumn["is_danantara_stage1_pilot"] == True]

if search_bumn.strip():
    q_b = search_bumn.lower()
    df_view_bumn = df_view_bumn[
        df_view_bumn["entity_name"].str.lower().str.contains(q_b, na=False) |
        df_view_bumn["parent_holding"].str.lower().str.contains(q_b, na=False) |
        df_view_bumn["sector"].str.lower().str.contains(q_b, na=False)
    ]
    
st.markdown(f"Menampilkan **{len(df_view_bumn)}** entitas:")

display_cols = ["entity_id", "entity_name", "entity_tier", "parent_holding", "sector", "ceo", "is_priority_for_green_screening", "is_danantara_stage1_pilot"]
existing_disp = [c for c in display_cols if c in df_view_bumn.columns]

st.dataframe(
    df_view_bumn[existing_disp],
    use_container_width=True,
    column_config={
        "entity_id": st.column_config.TextColumn("ID", width="small"),
        "entity_name": st.column_config.TextColumn("Nama Entitas", width="large"),
        "entity_tier": st.column_config.TextColumn("Tingkat Yuridis", width="medium"),
        "parent_holding": st.column_config.TextColumn("Grup Holding Induk", width="medium"),
        "sector": st.column_config.TextColumn("Sektor Bisnis", width="medium"),
        "ceo": st.column_config.TextColumn("Pimpinan / CEO", width="medium"),
        "is_priority_for_green_screening": st.column_config.CheckboxColumn("Prioritas Hijau (6 Sektor)", width="small"),
        "is_danantara_stage1_pilot": st.column_config.CheckboxColumn("Pilot Tahap 1 Danantara", width="small")
    },
    hide_index=True
)

# ─── BAGIAN 2: 14 GRUP HOLDING BUMN (LANGSUNG TAMPIL) ─────────────────────────
st.markdown('<div class="section-header">14 Grup Holding Pengendali BUMN</div>', unsafe_allow_html=True)
st.markdown("""
Holding BUMN merupakan entitas konsolidasi pengendali yang membawahi ratusan perseroan terbatas operasional lintas kluster industri:
""")
if not df_holdings.empty:
    st.dataframe(
        df_holdings,
        use_container_width=True,
        column_config={
            "holding_name": st.column_config.TextColumn("Nama Holding", width="medium"),
            "official_leading_entity": st.column_config.TextColumn("Entitas Resmi Leading", width="large"),
            "sector": st.column_config.TextColumn("Sektor Industri", width="medium"),
            "ceo": st.column_config.TextColumn("Pimpinan / CEO", width="medium"),
            "website": st.column_config.LinkColumn("Website Resmi", width="medium"),
            "source_url": st.column_config.TextColumn("Catatan Tambahan", width="small")
        },
        hide_index=True
    )

# ─── BAGIAN 3: AUDIT SPV & ELIMINASI SWASTA KEBETULAN ─────────────────────────
st.markdown('<div class="section-header">Audit Forensik: SPV Terindikasi vs Eliminasi Swasta Kebetulan</div>', unsafe_allow_html=True)

col_spv, col_ex = st.columns(2)

with col_spv:
    st.markdown(f"**9 Entitas SPV / Afiliasi Danantara Terindikasi ({len(df_spv)} PT):**")
    st.caption("Klasifikasi berbasis alamat kantor di Wisma Danantara Gatot Subroto (Menunggu Validasi AHU Kemenkumham).")
    if not df_spv.empty:
        st.dataframe(
            df_spv[["company_name", "verification_status"]],
            use_container_width=True,
            column_config={
                "company_name": st.column_config.TextColumn("Nama Entitas", width="large"),
                "verification_status": st.column_config.TextColumn("Status Verifikasi", width="large")
            },
            hide_index=True
        )

with col_ex:
    st.markdown(f"**8 Perusahaan Swasta Pihak Ketiga Tereksklusi ({len(df_excluded_ent)} PT):**")
    st.caption("False positives yang kebetulan mengandung kata 'Danantara' namun tidak memiliki relasi BUMN.")
    if not df_excluded_ent.empty:
        st.dataframe(
            df_excluded_ent[["company_name", "address", "exclusion_reason"]],
            use_container_width=True,
            column_config={
                "company_name": st.column_config.TextColumn("Nama PT Swasta", width="medium"),
                "address": st.column_config.TextColumn("Lokasi Domisili", width="large"),
                "exclusion_reason": st.column_config.TextColumn("Alasan Eliminasi", width="large")
            },
            hide_index=True
        )

st.caption("CELIOS · Center of Economic and Law Studies · Danantara Project 2026")

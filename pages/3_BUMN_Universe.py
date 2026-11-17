"""
CELIOS — Master Universe BUMN under Danantara
Taksonomi & Audit Yuridis 196 Entitas BUMN under Danantara
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
    page_title="CELIOS — BUMN Master Universe",
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
EXCLUDED_ENTITIES_PATH = PROJECT_ROOT / "data" / "processed" / "danantara_unrelated_companies_excluded.csv"

df_bumn = pd.read_csv(BUMN_MASTER_PATH) if BUMN_MASTER_PATH.exists() else pd.DataFrame()
df_holdings = pd.read_csv(HOLDINGS_PATH) if HOLDINGS_PATH.exists() else pd.DataFrame()
df_persero = pd.read_csv(PERSERO_PATH) if PERSERO_PATH.exists() else pd.DataFrame()
df_subs = pd.read_csv(SUBSIDIARIES_PATH) if SUBSIDIARIES_PATH.exists() else pd.DataFrame()
df_excluded_ent = pd.read_csv(EXCLUDED_ENTITIES_PATH) if EXCLUDED_ENTITIES_PATH.exists() else pd.DataFrame()

total_bumn = len(df_bumn)
total_holdings = len(df_holdings)
total_persero = len(df_persero)
total_subs = len(df_subs)
total_excluded_pt = len(df_excluded_ent)

st.markdown('<div class="page-title">Master Universe BUMN under Danantara</div>', unsafe_allow_html=True)
st.markdown(f'<div class="page-subtitle">Taksonomi Yuridis & Pemetaan Kepemilikan {total_bumn} Entitas BUMN under Konsolidasi BPI Danantara</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="note-box">
<strong>Latar Belakang Audit & Kurasi Universe BUMN</strong><br>
Untuk mencegah tumpang tindih data (sebagaimana evaluasi proyek sebelumnya), tim riset melakukan rekonstruksi hirarki kepemilikan BUMN menjadi 3 lapisan legal yang terpisah tegas:<br>
1. <strong>Holding BUMN ({total_holdings} Induk):</strong> Entitas holding pengendali saham lintas kluster industri.<br>
2. <strong>Persero Langsung ({total_persero} BUMN):</strong> Entitas persero dengan saham Seri A Dwiwarna langsung milik Negara.<br>
3. <strong>Anak & Cucu Perusahaan ({total_subs} Entitas):</strong> Entitas operasional yang dimiliki mayoritas oleh holding/persero BUMN.<br>
4. <strong>Eliminasi Swasta Kebetulan ({total_excluded_pt} PT):</strong> PT swasta pihak ketiga yang memiliki kemiripan nama "Danantara" telah divalidasi dan dikeluarkan dari master data.
</div>
""", unsafe_allow_html=True)

# ─── METRIC CARDS ─────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Entitas Terverifikasi</div>
        <div class="metric-value">{total_bumn}</div>
        <div class="metric-desc">Master BUMN under Danantara</div>
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
        <div class="metric-label">Persero Langsung Negara</div>
        <div class="metric-value">{total_persero}</div>
        <div class="metric-desc">Saham Seri A Dwiwarna</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Anak & Afiliasi BUMN</div>
        <div class="metric-value">{total_subs}</div>
        <div class="metric-desc">Entitas Operasional & SPV</div>
    </div>
    """, unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "🔍 Eksplorasi Master Universe (196 Entitas)",
    "🏛️ 14 Grup Holding BUMN",
    "🛡️ Audit Eliminasi Swasta Kebetulan (8 PT)"
])

with tab1:
    st.markdown('<div class="section-header">Pencarian & Filter Silsilah Entitas BUMN</div>', unsafe_allow_html=True)
    
    col_f1, col_f2 = st.columns([1.5, 2])
    with col_f1:
        type_options = ["Semua Tipe", "HOLDING", "PERSERO_DIRECT", "SUBSIDIARY"]
        sel_type = st.selectbox("Filter Tipe Yuridis:", type_options)
    with col_f2:
        search_bumn = st.text_input("Cari Nama BUMN / Holding Induk:", "")
        
    df_view_bumn = df_bumn.copy()
    if sel_type != "Semua Tipe":
        df_view_bumn = df_view_bumn[df_view_bumn["entity_type"] == sel_type]
    if search_bumn.strip():
        q_b = search_bumn.lower()
        df_view_bumn = df_view_bumn[
            df_view_bumn["entity_name"].str.lower().str.contains(q_b, na=False) |
            df_view_bumn["holding_group"].str.lower().str.contains(q_b, na=False)
        ]
        
    st.markdown(f"Menampilkan **{len(df_view_bumn)}** entitas:")
    
    st.dataframe(
        df_view_bumn,
        use_container_width=True,
        column_config={
            "entity_name": st.column_config.TextColumn("Nama Entitas BUMN", width="large"),
            "entity_type": st.column_config.TextColumn("Tipe Yuridis", width="medium"),
            "holding_group": st.column_config.TextColumn("Grup Holding Induk", width="medium"),
            "status": st.column_config.TextColumn("Status Audit", width="medium"),
            "notes": st.column_config.TextColumn("Catatan Validasi & Sektor", width="large")
        },
        hide_index=True
    )

with tab2:
    st.markdown('<div class="section-header">14 Grup Holding Pengendali BUMN</div>', unsafe_allow_html=True)
    st.markdown("""
    Holding BUMN merupakan entitas konsolidasi utama yang membawahi ratusan perseroan terbatas operasional:
    """)
    if not df_holdings.empty:
        st.dataframe(
            df_holdings,
            use_container_width=True,
            column_config={
                "entity_name": st.column_config.TextColumn("Nama Grup Holding", width="large"),
                "holding_group": st.column_config.TextColumn("Grup", width="medium"),
                "status": st.column_config.TextColumn("Status", width="medium"),
                "notes": st.column_config.TextColumn("Ruang Lingkup Operasi", width="large")
            },
            hide_index=True
        )

with tab3:
    st.markdown('<div class="section-header">Audit Eliminasi Perusahaan Swasta Kebetulan (False Positives)</div>', unsafe_allow_html=True)
    st.markdown("""
    Dalam proses crawling dan pemetaan kata kunci "Danantara", terdeteksi sejumlah perusahaan swasta independen yang tidak berafiliasi dengan BPI Danantara maupun BUMN. Demi **integritas metodologi**, entitas berikut telah resmi **dieliminasi dari analisis**:
    """)
    if not df_excluded_ent.empty:
        st.dataframe(
            df_excluded_ent,
            use_container_width=True,
            column_config={
                "company_name": st.column_config.TextColumn("Nama PT Swasta", width="large"),
                "address": st.column_config.TextColumn("Alamat Domisili", width="large"),
                "category": st.column_config.TextColumn("Klasifikasi", width="medium"),
                "exclusion_reason": st.column_config.TextColumn("Alasan Eliminasi", width="large")
            },
            hide_index=True
        )

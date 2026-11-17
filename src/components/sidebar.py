"""Shared sidebar component for Celios 9 Danantara Dashboard."""
import streamlit as st
import os

def render_sidebar():
    """Render CELIOS logo and Danantara dashboard navigation in sidebar."""
    _dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(_dir, "..", "..", "assets", "celios_logo.png")
    logo_path = os.path.normpath(logo_path)

    with st.sidebar:
        st.markdown("""
        <style>
        [data-testid="stSidebarNav"] { display: none !important; }
        [data-testid="stPageLink-Icon"], span[data-testid="stIconMaterial"], .st-emotion-cache-1fttcpj {
            display: none !important;
        }
        .sidebar-label {
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.08em;
            color: #66BB6A;
            text-transform: uppercase;
            padding: 12px 0 4px 0;
        }
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {
            color: #66BB6A !important;
        }
        </style>
        """, unsafe_allow_html=True)

        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)

        st.markdown("""
        <div style="text-align:center; padding: 6px 0 4px 0;">
            <div style="font-size:0.95rem; font-weight:700; color:#66BB6A; letter-spacing:0.03em;">DANANTARA MONITOR</div>
            <div style="font-size:0.72rem; color:#9E9E9E; margin-top:2px;">Sovereign Wealth Fund & Green SOE Tracker</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown('<div class="sidebar-label">Ringkasan Utama</div>', unsafe_allow_html=True)
        st.page_link("Dashboard.py", label="Overview & Eksekutif")

        st.markdown('<div class="sidebar-label">Pipeline Riset (Graphic 1)</div>', unsafe_allow_html=True)
        st.page_link("pages/1_Scraped_Metadata.py", label="1. Hasil Scrape & Metadata Bukti")
        st.page_link("pages/2_Project_Inventory_ETL.py", label="2. ETL & Ekstraksi 13 Atribut")
        st.page_link("pages/3_Green_Investment_Screening.py", label="3. Skrining & Green List")

        st.markdown('<div class="sidebar-label">Entitas & Dokumentasi</div>', unsafe_allow_html=True)
        st.page_link("pages/4_BUMN_Universe.py", label="4. Silsilah 196 Entitas BUMN")
        st.page_link("pages/5_Forensic_Evidence.py", label="5. Bukti Fisik & Unduhan HTML")
        st.page_link("pages/6_Metodologi_Brief.py", label="6. Dokumentasi Metodologi")

        st.markdown("---")
        st.caption("CELIOS · Danantara Monitor · 2026")

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
            color: #26A69A;
            text-transform: uppercase;
            padding: 12px 0 4px 0;
        }
        </style>
        """, unsafe_allow_html=True)

        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)

        st.markdown("""
        <div style="text-align:center; padding: 6px 0 4px 0;">
            <div style="font-size:0.95rem; font-weight:700; color:#26A69A; letter-spacing:0.03em;">DANANTARA MONITOR</div>
            <div style="font-size:0.72rem; color:#9E9E9E; margin-top:2px;">Sovereign Wealth Fund & Green SOE Tracker</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown('<div class="sidebar-label">Ringkasan Utama</div>', unsafe_allow_html=True)
        st.page_link("Dashboard.py", label="Overview & Eksekutif")

        st.markdown('<div class="sidebar-label">Pilar Riset & Pelacak</div>', unsafe_allow_html=True)
        st.page_link("pages/1_Danantara_Monitor.py", label="Danantara Monitor (>= 2025)")
        st.page_link("pages/2_Green_Investment_List.py", label="Proyek Hijau BUMN (>= 2020)")
        st.page_link("pages/3_BUMN_Universe.py", label="Daftar 196 Entitas BUMN")

        st.markdown('<div class="sidebar-label">Dokumentasi</div>', unsafe_allow_html=True)
        st.page_link("pages/4_Forensic_Evidence.py", label="Bukti Fisik & Unduhan HTML")
        st.page_link("pages/5_Metodologi_Brief.py", label="Dokumentasi Metodologi")

        st.markdown("---")
        st.caption("CELIOS · Danantara Monitor · 2026")

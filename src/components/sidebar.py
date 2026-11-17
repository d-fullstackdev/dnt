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
        st.page_link("Dashboard.py", label="Overview & Eksekutif", icon="🏛️")

        st.markdown('<div class="sidebar-label">Pilar Riset & Pelacak</div>', unsafe_allow_html=True)
        st.page_link("pages/1_Danantara_Monitor.py", label="Track A: Danantara Monitor", icon="📡")
        st.page_link("pages/2_Green_Investment_List.py", label="Track B: 15 Kluster Hijau", icon="🌱")
        st.page_link("pages/3_BUMN_Universe.py", label="Silsilah 196 Entitas BUMN", icon="🏢")

        st.markdown('<div class="sidebar-label">Forensik & Tata Kelola</div>', unsafe_allow_html=True)
        st.page_link("pages/4_Forensic_Evidence.py", label="Bukti Forensik & HTML Fisik", icon="💾")
        st.page_link("pages/5_Metodologi_Brief.py", label="Dokumentasi Metodologi", icon="📑")

        st.markdown("---")
        st.caption("CELIOS · Danantara Monitor · 2026")

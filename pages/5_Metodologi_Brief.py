"""
CELIOS — Dokumentasi Metodologi & Riset Danantara
Kesesuaian Metodologi SOW, Kontrak, dan Batasan Rentang Waktu Tabita Diela
"""

import streamlit as st
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.components.sidebar import render_sidebar
from src.utils.styling import get_danantara_css

st.set_page_config(
    page_title="CELIOS — Dokumentasi Metodologi",
    page_icon="assets/celios_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar()
st.markdown(get_danantara_css(), unsafe_allow_html=True)

st.markdown('<div class="page-title">Dokumentasi Metodologi & Riset Celios</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Rujukan Resmi Metodologi Penelitian dan Batasan Waktu Tabita Diela</div>', unsafe_allow_html=True)

st.markdown("""
<div class="note-box">
<strong>Landasan Rujukan Dokumen Riset:</strong><br>
1. <code>ref/brief-20260831_Methodological Approach.md</code> (Metodologi Pendekatan Riset Celios)<br>
2. <code>ref/brief - Permintaan Evaluasi Scope Of Work (SOW) & Penawaran Rekonstruksi Kontrak.pdf</code><br>
3. <code>ref/brief - MASTER LIST BUMN UNDER DANANTARA.xlsx</code>
</div>
""", unsafe_allow_html=True)

# ─── SECTION 1: BATASAN RENTANG WAKTU ─────────────────────────────────────────
st.markdown('<div class="section-header">1. Batasan Rentang Waktu (Verbatim Metodologi Riset Celios)</div>', unsafe_allow_html=True)
st.markdown("""
Sesuai teks asli pada dokumen `ref/brief-20260831_Methodological Approach.md` (baris 37):

> *"1. Map Indonesia's investable green and transition opportunities by creating an inventory of green projects announced by state-owned enterprises from 2020 onward and all projects confirmed by Danantara Indonesia since its launch in 2025."*

Artinya, pengumpulan data memiliki dua batasan rentang waktu yang tegas:
* **Track B: Proyek Hijau BUMN (Tahun 2020 ke atas):** Mencakup proyek-proyek hijau yang telah diumumkan oleh BUMN sejak tahun 2020 lintas 15 kluster proyek.
* **Track A: Proyek Danantara (Tahun 2025 ke atas):** Mencakup seluruh proyek dan kebijakan yang dikonfirmasi langsung oleh Danantara sejak diluncurkan pada tahun 2025.
""")

# ─── SECTION 2: 15 KLUSTER HIJAU BUMN ─────────────────────────────────────────
st.markdown('<div class="section-header">2. 15 Kluster Proyek Hijau (Sesuai Tabel Metodologi Celios)</div>', unsafe_allow_html=True)

c_col1, c_col2 = st.columns(2)
with c_col1:
    st.markdown("""
    1. **Solar:** PLTS, PLTS terapung, PLTS atap, solar panel, solar rooftop, tenaga surya.
    2. **Water:** PLTA, PLTMH, hidro, bendungan, pumped storage, mini-hydro.
    3. **Wind:** PLTB, tenaga bayu, turbin angin, wind farm.
    4. **Bioenergy:** biomassa, biogas, biofuel, biodiesel, bioetanol, SAF.
    5. **Waste and circular:** waste-to-energy, PSEL, RDF, pengolahan sampah menjadi energi, ekonomi sirkular.
    6. **Hydrogen:** hidrogen hijau, amonia hijau, hidrogen rendah karbon.
    7. **Electric vehicle:** kendaraan listrik, ekosistem EV, SPKLU, SPBKLU, bus listrik.
    8. **Battery:** baterai kendaraan listrik, rantai pasok baterai, daur ulang baterai.
    """)
with c_col2:
    st.markdown("""
    9. **Power network:** transmisi hijau, interkoneksi, smart grid, digitalisasi jaringan, grid fleksibel.
    10. **Industry decarbonization:** efisiensi energi, elektrifikasi, semen rendah karbon, baja ramah lingkungan.
    11. **Coal transition:** pensiun dini PLTU, penghentian PLTU, phase-down batu bara, aset terlantar.
    12. **Carbon:** perdagangan karbon, kredit karbon, pengurangan emisi, dekarbonisasi, net zero.
    13. **Mangrove, peatland:** rehabilitasi mangrove, restorasi gambut, reforestasi, konservasi.
    14. **Wastewater:** pengolahan air limbah, air bersih berkelanjutan, pengurangan kebocoran air.
    15. **Renewable energy (general):** energi terbarukan, energi bersih, energi hijau, pembangkit hijau.
    """)

# ─── SECTION 3: SKRINING 3-GATE ───────────────────────────────────────────────
st.markdown('<div class="section-header">3. Kerangka Penyaringan Proyek Hijau (3-Gate Taxonomy Screening)</div>', unsafe_allow_html=True)
st.markdown("""
Metodologi Celios menetapkan 3 gerbang penyaringan:

1. **Gate 1: Exclusionary & Negative Filter**
   * Pengecualian langsung untuk proyek batu bara baru, captive coal power plant, deforestasi, dan pelanggaran sosial.

2. **Gate 2: Technical Screening Criteria**
   * Pengujian proyek terhadap Taksonomi Keuangan Berkelanjutan Indonesia (TKBI Versi 3) dan ASEAN Taxonomy for Sustainable Finance (Versi 4).

3. **Gate 3: Norfund Additionality Principle**
   * Menguji prinsip adisionalitas sesuai standar Norfund: memastikan modal negara menghasilkan dampak yang tidak dapat dipenuhi oleh pasar biasa secara mandiri.
""")

# ─── SECTION 4: 13 ATRIBUT PROYEK VERBATIM ────────────────────────────────────
st.markdown('<div class="section-header">4. 13 Atribut Data Proyek yang Diekstraksi (Verbatim Brief)</div>', unsafe_allow_html=True)
st.markdown("""
Berdasarkan dokumen metodologi riset Celios (baris 68-80), berikut 13 data yang diekstraksi dari setiap proyek:
1. Project name
2. The name of the SOE
3. The name of the SOE subsidiary or special purpose vehicle
4. Sector
5. Project status (e.g. planning, studies, MoU, LoI, tender, construction, commissioning, operations)
6. Location
7. Capacity, including its denomination
8. Investment amount, including its currency
9. Funding source
10. Partners
11. Emission reduction target
12. Environment and social risks
13. Announcement date/latest update date
""")

st.caption("CELIOS · Center of Economic and Law Studies · Danantara Project 2026")

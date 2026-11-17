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
st.markdown('<div class="page-subtitle">Rujukan Resmi Metodologi Penelitian, Scope of Work (SOW), dan Batasan Waktu Tabita Diela</div>', unsafe_allow_html=True)

st.markdown("""
<div class="note-box">
<strong>Landasan Rujukan Dokumen Riset:</strong><br>
1. <code>ref/brief-20260831_Methodological Approach.md</code> (Metodologi Pendekatan Riset Celios)<br>
2. <code>ref/brief - Permintaan Evaluasi Scope Of Work (SOW) & Penawaran Rekonstruksi Kontrak.pdf</code><br>
3. <code>ref/brief - MASTER LIST BUMN UNDER DANANTARA.xlsx</code><br>
4. Arahan eksplisit Tim Riset Celios (Mba Tabita Diela, CC Mas Bhima Yudhistira).
</div>
""", unsafe_allow_html=True)

# ─── SECTION 1: BATASAN RENTANG WAKTU ─────────────────────────────────────────
st.markdown('<div class="section-header">1. Batasan Rentang Waktu (Time Series Bounding)</div>', unsafe_allow_html=True)
st.markdown("""
Sesuai arahan tertulis pada dokumen metodologi Celios, pengumpulan dan analisis data dibagi menjadi dua pilar waktu yang berbeda:

* **Tahun 2020 ke atas (2020 onward) — Untuk Proyek Hijau BUMN (Track B):**
  > *"creating an inventory of green projects already announced by the Indonesian government and/or state-owned enterprises from 2020 onwards."*
  >
  > Fokus pada inventarisasi proyek hijau yang telah diumumkan oleh pemerintah Indonesia dan/atau BUMN sejak tahun 2020 lintas 15 kluster proyek.

* **Tahun 2025 ke atas — Untuk Proyek & Kebijakan Danantara (Track A):**
  > *"and all projects confirmed by Danantara Indonesia since its launch in 2025."*
  >
  > Fokus pada seluruh proyek, kesepakatan investasi, dan arah kebijakan yang dikonfirmasi langsung oleh BPI Danantara sejak peluncuran resminya pada tahun 2025.
""")

# ─── SECTION 2: 15 KLUSTER HIJAU BUMN ─────────────────────────────────────────
st.markdown('<div class="section-header">2. Taksonomi 15 Kluster Proyek Hijau BUMN</div>', unsafe_allow_html=True)

c_col1, c_col2 = st.columns(2)
with c_col1:
    st.markdown("""
    1. **Solar Power (PLTS):** PLTS Terapung, PLTS Atap komersial/industri, PLTS Ground-mounted.
    2. **Geothermal Energy (PLTP):** Pembangkit panas bumi, eksplorasi sumur uap PGE & PLN.
    3. **Hydro Power (PLTA/PLTM):** PLTA skala besar, pumped storage, minihidro, mikrohidro.
    4. **Wind Power (PLTB):** Pembangkit listrik tenaga bayu/angin darat dan lepas pantai.
    5. **Bioenergy & Biomass:** Co-firing biomassa pada PLTU, biogas, pelet kayu, bioavtur, biodiesel.
    6. **Green Hydrogen & Ammonia:** Produksi hidrogen berbasis energi terbarukan dan amonia hijau.
    7. **EV Ecosystem & Battery:** Ekosistem rantai pasok sel baterai, EV charging (SPKLU), motor listrik.
    8. **Smart Grid & Transmission:** Penguatan transmisi tegangan tinggi, interkoneksi pulau, digital grid.
    """)
with c_col2:
    st.markdown("""
    9. **Energy Efficiency & Auditing:** Konservasi energi industri semen, pupuk, dan kilang.
    10. **Industrial Decarbonization:** Semen rendah karbon, green steel, elektrifikasi smelter mineral.
    11. **Waste to Energy (WtE):** Refuse Derived Fuel (RDF), insinerator ramah lingkungan, biogas TPA.
    12. **Nature-based Solutions (NBS):** Penanaman mangrove, restorasi gambut, silvikultur Perhutani.
    13. **Sustainable Agriculture:** Perkebunan sawit bersertifikasi ISPO/RSPO, pupuk organik, dekarbonisasi tanah.
    14. **Green Financing & ESG:** Penerbitan obligasi hijau (Green Bond), sukuk keberlanjutan, sindikasi ESG.
    15. **CCUS (Carbon Capture):** Penangkapan dan penyimpanan karbon pada sektor hulu migas dan industri berat.
    """)

# ─── SECTION 3: SKRINING 3-GATE ───────────────────────────────────────────────
st.markdown('<div class="section-header">3. Kerangka Penyaringan Proyek Hijau (3-Gate Taxonomy Screening)</div>', unsafe_allow_html=True)
st.markdown(r"""
Setiap proyek yang terinventarisasi akan melalui 3 gerbang validasi ketat:

```
[Master Green Evidence] ──> [Gate 1: Negative Filter] ──> [Gate 2: Technical Screening] ──> [Gate 3: Norfund Additionality] ──> [Green Investment List]
```

1. **Gate 1: Exclusionary & Negative Filter:**
   * Menolak proyek yang berkaitan dengan ekspansi batu bara, PLTU captive baru, deforestasi kawasan hutan lindung primer, atau proyek yang berada dalam sengketa hukum agraria berat.

2. **Gate 2: Technical Screening Criteria (TKBI v3 & ASEAN Taxonomy v4):**
   * Menguji proyek terhadap batas ambang emisi (threshold $\text{gCO}_2/\text{kWh}$), kriteria *Do No Significant Harm* (DNSH), dan kepatuhan perlindungan sosial minimum.

3. **Gate 3: Norfund Additionality & Financial Viability:**
   * Mengukur adisionalitas investasi (environmental & financial additionality), kemampuan menarik sindikasi modal swasta/internasional, dan rasio mitigasi risiko iklim jangka panjang.
""")

# ─── SECTION 4: 5-STAGE DATA PIPELINE ─────────────────────────────────────────
st.markdown('<div class="section-header">4. Alur 5 Tahap Pengolahan Data (Deterministic Pipeline)</div>', unsafe_allow_html=True)
st.markdown("""
1. **Langkah 1 & 1b — Ingesti Universe & Panen Bukti:**
   Pemetaan 196 BUMN master dan panen 1.847 tautan berita/regulasi dari 18 domain resmi dan kredibel.
2. **Langkah 2 — Filter Batasan Waktu (Time Series Bounding):**
   Penyaringan ketat menghasilkan 1.754 artikel lolos kurasi (903 Track B $\ge 2020$; 851 Track A $\ge 2025$), dan 93 artikel out-of-scope dieliminasi ke log audit.
3. **Langkah 3 — Unduh Forensik HTML Utuh (Sedang Berjalan):**
   Unduhan fisik file mentah `.html` ke disk lokal dengan TLS Impersonation & Puppeteer Stealth, menjamin kepatuhan penuh terhadap aturan *anti-hardcoding*.
4. **Langkah 4 — Ekstraksi Teks Bersih Markdown Offline (Siap Eksekusi):**
   Ekstraksi teks artikel bebas iklan/navigasi secara 100% offline menggunakan engine `trafilatura` dan `beautifulsoup`.
5. **Phase 3-5 — Deduplikasi MinHash LSH, Parsing 13 Atribut, & Skrining 3-Gate:**
   Eliminasi duplikasi sindikasi berita dan pengekstrakan atribut proyek (nama proyek, nilai investasi, kapasitas, lokasi, status konstruksi).
""")

st.caption("CELIOS · Center of Economic and Law Studies · Danantara Project 2026")

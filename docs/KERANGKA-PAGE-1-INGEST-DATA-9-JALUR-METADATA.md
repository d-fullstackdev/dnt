# Rencana Strategi & Teknologi Ingest Data 9 Jalur Metadata (Page 1)
## CELIOS 9: Danantara Monitor & Korpus Bukti Multi-Sumber Proyek Hijau BUMN
**Target Halaman Dashboard:** `pages/1_Scraped_Metadata.py`  
**Standar Pelaksanaan:** Paradigma Riset Investigatif Multi-Sumber (Adopsi Celios 2 D3TLH & Zero Hardcoded Data)  
**Tujuan Utama:** Membangun korpus bukti mentah (*raw evidence corpus*) terlengkap, terverifikasi secara forensik, dan multi-sudut pandang untuk mengisi **13 Atribut Inventaris Proyek Hijau** dan **Pelacakan Danantara**.

---

## 1. Filosofi & Strategi Ingest Data Multi-Sumber

### Mengapa Berita Media Saja Tidak Cukup?
Dalam riset investigatif energi dan transisi ekonomi (berkaca dari riset CELIOS 2 D3TLH):
* **Media Massa & Berita Kredibel:** Sangat efektif untuk *project discovery* (menemukan nama proyek, seremoni MoU/LoI, dan tanggal pengumuman). Namun, berita media memiliki kelemahan fatal: **tidak memuat data capex yang mengikat, detail porsi saham anak usaha, dan hampir 100% melakukan *greenwashing* dengan menyembunyikan risiko sosial/lingkungan.**
* **Laporan Tahunan BUMN:** Menyediakan angka investasi (*capex*), kapasitas riil terpasang, dan struktur hukum anak usaha/SPV yang diaudit resmi oleh akuntan publik (KAP).
* **Publikasi NGO & Advokasi Sipil:** Menjadi satu-satunya sumber independen yang membuka fakta lapangan mengenai **konflik agraria, tumpang tindih tanah adat, pencemaran lingkungan, dan pelanggaran AMDAL (Atribut 12)**.
* **Regulasi & RUPTL PLN:** Memberikan kepastian jadwal operasional komersial (*COD schedule*) dan komitmen resmi pemerintah.
* **Open Dataset & Spasial:** Menyediakan verifikasi izin tambang (MODI ESDM) dan koordinat satelit (GEM).

Dengan mengkombinasikan ke-9 jalur ini, setiap proyek hijau BUMN yang tercatat di dashboard akan memiliki bukti silang (*cross-validated evidence*) dari berbagai perspektif yang tidak terbantahkan.

---

## 2. Matriks Ringkasan: 9 Jalur Metadata, Strategi Ingestion, & Stack Teknologi

| No | Jalur Metadata | Target Sumber / Lembaga | Strategi Harvesting & Ingestion | Teknologi & Engine Ekstraksi | Lokasi Penyimpanan Raw | Relevansi Kunci terhadap 13 Atribut CELIOS |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Media Massa & Berita Kredibel** | 150+ Portal Berita Kredibel (Katadata, Bisnis, CNBC, Antara, Kompas, Tempo, Bloomberg) | • Google News RSS Dorking<br>• Canonical URL Unmasking<br>• Headless DOM Harvesting | • `feedparser`<br>• `requests` / `urllib3`<br>• **Puppeteer Stealth Engine** (`stealth_fetcher.js`) | `data/raw/evidence_dorking/html/` | **Atribut 1** (Project Name), **Atribut 2** (SOE Name), **Atribut 5** (Status), **Atribut 10** (Partners), **Atribut 13** (Date) |
| **2** | **Laporan Tahunan (Annual Report)** | 14 BUMN Holding Danantara (PLN, Pertamina, MIND ID, SIG, Mandiri, BRI, BNI, Telkom, dll) | • Investor Relations Web Scraper<br>• Unduhan PDF Keterbukaan IDX | • `Scrapling` (Adaptive Scraping)<br>• **PyMuPDF (`fitz`)**<br>• **`pdfplumber`** (Table Extractor) | `data/raw/annual_reports/pdf/` | **Atribut 3** (Anak Usaha/SPV di CALK), **Atribut 7** (Kapasitas), **Atribut 8** (Capex), **Atribut 9** (Funding) |
| **3** | **Laporan Keberlanjutan (SR)** | Emiten BUMN (PGAS, ANTM, PTBA, TINS, SMGR, TLKM, BBRI, BMRI, BBNI) | • Repositori ESG IDX & Web Korporat<br>• PDF Harvesting POJK 51 / GRI | • `requests` PDF Harvester<br>• **Trafilatura** (PDF text extraction)<br>• RegEx / LayoutParser | `data/raw/sustainability_reports/pdf/` | **Atribut 11** (Target Reduksi Emisi & Inventarisasi GRK Scope 1, 2, 3) |
| **4** | **Publikasi NGO & Advokasi Sipil** | WALHI, JATAM, Trend Asia, Auriga Nusantara, KPA, AMAN, ICW, PWYP Indonesia | • Sitemap & Publication Directory Crawler<br>• Full-text Report Harvesting | • **Crawl4AI** (Local Playwright Engine)<br>• `pdfplumber`<br>• `trafilatura` | `data/raw/ngo_publications/` | **KRUSIAL: Atribut 12** (Environment and Social Risks: konflik lahan, pencemaran, hak adat) |
| **5** | **Regulasi & Dokumen Perencanaan** | JDIH Setneg, JDIH Kemenkeu, RUPTL PLN 2021–2030, CIPP JETP Indonesia | • JDIH REST API / Scraper<br>• PDF Tabular Parsing (RUPTL Buku 1–3) | • `pdfplumber` (Table parsing)<br>• **Camelot** / `tabula-py`<br>• `requests` | `data/raw/regulations_planning/` | **Atribut 4** (Sektor), **Atribut 5** (Status & Target COD), **Atribut 9** (Skema JETP / Multilateral) |
| **6** | **Open Dataset Pemerintah & Industri** | MODI ESDM (Minerba One Data), Ditjen EBTKE, Global Energy Monitor (GEM) | • API Endpoint Ingestion<br>• CSV / GeoJSON Bulk Downloader | • `pandas` REST Ingestion<br>• `openpyxl`<br>• `geopandas` | `data/raw/open_datasets/` | **Atribut 6** (Location / Koordinat Spasial), **Atribut 7** (Kapasitas Izin Resmi IUP/IUPK) |
| **7** | **Jurnal Ilmiah & Policy Paper** | Jurnal SINTA 1–2 / Scopus, LPEM FEB UI, CSIS Indonesia, IESR, Arsip CELIOS | • Bibliometric API Querying<br>• Open-Access PDF Resolver | • **OpenAlex API** (`pyalex`)<br>• Semantic Scholar API<br>• `urllib` | `data/raw/academic_papers/` | Landasan Ilmiah Valuasi Ekonomi Hijau, Dampak Fiskal Danantara & Green Jobs |
| **8** | **Buku & Monograf Riset** | IFSWF (Santiago Principles), Monograf Tata Kelola SWF Global (Norfund, Temasek) | • Repositori Publikasi SWF Global<br>• Monograf Terbuka | • `PyMuPDF`<br>• Clean Markdown Converter | `data/raw/monographs_books/` | Landasan Metodologis Uji Additionality Norfund (Prinsip Gate 3 Brief CELIOS) |
| **9** | **Master Integrasi Metadata** | Konsolidasi Seluruh 9 Jalur di Atas | • Cross-Source Normalization<br>• Entity ID Linking ke 196 BUMN | • **MinHash LSH (`datasketch`)**<br>• Pydantic Strict Schema<br>• Parquet Storage | `data/processed/master_metadata_corpus.parquet` | Single Source of Truth Korpus Metadata Bukti Mentah untuk Handover Tahap 2 |

---

## 3. Rincian Strategi & Teknologi Ingest Data per Jalur

---

### Jalur 1: Media Massa & Berita Kredibel (Status: 1.754 Dokumen Aktif + Retry Engine)

* **Tujuan:** Menyediakan cakupan luas (*high recall*) pengumuman proyek BUMN ($\ge 2020$) dan kebijakan institusi Danantara ($\ge 2025$).
* **Sumber Target:** Portal berita terverifikasi Dewan Pers dan kantor berita internasional: *Katadata, Bisnis.com, Antaranews, CNBC Indonesia, Kompas, Tempo, Kontan, Detik, Kumparan, Bloomberg, Reuters, The Jakarta Post*.
* **Strategi Ingestion & Harvesting:**
  1. **Google News RSS Dorking Bertingkat:** Menjalankan kueri terspesialisasi berbasis 15 kluster proyek hijau dan nama resmi 196 entitas BUMN.
  2. **Canonical URL Unmasking:** Menguraikan tautan redirect protobuff `news.google.com` ke URL asli penerbit berita menggunakan script Python murni.
  3. **Puppeteer Stealth Fallback Engine (`tools/puppeteer_engine/stealth_fetcher.js`):** Mengatasi portal yang memblokir request HTTP biasa dengan browser headless yang dilengkapi ekstensi stealth anti-bot (Chrome evasion flags, randomized user-agents).
* **Teknologi & Library:**
  * `feedparser`: Pengurai RSS feed berita.
  * `Node.js` + `puppeteer-extra` + `puppeteer-extra-plugin-stealth`: Mesin pengunduh berkas HTML mentah untuk situs berproteksi WAF/Cloudflare.
* **Penyimpanan Raw & Integritas:**
  * Berkas HTML disimpan di: `data/raw/evidence_dorking/html/{evidence_id}_{slug}.html`.
  * Manifest unduhan: `data/raw/evidence_dorking/html_download_log.csv` (1.362 SUKSES, 392 GAGAL).
  * Manifest retry: `data/raw/evidence_dorking/failed_download_manifest.csv` (392 URL target untuk diselesaikan via Puppeteer Stealth).
* **Output Metadata:** `master_urls_manifest.csv` berisi kolom `evidence_id`, `track`, `cluster`, `target_soe`, `title`, `url`, `published_at`, `publisher`, `direct_url`.

---

### Jalur 2: Laporan Tahunan BUMN (Annual Report)

* **Tujuan:** Menyediakan kepastian legal dan audit finansial untuk **Atribut 3 (Anak Usaha/SPV)**, **Atribut 7 (Kapasitas Terpasang)**, **Atribut 8 (Nilai Investasi/Capex)**, dan **Atribut 9 (Sumber Pendanaan)**.
* **Sumber Target (14 Holding BUMN Danantara):**
  * Sektor Energi: *PT PLN (Persero)*, *PT Pertamina (Persero)*.
  * Sektor Hilirisasi & Mineral: *MIND ID (Inalum, Aneka Tambang, PTBA, Timah, Freeport)*.
  * Sektor Manufaktur: *PT Semen Indonesia (Persero) Tbk (SIG)*, *PT Pupuk Indonesia (Persero)*.
  * Sektor Perkebunan/Agri: *PTPN III (Holding Perkebunan)*.
  * Sektor Perbankan/Finansial: *PT Bank Rakyat Indonesia (Persero) Tbk (BRI)*, *PT Bank Mandiri (Persero) Tbk*, *PT Bank Negara Indonesia (Persero) Tbk (BNI)*.
  * Sektor Infrastruktur & Logistik: *PT Telkom Indonesia (Persero) Tbk*, *PT Kereta Api Indonesia (Persero)*, *PT ASDP Indonesia Ferry (Persero)*, *PT InJourney (Aviasi Pariwisata)*.
  * Sektor Farmasi/Kesehatan: *PT Bio Farma (Persero)*.
* **Strategi Ingestion & Harvesting:**
  1. Menargetkan halaman resmi *Investor Relations* / *Publikasi Laporan Tahunan* masing-masing BUMN.
  2. Mengunduh laporan tahunan audited rentang waktu 2020 s.d. 2024 (target 28 berkas PDF beresolusi tinggi).
  3. Menggunakan portal keterbukaan informasi Bursa Efek Indonesia (IDX) untuk emiten publik BUMN (BBRI, BMRI, BBNI, TLKM, SMGR, ANTM, PTBA, TINS, PGAS).
* **Teknologi & Library:**
  * `Scrapling` / `requests`: Menemukan dan mengunduh URL berkas PDF laporan secara otomatis.
  * **`pdfplumber`**: Mengekstrak tabel finansial dari Catatan Atas Laporan Keuangan (CALK), terutama bagian:
    * *Daftar Entitas Anak & Kepemilikan Efektif (%)*.
    * *Aset Tetap Dalam Konstruksi (Capex realisasi per proyek)*.
    * *Pinjaman Jangka Panjang & Fasilitas Kredit Sindikasi*.
  * **`PyMuPDF (fitz)`**: Konversi teks cepat berkinerja tinggi untuk pencarian kata kunci proyek hijau di ratusan halaman laporan.
* **Penyimpanan Raw:** `data/raw/annual_reports/pdf/{tahun}_{kode_bumn}_annual_report.pdf`.

---

### Jalur 3: Laporan Keberlanjutan (Sustainability Report)

* **Tujuan:** Menyediakan baseline dekarbonisasi dan data inventarisasi emisi untuk **Atribut 11 (Emission reduction target)** serta identifikasi awal risiko ESG.
* **Sumber Target:** Emiten dan holding BUMN yang menerbitkan Sustainability Report (SR) berkala sesuai POJK 51/POJK.03/2017 dan standar Global Reporting Initiative (GRI).
* **Strategi Ingestion & Harvesting:**
  1. Mengunduh berkas Sustainability Report terpisah dari Annual Report untuk periode 2021 s.d. 2024.
  2. Memfokuskan scraping pada bab *Kinerja Lingkungan*, *Emisi Gas Rumah Kaca (Scope 1, Scope 2, Scope 3)*, dan *Transisi Energi*.
* **Teknologi & Library:**
  * `requests`: Otomasi unduhan PDF dari repositori IDX dan website BUMN.
  * `pdfplumber`: Mengekstrak tabel matriks GRI Standards (khususnya GRI 302: Energy dan GRI 305: Emissions).
  * `pydantic`: Memvalidasi tipe data angka reduksi emisi ($tCO_2e/tahun$) agar seragam.
* **Penyimpanan Raw:** `data/raw/sustainability_reports/pdf/{tahun}_{kode_bumn}_sustainability_report.pdf`.

---

### Jalur 4: Publikasi NGO & Laporan Advokasi Sipil (Krusial untuk Atribut 12)

* **Tujuan:** Mengisi **Atribut 12 (`Environment and social risks`)** secara independen dan obyektif. Mengungkap dampak lingkungan, konflik hak ulayat/adat, sengketa lahan, kriminalisasi warga, dan deforestasi yang **tidak pernah diakui di publikasi media korporat BUMN**.
* **Sumber Target (8 Lembaga Advokasi Sipil Prioritas):**
  1. **WALHI (Wahana Lingkungan Hidup Indonesia):** Fokus pada pencemaran lingkungan, AMDAL bermasalah, kerusakan DAS, dan deforestasi proyek energi/tambang.
  2. **JATAM (Jaringan Advokasi Tambang):** Investigasi dampak hilirisasi nikel/batu bara, perampasan ruang hidup di pulau kecil, dan PLTU captive.
  3. **Trend Asia:** Investigasi mendalam terkait kritik transisi energi semu (*false solutions*: co-firing biomassa, CCS/CCUS, green coal, nuklir).
  4. **Auriga Nusantara:** Analisis spasial tutupan lahan, deforestasi di konsesi BUMN, dan kepemilikan manfaat (*beneficial ownership*).
  5. **Konsorsium Pembaruan Agraria (KPA):** Data konflik agraria struktural, sengketa lahan perkebunan PTPN dan kehutanan Perhutani dengan petani lokal.
  6. **Aliansi Masyarakat Adat Nusantara (AMAN):** Pelanggaran hak wilayah adat akibat proyek geotermal, PLTA skala besar, dan proyek hilirisasi.
  7. **Indonesia Corruption Watch (ICW):** Investigasi tata kelola, potensi benturan kepentingan, dan akuntabilitas SWF/BUMN.
  8. **Publish What You Pay (PWYP) Indonesia:** Transparansi rantai pasok industri ekstraktif dan akuntabilitas pendanaan transisi energi.
* **Strategi Ingestion & Harvesting:**
  1. Meng-crawl repositori *Publikasi*, *Laporan Investigasi*, dan *Policy Brief* pada domain resmi masing-masing NGO.
  2. Menargetkan laporan terbitan tahun 2020 s.d. 2026 yang menyebut nama-nama proyek transisi BUMN dan wilayah konsesinya.
* **Teknologi & Library:**
  * **`Crawl4AI`**: Menggunakan Playwright lokal untuk menjelajahi katalog publikasi NGO dan mengekstrak teks ringkasan eksekutif ke dalam format Clean Markdown murni tanpa iklan atau navigasi website.
  * `pdfplumber` / `PyMuPDF`: Membaca laporan investigasi lengkap format PDF.
* **Penyimpanan Raw:** `data/raw/ngo_publications/pdf/{nama_ngo}_{tahun}_{slug_judul}.pdf`.

---

### Jalur 5: Regulasi & Dokumen Perencanaan Pembangunan

* **Tujuan:** Memberikan dasar legalitas, target waktu operasional resmi (**Atribut 5: Project Status & COD schedule**), dan skema pembiayaan multilateral (**Atribut 9: Funding source**).
* **Sumber Target:**
  * **JDIH Setneg & Kemenkeu:** Peraturan Pemerintah (PP) dan Keputusan Presiden (Keppres) pendirian BPI Danantara, perubahan kepemilikan saham BUMN, dan penunjukan dewan pengawas/direksi.
  * **RUPTL PLN 2021–2030 (Green RUPTL):** Dokumen perencanaan kelistrikan nasional PT PLN (Persero).
  * **Dokumen CIPP JETP Indonesia:** *Comprehensive Investment and Policy Plan* Sekretariat Just Energy Transition Partnership bernilai USD 20 miliar.
* **Strategi Ingestion & Harvesting:**
  1. Mengambil berkas regulasi resmi langsung dari portal Jaringan Dokumentasi dan Informasi Hukum (JDIH).
  2. Membedah matriks lampiran RUPTL 2021–2030 untuk mengekstrak seluruh daftar pembangkit EBT per sistem kelistrikan (Jawa-Bali, Sumatera, Kalimantan, Sulawesi, Maluku, Papua).
* **Teknologi & Library:**
  * `pdfplumber` & `Camelot-py`: Ekstraksi tabel tabular RUPTL (mengubah ratusan tabel PDF RUPTL menjadi struktur DataFrame bersih).
* **Penyimpanan Raw:** `data/raw/regulations_planning/{kode_dokumen}.pdf`.

---

### Jalur 6: Open Dataset Pemerintah & Industri

* **Tujuan:** Verifikasi spasial koordinat geografis (**Atribut 6: Location**) dan kapasitas izin resmi pertambangan/pembangkit (**Atribut 7**).
* **Sumber Target:**
  * **MODI ESDM (Minerba One Data Indonesia):** Basis data perizinan tambang batubara, nikel, bauksit, tembaga milik MIND ID dan anak usahanya.
  * **Portal Satu Data Ditjen EBTKE ESDM:** Data operasional pembangkit EBT nasional.
  * **Global Energy Monitor (GEM Trackers):** Data koordinat lintang/bujur (*latitude/longitude*), status operasi, dan kepemilikan smelter serta pembangkit listrik di Indonesia.
* **Strategi Ingestion & Harvesting:**
  1. Menghubungkan script Python ke endpoint API publik Satu Data ESDM.
  2. Mengunduh dataset tabular resmi dari Global Energy Monitor (Global Coal Plant Tracker, Global Solar Power Tracker, Global Wind Power Tracker).
* **Teknologi & Library:**
  * `pandas` + `requests`: Pemrosesan tabular data masif.
  * `geopandas`: Validasi koordinat lintang dan bujur fasilitas proyek.
* **Penyimpanan Raw:** `data/raw/open_datasets/{nama_portal}_{kategori}.csv`.

---

### Jalur 7: Jurnal Ilmiah & Policy Paper

* **Tujuan:** Menjamin kedalaman akademis terkait valuasi ekonomi hijau, pemodelan dampak pembentukan Danantara terhadap PDB dan penerimaan fiskal negara, serta estimasi penciptaan lapangan kerja hijau (*green jobs*).
* **Sumber Target:** Paper jurnal terindeks SINTA 1–2 / Scopus, publikasi riset LPEM FEB UI, CSIS Indonesia, IESR, dan arsip policy paper CELIOS terdahulu.
* **Strategi Ingestion & Harvesting:**
  1. Menggunakan **OpenAlex API** untuk mencari publikasi ilmiah dengan kueri `Danantara`, `transisi energi BUMN`, `Sovereign Wealth Fund Indonesia`, dan `green industrial policy Indonesia`.
  2. Mengunduh PDF berstatus Open Access (OA) secara otomatis via API resolver.
* **Teknologi & Library:**
  * `pyalex` (OpenAlex Python SDK): Mengambil metadata judul, penulis, abstrak, dan tautan PDF open access.
  * `requests`: Pengunduhan PDF berkas ilmiah.
* **Penyimpanan Raw:** `data/raw/academic_papers/{tahun}_{penulis_utama}_{slug}.pdf`.

---

### Jalur 8: Buku & Monograf Riset Tata Kelola SWF Global

* **Tujuan:** Memberikan landasan komparasi internasional dalam penyusunan rekomendasi mitigasi risiko *moral hazard* Danantara dan perumusan **Uji Gate 3: Norfund Additionality**.
* **Sumber Target:** Publikasi resmi *International Forum of Sovereign Wealth Funds (IFSWF)* mengenai *Santiago Principles*, laporan tahunan *Norfund* (Norwegian Investment Fund for developing countries), serta monograf komparatif Temasek Holdings dan Khazanah Nasional.
* **Strategi Ingestion:** Mengunduh dokumen panduan prinsip investasi berdampak (*impact investing guidelines*) dan kriteria *additionality* dari repositori resmi Norfund.
* **Teknologi & Library:** `PyMuPDF` + `trafilatura` untuk mengekstrak definisi dan standar evaluasi *additionality*.
* **Penyimpanan Raw:** `data/raw/monographs_books/{lembaga}_{judul_monograf}.pdf`.

---

### Jalur 9: Master Integrasi & Korpus Metadata Terpadu

* **Tujuan:** Mengonsolidasikan seluruh metadata yang diperoleh dari Jalur 1 s.d. 8 ke dalam satu *Single Source of Truth* yang terindeks rapi untuk diserahkan ke pipeline Tahap 2 (ETL 13 Atribut).
* **Strategi Konsolidasi & Resolusi Identitas:**
  1. **Standardisasi ID Bukti (Prefix Format):**
     * Berita Media: `EVID-DNT-NEWS-xxxx`
     * Laporan Tahunan: `EVID-DNT-AR-xxxx`
     * Laporan Keberlanjutan: `EVID-DNT-SR-xxxx`
     * Publikasi NGO: `EVID-DNT-NGO-xxxx`
     * Dokumen Regulasi: `EVID-DNT-REG-xxxx`
     * Open Dataset: `EVID-DNT-DATA-xxxx`
     * Jurnal Ilmiah: `EVID-DNT-ACAD-xxxx`
     * Monograf: `EVID-DNT-BOOK-xxxx`
  2. **Deduplikasi Cepat via MinHash LSH (`datasketch`):**
     * Menghilangkan duplikasi berita sindikasi dengan membandingkan 128 signature MinHash dalam kompleksitas waktu $O(N)$ (menggantikan nested loop $O(N^2)$ lama yang lambat).
     * Ambang batas (*threshold*) kesamaan Jaccard ditetapkan $\ge 0.85$.
  3. **Pemetaan Entitas ke Master Universe 196 BUMN:**
     * Menyelaraskan seluruh variasi nama BUMN di dokumen ke silsilah resmi di `data/processed/bumn_master_clean.csv`.
* **Penyimpanan Data Terpadu:**
  * Format Cepat: `data/processed/master_metadata_corpus.parquet` (kinerja pembacaan kilat di Streamlit).
  * Format Tabular: `data/processed/master_metadata_corpus.csv`.

---

## 4. Protokol Forensik & Integritas Data

1. **Aturan Anti-Hardcoding (100% Dynamic):**
   * Seluruh angka metrik dan ringkasan pada dashboard `pages/1_Scraped_Metadata.py` dihitung secara dinamis dari file data mentah. Tidak ada satu pun angka statistik yang ditulis manual dalam kode.
2. **Kepatuhan Zero Network Call Saat Rendering Streamlit:**
   * Dashboard tidak melakukan koneksi web atau scraping saat pengguna berinteraksi. Seluruh pengumpulan data dilakukan di latar belakang oleh skrip di folder `scripts/01_data_collection/`.
3. **Penyimpanan Hash SHA-256:**
   * Setiap berkas mentah HTML dan PDF di `data/raw/` dicatat nilai hash SHA-256-nya di manifest audit untuk memastikan bukti otentik dan bebas dari perubahan sepihak.

---

## 5. Rangkaian Skrip Sekuensial Ingest Data (`scripts/01_data_collection/`)

Eksekusi teknis pengumpulan data diorganisasikan ke dalam skrip Python independen yang dapat dijalankan secara modular:

* `scripts/01_01_retry_media_stealth.py`: Menyelesaikan unduhan 392 berkas HTML berita media yang tertunda via Puppeteer Stealth.
* `scripts/01_02_ingest_bumn_annual_reports.py`: Mengunduh 28 berkas PDF Annual Report dari 14 BUMN Holding Danantara (2020–2024).
* `scripts/01_03_ingest_sustainability_reports.py`: Mengunduh Sustainability Report emiten BUMN dari IDX.
* `scripts/01_04_ingest_ngo_investigations.py`: Mengkoleksi 50+ laporan investigasi kritis dari 8 NGO (WALHI, JATAM, Trend Asia, dll).
* `scripts/01_05_parse_ruptl_and_regulations.py`: Mengekstrak tabel proyek EBT dari Green RUPTL PLN 2021–2030 dan JETP.
* `scripts/01_06_fetch_open_datasets_esdm_gem.py`: Mengunduh dataset tabular MODI ESDM dan Global Energy Monitor.
* `scripts/01_07_build_master_metadata_corpus.py`: Menjalankan MinHash LSH deduplikasi dan membangun master manifest korpus metadata terpadu lintas 9 jalur.

---

## 6. Kesiapan Handover ke Tahap 2 (ETL 13 Atribut)

Dengan selesainya arsitektur dan skema pengumpulan 9 jalur metadata ini, korpus data mentah yang tersimpan di `data/raw/` telah memiliki kerangka kerja yang solid. Pipeline kemudian siap melanjutkan ke **Tahap 2 (`pages/2_Project_Inventory_ETL.py`)**, di mana teks bersih dari seluruh berkas bukti akan diekstraksi ke dalam skema 13 atribut inventaris proyek hijau menggunakan model Information Extraction (*Pydantic Strict Schema*).

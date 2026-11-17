# Kerangka Desain & Rencana Eksekusi Ingest Data 9 Jalur Metadata (Page 1)
## CELIOS 9: Danantara Monitor & Korpus Bukti Multi-Sumber Proyek Hijau BUMN
**Dokumen Referensi:** `docs/KERANGKA-PAGE-1-INGEST-DATA-9-JALUR-METADATA.md`  
**Target Implementasi Dashboard:** `pages/1_Scraped_Metadata.py`  
**Standar Metodologi Riset:** 100% Mengadopsi Paradigma Investigatif Multi-Sumber CELIOS 2 (D3TLH) & Arsitektur Celios 8 Solar  
**Kepatuhan Aturan:** Mematuhi 5 Standar Mutlak (`no_hardcoded_data`, `strict_data_folder_boundary`, `anti_yesman_methodology_integrity`, `statistical_and_forensic_auditor`, `never_use_destructive_commands`)  
**Penomoran Bab:** Hierarkis Standar Bab 1 (Sub-Bab 1.1 s.d. 1.7)  

---

## 1. Ringkasan Visi, Filosofi, & Paradigma Multi-Sumber Halaman 1

### 1.1 Posisi Sentral Halaman 1 dalam Metodologi CELIOS 9
Halaman **"Hasil Scrape & Metadata Bukti" (`pages/1_Scraped_Metadata.py`)** bertindak sebagai **fondasi empiris dan repositori bukti mentah terverifikasi (*evidence base*)** bagi seluruh ekosistem riset Celios 9 Danantara. 

Sesuai dokumen metodologi resmi (*brief-20260831_Methodological Approach.md* baris 37), riset ini memiliki dua mandat pelacakan utama:
1. **Danantara Monitor (Rentang Waktu $\ge$ 2025):** Melacak pembentukan Badan Pengelola Investasi (BPI) Danantara sebagai Sovereign Wealth Fund (SWF) Indonesia, regulasi pendirian (Keppres/PP), susunan dewan pengawas/direksi, kepemilikan aset jumbo USD 600 miliar, 7 BUMN raksasa tahap awal (pilot cohort), hingga 9 Special Purpose Vehicles (SPV) operasional di Wisma Danantara.
2. **Proyek Hijau BUMN (Rentang Waktu $\ge$ 2020):** Menginventarisasi proyek transisi energi, energi terbarukan, dan dekarbonisasi industri yang diumumkan oleh BUMN Indonesia dalam 5 tahun terakhir lintas 15 kluster proyek.

---

### 1.2 Paradigma Investigatif Multi-Sumber (Adopsi Benchmark Celios 2 D3TLH)
Salah satu temuan paling krusial dari evaluasi metodologi awal adalah: **Berita media massa saja TIDAK CUKUP untuk mengisi 13 atribut inventaris proyek hijau (*Inventory of Green Projects*) secara valid dan ilmiah.**

```
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|                    KETERBATASAN MEDIA MASSA VS KEBUTUHAN DATA CELIOS                             |
|                                                                                                  |
|  [ Media Massa & Berita Kredibel ]                                                               |
|  • Sangat unggul untuk: Nama Proyek, BUMN Pelaksana, Tanggal Rilis, Status Seremonial (MoU/LoI). |
|  • SANGAT LEMAH / TIDAK ADA: Detail Capex mengikat, Kapasitas riil, Struktur kepemilikan saham,   |
|    dan yang paling fatal: RISIKO LINGKUNGAN DAN SOSIAL (ATRIBUT 12).                             |
|                                                                                                  |
|                                       VS                                                         |
|                                                                                                  |
|  [ Paradigma Multi-Sumber CELIOS 2 D3TLH ]                                                       |
|  Untuk menghasilkan riset investigatif kredibel, Celios wajib "menyelam" ke 9 Jalur Metadata:   |
|  1. Media Massa      4. Laporan Keberlanjutan   7. Open Dataset Spasial                          |
|  2. Laporan Tahunan  5. Publikasi / Advokasi NGO 8. Jurnal Ilmiah / Policy Paper                |
|  3. Regulasi & RUPTL 6. Laporan Keuangan IDX     9. Buku & Monograf Tata Kelola SWF              |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
```

Khusus untuk **Atribut 12 (`Environment and social risks`)**, siaran pers korporasi BUMN dan berita advertorial hampir **100% melakukan *greenwashing***—tidak pernah membeberkan konflik agraria, tumpang tindih lahan adat, kriminalisasi warga lokal, pencemaran daerah aliran sungai (DAS), atau deforestasi. Oleh karena itu, pengumpulan dokumen laporan investigasi masyarakat sipil (**WALHI, JATAM, Trend Asia, Auriga Nusantara, KPA, AMAN**) menjadi syarat mutlak metodologis, persis seperti metodologi yang terbukti sukses diterapkan pada proyek riset CELIOS 2 D3TLH.

---

### 1.3 Alur Kausalitas Tiga Tahap Riset (Graphic 1 Pipeline)
Halaman 1, 2, dan 3 saling terikat secara berurutan dan tidak boleh dicampuradukkan:

```
┌─────────────────────────────────┐
│           HALAMAN 1             │
│   HASIL SCRAPE & METADATA BUKTI │ ──> Mengumpulkan & memverifikasi korpus dokumen mentah
│    (9 Jalur Metadata Dokumen)   │     dari media massa, NGO, laporan BUMN, dan regulasi.
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│           HALAMAN 2             │
│   ETL & EKSTRAKSI 13 ATRIBUT    │ ──> Membedah teks bersih berkas bukti untuk mempopulasikan
│  (Database Inventaris Proyek)   │     13 kolom atribut proyek ke dalam 6 sektor ekonomi.
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│           HALAMAN 3             │
│  SKRINING 3-GATE & GREEN LIST   │ ──> Menyaring inventaris proyek melalui 3 gerbang eliminasi:
│ (Portofolio Rekomendasi Hijau)  │     Negative Filter, TKBI v3/ASEAN v4, dan Norfund Additionality.
└─────────────────────────────────┘
```

---

## 2. Struktur Visual & Komponen Antarmuka Dashboard (UI/UX Page 1)

Sesuai standar antarmuka Celios 8 Solar (`docs/KERANGKA-PAGE-1-PEMETAAN-POTENSI.md`), Halaman 1 dibangun dengan hierarki visual yang ketat:

### 2.1 Identitas Header
* **Org Badge Institusi:** `<div class="org-badge">CELIOS — CENTER OF ECONOMIC AND LAW STUDIES</div>`  
  *Warna teks putih, latar belakang hijau gelap `#2E7D32`, sudut melengkung kapsul (`border-radius: 20px`), teks uppercase.*
* **Main Title:** `Hasil Scrape & Metadata Bukti`  
  *Font 2.4rem, bold 800, warna hijau terang `#66BB6A`.*
* **Sub-Title Deskriptif:**  
  `Tahap 1: Korpus 1.754+ Dokumen Bukti Publikasi Terverifikasi — Danantara Monitor & Proyek Hijau BUMN Lintas 9 Jalur Metadata`
* **Dropdown Metodologi (Accordion Expander):**  
  Penjelasan resmi mengenai batasan rentang waktu riset TOR CELIOS, dasar yuridis pemisahan data, dan tautan dokumen metodologi.

### 2.2 Hero Metric Cards (4 Pilar Agregat Dinamis Tanpa Hardcode)
Menggunakan Bento Card bersudut lengkung dengan highlight hover `#4CAF50`:
1. **Bento Card 1:** *Total Bukti Publikasi* (`1,754 Dokumen`) — Terhitung dinamis dari `master_urls_manifest.csv`.
2. **Bento Card 2:** *Danantara Monitor ($\ge$ 2025)* (`851 Dokumen`) — Dokumen struktur kelembagaan, kepemilikan aset, dan regulasi Danantara.
3. **Bento Card 3:** *Proyek Hijau BUMN ($\ge$ 2020)* (`903 Dokumen`) — Pengumuman proyek rendah karbon 9 grup BUMN champion.
4. **Bento Card 4:** *Penerbit / Sumber Kredibel* (`154 Media & Lembaga`) — Jumlah penerbit unik terverifikasi.

### 2.3 Kontrol Filter Multi-Dimensi
Disusun dalam dua baris responsif yang elegan:
* **Baris 1:**
  * **Dropdown Jalur Metadata (9 Opsi):** Mengendalikan apakah dashboard menampilkan korpus berita media aktif atau profil kerangka kerja penyelaman multi-sumber non-media.
  * **Dropdown Track Riset:** `Semua Track`, `Danantara Monitor (>= 2025)`, `Proyek Hijau BUMN (>= 2020)`.
  * **Dropdown Kluster Proyek:** 15 kluster resmi SOW CELIOS (Solar, Air, Angin, Bioenergi, Panas Bumi Pensiun Dini, Hidrogen, Transmisi/Grid, Baterai & EV, CCUS, Dekarbonisasi Industri, Efisiensi Energi, Perhutanan/Solusi Berbasis Alam, Pertanian Berkelanjutan, Pengelolaan Sampah & Sirkular, Pembiayaan Hijau).
* **Baris 2:**
  * **Dropdown Tahun Publikasi:** 2020 s.d. 2026.
  * **Text Input Pencarian Terpadu:** Pencarian lintas judul artikel, BUMN target, penerbit, dan ID bukti.

---

## 3. Rincian Hierarkis Sub-Bab (Peta Rencana Kerja Halaman 1)

```
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|                    PETA STRUKTUR SUB-BAB KERANGKA INGEST DATA HALAMAN 1                          |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 1.1: ARSITEKTUR KORPUS JALUR 1 (MEDIA MASSA & BERITA KREDIBEL - 1.754 DOKUMEN AKTIF)    |
|  1.1.1 Target Portal & Kriteria Inklusi Jurnalisme Investigatif                                  |
|  1.1.2 Mesin Ingestion: Google News RSS Dorking, Canonical Resolving, & Puppeteer Stealth Engine |
|  1.1.3 Preservasi Bukti Fisik Mentah HTML (1.362 Berkas Tersimpan & Manifest Kegagalan 392 URL) |
|  1.1.4 Data Lineage: `master_urls_manifest.csv` & `html_download_log.csv`                        |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 1.2: ARSITEKTUR JALUR 2 & 3 (LAPORAN TAHUNAN & LAPORAN KEBERLANJUTAN BUMN)              |
|  1.2.1 Target 14 Holding BUMN di Bawah Danantara (PLN, Pertamina, MIND ID, Semen Indonesia, dll) |
|  1.2.2 Ekstraksi Laporan Keuangan Diaudit (CALK) untuk Atribut 3, 7, 8, dan 9                   |
|  1.2.3 Laporan Keberlanjutan Standar GRI & POJK 51 untuk Target Emisi Scope 1, 2, 3 (Atribut 11) |
|  1.2.4 Pipeline Ingestion: PDF Harvester & Table Parser (`pdfplumber` / `PyMuPDF`)               |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 1.3: ARSITEKTUR JALUR 4 (PUBLIKASI NGO & LAPORAN ADVOKASI LINGKUNGAN / SOSIAL)          |
|  1.3.1 Target Lembaga Sipil: WALHI, JATAM, Trend Asia, Auriga Nusantara, KPA, AMAN, ICW, PWYP   |
|  1.3.2 Pemenuhan Mutlak Atribut 12: Konflik Agraria, Kriminalisasi, Pencemaran DAS, Deforestasi |
|  1.3.3 Skema Metadata Dokumen Advokasi & Pembentukan Korpus Bukti Kritis                        |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 1.4: ARSITEKTUR JALUR 5 & 6 (REGULASI, RUPTL, CIPP JETP, & OPEN DATASET INDUSTRI)       |
|  1.4.1 Regulasi Resmi Pembentukan Danantara (JDIH Setneg, PP/Keppres, BPK)                      |
|  1.4.2 Dokumen Perencanaan: RUPTL PLN 2021–2030 (Jadwal COD & Pembangkit EBT) & CIPP JETP        |
|  1.4.3 Open Dataset Spasial: MODI Minerba ESDM, Ditjen EBTKE, & Global Energy Monitor (GEM)      |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 1.5: ARSITEKTUR JALUR 7 & 8 (JURNAL ILMIAH, POLICY PAPER, & BUKU MONOGRAF RISET)       |
|  1.5.1 Basis Akademis Valuasi Ekonomi Hijau & Dampak Fiskal Danantara (SINTA/Scopus/LPEM/CSIS)  |
|  1.5.2 Studi Komparasi Sovereign Wealth Fund Global (Temasek, Khazanah, Santiago Principles)    |
|  1.5.3 Fondasi Metodologis Uji Additionality Norfund (Prinsip Gate 3 Brief CELIOS)               |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 1.6: ALGORITMA DEDUPLIKASI LINTAS SUMBER & NORMALISASI ENTITAS                          |
|  1.6.1 Masalah Berita Sindikasi & Eliminasi Redundansi Berbiaya O(N) via MinHash LSH             |
|  1.6.2 Normalisasi Nama Entitas BUMN Menggunakan Master Universe 196 Entitas                    |
|  1.6.3 Standarisasi Prefix Identifikasi Bukti (`EVID-DNT-NEWS-xxxx`, `EVID-DNT-NGO-xxxx`, dll)   |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 1.7: PROTOKOL PRESERVASI FORENSIK, AUDIT TRAIL, & JADWAL KERJA BACKLOG                 |
|  1.7.1 Standar Integritas Hash SHA-256 untuk Setiap Berkas Mentah di Disk Lokal                  |
|  1.7.2 Kepatuhan Zero Network Call Saat Rendering Dashboard Streamlit                            |
|  1.7.3 Backlog Sekuensial Penyelesaian Ingest Data Menuju Tahap 2 (ETL 13 Atribut)               |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
```

---

## 4. Sub-Bab 1.1: Arsitektur Korpus Jalur 1 (Media Massa & Berita Kredibel)

### 4.1 Status Realisasi Saat Ini (1.754 Dokumen Terverifikasi)
Jalur 1 telah berhasil dikurasi dan disaring mematuhi batasan rentang waktu resmi TOR CELIOS:
* **Track A — Danantara Monitor:** 851 artikel terbit tahun 2025 s.d. 2026.
* **Track B — Proyek Hijau BUMN:** 903 artikel terbit tahun 2020 s.d. 2026.
* **Audit Batasan Waktu:** Sebanyak **1.458 URL artikel sampah/di luar rentang waktu** telah diaudit dan dikeluarkan secara transparan ke berkas `data/raw/evidence_dorking/urls_excluded_time_series.csv`.

### 4.2 Mesin Ingestion & Bypass Redirect Google News
Untuk mengatasi proteksi anti-bot dan halaman redirect perantara `news.google.com`, pipeline mengintegrasikan dua lapis mesin:
1. **Protokol Resolving URL Kanonikal:** Memecah base64 protobuff Google News menjadi URL asli penerbit berita (Katadata, Kompas, CNBC Indonesia, Antaranews, Bisnis.com, Tempo, Kumparan, Bloomberg, dll.).
2. **Puppeteer Stealth Headless Engine (`tools/puppeteer_engine/stealth_fetcher.js`):** Menembus portal berita berproteksi Cloudflare/WAF dan mengekstrak berkas HTML murni beserta URL kanonikal langsung dari elemen `<link rel="canonical">`.

### 4.3 Log Audit Bukti Fisik Mentah HTML
* **Lokasi Penyimpanan Disk Lokal:** `data/raw/evidence_dorking/html/{evidence_id}_{slug}.html`
* **Capaian Download Fisik:** **1.362 berkas HTML (77,65%)** telah tersimpan utuh di disk lokal.
* **Manifest Kegagalan & Retry:** Sebanyak **392 URL** tercatat dalam `data/raw/evidence_dorking/failed_download_manifest.csv` akibat pembatasan koneksi sementara dan siap dijalankan ulang menggunakan mesin Puppeteer Stealth.

---

## 5. Sub-Bab 1.2: Arsitektur Jalur 2 & 3 (Laporan Tahunan & Laporan Keberlanjutan BUMN)

### 5.1 Target 14 BUMN Holding di Bawah Danantara
Laporan Tahunan (*Annual Report*) dan Laporan Keberlanjutan (*Sustainability Report*) adalah dokumen legal resmi yang diaudit oleh Akuntan Publik terdaftar dan otoritas bursa (IDX/OJK). Dokumen ini menjadi sumber data primer untuk 4 dari 13 atribut CELIOS:

| No | Entitas Holding BUMN Target | Kluster Sektoral | Peran Spesifik dalam 13 Atribut CELIOS |
| :---: | :--- | :--- | :--- |
| 1 | **PT PLN (Persero)** | Energy / Ketenagalistrikan | Pembangkit EBT, jaringan transmisi, Capex pensiun PLTU |
| 2 | **PT Pertamina (Persero)** | Energy / Bioenergi & Geotermal | Kilang hijau, biofuel, geotermal PGE, hidrogen hijau |
| 3 | **MIND ID (Inalum, Aneka Tambang, PTBA, Timah, Freeport)** | Downstream / Hilirisasi Mineral | Smelter nikel/tembaga rendah karbon, PLTS pasca tambang |
| 4 | **PT Semen Indonesia (Persero) Tbk (SIG)** | Manufacturing / Bahan Bangunan | Semen rendah karbon, substitusi bahan bakar RDF |
| 5 | **PT Pupuk Indonesia (Persero)** | Manufacturing / Kimia | Green ammonia, green hydrogen untuk pabrik pupuk |
| 6 | **PTPN III (Holding Perkebunan)** | Agriculture / Bioenergi | Bioetanol tebu, biomassa cangkang sawit, reforestasi |
| 7 | **PT Bank Rakyat Indonesia (Persero) Tbk (BRI)** | Financial / Pembiayaan Berkelanjutan | Portofolio kredit hijau KKUB POJK 51, obligasi hijau |
| 8 | **PT Bank Mandiri (Persero) Tbk** | Financial / Pembiayaan Berkelanjutan | ESG financing, pembiayaan sindikasi proyek EBT |
| 9 | **PT Bank Negara Indonesia (Persero) Tbk (BNI)** | Financial / Pembiayaan Berkelanjutan | Green loan korporasi BUMN, pembiayaan transisi energi |
| 10 | **PT Telkom Indonesia (Persero) Tbk** | Infrastructure / Digital | Green data center, efisiensi energi menara BTS |
| 11 | **PT Kereta Api Indonesia (Persero) (KAI)** | Infrastructure / Transportasi Rel | Elektrifikasi jalur rel, efisiensi energi logistik |
| 12 | **PT ASDP Indonesia Ferry (Persero)** | Infrastructure / Transportasi Laut | Elektrifikasi dermaga, armada kapal feri hibrida |
| 13 | **PT InJourney (Aviasi Pariwisata Indonesia)** | Infrastructure / Bandara Hijau | Green airport operation, efisiensi energi terminal |
| 14 | **PT Bio Farma (Persero)** | Healthcare / Manufaktur | Efisiensi fasilitas manufaktur farmasi ramah lingkungan |

### 5.2 Strategi Ingestion & Parsing Tabel Keuangan
* **Skrip Ingestion:** `scripts/01_ingest_annual_reports.py`
* **Metode:** Mengunduh berkas PDF laporan resmi tahun 2020 s.d. 2024 dari menu *Investor Relations* masing-masing situs resmi BUMN atau keterbukaan informasi Bursa Efek Indonesia (IDX).
* **Lokasi Penyimpanan Raw:** `data/raw/annual_reports/pdf/{tahun}_{kode_bumn}_annual_report.pdf`
* **Ekstraksi Khusus:** Membaca Catatan Atas Laporan Keuangan (CALK) bagian *Aset Tetap Dalam Konstruksi*, *Penyertaan Saham Anak Perusahaan/SPV*, dan *Segmen Usaha Berkelanjutan*.

---

## 6. Sub-Bab 1.3: Arsitektur Jalur 4 (Publikasi NGO & Laporan Advokasi Lingkungan/Sosial)

### 6.1 Landasan Kebutuhan Investigatif
Siaran pers BUMN dan media arus utama hampir tidak pernah mencatat dampak negatif proyek hijau. Untuk memenuhi **Atribut 12 (`Environment and social risks`)**, CELIOS mengadopsi metodologi riset investigasi CELIOS 2 D3TLH dengan mengkoleksi dokumen dari 8 organisasi masyarakat sipil terdepan:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                   8 LEMBAGA MASYARAKAT SIPIL (NGO) PRIORITAS CELIOS 9                            │
├────────────────────────────────┬─────────────────────────────────────────────────────────────────┤
│ Lembaga Mitra / Sumber Target  │ Fokus Isu Spesifik terhadap Proyek BUMN & Danantara              │
├────────────────────────────────┼─────────────────────────────────────────────────────────────────┤
│ 1. WALHI (Nasional & Daerah)   │ Pencemaran lingkungan hidup, AMDAL bermasalah, deforestasi      │
│ 2. JATAM (Jaringan Tambang)    │ Kerusakan ekologis hilirisasi nikel/batu bara, perampasan ruang │
│ 3. Trend Asia                  │ Kritik transisi energi semu (co-firing biomassa, CCS, nuklir)   │
│ 4. Auriga Nusantara            │ Investigasi tutupan lahan, deforestasi konsesi, kepemilikan aset│
│ 5. KPA (Pembaruan Agraria)     │ Konflik agraria, tumpang tindih tanah BUMN PTPN/Perhutani       │
│ 6. AMAN (Masyarakat Adat)      │ Pelanggaran wilayah adat proyek geotermal/PLTA/hilirisasi       │
│ 7. ICW (Corruption Watch)      │ Potensi benturan kepentingan, tata kelola & transparansi SWF    │
│ 8. PWYP Indonesia              │ Transparansi pendapatan ekstraktif & akuntabilitas transisi     │
└────────────────────────────────┴─────────────────────────────────────────────────────────────────┘
```

### 6.2 Skema Data Korpus Advokasi NGO (`data/raw/ngo_publications/`)
Setiap dokumen advokasi diindeks dengan atribut metadata ketat:
* `doc_id`: `EVID-DNT-NGO-xxxx`
* `ngo_name`: Nama organisasi penerbit.
* `report_title`: Judul laporan investigasi atau *policy brief*.
* `publication_date`: Tanggal publikasi dokumen.
* `targeted_soe_or_project`: Nama proyek BUMN yang diinvestigasi.
* `risk_category`: Klasifikasi risiko (*Land Conflict*, *Water Pollution*, *Deforestation*, *Indigenous Rights Violation*, *Labor Exploitation*).
* `summary_findings`: Ringkasan temuan bukti pelanggaran sosial/lingkungan.
* `file_path`: Tautan berkas PDF lokal di `data/raw/ngo_publications/pdf/`.

---

## 7. Sub-Bab 1.4: Arsitektur Jalur 5 s.d. 8 (Regulasi, Open Data, Jurnal, & Monograf)

### 7.1 Jalur 5: Regulasi & Dokumen Perencanaan Pembangunan
* **JDIH Setneg & Kemenkeu:** Mengunduh berkas regulasi resmi pendirian BPI Danantara (Peraturan Pemerintah, Keputusan Presiden, Peraturan Menteri BUMN).
* **RUPTL PLN 2021–2030 (Green RUPTL):** Buku Rencana Usaha Penyediaan Tenaga Listrik PT PLN (Persero). Menjadi acuan mutlak untuk:
  * Nama resmi seluruh proyek pembangkit EBT yang masuk daftar rencana pemerintah.
  * Target kapasitas teknis megawatt (MW).
  * Jadwal target operasi komersial (*Commercial Operation Date / COD*).
* **Dokumen CIPP JETP Indonesia:** *Comprehensive Investment and Policy Plan* Sekretariat Just Energy Transition Partnership (JETP) bernilai USD 20 miliar untuk memetakan proyek BUMN yang diusulkan mendapat pendanaan transisi internasional.

### 7.2 Jalur 6: Open Dataset Pemerintah & Industri
* **MODI ESDM (Minerba One Data Indonesia):** Memverifikasi status izin usaha pertambangan (IUP/IUPK) milik holding tambang BUMN (MIND ID, Antam, Bukit Asam, Timah, Freeport).
* **Portal Satu Data EBTKE ESDM:** Data operasional pembangkit panas bumi, surya, hidro, dan bioenergi terpasang di Indonesia.
* **Global Energy Monitor (GEM Trackers):** Mengintegrasikan koordinat lintang/bujur (*latitude/longitude*) pembangkit listrik dan smelter industri untuk verifikasi spasial Atribut 6 (Location).

### 7.3 Jalur 7 & 8: Jurnal Ilmiah, Policy Paper, & Monograf SWF
* **Jurnal Terindeks SINTA 1–2 & Scopus:** Paper ilmiah terkait valuasi ekonomi hijau, pemodelan IRIO dampak pembentukan Danantara terhadap PDB dan penyerapan tenaga kerja.
* **Publikasi Lembaga Kebijakan Terkemuka:** Dokumen riset LPEM FEB UI, CSIS Indonesia, IESR, dan arsip internal riset CELIOS terdahulu.
* **Monograf Tata Kelola SWF Global:** Studi komparasi standar *Santiago Principles*, kerangka Norfund Additionality (*Norwegian Investment Fund*), dan tata kelola Temasek Holdings Singapura serta Khazanah Nasional Malaysia untuk menyusun rekomendasi mitigasi risiko *moral hazard* Danantara.

---

## 8. Sub-Bab 1.5: Algoritma Deduplikasi & Normalisasi Lintas Sumber

### 8.1 Eliminasi Redundansi Sindikasi via MinHash LSH
Pada riset `2. Celios`, perbandingan teks dilakukan secara berpasangan (*pairwise cosine similarity*) menggunakan nested loop $O(N^2)$, yang menyebabkan sistem membeku pada volume ribuan artikel.

Untuk Celios 9 Danantara, pipeline menerapkan algoritma **Locality-Sensitive Hashing (LSH)** berbasis pustaka `datasketch`:
* **Kompleksitas Komputasi:** Dipangkas dari $O(N^2)$ menjadi **$O(N)$**.
* **Metode Fingerprinting:** Mengonversi teks artikel bersih menjadi 128 permutasi MinHash signature.
* **Ambang Batas (Threshold):** Menetapkan Jaccard similarity $\ge 0.85$ untuk mengelompokkan berita sindikasi (misal 1 rilis ANTARA yang diterbitkan ulang oleh 40 portal daerah).
* **Resolusi Kluster:** Memilih 1 artikel dengan teks paling lengkap sebagai *Canonical Master Article*, sementara 39 artikel lainnya dicatat sebagai *Syndicated Duplicates* tanpa menghapus rekam jejak jangkauan media.

### 8.2 Normalisasi Nama BUMN ke Silsilah Resmi 196 Entitas
Setiap penyebutan entitas di media (seperti *"PLN Nusantara Power"*, *"PT PJB"*, *"Indonesia Power"*, *"PLN IP"*) dinormalisasi secara otomatis merujuk ke tabel induk `data/processed/bumn_master_clean.csv`:
* Menentukan BUMN Induk (Holding Tier).
* Menentukan Anak Perusahaan / SPV (Operating Subsidiary Tier).
* Mencegah fragmentasi data akibat variasi singkatan jurnalisme.

---

## 9. Sub-Bab 1.6: Protokol Preservasi Forensik & Kepatuhan Arsitektur

### 9.1 Standar Anti-Hardcoding (100% Dynamic Loading)
* Seluruh angka agregat, metrik persentase, dan jumlah dokumen pada Halaman 1 **wajib dihitung langsung secara dinamis** dari file CSV/Parquet di `data/`.
* Dilarang keras menaruh angka mentah di dalam kode Python (seperti `total_articles = 1754`). Setiap kali file dataset diperbarui, UI Streamlit harus secara otomatis mencerminkan angka terbaru.

### 9.2 Kepatuhan Zero Network Call Saat Rendering Streamlit
* Halaman `pages/1_Scraped_Metadata.py` **dilarang melakukan web scraping langsung atau HTTP request ke internet** saat pengguna membuka atau memfilter dashboard.
* Seluruh scraping dan pengunduhan file mentah harus diselesaikan di latar belakang oleh skrip di folder `scripts/01_data_collection/` dan disimpan di disk lokal `data/raw/`. Dashboard murni bertindak sebagai antarmuka pembaca data lokal (*offline-first dashboard*).

### 9.3 Integritas Hash SHA-256
Untuk menjamin bukti tidak dimanipulasi (*tamper-proof*), setiap berkas HTML dan PDF mentah yang disimpan di `data/raw/` dihitung nilai hash SHA-256-nya dan dicatat ke dalam log manifest induk.

---

## 10. Sub-Bab 1.7: Jadwal Eksekusi Sekuensial & Backlog Kerja Halaman 1

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                     JADWAL KERJA SEKUENSIAL INGEST DATA HALAMAN 1                                │
├───────┬──────────────────────────────────────────┬─────────────────────────────┬─────────────────┤
│ Tahap │ Rincian Tugas & Deliverable Teknis       │ Skrip / Modul Eksekusi      │ Status Target   │
├───────┼──────────────────────────────────────────┼─────────────────────────────┼─────────────────┤
│ 1.1   │ Retry 392 berkas HTML media yang gagal   │ `scripts/01_retry_html.py`  │ Prioritas 1     │
│       │ menggunakan Puppeteer Stealth Engine.    │ (Puppeteer Stealth)         │                 │
├───────┼──────────────────────────────────────────┼─────────────────────────────┼─────────────────┤
│ 1.2   │ Harvesting 28 Laporan Tahunan BUMN       │ `scripts/01_ingest_ar.py`   │ Prioritas 2     │
│       │ (14 Holding BUMN x 2 tahun 2023–2024).   │ (PDF Harvester IR BUMN)     │                 │
├───────┼──────────────────────────────────────────┼─────────────────────────────┼─────────────────┤
│ 1.3   │ Kurasi 50 Laporan Investigasi Kritis     │ `scripts/01_ingest_ngo.py`  │ Prioritas 3     │
│       │ dari 8 NGO (WALHI, JATAM, Trend Asia).   │ (PDF NGO Harvester)         │ (Isi Atribut 12)│
├───────┼──────────────────────────────────────────┼─────────────────────────────┼─────────────────┤
│ 1.4   │ Ekstraksi tabel proyek EBT dari Green    │ `scripts/01_parse_ruptl.py` │ Prioritas 4     │
│       │ RUPTL PLN 2021–2030 & Dokumen CIPP JETP. │ (PDF Table Extractor)       │                 │
├───────┼──────────────────────────────────────────┼─────────────────────────────┼─────────────────┤
│ 1.5   │ Deduplikasi korpus berita via MinHash    │ `src/nlp/deduplication.py`  │ Prioritas 5     │
│       │ LSH untuk memetakan kluster sindikasi.   │ (MinHash LSH $O(N)$)        │                 │
├───────┼──────────────────────────────────────────┼─────────────────────────────┼─────────────────┤
│ 1.6   │ Pembentukan Master Metadata Corpus CSV   │ `scripts/01_build_master.py`│ Prioritas 6     │
│       │ lintas 9 jalur sebagai input Tahap 2.   │                             │ (Handover ETL)  │
└───────┴──────────────────────────────────────────┴─────────────────────────────┴─────────────────┘
```

---

## 11. Kesimpulan & Kesiapan Handover ke Tahap 2 (ETL 13 Atribut)

Dokumen kerangka kerja ini membakukan seluruh spesifikasi teknis dan metodologis untuk **Halaman 1: Hasil Scrape & Metadata Bukti**. Dengan mengintegrasikan 9 jalur metadata dokumen, CELIOS memastikan bahwa korpus data yang dikumpulkan memiliki dasar ilmiah yang kokoh, seimbang (*checks and balances* antara klaim korporasi BUMN dan investigasi masyarakat sipil), serta memenuhi standar replikabilitas riset internasional.

Setelah seluruh korpus bukti pada Halaman 1 terkompilasi dan tersimpan di `data/raw/`, pipeline akan siap dilanjutkan ke **Tahap 2 (`pages/2_Project_Inventory_ETL.py`)** untuk mengekstrak dan mempopulasikan 13 atribut inventaris proyek hijau menggunakan model Information Extraction (*Pydantic Strict Schema*).

# Laporan Evaluasi Arsitektur Scraping & Rencana Implementasi Pipeline Data Celios 9 (Danantara)

**Tanggal:** 16 November 2026  
**Dokumen:** `docs/report_plan_scraper_engine_danantara.md`  
**Proyek:** Celios 9 Danantara Monitor (Green Investment List)  
**Kepatuhan:** Sesuai Pedoman Mutlak [`.agents/rules`](../.agents/rules)  

---

## 1. Ringkasan Eksekutif

Dokumen ini memuat audit teknis komparatif antara struktur folder proyek **Celios 8 Solar Panel** (`23. Celios8-solarpanel`) dan sistem pemantauan di **2. Celios** (`client/2. Celios/dev`). Laporan ini membedah akar permasalahan (*root causes*) mengapa *pipeline* di `2. Celios` mengalami hambatan besar (*bottleneck*) pada proses pembersihan data (*cleaning*) dan redundansi data, serta merumuskan **rencana arsitektur dan mesin ekstraksi modern (*frontier engines*)** berbasis repositori teruji di GitHub untuk diimplementasikan pada proyek **Celios 9 Danantara**.

---

## 2. Benchmarking Struktur Proyek Celios 8 Solar Panel (`23. Celios8-solarpanel`)

Proyek Celios 8 menerapkan standar arsitektur modular yang rapi, mematuhi prinsip *Separation of Concerns* (SoC), dan menjadi acuan tata kelola repositori untuk Celios 9:

```text
C:\Users\yooma\OneDrive\Desktop\duniahub\client\23. Celios8-solarpanel\
├── .agents/rules/        # Aturan metodologi, anti-yes-man, zero hardcoded
├── ref/                  # Dokumen brief, referensi akademis, feedback metodologi
├── data/                 # Single Source of Truth
│   ├── raw/              # Berkas bukti fisik mentah (per kategori/sumber)
│   ├── processed/        # Data bersih terstruktur hasil olah (CSV/Parquet)
│   └── external/         # Data unduhan API eksternal
├── docs/                 # Dokumentasi teknis, metodologi, dan log rapat
├── scripts/              # Pipeline sekuensial bernomor (01 s/d 05):
│   ├── 01_data_collection/
│   ├── 02_gis_processing/
│   ├── 03_calculation/
│   ├── 04_financial_modeling/
│   └── 05_visualization/
├── src/                  # Modul Python murni (reusable functions, pure logic)
├── output/               # Deliverables akhir (charts, datasets, maps, reports)
├── Infografis/           # Aset visual untuk kebutuhan publikasi
└── tools/                # Utility & parser (seperti parser_opendataloader)
```

### Keunggulan yang Diadopsi untuk Celios 9:
1. **Pipeline Bertahap Bernomor (`scripts/01_` s/d `05_`):** Memisahkan alur pengumpulan data, pembersihan, ekstraksi terstruktur, pemodelan, hingga visualisasi ke dalam skrip mandiri, mencegah terjadinya file monolitik raksasa.
2. **Pemisahan `src/` vs `scripts/`:** Fungsi logika inti (*pure functions*) berada di `src/`, sementara skrip di `scripts/` murni memanggil fungsi dan membaca/menulis data.
3. **Kepatuhan Batasan Data (`data/`):** Terdapat pemisahan tegas antara `data/raw/` (bukti forensik) dan `data/processed/` (data siap analisis).

---

## 3. Bedah Forensik Mekanisme Scraping & Akar Masalah di `2. Celios`

Pada repositori `client/2. Celios/dev`, sistem dibangun untuk memantau 15 perusahaan tambang/komoditas dengan arsitektur:
* **Search Engine:** Local SearXNG instance (Docker port 8080).
* **Strategi Kueri:** Dual search (Kueri Boolean `"Nama PT" AND ("limbah" OR "konflik")` + Google Dorking `site:mongabay.co.id "Nama PT"`).
* **Ekstraktor Konten:** `newspaper3k` dengan fallback ke `BeautifulSoup` standar (`requests.get`).
* **Pipeline Pemrosesan:** Terkonsentrasi dalam satu file monolitik [**`pipeline.py`**](file:///C:/Users/yooma/OneDrive/Desktop/duniahub/client/2.%20Celios/dev/pipeline.py) sepanjang **2.550 baris**.

### Empat (4) Akar Masalah Utama di `2. Celios`:

```
[1. Kueri SearXNG Luas] ──> [2. Masuk Ribuan Sampah] ──> [3. Extractor Usang] ──> [4. Regex 100+ Kata] ──> [5. Loop O(N^2) Freezing]
  (Bocoran Loker/Skripsi)     (Teks Navigasi/Iklan Masuk)    (newspaper3k/BS4)      (Anti-Pattern Kucing-Tikus)  (SBERT/SequenceMatcher)
```

### 1. *Upstream Pollution* (Kueri Terlalu Liar & Mengambil Sampah Web)
* SearXNG menyebarkan kueri ke puluhan mesin pencari tanpa pembatasan domain yang terkurasi.
* Hasilnya ribuan artikel sampah masuk ke database: **lowongan kerja (loker), skripsi mahasiswa (Bab I, Bab II), obituari/berita duka peracik bumbu, kuis/resep masakan, dan siaran pers korporat**.

### 2. *Jebakan Heuristik Regex Ad-hoc* (`IRRELEVANT_KEYWORDS`)
* Di baris 657–684 `pipeline.py`, terdapat daftar `IRRELEVANT_KEYWORDS` berisi 100+ kata kunci yang di-hardcode (`'loker'`, `'skripsi'`, `'nuansa romantis'`, `'peracik bumbu'`, dll.).
* **Kelemahan Fatal:** Setiap kali muncul variasi konten sampah baru, pengembang terpaksa menambahkan kata kunci baru secara manual. Pola "kucing dan tikus" ini menyebabkan baris kode membengkak dan melanggar prinsip *No Reinventing The Wheel*.

### 3. *Content Extractor* Usang (`newspaper3k` & Naive BS4)
* `newspaper3k` sudah tidak aktif dirawat dan gagal memproses halaman web modern berbasis JavaScript/Client-Side Rendering (Next.js, React SPA) serta situs berproteksi Cloudflare/WAF.
* Fallback `BeautifulSoup` hanya menyapu seluruh tag `<p>`, sehingga teks menu navigasi (*header/footer*), banner persetujuan *cookie*, dan daftar berita terkait di *sidebar* ikut terserap sebagai isi berita. Hal ini mengotori teks yang akan dianalisis.

### 4. *Bottleneck* Deduplikasi Berbiaya $O(N^2)$ (Nested Loop)
* Di baris 1920–1967 `pipeline.py`, deduplikasi artikel dilakukan dengan membandingkan teks satu per satu menggunakan **nested loop ($N \times N$)**:
  * Menghitung pairwise cosine similarity menggunakan SBERT / `SequenceMatcher`.
* Untuk 1.000 artikel, dibutuhkan **~500.000 kali komputasi perbandingan**. Pada volume 3.000–5.000 artikel, pipeline mengalami pembekuan (*freezing*).
* Berita sindikasi (misal 1 rilis ANTARA disalin oleh 40 portal berita lokal) memiliki teks tubuh 80% identik namun judul berbeda, sehingga sering lolos dari filter atau sebaliknya menghapus data yang salah.

---

## 4. Komparasi Frontier Scraping & Extraction Engines di GitHub (2025/2026)

Untuk proyek Celios 9 Danantara, kita mengganti teknologi usang dengan pustaka standar industri terkini:

| Engine / Library | Repositori GitHub | Keunggulan Utama | Implementasi pada Celios 9 |
| :--- | :--- | :--- | :--- |
| **Crawl4AI** *(Top Frontier Local)* | [`unclecode/crawl4ai`](https://github.com/unclecode/crawl4ai) | • 100% open-source, gratis, jalan lokal via Playwright.<br>• Menghasilkan **Clean Markdown murni** (otomatis membuang nav, ads, cookie banners, script).<br>• Mampu mengeksekusi JavaScript, infinite scroll, dan bypass bot. | **Ekstraktor Utama (Halaman Dinamis):** Crawling website BUMN & portal berita modern tanpa biaya API. |
| **Trafilatura** *(Python Library)* | [`adbar/trafilatura`](https://github.com/adbar/trafilatura) | • Standar emas akademis untuk *content extraction*.<br>• Presisi tertinggi memisahkan teks artikel utama dari boilerplate tanpa perlu overhead browser headless. | **Ekstraktor Cepat (Halaman Statis):** Menggantikan `newspaper3k` & BS4 untuk ribuan artikel berita teks. |
| **Firecrawl** *(Turnkey SaaS / Docker)* | [`mendableai/firecrawl`](https://github.com/mendableai/firecrawl) | • Mengubah URL web apa pun menjadi Clean Markdown & Structured JSON.<br>• Sangat tangguh menembus Cloudflare/Akamai enterprise. | **Alternatif Turnkey:** Dipakai jika ada endpoint web BUMN yang menerapkan proteksi WAF ketat. |
| **Scrapling** *(Adaptive Stealth)* | [`D4Vinci/Scrapling`](https://github.com/D4Vinci/Scrapling) | • Library stealth anti-detect dengan selector cerdas.<br>• Tidak rusak saat struktur HTML website target berubah. | Scraping portal regulasi pemerintah (JDIH, BPK, Setneg). |
| **MinHash LSH (`datasketch`)** | [`ekzhu/datasketch`](https://github.com/ekzhu/datasketch) | • Algoritma deduplikasi berbasis *Locality-Sensitive Hashing*.<br>• Memangkas kompleksitas perbandingan dari **$O(N^2)$ menjadi $O(N)$**.<br>• Mendeteksi berita sindikasi (*near-duplicate news*) dalam hitungan milidetik. | **Solusi Mutlak Redundansi:** Menggantikan nested loop SBERT/SequenceMatcher lama. |
| **Pydantic / Instructor** | [`jxnl/instructor`](https://github.com/jxnl/instructor) | • Ekstraksi terstruktur berbasis skema data ketat (*strict schema enforcement*).<br>• Menjamin validitas tipe data tanpa regex manual. | **Ekstraktor 13 Atribut:** Mengonversi Clean Markdown ke 13 atribut proyek Danantara. |

---

## 5. Rencana Arsitektur & Pipeline Eksekusi Celios 9 Danantara

### A. Struktur Folder Celios 9 yang Diterapkan
```text
C:\Users\yooma\OneDrive\Desktop\duniahub\client\28. Celios9-danantara\
├── .agents/rules/                # 5 Aturan mutlak tata kelola
├── data/
│   ├── raw/
│   │   ├── sources/              # Unduhan PDF laporan tahunan & publikasi resmi BUMN
│   │   └── evidence_dorking/     # Bukti forensik unduhan web / snapshot HTML
│   └── processed/
│       ├── bumn_master_clean.csv # Master list BUMN terverifikasi (bebas PT swasta)
│       ├── green_inventory.csv   # Database 13 atribut proyek hijau BUMN
│       └── green_investment_list.csv # Hasil akhir rekomendasi lolos screening
├── docs/                         # Laporan, metodologi, dan dokumen kontrak
├── ref/                          # Acuan metodologi author (Methodological Approach)
├── scripts/                      # Alur Eksekusi Bertahap:
│   ├── 01_dorking_collection.py  # Targeted discovery (14 kluster x BUMN)
│   ├── 02_extract_clean.py       # Ekstraksi Clean Markdown (Trafilatura / Crawl4AI)
│   ├── 03_dedup_minhash.py       # Deduplikasi linear time O(N) via datasketch
│   ├── 04_structure_pydantic.py  # Parsing 13 atribut data proyek
│   └── 05_taxonomy_screening.py  # Negative filter, TKBI v3, & Norfund Additionality
├── src/                          # Reusable modules:
│   ├── crawler.py                # Wrapper Crawl4AI & Trafilatura
│   ├── dedup.py                  # Logika MinHash LSH
│   ├── schema.py                 # Skema Pydantic 13 Atribut Proyek
│   └── screening.py              # Logika Three-Gate Decision System
└── tool/
    └── parser_opendataloader/    # Parser dokumen acuan
```

---

### B. Alur Kerja Pipeline Sekuensial (Sequential Workflow)

```
[01. Targeted Search] ──> [02. Clean Extraction] ──> [03. MinHash Dedup] ──> [04. Pydantic Parsing] ──> [05. 3-Gate Screening]
  (Dorking 14 Kluster)     (Trafilatura / Crawl4AI)    (Linear O(N) Hashing)     (Ekstraksi 13 Atribut)    (Negative + TKBI + Norfund)
           │                          │                                                  │                          │
           ▼                          ▼                                                  ▼                          ▼
   File Bukti Fisik           Clean Markdown Text                                Database Terstruktur       GREEN INVESTMENT LIST
  (data/raw/sources/)        (Bebas Nav/Footer/Ads)                            (data/processed/green.csv)      (Hasil Rekomendasi)
```

1. **Tahap 1 (`01_dorking_collection.py`):**
   * Menargetkan pencarian terarah berdasarkan entitas induk BUMN di [**`MASTER LIST BUMN UNDER DANANTARA.xlsx`**](file:///C:/Users/yooma/OneDrive/Desktop/duniahub/client/28. Celios9-danantara/ref/MASTER%20LIST%20BUMN%20UNDER%20DANANTARA.xlsx) digabungkan dengan **14 Kluster Kata Kunci** author.
   * Setiap dokumen/laporan proyek wajib diunduh berkas fisiknya ke `data/raw/sources/` sesuai aturan [`.agents/rules/no_hardcoded_data.md`](../.agents/rules/no_hardcoded_data.md).
2. **Tahap 2 (`02_extract_clean.py`):**
   * Menggunakan **Trafilatura** (untuk artikel berita teks statis) dan **Crawl4AI** (untuk portal interaktif/CSR).
   * Menghasilkan teks berformat *Clean Markdown* murni. Membuang kebutuhan 100+ baris regex `IRRELEVANT_KEYWORDS`.
3. **Tahap 3 (`03_dedup_minhash.py`):**
   * Menggunakan **MinHash LSH (`datasketch`)** dengan ambang batas Jaccard Similarity 0.80.
   * Berita sindikasi yang disalin lintas portal berita disaring dalam hitungan detik ($O(N)$), hanya mempertahankan 1 salinan terbaik.
4. **Tahap 4 (`04_structure_pydantic.py`):**
   * Clean Markdown diparsing ke dalam skema Pydantic yang memuat 13 atribut wajib:
     `project_name`, `soe_parent`, `soe_subsidiary`, `sector`, `project_status`, `location`, `capacity`, `investment_amount`, `funding_source`, `partners`, `emission_target`, `es_risks`, `announcement_date`.
   * Disimpan ke file fisik [**`data/processed/green_inventory.csv`**](file:///C:/Users/yooma/OneDrive/Desktop/duniahub/client/28. Celios9-danantara/data/processed).
5. **Tahap 5 (`05_taxonomy_screening.py`):**
   * **Gate 1 (Negative Filter):** Mengeliminasi proyek batubara ("green coal"/repurposing), geothermal, nuklir, dan proyek berisiko deforestasi/konflik sosial.
   * **Gate 2 (Taxonomy Benchmarking):** Uji kesesuaian terhadap TKBI v3 dan ASEAN Taxonomy v4.
   * **Gate 3 (Additionality Test):** Uji peran *de-risking* Danantara berbasis prinsip Norfund.
   * Menghasilkan deliverable akhir: **`data/processed/green_investment_list.csv`**.

---

## 6. Kepatuhan Mutlak terhadap `.agents/rules`

1. **Zero Hardcoded Data (`no_hardcoded_data.md`):** Tidak ada angka kapasitas atau status proyek yang dimasukkan langsung ke kode Python. Semua mengalir dari berkas terstruktur fisik di `data/`.
2. **Strict Data Boundary (`strict_data_folder_boundary.md`):** Seluruh data hasil temuan dorking wajib disimpan bukti unduhannya di `data/raw/` sebelum dapat diolah.
3. **Anti-Yes-Man & No Reinventing The Wheel (`anti_yesman_spatial_methodology_integrity.md`):** Menggunakan library standar industri (`datasketch`, `trafilatura`, `crawl4ai`, `pydantic`) dan menolak manipulasi rumus manual ad-hoc.
4. **Keselamatan File & Auto-Commit (`never_use_destructive_commands.md`):** Setiap penambahan dan pembaruan kode langsung di-commit ke repositori Git lokal proyek sebagai titik *checkpoint*.

---

*Dokumen ini menjadi acuan kerja resmi tim pengembang dan peneliti dalam membangun sistem data mining Danantara Monitor.*

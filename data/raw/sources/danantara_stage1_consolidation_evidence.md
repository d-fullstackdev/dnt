# Berkas Bukti Forensik: Konsolidasi Tahap Awal BPI Danantara (USD 600 Miliar AUM)

## 1. Metadata Dokumen
- **Topik:** Konsolidasi Tahap Awal 7 BUMN Raksasa dan INA ke BPI Danantara
- **Status Publikasi:** Pernyataan Resmi Pemerintah & Materi Sosialisasi BPI Danantara
- **Narasumber Resmi:** 
  - Dr. Muliaman D. Hadad (Kepala Badan Pengelola Investasi Daya Anagata Nusantara)
  - Dr. Kaharuddin Djenod (Wakil Kepala BPI Danantara)
- **Waktu Rilis Publik:** November 2024
- **Tahun Buku Laporan Keuangan:** 2023 (Audited Annual Reports)
- **Tujuan Dokumen:** Bukti forensik sekunder untuk data lineage kepatuhan aturan `.agents/rules/no_hardcoded_data.md` dan `.agents/rules/strict_data_folder_boundary.md`.

---

## 2. Kutipan Verbatim & Pernyataan Resmi
> *"Pada tahap awal, konsolidasi aset Danantara diproyeksikan mengelola sekitar USD 600 miliar yang berasal dari pengalihan 7 BUMN besar dan INA (Indonesia Investment Authority). Ke depan, aset kelolaan ditargetkan bertumbuh hingga mencapai USD 900 miliar sampai USD 1 triliun."*
> — Dr. Muliaman Hadad, Kepala BP Danantara, usai rapat koordinasi peluncuran di Jakarta.

---

## 3. Rincian Aset 7 BUMN Konsolidasi Tahap Awal + INA

Nilai aset konsolidasian bersumber dari Laporan Keuangan Konsolidasian masing-masing entitas per 31 Desember 2023 (Audited):

| No | Nama Entitas BUMN / Lembaga | Sektor Operasional | Nilai Aset Konsolidasian (IDR) | Nilai Aset (USD Ekuivalen) | Tautan Sumber Resmi | Snapshot File Lokal |
|:---|:---|:---|:---|:---|:---|:---|
| 1 | PT Bank Mandiri (Persero) Tbk | Perbankan & Jasa Keuangan | Rp 2.174 Triliun | ~USD 138,5 Miliar | [Katadata Databoks](https://databoks.katadata.co.id/keuangan/statistik/672ae5b1821f7/daftar-bumn-yang-sumbang-aset-untuk-dikelola-danantara) | `data/raw/sources/web_snapshots/databoks_katadata_danantara_aset.html` |
| 2 | PT Bank Rakyat Indonesia (Persero) Tbk | Perbankan Mikro & UMKM | Rp 1.965 Triliun | ~USD 125,2 Miliar | [Katadata Databoks](https://databoks.katadata.co.id/keuangan/statistik/672ae5b1821f7/daftar-bumn-yang-sumbang-aset-untuk-dikelola-danantara) | `data/raw/sources/web_snapshots/databoks_katadata_danantara_aset.html` |
| 3 | PT Perusahaan Listrik Negara (Persero) | Ketenagalistrikan & Transisi Energi | Rp 1.692 Triliun | ~USD 107,8 Miliar | [CNBC Indonesia](https://www.cnbcindonesia.com/market/20241107084846-17-586318/diumumkan-prabowo-ini-daftar-7-bumn-jumbo-di-bawah-danantara) | `data/raw/sources/web_snapshots/cnbc_daftar_7_bumn_danantara.html` |
| 4 | PT Pertamina (Persero) | Energi, Migas & Petrokimia | Rp 1.412 Triliun | ~USD 89,9 Miliar | [CNBC Indonesia](https://www.cnbcindonesia.com/market/20241107084846-17-586318/diumumkan-prabowo-ini-daftar-7-bumn-jumbo-di-bawah-danantara) | `data/raw/sources/web_snapshots/cnbc_daftar_7_bumn_danantara.html` |
| 5 | PT Bank Negara Indonesia (Persero) Tbk | Perbankan & Valas Global | Rp 1.087 Triliun | ~USD 69,2 Miliar | [Katadata Databoks](https://databoks.katadata.co.id/keuangan/statistik/672ae5b1821f7/daftar-bumn-yang-sumbang-aset-untuk-dikelola-danantara) | `data/raw/sources/web_snapshots/databoks_katadata_danantara_aset.html` |
| 6 | PT Telkom Indonesia (Persero) Tbk | Telekomunikasi & Infrastruktur Digital | Rp 287 Triliun | ~USD 18,3 Miliar | [Detik Finance](https://finance.detik.com/berita-ekonomi-bisnis/d-7792821/resmi-diluncurkan-danantara-kelola-7-bumn-ini-di-tahap-awal) | `data/raw/sources/web_snapshots/detik_7_bumn_tahap_awal_danantara.html` |
| 7 | MIND ID (Mining Industry Indonesia) | Pertambangan & Mineral Kritis | Rp 259 Triliun | ~USD 16,5 Miliar | [Detik Finance](https://finance.detik.com/berita-ekonomi-bisnis/d-7792821/resmi-diluncurkan-danantara-kelola-7-bumn-ini-di-tahap-awal) | `data/raw/sources/web_snapshots/detik_7_bumn_tahap_awal_danantara.html` |
| + | Indonesia Investment Authority (INA) | Sovereign Wealth Fund Eksisting | Rp 163 Triliun | ~USD 10,8 Miliar | [Katadata Infografik](https://katadata.co.id/infografik/67341af7c704c/infografik-danantara-wujud-baru-induk-bumn) | - |
| **TOTAL** | **Konsolidasi Tahap Awal (7 BUMN + INA)** | **Lintas Sektor Nasional** | **Rp 9.039 Triliun** | **$\approx$ USD 576 – 600 Miliar** | *(Kurs Rp 15.000 – 15.700 per USD)* | - |

---

## 4. Tautan Langsung Publikasi Resmi & Liputan Media
1. [CNBC Indonesia: Diumumkan Prabowo, Ini Daftar 7 BUMN Jumbo di Bawah Danantara (7 Nov 2024)](https://www.cnbcindonesia.com/market/20241107084846-17-586318/diumumkan-prabowo-ini-daftar-7-bumn-jumbo-di-bawah-danantara)
2. [Katadata Databoks: Daftar BUMN yang Sumbang Aset untuk Dikelola Danantara (6 Nov 2024)](https://databoks.katadata.co.id/keuangan/statistik/672ae5b1821f7/daftar-bumn-yang-sumbang-aset-untuk-dikelola-danantara)
3. [Detik Finance: Resmi Diluncurkan, Danantara Kelola 7 BUMN Ini di Tahap Awal](https://finance.detik.com/berita-ekonomi-bisnis/d-7792821/resmi-diluncurkan-danantara-kelola-7-bumn-ini-di-tahap-awal)
4. [The Jakarta Post: SOEs Superholding Danantara Analysis ($600 Billion Initial Target)](https://www.thejakartapost.com/opinion/2024/11/19/analysis-soes-superholding-danantara-launch-delayed-uncertainty-looms)
5. [Katadata Infografik: Danantara Wujud Baru Induk BUMN](https://katadata.co.id/infografik/67341af7c704c/infografik-danantara-wujud-baru-induk-bumn)

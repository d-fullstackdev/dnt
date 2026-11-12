# Hasil Asesmen Pemantauan Web (Scraping) Danantara Monitor

Berdasarkan pengujian awal menggunakan *standard HTTP request* (seperti bot biasa), berikut adalah peta kelayakan *scraping* dari 18 situs web yang masuk dalam *Scope of Work*:

## Tabel Hasil *Scrape Test*

| No | Situs Web Target | Status | Hasil Asesmen | Keterangan / Proteksi |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `danantaraindonesia.co.id` | 200 OK | ✅ **Aman (Bisa di-scrape)** | Tidak ada proteksi ketat. |
| 2 | `jdih.setneg.go.id` | 200 OK | ❌ **Gagal** | Terblokir Cloudflare / Bot Protection. Harus melewati *captcha*. |
| 3 | `peraturan.bpk.go.id` | 200 OK | ❌ **Gagal** | Terblokir Cloudflare / Bot Protection. |
| 4 | `setneg.go.id` | 200 OK | ✅ **Aman (Bisa di-scrape)** | Bisa ditarik langsung. |
| 5 | `presidenri.go.id` | 403 Forbidden | ❌ **Gagal Akses** | Proteksi ketat (Akamai / Cloudflare). Bot langsung ditolak. |
| 6 | `setkab.go.id` | Timeout | ❌ **Gagal Akses** | Server tidak merespons bot (Connection Error). |
| 7 | `kompas.id` | 200 OK | ⚠️ **Aman, tapi Terbatas** | Web bisa dibuka, tapi membaca konten penuh butuh *Login/Paywall*. |
| 8 | `kontan.co.id` | 200 OK | ✅ **Aman (Bisa di-scrape)** | Bisa ditarik langsung. |
| 9 | `bisnis.com` | 200 OK | ✅ **Aman (Bisa di-scrape)** | Bisa ditarik langsung. |
| 10 | `thejakartapost.com` | 200 OK | ⚠️ **Aman, tapi Terbatas** | Artikel sering kali dibatasi *Paywall*. |
| 11 | `kompas.com` | 200 OK | ✅ **Aman (Bisa di-scrape)** | Bisa ditarik langsung. |
| 12 | `cnbcindonesia.com` | 200 OK | ✅ **Aman (Bisa di-scrape)** | Bisa ditarik langsung. |
| 13 | `detik.com` | 200 OK | ✅ **Aman (Bisa di-scrape)** | Bisa ditarik langsung. |
| 14 | `reuters.com` | 401 Unauth | ❌ **Gagal** | Butuh otentikasi ketat (Bot Protection / Paywall). |
| 15 | `bloombergtechnoz.com`| 200 OK | ✅ **Aman (Bisa di-scrape)** | Bisa ditarik langsung. |
| 16 | `bloomberg.com` | 403 Forbidden | ❌ **Gagal Akses** | Proteksi tingkat tinggi (Datadome/Cloudflare). Sangat sulit ditembus bot biasa. |
| 17 | `spglobal.com` | 403 Forbidden | ❌ **Gagal Akses** | Proteksi Anti-Bot tingkat Enterprise. |
| 18 | `moodys.com` | 200 OK | ✅ **Aman (Bisa di-scrape)** | Aman ditarik (halaman publiknya). |

---

## Analisis Error (Mengapa Gagal?)

Dari 18 situs, ada **6 situs** yang menolak ditarik datanya oleh skrip standar. Error utamanya terbagi menjadi dua:
1. **Proteksi Anti-Bot (Cloudflare / Akamai / Datadome):** Situs-situs besar (seperti Bloomberg, S&P, BPK, PresidenRI) menggunakan sistem pendeteksi bot yang sangat canggih. Jika kita sekadar menembakkan skrip Python biasa, sistem mereka akan memberikan kode **403 Forbidden** atau memaksa kita mencentang *"Verify you are human"* (halaman Cloudflare).
2. **Paywall / Otentikasi (Error 401):** Reuters dan Kompas.id mewajibkan *login* akun premium (berbayar) untuk bisa mengakses teks beritanya secara utuh. Jika bot mencoba mengakses, akan ditolak atau hanya disajikan paragraf pertama.

## Solusi *Tools* & Arsitektur yang Direkomendasikan

Mengingat kompleksitas proteksi di atas, pembuatan *dashboard* pemantauan tidak bisa menggunakan *library* standar seperti `BeautifulSoup` biasa. Anda harus menggunakan beberapa instrumen ( *tools* ) kelas menengah-atas:

1. **Undetected Chromedriver / Playwright-Stealth:**
   Untuk menembus Cloudflare dan sistem *Anti-Bot* di situs JDIH, BPK, Bloomberg, dan S&P. Ini adalah *browser headless* yang dimodifikasi khusus agar bertingkah 100% mirip manusia sehingga tidak memicu *captcha*.
2. **Rotating Residential Proxies:**
   Untuk mencegah IP Anda diblokir karena terlalu sering me-*refresh* situs target. Sangat dibutuhkan untuk *scraping* harian.
3. **News API (Alternatif Paling Aman):**
   Daripada me-*scrape* Detik, Kompas, Kontan satu per satu, jauh lebih aman dan cepat menggunakan *Aggregator News API* komersial (seperti *GNews API*, *NewsCatcher*, atau *Mediastack*) yang mengumpulkan berita dari ratusan media nasional, dan kita cukup menarik data menggunakan parameter `q="Danantara"`.
4. **Session / Cookies Authentication:**
   Untuk menembus situs *Paywall* (Kompas.id, TheJakartaPost), bot harus dipasangi *cookies* otentikasi dari akun berlangganan yang sah, atau membukanya secara manual menggunakan *browser extension*.

**Kesimpulan:** Untungnya, kesepakatan akhir Anda di kontrak telah menghapus tuntutan *software monitoring* serba otomatis ini, karena secara teknis mengelola *scraper* menembus 18 tembok pertahanan *cyber* ini adalah pekerjaan *Data Engineering* tingkat tinggi yang butuh OPEX infrastruktur tidak sedikit.

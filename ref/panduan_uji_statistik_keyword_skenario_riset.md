# Panduan Pemilihan Uji Statistik Berdasarkan Keyword / Skenario Riset

| Keyword / skenario riset | Kondisi data | Uji / analisis menurut buku | Minimum n menurut buku | n ideal / catatan |
|---|---|---|---|---|
| **“Gambaran…” / “Karakteristik…” / “Distribusi…”** | Hanya mendeskripsikan data | Statistik deskriptif: mean, median, modus, frekuensi, %, SD | **Tidak ditetapkan khusus** | Secara umum menyesuaikan populasi dan tujuan penelitian |
| **“Hubungan X dengan Y”** | 2 variabel kontinu, normal | **Pearson Correlation** | **Tidak ditetapkan khusus**; buku memberi pedoman umum menghindari **n < 30** untuk parametrik | Pedoman umum Roscoe: **30–<500** |
| **“Hubungan X dengan Y”** | Ordinal / tidak normal | **Spearman Rank Correlation** | **Tidak ditetapkan khusus** | Nonparametrik lebih fleksibel untuk sampel kecil |
| **“Hubungan / asosiasi X dengan Y”** | Kedua variabel kategorik | **Chi-square** | **Tidak ditetapkan khusus** | Perhatikan **expected count**; bila kecil pada tabel 2×2, dapat dipertimbangkan Fisher’s Exact |
| **“Pengaruh X terhadap Y”** | 1 X kontinu/kategorik yang sesuai, Y kontinu, asumsi parametrik terpenuhi | **Regresi Linear Sederhana** | **Tidak ditetapkan khusus** | Pedoman umum parametrik: hindari n < 30; semakin besar n semakin stabil |
| **“Pengaruh X1, X2, X3 terhadap Y”** | Beberapa variabel independen, Y kontinu | **Regresi Linear Berganda** | Tidak diberi satu angka minimum khusus | Termasuk analisis multivariat; buku menyebut kisaran umum **100–500** tergantung kompleksitas |
| **“Prediksi kejadian…” / “Peluang terjadinya…”** | Y dikotomis, misalnya ya/tidak | **Regresi Logistik** | Tidak ditetapkan khusus dalam buku | Lebih penting memperhatikan jumlah kejadian dan kestabilan model |
| **“Perbedaan 2 kelompok”** | 2 kelompok independen, data normal | **Independent t-test** | Tidak ditetapkan khusus | Pedoman umum parametrik: hindari n < 30 jika memungkinkan |
| **“Perbedaan 2 kelompok”** | 2 kelompok independen, ordinal / tidak normal | **Mann–Whitney U** | Tidak ditetapkan khusus | Cocok untuk sampel kecil dan data ordinal |
| **“Sebelum dan sesudah…”** | 2 pengukuran berpasangan, normal | **Paired t-test** | Tidak ditetapkan khusus | Data berasal dari subjek yang sama / pasangan |
| **“Sebelum dan sesudah…”** | 2 pengukuran berpasangan, tidak normal | **Wilcoxon Signed-Rank** | Tidak ditetapkan khusus | Nonparametrik |
| **“Perbedaan lebih dari 2 kelompok”** | ≥3 kelompok independen, normal | **ANOVA** | Tidak ditetapkan khusus | Bila signifikan, dapat dilanjutkan post-hoc seperti Tukey |
| **“Perbedaan lebih dari 2 kelompok”** | ≥3 kelompok independen, tidak normal | **Kruskal–Wallis** | Tidak ditetapkan khusus | Bila signifikan, lanjut post-hoc seperti Dunn |
| **“Perbedaan >2 pengukuran berulang”** | Subjek sama, data normal | **Repeated Measures ANOVA** | Tidak ditetapkan khusus | Untuk pengukuran berulang |
| **“Perbedaan >2 pengukuran berulang”** | Subjek sama, data tidak normal | **Friedman Test** | Tidak ditetapkan khusus | Alternatif nonparametrik repeated measures ANOVA |
| **“Perbedaan kelompok dengan variabel kontrol”** | Ada variabel kovariat/kontrol | **ANCOVA** | Tidak ditetapkan khusus | Mengontrol pengaruh variabel lain |
| **“Perbedaan beberapa variabel dependen”** | Lebih dari satu Y | **MANOVA** | Tidak ditetapkan khusus | Termasuk analisis multivariat |
| **“Beberapa Y + variabel kontrol”** | Lebih dari satu Y dan ada kovariat | **MANCOVA** | Tidak ditetapkan khusus | Multivariat dengan kontrol |
| **“Pengaruh langsung dan tidak langsung”** | Ada jalur X → M → Y | **Path Analysis** | Tidak ditetapkan khusus | Umumnya membutuhkan sampel lebih besar daripada regresi sederhana |
| **“Hubungan konstruk laten” / “Model kompleks”** | Banyak variabel laten dan indikator | **SEM / PLS-SEM** | Buku menyebut rekomendasi **100–200** untuk SEM; juga rasio **5–10 : 1** atau sekitar **10 responden per indikator** | PLS-SEM lebih fleksibel untuk data tidak normal dan sampel relatif kecil |
| **“Data provinsi/perusahaan selama beberapa tahun”** | Gabungan cross-section dan time series | **Regresi Data Panel** | Tidak ditetapkan khusus | Pilihan model: pooled OLS, fixed effect, random effect |
| **“Perbedaan struktur multivariat antar kelompok”** | Data multivariat, tidak memenuhi asumsi parametrik | **PERMANOVA** | Tidak ditetapkan khusus | Menggunakan distance/dissimilarity dan permutation |
| **“Hubungan ordinal / ranking”** | Data ordinal | **Spearman / Kendall** | Tidak ditetapkan khusus | Nonparametrik |
| **“Hubungan kompleks banyak variabel”** | ≥3 variabel | **Analisis multivariat** | Buku menyebut kisaran umum **100–500** tergantung kompleksitas | Tidak berarti semua metode wajib minimal 100 |

## Catatan penting

Angka **30** bukan minimum khusus untuk Pearson, t-test, regresi, atau Chi-square. Itu merupakan **pedoman umum Roscoe**, bahwa ukuran sampel yang lazim adalah sekitar **30 sampai kurang dari 500**, dan sampel di bawah 30 umumnya dihindari terutama untuk statistik parametrik.

Untuk penelitian kualitatif, logikanya berbeda karena lebih menekankan **informan, kedalaman data, relevansi, dan saturasi**, bukan minimum n statistik.

# 20 Kombinasi Model Prediksi & Preprocessing Standar Industri (Golden Standard 2026)

Dokumen ini merangkum **20 kombinasi pipeline preprocessing dan model prediksi** paling teruji dan menjadi *de facto golden standard* di industri enterprise modern pada tahun 2026, lengkap dengan **klasifikasi tingkat analisis riset: Makro, Mikro, dan Meso (Jembatan Makro-Mikro)**.

---

## Ringkasan Matriks 20 Kombinasi & Klasifikasi Riset (Makro vs Mikro)

| No | Klasifikasi Riset | Kategori / Tipe Data | Domain / Kasus Penggunaan Riil | Pipeline Preprocessing (2026 Standard) | Arsitektur Model Prediksi | Tech Stack Utama |
|---|---|---|---|---|---|---|
| **01** | **Mikro** | Tabular ML | Churn, Credit Scoring, Fraud Nasabah | Out-of-Fold Target Encoding, RobustScaler, Optuna Tuning, Native Missing | **LightGBM / CatBoost + Optuna** | Polars, CatBoost, Optuna |
| **02** | **Mikro** | Tabular Deep Learning | Transaksi Multi-Tabel Enterprise & Marketplace | Entity Embeddings, Quantile Normalization, Cross-Feature Layer | **FT-Transformer / SAINT** | PyTorch 2.x, rtdl, DuckDB |
| **03** | **Makro** | Time Series (Ekonometrika) | Inflasi, PDB, Suku Bunga Acuan, Fiskal | ADF/KPSS Stationary Test, Box-Cox, STL Decomposition, Exogenous Lags | **SARIMAX + GARCH (1,1)** | statsmodels, arch, sktime |
| **04** | **Mikro** | Time Series (Foundation Model) | Demand Forecasting Ribuan SKU Ritel Toko | RevIN (Reversible Instance Norm), Patch Tokenizer, Calendar Encoding | **Chronos / PatchTST / Time-LLM** | Hugging Face, AutoGluon-TS |
| **05** | **Mikro / Meso** | Time Series (DL Hybrid) | Multi-Horizon Supply Chain Gudang & Logistik | Missing Linear Interpolation, Static Entity Embedding, Scaler Window | **Temporal Fusion Transformer (TFT) / TiDE** | Darts, PyTorch Forecasting |
| **06** | **Mikro** | NLP Text Scoring | Skrining Kontrak Hukum, Dokumen Klausul, ESG | Text Normalization, Semantic Chunking, Multilingual Dense Vectors | **BAAI/bge-m3 + CatBoost / Ridge** | BAAI/bge-m3, sentence-transformers |
| **07** | **Meso / Makro Sektoral** | LLM Agentic Prediction | Prediksi Kinerja Finansial Emiten & Rasio Pasar | Document Parser (Docling), Hybrid BM25/Vector Search, Reranking | **Fine-Tuned LLM (Llama 3/Mistral) + DSPy** | vLLM, DSPy, Cohere Rerank |
| **08** | **Mikro** | Computer Vision (Klasifikasi) | Deteksi Cacat Komponen & Citra Medis Pasien | RandAugment, CutMix/MixUp, Adaptive Letterbox Resizing | **ConvNeXt V2 / Swin Transformer V2** | PyTorch, Timm, Albumentations |
| **09** | **Mikro** | Computer Vision (Deteksi) | Warehouse Robotics & Visual Quality Inspection | Mosaic Augmentation, HSV Jitter, Bounding Box Normalization | **YOLOv10 / YOLO11 / RT-DETR** | Ultralytics, TensorRT |
| **10** | **Mikro** | Multimodal (Vision + Text) | Prediksi CTR & Pengembalian Barang E-commerce | SigLIP Visual Preprocessing, Text Tokenizer, RobustScaler | **SigLIP / OpenCLIP + Late-Fusion MLP** | Transformers, Triton Server |
| **11** | **Mikro** | RecSys (Candidate Retrieval) | Streaming & E-commerce Personalization | In-batch Negatives, ID Hashing Trick, Log1p Frequency Scaling | **Two-Tower Neural Network / DLRM** | Feast, TorchRec, NVIDIA Merlin |
| **12** | **Mikro** | RecSys (Sequential / Session) | Next-Item Click Prediction Sesi Belanja Aktif | Clickstream Sliding Window, Cloze Masking, Time-Delta ($\Delta t$) | **SASRec / BERT4Rec** | PyTorch, RecBole, Redis |
| **13** | **Meso (Jaringan)** | Graph ML (GNN) | AML (Anti-Money Laundering) & Sindikat Fraud | Bipartite Graph, GraphSAINT Neighbor Sampling, Degree-Norm | **GATv2 / GraphSAGE** | PyTorch Geometric (PyG), DGL |
| **14** | **Mikro** | Survival Analysis | Predictive Maintenance Mesin & Churn Pelanggan | `(time, event)` Censoring Format, Nelson-Aalen Scaling, VIF Pruning | **DeepSurv / Random Survival Forests** | lifelines, scikit-survival |
| **15** | **Mikro** | Anomaly Detection | Intrusi Server Jaringan & Telemetri Sensor IoT | Rolling Window Z-score/EWMA, FFT Spectral Energy, Robust MAD | **Anomaly Transformer + Isolation Forest** | PyOD, PyTorch, SciPy |
| **16** | **Makro & Mikro** | Causal ML & Uplift Modeling | Evaluasi Kebijakan Publik (Makro) / Promo (Mikro) | Propensity Score Matching (PSM), Covariate Balance Check (SMD < 0.1) | **Double Machine Learning (DML) / Causal Forest** | EconML, CausalML, DoWhy |
| **17** | **Meso (Jembatan)** | Hierarchical Forecasting | Konsiliasi Stok Multi-Level (SKU $\to$ Nasional) | Outlier Capping (Tukey), Hierarchical Matrix ($S$-Matrix), Calendar Feat | **Base Model (LightGBM) + MinT Reconciliation** | HierarchicalForecast, Nixtla |
| **18** | **Mikro** | Audio / Speech Prediction | Sentimen Suara Call Center & Biomarker Pasien | Voice Activity Detection (VAD), 128 Mel-Bands, SpecAugment | **Wav2Vec 2.0 / Whisper Encoder + BiLSTM** | torchaudio, librosa, Hugging Face |
| **19** | **Mikro** | Extreme Multi-Label (XML) | Otomasi Kode Klaim Medis (ICD-10) & Paten | Domain Subword Tokenizer, Asymmetric Loss (ASL) / Focal Loss | **ModernBERT / LightXML** | Hugging Face, fasttext, PyTorch |
| **20** | **Makro** | Probabilistic Forecasting | Stabilitas Beban Grid PLTS/PLTB & VaR Finansial | Quantile Binning, Exogenous Weather Lagging, Copula Alignment | **DeepAR / N-BEATS + Conformal Prediction** | GluonTS, MAPIE, statsforecast |

---

## Taksonomi: Karakteristik Riset Makro vs Mikro

### 1. Riset Makro (Macro-Level Research)
* **Karakteristik Data:** Agregat agregatif (skala nasional, regional, sektoral), frekuensi relatif rendah (harian, bulanan, kuartalan), ukuran baris data ratusan hingga puluhan ribu titik waktu, rasio sinyal terhadap *noise* rentan terhadap guncangan eksternal (*black swan events*).
* **Fokus Utama:** Kausalitas terstruktur, ekuilibrium umum, stabilitas sistemik, kepatuhan regulasi publik, dan akuntabilitas audit.
* **Kombinasi Terkait:**
  - **No. 03 (Ekonometrika SARIMAX + GARCH):** Analisis suku bunga acuan, inflasi IHK, nilai tukar, dan neraca perdagangan.
  - **No. 16 (Causal ML untuk Kebijakan Publik):** Evaluasi efektivitas intervensi subsidi sosial, tarif pajak, atau program jaminan kesehatan nasional.
  - **No. 20 (Peramalan Probabilistik Kapasitas Grid Energi & VaR):** Keseimbangan transmisi beban listrik lintas pulau/provinsi dan risiko kegagalan sistem perbankan.

### 2. Riset Mikro (Micro-Level Research)
* **Karakteristik Data:** Tingkat atomik (perorangan, transaksi tunggal, sinyal sensor per detik, gambar produk, klik sesi), volume data sangat masif (jutaan hingga miliaran baris), dimensi fitur sangat heterogen.
* **Fokus Utama:** Optimasi konversi, otomatisasi keputusan real-time, minimasi latensi inferensi (<20 ms), personalisasi pengguna.
* **Kombinasi Terkait:**
  - **No. 01, 02, 11, 12:** Pemodelan perilaku nasabah, sistem rekomendasi produk, dan credit scoring personal.
  - **No. 04, 05, 14, 15:** Prediksi kebutuhan per SKU barang, kerusakan fisik mesin tunggal, dan deteksi anomali pada sensor per detik.
  - **No. 08, 09, 10, 18, 19:** Pemrosesan citra cacat pabrik, analisis suara penelepon, dan klasifikasi kode ICD rekam medis per individu.

### 3. Riset Meso & Jembatan Makro-Mikro (Cross-Scale Integration)
* **Karakteristik Data:** Relasi jaringan multi-entitas atau struktur data bertingkat (*nested/hierarchical*).
* **Fokus Utama:** Menjembatani keputusan unit individu dengan dampaknya terhadap agregat kolektif.
* **Kombinasi Terkait:**
  - **No. 13 (Graph Neural Networks untuk AML/Fraud):** Menghubungkan transaksi mikro antar-rekening individual untuk mendeteksi sindikat terorganisir skala makro.
  - **No. 17 (Hierarchical Forecasting via MinT):** Menjamin konsistensi matematika bahwa penjumlahan peramalan mikro (penjualan per toko per produk) tepat sama dengan target makro (rencana anggaran perusahaan/nasional).
  - **No. 07 (Agentic LLM untuk Analisis Emiten):** Membaca dokumen spesifik emiten tunggal untuk memprediksi arah tren industri per sektor.

---

## Rincian Mendalam 20 Kombinasi

*(Untuk rincian lengkap arsitektur teknis tiap nomor, silakan telusuri sub-bagian pada file [docs/standar_industri_prediksi_2026.md](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/28.%20Celios9-danantara/docs/standar_industri_prediksi_2026.md))*

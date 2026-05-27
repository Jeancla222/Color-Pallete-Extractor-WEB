# Color-Pallete-Extractor-WEB

## Deskripsi
Aplikasi web untuk mengekstrak **warna paling dominan** dari sebuah gambar menggunakan algoritma **K-Means Clustering** (Unsupervised Learning).

## Persyaratan Tugas
- Upload gambar
- Menggunakan **K-Means Clustering**
- Menghasilkan **minimal 3 warna palette**

## Metode yang Digunakan
- **Algoritma**: K-Means Clustering
- **Jumlah Cluster (K)**: 3-10 (bisa diatur 3-10 via slider)
- **Metode Jarak**: Euclidean Distance
- **Inisialisasi**: K-Means++ (lebih stabil)
- **Maks Iterasi**: 300

## Cara Menjalankan

### Lokal
```bash
# 1. Clone repository
git clone https://github.com/Jeancla222/Color-Pallete-Extractor-WEB.git
cd color-palette-extractor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Jalankan aplikasi
streamlit run app.py

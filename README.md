# SKY - Web Reconnaissance & Tool v1.0

SKY adalah alat pemindaian (_scanner_) subdomain dan direktori berbasis Python. Alat ini dirancang khusus menggunakan teknik _Multi-Threading_ untuk kecepatan optimal, serta dilengkapi dengan _Stealth Mode_ (jeda waktu acak dan rotasi _User-Agent_) guna meminimalisir risiko pemblokiran oleh Firewall web (WAF/Cloudflare).

## ✨ Fitur Utama

- **Subdomain Finder**: Mencari subdomain aktif dari domain target.
- **Directory Scanner**: Memindai direktori sensitif atau jalur (_path_) tersembunyi pada web.
- **Stealth Mode**: Menggunakan jeda waktu dinamis (1.5 - 4.0 detik) dan mendistribusikan identitas peramban (_User-Agent_) acak pada setiap permintaan.
- **Multi-Threading Aman**: Menggunakan `ThreadPoolExecutor` yang dibatasi (`MAX_THREADS = 3`) agar performa tetap cepat namun tidak memicu DDoS.
- **Auto-Save**: Hasil yang berstatus aktif (`FOUND` & `REDIRECT`) otomatis tersimpan ke dalam file teks khusus.
- **Tampilan Interaktif**: Tampilan terminal berwarna memanfaatkan _library_ `colorama` lengkap dengan indikator persentase progres.

## 🛠️ Prasyarat & Instalasi

Pastikan Anda sudah menginstal Python di komputer Anda. Sebelum menjalankan alat ini, instal pustaka (_library_) eksternal yang diperlukan melalui terminal:

```bash
pip install colorama requests
```

## 🚀 Cara Penggunaan

1. Siapkan berkas kata kunci Anda di dalam folder yang sama:
   - Buat berkas `subdomains.txt` jika ingin mencari subdomain.
   - Buat berkas `wordlist.txt` jika ingin mencari direktori.
2. Jalankan skrip melalui terminal atau command prompt dengan menyertakan domain target:

```bash
python index.py google.com
```

## 📝 Catatan Penting

Alat ini dibuat hanya untuk tujuan pendidikan dan pengujian keamanan yang sah (_Authorized Penetration Testing_). Penyalahgunaan alat ini untuk meretas sistem tanpa izin adalah tindakan ilegal.

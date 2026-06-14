# SKY - Web Reconnaissance & Tool v1.0

SKY adalah alat pemindaian (_scanner_) subdomain dan direktori berbasis Python. Alat ini dirancang khusus menggunakan teknik _Multi-Threading_ untuk kecepatan optimal, serta dilengkapi dengan _Stealth Mode_ (jeda waktu acak dan rotasi _User-Agent_) guna meminimalisir risiko pemblokiran oleh Firewall web (WAF/Cloudflare).

## ✨ Fitur Utama

- **Subdomain Finder**: Mencari subdomain aktif dari domain target.
- **Directory Scanner**: Memindai direktori sensitif atau jalur (_path_) tersembunyi pada web.
- **Stealth Mode**: Menggunakan jeda waktu dinamis (1.5 - 4.0 detik) dan mendistribusikan identitas peramban (_User-Agent_) acak pada setiap permintaan.
- **Multi-Threading Aman**: Menggunakan `ThreadPoolExecutor` yang dibatasi (`MAX_THREADS = 3`) agar performa tetap cepat namun tidak memicu DDoS.
- **Auto-Save**: Hasil yang berstatus aktif (`FOUND` & `REDIRECT`) otomatis tersimpan ke dalam file teks khusus.
- **Tampilan Interaktif**: Tampilan terminal berwarna memanfaatkan _library_ `colorama` lengkap dengan indikator persentase progres.

## 🛠️ Daftar Pustaka (Dependencies) & Instalasi

Alat ini dibangun menggunakan kombinasi pustaka bawaan Python dan pustaka pihak ketiga.

### 1. Pustaka Eksternal (Wajib Diinstal)

Anda **wajib** menginstal pustaka berikut melalui terminal sebelum menjalankan program agar tidak terjadi error `ModuleNotFoundError`:

- **`requests`**: Digunakan untuk mengirim permintaan HTTP/HTTPS ke server target.
- **`colorama`**: Digunakan untuk memberikan warna pada teks output di terminal.

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

---

## 💙 Penutup & Dukungan

Terima kasih banyak sudah berkunjung dan menggunakan alat **SKY** ini! Proyek ini dibangun dengan semangat untuk terus belajar dan berbagi di dunia pengembangan perangkat lunak serta keamanan siber.

Jika alat ini bermanfaat untukmu, jangan lupa memberikan **Star (⭐)** pada repositori ini ya! Tetap semangat belajar, terus ngoding, dan mari kita melangkah lebih jauh bersama! 🚀🔥

_Happy Coding & Stay Safe!_ 🌤️💻✨

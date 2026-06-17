# SKY - Web Reconnaissance & Tool v1.3

SKY adalah alat pemindaian (_scanner_) subdomain dan direktori berbasis Python yang tangguh dan ringan. Alat ini dirancang menggunakan arsitektur _Multi-Threading_ murni untuk kecepatan eksekusi tinggi, serta dilengkapi dengan kendali _Stealth Mode_ yang dinamis dan fitur filtrasi output untuk kenyamanan proses pengintaian siber (_recon_).

## ✨ Fitur Utama (v1.3)

- **Subdomain Finder**: Melacak keberadaan subdomain aktif dari domain target yang Anda tuju.
- **Directory Scanner**: Memindai jalur sensitif atau direktori tersembunyi pada struktur web target.
- **High-Speed Spawning**: Sistem pengiriman tugas _thread_ yang optimal tanpa adanya hambatan sumbatan antrean (*bottleneck*).
- **Stealth Mode (Anti-WAF)**: Fitur penyamaran pintar berupa rotasi identitas peramban (_User-Agent acak_) dan jeda waktu dasar dinamis untuk mengelabui deteksi firewall.
- **Advanced Status Code Filter**: Menyembunyikan status respon tertentu (misal: `404` atau `403`) agar layar terminal Anda tetap bersih dan hanya fokus pada data penting.
- **Precision Progress Bar**: Indikator persentase kemajuan yang tetap akurat dan sinkron meskipun ada ribuan status kode yang Anda filter di latar belakang.
- **Clean Run**: Menampilkan hasil langsung ke layar terminal tanpa membuat file log otomatis yang mengotori direktori Anda.

## 🛠️ Persyaratan & Instalasi

Alat ini membutuhkan **Python 3.x** dan beberapa pustaka pihak ketiga agar dapat menampilkan visual warna yang interaktif.

### Instalasi Dependensi
Jalankan perintah berikut di terminal Anda untuk menginstal pustaka yang dibutuhkan:

```bash
pip install colorama requests
```

## 🚀 Cara Penggunaan & Argumen Terminal

Anda wajib menyertakan argumen perintah saat menjalankan skrip ini melalui terminal. 

### Parameter Perintah:

| Argumen | Alias | Deskripsi | Status |
| :--- | :--- | :--- | :--- |
| `target` | - | Domain target yang akan dipindai (Contoh: `google.com`) | **Wajib** |
| `--mode` | `-m` | Pilihan mode pemindaian: `subdomain` atau `direktori` | **Wajib** |
| `--wordlist` | `-w` | Path/lokasi file teks daftar kata kunci kamus Anda | **Wajib** |
| `--filter-status`| `-fs`| Menyembunyikan status tertentu dari layar (Contoh: `-fs 404 403`) | Opsional |
| `--threads` | `-t` | Jumlah pekerja simultan yang berjalan bersamaan (Bawaan: `3`) | Opsional |
| `--delay` | `-d` | Jeda waktu dasar antar-permintaan dalam detik (Bawaan: `0.5`) | Opsional |
| `--version` | `-v` | Menampilkan versi skrip saat ini (`v1.3`) | Opsional |

### Contoh Perintah Eksekusi:

1. **Memindai Subdomain (Menyembunyikan Status 404):**
   ```bash
   python sky_recon.py target_kamu.com -m subdomain -w subdomains.txt -fs 404
   ```

2. **Memindai Direktori dengan 5 Pekerja Sekaligus:**
   ```bash
   python sky_recon.py target_kamu.com -m direktori -w wordlist.txt -t 5
   ```

3. **Memindai dengan Filter Ganda (Sembunyikan 404 dan 403):**
   ```bash
   python sky_recon.py target_kamu.com -m direktori -w wordlist.txt -fs 404 403
   ```

## 📝 Aturan Penggunaan (Disclaimer)

Alat ini dibuat hanya untuk tujuan edukasi, pembelajaran kode, dan pengujian keamanan yang sah (_Authorized Penetration Testing_). Segala bentuk penyalahgunaan alat ini untuk meretas atau merugikan infrastruktur sistem milik orang lain tanpa izin tertulis adalah tindakan ilegal di mata hukum. Pengembang tidak bertanggung jawab atas segala dampak yang ditimbulkan oleh pengguna.

---

## 💙 Dukungan & Kontribusi

Terima kasih banyak telah menggunakan alat **SKY v1.3**! Proyek ini terus dikembangkan untuk memberikan performa pengintaian web yang efisien, bersih, dan andal.

Jika alat ini membantu mempermudah pekerjaan Anda, jangan lupa untuk memberikan **Star (⭐)** pada repositori ini! Tetap konsisten belajar, jaga kode Anda tetap bersih, dan mari melangkah lebih jauh bersama! 🚀🔥

_Happy Coding, Stay Anonymous, & Stay Safe!_ 🌤️💻✨

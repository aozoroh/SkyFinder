import sys
import os
import time
import requests
import random
import argparse 
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

# --- INTEGRASI WARNA (Colorama) ---
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    print("[!] Library 'colorama' belum diinstal. Jalankan perintah: pip install colorama")
    sys.exit(1)

# Pengaturan performa thread
MAX_THREADS = 3 

# Variabel global untuk menghitung persentase progress
counter = 0
total_urls = 0
print_lock = Lock()
file_lock = Lock()  # Lock tambahan agar penulisan file tidak bertabrakan antar-thread

# Daftar User-Agent variatif
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15'
]

def show_banner():
    """Menampilkan banner bergaya hacker dengan nama SKY"""
    banner = fr"""
{Fore.CYAN}     ____  _  ____     __
{Fore.CYAN}    / ___|| |/ /\ \   / /
{Fore.BLUE}    \___ \| ' /  \ \ / / 
{Fore.BLUE}     ___) | . \   \ V /  
{Fore.GREEN}    |____/|_|\_\   |_|   
{Fore.CYAN}  ===========================================
{Fore.GREEN}   [+] SKY - Web Reconnaissance & Tool v1.0
{Fore.GREEN}   [+] Stealth Mode: ACTIVE (Delay & Random UA)
{Fore.CYAN}  ===========================================
    """
    print(banner)

def save_result(filename, text):
    """Fungsi mengunci dan menulis hasil ke file secara aman dari konflik thread"""
    with file_lock:
        with open(filename, 'a') as f:
            f.write(text + "\n")

def check_url(url, output_file):
    """Fungsi mendeteksi status code URL secara aman dengan identitas acak"""
    global counter, total_urls
    
    # Jeda acak diperlebar sedikit untuk mengacaukan ritme deteksi firewall
    time.sleep(random.uniform(1.5, 4.0)) 
    
    try:
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive'
        }
        
        response = requests.get(url, timeout=4, allow_redirects=False, headers=headers)
        status = response.status_code
        
        # --- HITUNG PROGRESS PERSEN & OUTPUT WARNA KUSTOM ---
        with print_lock:
            counter += 1
            percentage = (counter / total_urls) * 100
            progress = f"[{percentage:.1f}%]"
            
            # 200 = GREEN
            if status == 200:
                print(f"{Fore.GREEN}[+] {progress} FOUND: {url} (Status: {status})")
                save_result(output_file, f"[FOUND] {url} (Status: {status})")
                
            # Menggunakan pengecekan rentang angka eksplisit yang valid
            elif 300 <= status <= 307:
                loc = response.headers.get('Location', 'Unknown')
                print(f"{Fore.YELLOW}[!] {progress} REDIRECT: {url} (Status: {status} -> {loc})")
                save_result(output_file, f"[REDIRECT] {url} (Status: {status} -> {loc})")
                
            # 403 = ORANGE
            elif status == 403:
                print(f"{Style.BRIGHT}{Fore.YELLOW}[-] {progress} FORBIDDEN: {url} (Status: {status}) - Diblokir/WAF Aktif")
                
            # 404 = RED
            elif status == 404:
                print(f"{Fore.RED}[-] {progress} NOT FOUND: {url} (Status: {status})")
            
            # Kode status lain selain di atas
            else:
                print(f"{Style.DIM}[?] {progress} OTHER: {url} (Status: {status})")
            
    except requests.RequestException:
        with print_lock:
            if counter < total_urls:
                counter += 1
        pass

def subfinder(domain_target, mode):
    global total_urls
    
    # Membersihkan nama domain
    domain_target = domain_target.replace("http://", "").replace("https://", "").strip("/")

    # Penentuan file berdasarkan parameter 'mode' dari argparse
    if mode == 'subdomain':
        filename = 'subdomains.txt'
        menu_name = "subdomain"
        output_file = f"live_subdomains_{domain_target}.txt"
    elif mode == 'direktori':
        filename = 'wordlist.txt'
        menu_name = "direktori"
        output_file = f"live_directories_{domain_target}.txt"

    try:
        with open(filename, 'r') as file:
            items = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{filename}' tidak ditemukan di folder ini!")
        return

    total_urls = len(items)
    if total_urls == 0:
        print(f"{Fore.RED}Error: File '{filename}' kosong.")
        return

    print(f"\n{Fore.BLUE}[+] Memulai scanning {menu_name} pada: {domain_target} (Total: {total_urls} target)")
    print(f"{Fore.MAGENTA}[+] Hasil aktif akan otomatis disimpan ke: {output_file}")
    print(f"{Fore.YELLOW}[!] Tekan Ctrl + C untuk membatalkan.")
    
    urls = []
    for item in items:
        if mode == 'subdomain':
            urls.append(f"https://{item}.{domain_target}")
        else:
            urls.append(f"https://{domain_target}/{item}")

    # Menggunakan Executor tanpa blok 'with' agar loop utama bisa menangkap sinyal interrupt
    executor = ThreadPoolExecutor(max_workers=MAX_THREADS)
    futures = [executor.submit(check_url, url, output_file) for url in urls]
    
    try:
        while True:
            unfinished = [f for f in futures if not f.done()]
            if not unfinished:
                break
            time.sleep(0.1) # Durasi tidur kecil agar penangkapan Ctrl+C responsif
            
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}[!] Scanning dibatalkan oleh pengguna (Ctrl + C). Menghentikan semua proses...")
        executor.shutdown(wait=False, cancel_futures=True) # Batalkan semua sisa antrean thread
        os._exit(0) # Tutup paksa seluruh engine Python secara instan di OS Windows
                    
    print(f"\n{Fore.GREEN}[+] Scanning {menu_name} selesai. Hasil tersimpan di {output_file}")
            
if __name__ == "__main__":
    show_banner() # Menampilkan banner visual pertama kali
    
    # Inisialisasi parser argparse
    parser = argparse.ArgumentParser(description="SKY - Web Reconnaissance Tool")
    
    # Registrasi argumen terminal
    parser.add_argument("target", help="Domain target scanner (contoh: google.com)")
    parser.add_argument(
        "--mode", "-m", 
        choices=["subdomain", "direktori"], 
        required=True, 
        help="Pilih mode scanning: 'subdomain' atau 'direktori'"
    )
    
    # Mengambil nilai input dari user
    args = parser.parse_args()
    
    try:
        subfinder(args.target, args.mode)
    except KeyboardInterrupt:
        os._exit(0)

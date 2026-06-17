import sys
import os
import time
import requests
import random
import argparse 
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    print("[!] Library 'colorama' belum diinstal. Jalankan perintah: pip install colorama")
    sys.exit(1)

counter = 0
total_urls = 0
print_lock = Lock()

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
{Fore.GREEN}   [+] SKY - Web Reconnaissance & Tool v1.3
{Fore.GREEN}   [+] Stealth Mode: ACTIVE (Delay & Random UA)
{Fore.CYAN}  ===========================================
    """
    print(banner)

def check_url(url):
    """Fungsi mendeteksi status code URL secara aman dengan identitas acak"""
    global counter, total_urls
    
    if args.delay > 0:
        time.sleep(args.delay + random.uniform(0.1, 0.9))
    
    try:
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive'
        }
        
        response = requests.get(url, timeout=4, allow_redirects=False, headers=headers)
        status = response.status_code
        
        with print_lock:
            counter += 1
            percentage = (counter / total_urls) * 100
            progress = f"[{percentage:.1f}%]"

            if args.filter_status and status in args.filter_status:
                return

            if status == 200:
                print(f"{Fore.GREEN}[+] {progress} FOUND: {url} (Status: {status})")
                
            elif 300 <= status <= 307:
                loc = response.headers.get('Location', 'Unknown')
                print(f"{Fore.YELLOW}[!] {progress} REDIRECT: {url} (Status: {status} -> {loc})")
                
            elif status == 403:
                print(f"{Style.BRIGHT}{Fore.YELLOW}[-] {progress} FORBIDDEN: {url} (Status: {status}) - Diblokir/WAF Aktif")
                
            elif status == 404:
                print(f"{Fore.RED}[-] {progress} NOT FOUND: {url} (Status: {status})")
            
            else:
                print(f"{Style.DIM}[?] {progress} OTHER: {url} (Status: {status})")
            
    except requests.RequestException:
        with print_lock:
            counter += 1
        pass

def subfinder(domain_target, mode):
    global total_urls
    
    menu_name = mode.upper()
    domain_target = domain_target.replace("http://", "").replace("https://", "").strip("/")

    if not args.wordlist:
        print(f"{Fore.RED}Error: Argumen --wordlist atau -w wajib diisi!")
        return

    try:
        with open(args.wordlist, 'r') as file:
            items = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{args.wordlist}' tidak ditemukan di folder ini!")
        return
        
    total_urls = len(items)
    if total_urls == 0:
        print(f"{Fore.RED}Error: File '{args.wordlist}' kosong.")
        return

    print(f"\n{Fore.BLUE}[+] Memulai scanning {menu_name} pada: {domain_target} (Total: {total_urls} target)")
    if args.filter_status:
        print(f"{Fore.MAGENTA}[+] Menyembunyikan status kode: {', '.join(map(str, args.filter_status))}")
    print(f"{Fore.YELLOW}[!] Tekan Ctrl + C untuk membatalkan.")
    
    urls = []
    for item in items:
        if mode == 'subdomain':
            urls.append(f"https://{item}.{domain_target}")
        else:
            urls.append(f"https://{domain_target}/{item}")

    executor = ThreadPoolExecutor(max_workers=MAX_THREADS)
    
    try:
        futures = [executor.submit(check_url, url) for url in urls]

        while True:
            unfinished = [f for f in futures if not f.done()]
            if not unfinished:
                break
            time.sleep(0.1)
            
        executor.shutdown(wait=True)
            
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}[!] Scanning dibatalkan oleh pengguna (Ctrl + C). Menghentikan semua proses...")
        executor.shutdown(wait=False, cancel_futures=True) 
        os._exit(0) 
                    
    print(f"\n{Fore.GREEN}[+] Scanning {menu_name} selesai.")
            
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="SKY - Web Reconnaissance Tool")

    parser.add_argument(
        "target", 
        help="Domain target scanner (contoh: google.com)"
    )

    parser.add_argument(
        "--filter-status", "-fs",
        nargs="+",
        type=int,
        help="Sembunyikan status codes tertentu dari layar (contoh: -fs 404 403)"
    )

    parser.add_argument(
        "--delay", "-d", 
        type=float, 
        default=0.5, 
        help="Jeda waktu dasar per pekerjaan untuk menghindari deteksi firewall"
    )

    parser.add_argument(
        "--version", "-v", 
        action="version", 
        version="v1.3"
    )

    parser.add_argument(
        "--wordlist", "-w",
        required=True, 
        help="Path to wordlist file"
    )

    parser.add_argument(
        "--mode", "-m", 
        choices=["subdomain", "direktori"], 
        required=True,  
        help="Pilih mode scanning: 'subdomain' atau 'direktori'"
    )

    parser.add_argument(
        "--threads", "-t", 
        type=int, 
        default=3, 
        help="Jumlah thread pekerja simultan"
    )

    args = parser.parse_args()


    if not args.target:
        sys.exit(1)
    else:
        show_banner()
    
    MAX_THREADS = args.threads

    try:
        subfinder(args.target, args.mode)
    except KeyboardInterrupt:
        os._exit(0)

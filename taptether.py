import threading
import requests
import time
import json
import urllib.parse
import sys
from colorama import init, Fore, Style
import base64

# Inisialisasi colorama
init()

# Fungsi untuk mencetak teks berwarna
def print_colored(text, color=Fore.WHITE):
    sys.stdout.write(color + text + Style.RESET_ALL + '\n')
    sys.stdout.flush()

# Fungsi untuk mencetak tanda pengenal di setiap perulangan
def print_identifier():
    print_colored("Channel TG: @airdrop_ea", Fore.GREEN)
    print_colored("Github: github.com/sakazukiz", Fore.GREEN)
    print_colored("Info: Jangan dijual ! Ngotak dikit !!", Fore.GREEN)
    print()  # Menambahkan baris baru agar tidak terlalu dekat

# Fungsi untuk mengirimkan permintaan GET
def send_post_request(url, query, start_param):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'access-control-allow-origin': '*',
        'authorization': f'tma {query}',  # Menggunakan query utuh di header Authorization
        'priority': 'u=1, i',
        'referer': f'https://tap-tether.org/?tgWebAppStartParam={start_param}',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    while True:
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    # Mengecek dan mencetak nilai remainingClicks dan pesan keberhasilan
                    remaining_clicks = json_response.get("remainingClicks")
                    success = json_response.get("success")
                    decoded_url = urllib.parse.unquote(query)
                    cleaned_text = decoded_url.replace("user=", "")
                    pos = cleaned_text.find('&')
                    cleaned = cleaned_text[:pos]
                    data = json.loads(cleaned)
                    first_name = data.get('first_name')
                    last_name = data.get('last_name')
                    print_identifier()
                    
                    if success:
                        print(Fore.CYAN + "Nama Akun: " + Fore.YELLOW + first_name + last_name + Style.RESET_ALL)
                        print(Fore.CYAN + "Tap: " + Fore.YELLOW + "Berhasil" + Style.RESET_ALL)
                    if remaining_clicks is not None:
                        print(Fore.CYAN + "Jumlah energy tersisa: " + Fore.YELLOW + f"{remaining_clicks}" + Style.RESET_ALL)
                        
                except ValueError as e:
                    print_identifier()  # Menampilkan tanda pengenal meskipun terjadi error
                    print(f"Error decoding JSON with token {query}: {e}, Response content: {response.text}")
            elif response.status_code not in [500, 503, 502, 520, 521]:
                print_identifier()  # Menampilkan tanda pengenal meskipun permintaan gagal
                print(f"Request with token {query} failed with status code {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            print_identifier()  # Menampilkan tanda pengenal meskipun terjadi request exception
            print(f"Request error with token {query}: {e}")
        
        time.sleep(1)  # Menunggu 1 detik sebelum mengirim permintaan berikutnya

# Membaca URL-encoded strings dari file dan memulai thread
def main():
    current_timestamp = int(time.time())
    url = f'https://tap-tether.org/server/clicks?clicks=2&lastClickTime={current_timestamp}'

    with open('session.txt', 'r') as file:
        lines = file.readlines()

    threads = []
    for line in lines:
        content = line.strip()
        
        # Memparsing data dari setiap baris
        parsed_data = {}
        for item in content.split('&'):
            key, value = item.split('=')
            parsed_data[key] = urllib.parse.unquote(value)

        # Cek dan ambil data yang diperlukan
        if 'tgWebAppData' in parsed_data and 'tgWebAppStartParam' in parsed_data:
            query = parsed_data['tgWebAppData']
            start_param = parsed_data['tgWebAppStartParam']
            thread = threading.Thread(target=send_post_request, args=(url, query, start_param))
            threads.append(thread)
            thread.start()
        else:
            print("Data yang diperlukan tidak ditemukan dalam query.txt")

    for thread in threads:
        thread.join()

    print("All requests have been sent.")

if __name__ == "__main__":
    main()

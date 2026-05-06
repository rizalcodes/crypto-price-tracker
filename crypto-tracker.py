import requests
from datetime import datetime
import time
import csv

def simpan_csv(waktu, coin, harga, perubahan):
    with open("crypto_history.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([waktu, coin, harga, perubahan])

def get_harga():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,solana,binancecoin,dogecoin",
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }

    response = requests.get(url, params=params)
    data = response.json()

    waktu = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print("\n=== CRYPTO PRICE TRACKER ===")
    print(f"Update: {waktu}\n")

    coins = {
        "bitcoin": "Bitcoin  ",
        "ethereum": "Ethereum ",
        "solana": "Solana   ",
        "binancecoin": "BNB      ",
        "dogecoin": "Dogecoin "
    }

    for coin_id, nama in coins.items():
        harga = data[coin_id]['usd']
        perubahan = data[coin_id]['usd_24h_change']
        arah = "↑" if perubahan > 0 else "↓"
        print(f"{nama}: ${harga:,.2f}  {arah} {abs(perubahan):.2f}%")

        # Auto save ke CSV setiap refresh
        simpan_csv(waktu, coin_id, harga, round(perubahan, 2))

    print("✓ Data tersimpan ke crypto_history.csv")

# Auto refresh setiap 60 detik
while True:
    get_harga()
    print("\nRefresh dalam 60 detik...")
    time.sleep(60)
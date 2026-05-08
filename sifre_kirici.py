import threading
import time
import os

bulundu = threading.Event()
kilit = threading.Lock()

def dene(hedef_sifre, sifre):
    if bulundu.is_set():
        return
    if sifre == hedef_sifre:
        bulundu.set()
        with kilit:
            print(f"\n  SIFRE BULUNDU: {sifre}")

def kirici(hedef_sifre, wordlist_yolu):
    print(f"\n{'='*40}")
    print(f"Hedef    : {hedef_sifre}")
    print(f"Wordlist : {wordlist_yolu}")
    print(f"Baslangic: {time.strftime('%H:%M:%S')}")
    print(f"{'='*40}\n")

    try:
        with open(wordlist_yolu, "r", encoding="utf-8", errors="ignore") as f:
            sifreler = [satir.strip() for satir in f.readlines()]
    except FileNotFoundError:
        print("Wordlist dosyasi bulunamadi!")
        return

    print(f"Toplam {len(sifreler)} sifre deneniyor...\n")

    threads = []
    for sifre in sifreler:
        if bulundu.is_set():
            break
        t = threading.Thread(target=dene, args=(hedef_sifre, sifre))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if not bulundu.is_set():
        print("Sifre wordlistte bulunamadi.")

    print(f"\nBitis: {time.strftime('%H:%M:%S')}")

kirici("admin123", "wordlist.txt")
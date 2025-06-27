This is a proof-of-concept Python script that exploits a SQL Injection vulnerability in the AMUserResourcesSyncServlet endpoint of ManageEngine Applications Manager (versions 11.0 to <14.0). The backend database for vulnerable installations is PostgreSQL, which allows attackers to define User-Defined Functions (UDFs) written in C.

The exploit leverages unauthenticated SQL injection to create a UDF that loads a malicious DLL over SMB, achieving remote code execution (RCE) on the underlying Windows system running the PostgreSQL database service.

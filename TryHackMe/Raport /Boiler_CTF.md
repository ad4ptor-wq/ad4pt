#  Pentest Report: Boiler CTF

## 1. Introduction
- **Room:** Boiler CTF  
- **Level:** Easy  
- **Date:** 10.09.2025  
- **Pentester:** ad4pt  
- **Target IP:** xxx.xxx.xxx.xxx  
- **Goal:** Identify vulnerabilities and obtain root access.

---

## 2. Executive Summary
The penetration test was conducted against the target **Boiler CTF**.  
- **Total vulnerabilities found:** 2  
- **Highest risk:** Remote Code Execution via sar2html v3.2.1  
- **Impact:** Full system compromise (root access)  
- **Recommendation:** Update or remove vulnerable services, implement stricter access controls.

---

## 3. Methodology
1. **Reconnaissance** — Port scanning with nmap  
2. **Enumeration** — Directory brute-force (ffuf), service fingerprinting  
3. **Exploitation** — sar2html RCE → web shell → SSH credentials discovery  
4. **Privilege Escalation** — Abusing SUID binary (`find`)  
5. **Post-Exploitation** — Proof of root access

---

## 4. Findings & Exploitation

### 4.1 Open Ports
**Nmap command:**
```bash
sudo nmap -sV -sC -Pn -p- xxx.xxx.xxx.xxx
```

**Results:**
- 21/tcp → FTP (no useful files)  
- 80/tcp → HTTP (web service)  
- 10000/tcp → MiniServ v1.930 (no known exploit found)  
- 55007/tcp → SSH  

---

### 4.2 Web Enumeration
Using `ffuf` on port 80 revealed directories:  
- `/joomal` → Joomla site  
- `/joomal/manual`  
- `/joomal/administrator`  
- `/joomal/_file`  
- `/joomal/_test` → **sar2html v3.2.1**

---

### 4.3 Exploitation
- Vulnerable service: **sar2html v3.2.1**  
- Exploit used: [sar2HTML_exploit](https://github.com/Jsmoreira02/sar2HTML_exploit)  
- Result: Reverse shell as `www-data`  

During enumeration, a file `log.txt` was discovered both on the website and on the shell. It contained valid **SSH credentials**:  
```
User: basterd
Password: superduperp@$$
```

---

### 4.4 Privilege Escalation
After logging in via SSH as `basterd`, SUID binaries were enumerated:  
```bash
find / -user root -perm -4000 -type f 2>/dev/null
```

The `find` binary was exploitable for privilege escalation:  
```bash
find . -exec /bin/bash -p \; -quit
```

Result: **root access obtained**.

---

## 5. Proof of Compromise
```
cat /root/root.txt
```
✅ Root flag successfully retrieved.  
**Current status:** Full system compromise.

---

## 6. Recommendations
- Remove or update vulnerable **sar2html** to the latest version.  
- Do not store plaintext credentials (`log.txt`) on the server.  
- Restrict access to administrative services (e.g., MiniServ).  
- Review SUID binaries and remove unnecessary privileges.  
- Regularly patch and harden the system.

---

## 7. Appendix
- Full nmap scan results  
- ffuf output for directory enumeration  
- Exploit script reference  
- Screenshots of exploitation steps  

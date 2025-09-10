# Pentesting Raport: Boiler CTF 
## 1. Introduct 
-**Room** Boiler
-**Level** Easy
-**Date** 10.09.2025
-**Pintester:** Alex
-**Target IP:**xxx.xxx.xxx.xxx
-**Goal** Indentify vulnerabilities and obtain root acces.

---

## 2. Executive Summary 
The penetration test was conducted against the target **Boiler**
-**Total vulnerabilities found:** 2 
-**Highes risk:** Remote Code Execution via sar2html v3.2.1
-**Impact** Full system compromise (root acces)
-**Recommendation** Update or remove vulnerable server, implement stricter access controls.

---

## 3. Methodology 
1. **Reconnaisance** - Port scanning with nmap
2. **Enumeration** - Directory brute-force (ffuf), server fingerprinting
3. **Exploitation** - sar2html RCE > web shell > SSH credentials discovery
4. **Privelege Escalation** - Abusing SUID binary ('find')
5. **Post-Exploitation** - Proof of root access

--

## 4. Find & Exploitation

### 4.1 Opens Ports
**Nmap command:**
```bash
sudo nmap -sC -sV -Pn -p- xxx.xxx.xxx.xxx

**Results:**
- 21/tcp > ftp(no use files)
- 80/tcp > HTTP(web server)
- 10000/tcp > MiniServ v1.930(no known exploit found)
- 55007/tcp > SSH
### 4.2 Web Enumeration
- Vulnerable service: **sar2html v3.2.1**
- Exploit used: [sar2HTML_exploit](https://github.com/Jsmoreira02/sar2HTML_exploit)
- Result: Reverse shell as ``www-data``

During enumeration, a file `log.txt` was discovered both on the wbsite and on the shell. It contained valid **SSH creditals**:
```
User: basterd
Password: superduperp@$$

---

### 4.4 Privelege Escalation 
After logging in vis SSH as `basterd`. SUID binaries were enumerated:
```bash
find / -user root -perm -4000 -type f 2>/dev/null
```
Result: **root access obtained**.

---

## 5. Proof of Compromise
```
cat /root/root.txt
```
Root flag successsfully retrieved.
**Curent status:** Full system compromise.

---

## 6. Recomandations
- Remove or  update vulnerable **sar2html** to the latest version.
- Do not store plaintext credentials (`log.txt`) on the server.
- Restrict access to administrative service (e.g.,MiniServ).
- Reviwe SUID binaries and remove unnacessary priveleges.
- Regulary pach and harden the system.

---

### 7. Appendix
- Full nmap results
- ffuf output for directory enumeration
- Exploit script reference


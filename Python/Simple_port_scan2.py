import socket # socket modul for network conections

# target host
target = "scanme.nmap.org"


# scan first 100 ports
for port in range(1, 100):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a TCP socket
    sock.settimeout(2) # set timeout to avoid waiting too long
    result = sock.connect_ex((target, port)) # try to connect to the port


    if result == 0: # if result is 0, port is open
        print(f"[+] Port {port} is OPEN")
    sock.close() #close socket

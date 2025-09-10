import socket  # Import the socket module to work with network connections

# Loop through ports 1 to 99
for port in range(1, 100):
    # Create a new socket for each port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP
    s.settimeout(2)  # Set a timeout of 2 seconds for the connection

    try:
        # Attempt to connect to the target server and port
        s.connect(('ad.samsclass.info', port))

        try:
            # Receive up to 1024 bytes of data from the server
            r = s.recv(1024)
            # Decode the received bytes into a string (ignore errors if not valid UTF-8)
            response = r.decode('utf8', errors='ignore')

            # Check if the hidden service message is in the response
            if 'CongratuLations' in response:
                print(f'[!] HIDDEN SERVICE FOUND: {port} ~ {response}')
                break  # Stop scanning if hidden service is found
            else:
                print(f'{port} ~ {response}')  # Print normal response

        except socket.timeout:
            # Handle cases where the server doesn't send any data within timeout
            print(f'{port} ~ No response (timeout)')

        finally:
            # Close the socket after finishing with this port
            s.close()

    except socket.error as err:
        # Handle connection errors (e.g., port closed or refused)
        print(f'{port} ~ {err}')

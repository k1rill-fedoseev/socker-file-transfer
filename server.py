import sys
import os
import socket


sock = socket.socket()

sock.bind(("0.0.0.0", int(sys.argv[1])))
sock.listen(10)

PACKET_SIZE = 1024

while True:
    conn, address = sock.accept()

    print(f'Accepted connection from: {address}')
    
    file_name_len = conn.recv(1)[0]
    file_name = conn.recv(file_name_len).decode('utf-8')

    if os.path.exists(file_name):
        parts = file_name.split('.')
        i = 1
        while True:
            tag = '_copy' + str(i) + '.'
            new_file_name = parts[0] + tag + '.'.join(parts[1:])
            if not os.path.exists(new_file_name):
                file_name = new_file_name
                break
            i += 1

    with open(file_name, 'wb') as file:
        while True:
            blob = conn.recv(PACKET_SIZE)
            if not blob:
                break
            file.write(blob)
    conn.close()

sock.close()

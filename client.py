import sys
import os
import time
import socket


sock = socket.socket()
sock.connect((sys.argv[2],int(sys.argv[3])))

PACKET_SIZE = 1024
UPDATE_INTERVAL = 1

def fmt_size(size):
    for unit in ['','KB','MB','GB','TB']:
        if size < 1024:
            return f"{size:3.1f}{unit}"
        size /= 1024.0

file_path = sys.argv[1]
file_name = file_path.split('/')[-1]

spaces = ' ' * 10
with open(file_path, "rb") as file:
    size = os.path.getsize(file_path)
    print(f'Start sending file {file_name} of size {size} bytes')
    sock.send(bytes([len(file_name)]) + file_name.encode('utf-8'))

    count = 0
    last_update = 0
    while True:
        blob = file.read(PACKET_SIZE)
        if not blob:
            break
        sock.send(blob)
        count += len(blob)
        if time.time() - last_update > UPDATE_INTERVAL:
            last_update = time.time()
            sys.stdout.write(f'\rProgress: {fmt_size(count)}/{fmt_size(size)} - {100 * count / size:2.1f}%{spaces}')
        #sys.stdout.flush()
    sys.stdout.write(f'\rProgress: {fmt_size(size)}/{fmt_size(size)} - 100.0%{spaces}')

sock.close()

print('\nFile sending is completed')

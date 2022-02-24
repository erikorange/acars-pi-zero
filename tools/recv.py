import socket

sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sck.bind(('127.0.0.1', 5555))
sck.setblocking(0)

while True:

    try:
        data, address = sck.recvfrom(1024)
    except Exception as msg:
        pass
    else:
        print(data.decode('utf-8'))


# acarsdec -N 127.0.0.1:5555 -r 0 131.55
# acarsdec -j 127.0.0.1:5555 -r 0 131.55
# acarsdec -l acars.log -D -j 127.0.0.1:5555 -r 0 131.55
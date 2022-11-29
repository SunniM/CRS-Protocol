import socket
def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', 59003))
    while True:
        msg, addr = sock.recvfrom(1024)
        print(addr)
        print(msg)
        if(msg.decode() == "DONE"):
            break

if __name__ == '__main__':
    main()
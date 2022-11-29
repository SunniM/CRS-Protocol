import multiprocessing as mp
import time
import socket
def test():
    f = open('test.txt', 'w')
    print("TESTING")

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto("DONE".encode(), ('127.0.0.1',59003))


if __name__ == '__main__':
    main()


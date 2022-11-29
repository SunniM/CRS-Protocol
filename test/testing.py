import multiprocessing as mp
import time
import socket
def test():
    f = open('test.txt', 'r')
    print(f.readlines())
    f.close()

def main():
    print(len('300'.encode()))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto("TESTING.py".encode(), ('127.0.0.1',59003))


if __name__ == '__main__':
    test()


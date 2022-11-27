import Services
import socket
import multiprocessing as mp
import threading
import time
import os


SRVR_IP = '10.0.0.1'
#SRVR_IP = '127.0.0.1'
SRVR_PORT = 59001
SRVR_ADDR = (SRVR_IP, SRVR_PORT)

REND_IP = '10.0.0.1'
#REND_IP = '127.0.0.1'
C_REND_PORT = 59002
C_REND_ADDR = (REND_IP, C_REND_PORT)

S_REND_PORT = 59003
S_REND_ADDR = (REND_IP, S_REND_PORT)

MSG_SIZE = 500

def main():


    c_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    c_sock.bind(C_REND_ADDR)
    s_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_sock.bind(S_REND_ADDR)


    exit = False
    while(not exit):

        data, address = c_sock.recvfrom(MSG_SIZE)
        messageType, morePortions, message = Services.parseMessage(data)
        
        if messageType =='20':     # Request file to render
            message = Services.build_Message(messageType, morePortions, message)
            s_sock.sendto(message, SRVR_ADDR)
            global p
            p = threading.Thread(target=renderFile, args=(c_sock,s_sock, address))
            p.start()
            message = Services.build_Message('22', '0', '')
            c_sock.sendto(message, address)

        elif messageType =='30':     # Request pause
            message = Services.build_Message(messageType, morePortions, message)
            s_sock.sendto(message, (SRVR_IP, SRVR_PORT))

        elif messageType =='32':     # Request resume
            message = Services.build_Message(messageType, morePortions, message)
            s_sock.sendto(message, (SRVR_IP, SRVR_PORT))

        elif messageType == '34':     # Request restart
            message = Services.build_Message(messageType, morePortions, message)
            s_sock.sendto(message, (SRVR_IP, SRVR_PORT))

        elif messageType =='99':
            os._exit(0)
            exit = True

def renderFile(c_sock, s_sock, c_address):
    while(True):
        data, _ = s_sock.recvfrom(MSG_SIZE)
        messageType, morePortions, message = Services.parseMessage(data)
        
        if messageType ==  '21' :
            print(message, end='', flush=True)
            if(morePortions == '0'):
                message = Services.build_Message('23', '0', '')
                c_sock.sendto(message,c_address)
        elif messageType == '31' :
            print("Rendering Paused")
        elif messageType == '33' :
            print("Rendering Resumed")
        elif messageType == '35' :
            print("Rendering Restarted")

if __name__ == '__main__':
    main()
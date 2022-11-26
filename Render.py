import Services
import socket
import multiprocessing as mp
import os
SRVR_IP = '127.0.0.1'
CTRL_IP = '127.0.0.1'
SRVR_PORT = 59001
REND_PORT = 59002
CTRL_PORT = 59003
MSG_SIZE = 1000

def main():


    c_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    exit = False
    while(not exit):
        data, address = c_sock.recvfrom(MSG_SIZE)
        messageType, morePortions, message = Services.parseMessage(data)

        match(messageType):
            case('20'):     # Request file to render
                message = Services.build_Message(messageType, morePortions, message)
                s_sock.sendto(message, (SRVR_IP, SRVR_PORT))
                global p
                p = mp.Process(target=renderFile, args=(c_sock, s_sock))
                p.start()

            case('30'):     # Request pause
                message = Services.build_Message(messageType, morePortions, message)
                s_sock.sendto(message, (SRVR_IP, SRVR_PORT))


            case('32'):     # Request resume
                message = Services.build_Message(messageType, morePortions, message)
                s_sock.sendto(message, (SRVR_IP, SRVR_PORT))


            case('34'):     # Request restart
                message = Services.build_Message(messageType, morePortions, message)
                s_sock.sendto(message, (SRVR_IP, SRVR_PORT))

                '''
                p.terminate()
                empty_socket(s_sock)
                p.start()
                '''
            case('99'):
                p.terminate()
                exit = True


def empty_socket(s_sock):
    while(s_sock.recvFrom(MSG_SIZE)):
        pass

def renderFile(c_sock, s_sock):
    while(True):
        data, _ = s_sock.recvfrom(MSG_SIZE)
        messageType, morePortions, message = Services.parseMessage(data)
        match messageType:
            case '20' :
                print(message, end='')
                if(not morePortions):
                    message = Services.build_Message('23', '0', '')
                    c_sock.sendto(message,(CTRL_IP, CTRL_PORT))
            case '31' :
                print("Rendering Paused")
            case '33' :
                print("Rendering Resumed")
            case '35' :
                print("Rendering Restarted")


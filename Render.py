import Services
import socket
import multiprocessing as mp
import time
SRVR_IP = '127.0.0.1'
SRVR_PORT = 59001
SRVR_ADDR = (SRVR_IP, SRVR_PORT)

REND_IP = '127.0.0.1'
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
        print('Message Type: ' + messageType)
        print('More Portions: ' + morePortions)
        print('Received Message: ' + message)
        match(messageType):
            case('20'):     # Request file to render
                message = Services.build_Message(messageType, morePortions, message)
                s_sock.sendto(message, SRVR_ADDR)
                global p
                p = mp.Process(target=renderFile, args=(c_sock,s_sock, address))
                p.start()
                message = Services.build_Message('22', '0', '')
                c_sock.sendto(message, address)

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

def renderFile(c_sock, s_sock, c_address):
    print('TEST')
    while(True):
        data, _ = s_sock.recvfrom(MSG_SIZE)
        messageType, morePortions, message = Services.parseMessage(data)

        match messageType:
            case '21' :
                print(message, end='', flush=True)
                if(morePortions == '0'):
                    message = Services.build_Message('23', '0', '')
                    c_sock.sendto(message,c_address)
            case '31' :
                print("Rendering Paused")
            case '33' :
                print("Rendering Resumed")
            case '35' :
                print("Rendering Restarted")

if __name__ == '__main__':
    main()